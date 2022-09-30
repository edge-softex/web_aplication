from celery import shared_task

from datetime import datetime, timedelta
from pytz import timezone
import numpy as np
import random
import re

from api import settings

from .util import read_dat_file, stringify_datetime, timestamp_aware, alert_definition

from photovoltaic.models import PVData, PVString, PowerForecast, YieldDay, YieldMonth, YieldYear, YieldMinute, AlertTreshold, Settings, Log, AIAlgorithm
from photovoltaic.serializers import PVDataSerializer

from api.wsgi import registry

def createLog(self, exc, task_id, args, kwargs, einfo):
    log = Log.create(title='Backend system error.', message='Task execution error {task}: {einfo}'.format(task=task_id, einfo=einfo))
    log.save()

@shared_task(bind=True, max_retries=3, on_failure=createLog)
def simulate_input(self):
    """Simulates data entry to perform system tests."""
    
    df = read_dat_file('./photovoltaic/fixtures/test_day.dat')

    tz = timezone(settings.TIME_ZONE)
    datetime_now = tz.localize(datetime.now())
    datetime_string = str(datetime_now).replace(' ', 'T')

    index = datetime_now.hour*60 + datetime_now.minute

    df_row = df.iloc[[index]]

    s1 = PVString.objects.create(name='S1 ' + datetime_string, 
                                timestamp=datetime_now,
                                voltage=df_row['Tensao_S1_Avg'],
                                current=df_row['Corrente_S1_Avg'],
                                power=df_row['Potencia_S1_Avg'],
                                voltage_alert=np.random.choice(['NM', 'WA', 'FT'], p=[0.88, 0.10, 0.02]),
                                current_alert=np.random.choice(['NM', 'WA', 'FT'], p=[0.88, 0.10, 0.02]),
                                string_number=1)
    
    s2 = PVString.objects.create(name='S2 ' + datetime_string,
                                timestamp=datetime_now,
                                voltage=df_row['Tensao_S2_Avg'],
                                current=df_row['Corrente_S2_Avg'],
                                power=df_row['Potencia_S2_Avg'],
                                voltage_alert=np.random.choice(['NM', 'WA', 'FT'], p=[0.83, 0.15, 0.02]),
                                current_alert=np.random.choice(['NM', 'WA', 'FT'], p=[0.83, 0.15, 0.02]),
                                string_number=2)

    data = PVData.objects.create(timestamp=datetime_now,
                                irradiance=df_row['Radiacao_Avg'],
                                temperature_pv=df_row['Temp_Cel_Avg'],
                                temperature_amb=df_row['Temp_Amb_Avg'],
                                power_avg=df_row['Potencia_FV_Avg'])

    data.strings.set([s1, s2])

    energy = df_row['Potencia_FV_Avg']*(1/60)/1000

    day = datetime_now.replace(hour=0, minute=0, second=0, microsecond=0)
    yield_day, created = YieldDay.objects.get_or_create(timestamp=day)
    yield_day.yield_day = yield_day.yield_day + energy #kWh
    yield_day.yield_day_forecaste = 30
    yield_day.save()

    yield_minute, created = YieldMinute.objects.get_or_create(timestamp=datetime_now)
    yield_minute.yield_minute = yield_day.yield_day #kWh
    yield_minute.yield_day_forecaste = 30
    yield_minute.save()

    month = day.replace(day=1)
    yield_month, created = YieldMonth.objects.get_or_create(timestamp=month)
    yield_month.yield_month = yield_month.yield_month + energy #kWh
    yield_month.save()

    year = month.replace(month=1)
    yield_year, created = YieldYear.objects.get_or_create(timestamp=year)
    yield_year.yield_year = yield_year.yield_year + (energy/1000) #MWh
    yield_year.save()

    power1 = float(df.iloc[[index+1]]['Potencia_FV_Avg'])
    power2 = float(df.iloc[[index+2]]['Potencia_FV_Avg'])
    power3 = float(df.iloc[[index+3]]['Potencia_FV_Avg'])
    power4 = float(df.iloc[[index+4]]['Potencia_FV_Avg'])
    power5 = float(df.iloc[[index+5]]['Potencia_FV_Avg'])

    simulate_model.apply_async(args=[datetime_now, power1, power2, power3, power4, power5], kwargs={}, queue='run_models')
    #instant_power_forecast.apply_async(args=[datetime_now], kwargs={}, queue='run_models')

@shared_task(bind=True, max_retries=3, on_failure=createLog)
def simulate_model(self, datetime_now, power1, power2, power3, power4, power5):
    """Simulates instantaneous power forecast to perform system tests.

    param datetime_now: timestamp of generated data
    type username: datetime
    param power_1: power of the next data set
    type power_1: float
    param power_2: power of the second data set ahead
    type power_2: float
    param power_3: power of the third data set ahead
    type power_3: float
    param power_4: power of the fourth data set ahead
    type power_4: float
    param power_5: power of the fifth data set ahead
    type power_5: float
    """
    pf = PowerForecast.objects.create(timestamp=datetime_now,
                                    t1=power1 + random.uniform(0, 1.0),
                                    t2=power2 + random.uniform(0.3, 1.3),
                                    t3=power3 + random.uniform(0.6, 1.6),
                                    t4=power4 + random.uniform(0.9, 1.9),
                                    t5=power5 + random.uniform(1.2, 2.2))


@shared_task(bind=True, max_retries=3, on_failure=createLog)
def calculate_alerts_tresholds(self):
    """Calculates the thresholds used to activate alerts."""

    now = timestamp_aware()
    yesterday = now - timedelta(days=1)
    datetime_lte = re.sub(r'\d\d:\d\d:\d\d.\d+', '23:59:59.999999', stringify_datetime(yesterday))
    month_before = yesterday - timedelta(days=30)
    datetime_gte = re.sub(r'\d\d:\d\d:\d\d.\d+', '00:00:00.000000', stringify_datetime(month_before))

    pv_data = PVData.objects.filter(timestamp__gte=datetime_gte, timestamp__lte=datetime_lte, irradiance__gte=120)
    length = len(pv_data)

    st, created = Settings.objects.get_or_create(id=1)

    if(length < 4000):
        st.alert_days_active = False
        st.days_left = 7 - int(length/571)
        st.save()
    else:
        json_data = PVDataSerializer(pv_data[0]).data
        number_strings = len(json_data['strings'])

        data_ordered_irrad = pv_data.order_by('irradiance')
        data_ordered_temp = pv_data.order_by('temperature_pv')

        min_irrad = round(data_ordered_irrad[0].irradiance)
        max_irrad = round(data_ordered_irrad[length-1].irradiance)
        min_temp = round(data_ordered_temp[0].temperature_pv)
        max_temp = round(data_ordered_temp[length-1].temperature_pv)

        fault_vt = st.fault_vt_percentile
        warning_vt = st.warning_vt_percentile
        delt_vt = st.delt_vt

        fault_cr = st.fault_cr_percentile
        warning_cr = st.warning_cr_percentile
        delt_cr = st.delt_cr

        for value in range(min_irrad, max_irrad+1):
            data_filtered = pv_data.filter(irradiance__gte = value - delt_cr, irradiance__lte = value + delt_cr)

            current_data = np.zeros((number_strings, data_filtered.count()))

            for i in range(0, data_filtered.count()):
                for j in range(0, number_strings):
                    string = data_filtered[i].strings.all()[j]
                    current_data[string.string_number - 1][i] = string.current
        
            for string_number in range(0, number_strings):
                if(len(current_data[string_number]) > 0):
                    th = np.percentile(current_data[string_number], [fault_cr, 100-fault_cr, warning_cr, 100-warning_cr])
                    
                    alert_th, created = AlertTreshold.objects.get_or_create(alert_type='CR', string_number=string_number+1, meteorological_value=value)
                    alert_th.treshold_ft_max = th[0]
                    alert_th.treshold_ft_min = th[1]
                    alert_th.treshold_wa_max = th[2]
                    alert_th.treshold_wa_min = th[3]
                    alert_th.save()

        for value in range(min_temp, max_temp+1):
            data_filtered = pv_data.filter(temperature_pv__gte = value - delt_vt, temperature_pv__lte = value + delt_vt)

            voltage_data = np.zeros((number_strings, data_filtered.count()))

            for i in range(0, data_filtered.count()):
                for j in range(0, number_strings):
                    string = data_filtered[i].strings.all()[j]
                    voltage_data[string.string_number - 1][i] = string.voltage
        
            for string_number in range(0, number_strings):
                if(len(voltage_data[string_number]) > 0):
                    th = np.percentile(voltage_data[string_number], [fault_vt, 100-fault_vt, warning_vt, 100-warning_vt])

                    alert_th, created = AlertTreshold.objects.get_or_create(alert_type='VT', string_number=string_number+1, meteorological_value=value)
                    alert_th.treshold_ft_max = th[0]
                    alert_th.treshold_ft_min = th[1]
                    alert_th.treshold_wa_max = th[2]
                    alert_th.treshold_wa_min = th[3]
                    alert_th.save()

        st.alert_days_active = True
        st.save()


@shared_task(bind=True, max_retries=3, on_failure=createLog)
def set_data(self, request_data):
    """ Function that receives data from external sources, processes it and saves it in the database.

    param request_data: dataset for insertion into the system
    tupe request_data: json
    """

    strings_ref = []

    data_timestamp = request_data['timestamp']

    if request_data['temperature_pv'] is not None:
        temperature = request_data['temperature_pv']
    elif request_data['temperature_amb'] is not None:
        temperature = request_data['temperature_amb']
    else:
        temperature = 0

    if request_data['irradiance'] is not None:
        irradiance = request_data['irradiance']
    else:
        irradiance = 0 

    for string in request_data['strings']:
        if string['power'] is None and string['voltage'] is not None and string['current'] is not None:
            string_power = string['voltage'] * string['current']
        else:
            string_power = string['power']
        string_obj = PVString.objects.create(name='S' + str(string['string_number']) + ' ' + request_data['timestamp'], 
                                timestamp=data_timestamp,
                                voltage=string['voltage'],
                                current=string['current'],
                                power=string_power,
                                voltage_alert=alert_definition('VT', string['string_number'], temperature, string['voltage']),
                                current_alert=alert_definition('CR', string['string_number'], irradiance, string['current']),
                                string_number=string['string_number'])
        strings_ref.append(string_obj)

    data = PVData.objects.create(timestamp=data_timestamp,
                                irradiance=request_data['irradiance'],
                                temperature_pv=request_data['temperature_pv'],
                                temperature_amb=request_data['temperature_amb'])

    data.strings.set(strings_ref)

    day = re.sub(r'\d\d:\d\d:\d\d.\d+', '00:00:00.000000', data_timestamp)
    yield_day, created = YieldDay.objects.get_or_create(timestamp=day)

    if request_data['generation'] is None and request_data['power_avr'] is None:
        power = 0
        energy = 0
    elif request_data['generation'] is None and request_data['power_avr'] is not None:
        power = request_data['power_avr']
        energy = request_data['power_avr']*(1/60)/1000
    elif request_data['generation'] is not None and request_data['power_avr'] is None:
        energy = request_data['generation'] - yield_day.yield_day
        power = energy*60*1000
    else:
        power = request_data['power_avr']
        energy = request_data['generation'] - yield_day.yield_day

    data.power_avg = power
    data.save()

    yield_day.yield_day = yield_day.yield_day + energy #kWh
    yield_day.yield_day_forecaste = 30 #TODO run generation forecast
    yield_day.save()

    yield_minute, created = YieldMinute.objects.get_or_create(timestamp=data_timestamp)
    yield_minute.yield_minute = yield_day.yield_day #kWh
    yield_minute.yield_day_forecaste = 30 #TODO run generation forecast
    yield_minute.save()

    month = re.sub(r'\d\dT\d\d:\d\d:\d\d.\d+', '01T00:00:00.000000', data_timestamp)
    yield_month, created = YieldMonth.objects.get_or_create(timestamp=month)
    yield_month.yield_month = yield_month.yield_month + energy #kWh
    yield_month.save()

    year = re.sub(r'\d\d-\d\dT\d\d:\d\d:\d\d.\d+', '01-01T00:00:00.000000', data_timestamp)
    yield_year, created = YieldYear.objects.get_or_create(timestamp=year)
    yield_year.yield_year = yield_year.yield_year + (energy/1000) #MWh
    yield_year.save()

    instant_power_forecast.apply_async(args=[data_timestamp], kwargs={}, queue='run_models')

@shared_task(bind=True, max_retries=3, on_failure=createLog)
def instant_power_forecast(self, timestamp):
    #Get data
    datetime_gte = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')
    datetime_gte = datetime_gte - timedelta(minutes=120)
    data = PVData.objects.filter(timestamp__gte=stringify_datetime(datetime_gte), timestamp__lte=timestamp)
    irradiance = data.values_list('irradiance', flat=True)
    temperature_pv = data.values_list('temperature_pv', flat=True)
    power_avr = data.values_list('power_avg', flat=True)

    input_data = irradiance+temperature_pv+power_avr

    if len(input_data) != 360:
        input_data = [27.58, 26.6, 41.31, 28.39, 26.57, 41.54, 29.75, 26.29, 74.04, 31.27, 26.28, 70.62, 32.81, 26.39, 80.7, 34.27, 26.51, 86.1, 34.24, 26.59, 79.31, 33.28, 26.45, 80.3, 32.36, 26.46, 75.12, 30.57, 26.5, 59.56, 30.41, 26.47, 52.85, 30.81, 26.51, 50.45, 31.99, 26.69, 65.85, 32.37, 26.63, 68.88, 32.88, 26.58, 71.74, 33.34, 26.29, 76.51, 34.9, 26.56, 80.9, 38.41, 26.7, 101.9, 40.65, 26.6, 116.2, 40.76, 26.38, 118.4, 38.16, 26.77, 84.4, 36.21, 26.83, 77.78, 35.2, 26.71, 72.37, 36.36, 26.68, 86.5, 38.15, 26.58, 93.1, 39.82, 26.97, 97.4, 40.64, 27.08, 104.2, 40.54, 26.6, 106.1, 37.98, 26.73, 85.3, 36.68, 26.53, 81.3, 37.94, 26.65, 79.42, 38.74, 26.97, 82.5, 40.39, 26.84, 106.8, 43.69, 27.15, 122.6, 47.97, 26.78, 134.2,53.51, 26.93, 164.0, 56.14, 26.56, 173.9, 56.67,26.69, 180.5, 60.96, 26.79, 214.5, 70.39, 26.77, 248.5, 102.8, 27.0, 404.3, 148.6, 26.97, 651.4, 195.1, 27.43, 906.0, 208.7, 27.7, 987.0, 216.0, 27.85, 1029.0, 220.9, 27.99, 1028.0, 231.9, 28.27, 1099.0, 245.9, 28.69, 1164.0, 248.8, 29.06, 1181.0 , 235.0, 29.72, 1084.0, 249.6, 29.99, 1151.0, 255.3, 30.23, 1163.0, 227.8, 30.7, 1022.0, 179.3, 30.7, 762.3, 179.3, 30.24, 757.0, 178.3, 29.73, 745.8, 158.1, 29.18, 644.4, 152.1, 29.2, 618.1, 171.4, 29.14, 711.6, 168.5, 29.21, 703.9, 167.4, 29.79, 688.4, 253.8, 30.04, 1131.0, 261.6, 30.1, 1160.0, 202.2, 30.59, 857.0, 182.8, 31.0, 750.4, 194.0, 31.23, 813.0, 177.3, 31.51, 732.6, 222.1, 31.41, 978.0, 213.9, 31.58, 924.0, 206.7, 31.62, 882.0, 199.7, 32.08, 854.0, 209.9, 32.39, 902.0, 222.4, 32.69, 962.0, 254.5, 33.16, 1112.0, 306.1, 33.43, 1385.0, 204.2, 33.44, 874.0, 253.2, 33.66, 1108.0, 345.1, 34.04, 1587.0, 357.6, 34.63, 1665.0, 337.9, 35.02, 1551.0, 287.6, 35.52, 1290.0, 257.0, 35.15, 1125.0, 218.6, 35.55, 934.0, 210.6, 35.39, 875.0, 260.6, 35.4, 1153.0, 342.1, 35.38, 1573.0, 333.1, 35.18, 1528.0, 311.3, 35.67, 1401.0, 262.4, 36.21, 1156.0, 313.8, 36.31, 1416.0, 380.3, 36.38, 1773.0, 350.8, 36.45, 1617.0, 213.1, 36.14, 895.0, 177.8, 35.83, 729.3, 322.3, 36.17, 1462.0, 438.2, 36.13, 2092.0, 374.0, 36.44, 1751.0, 278.7, 36.68, 1212.0, 339.0, 37.11, 1522.0, 400.9, 37.16, 1876.0, 346.2, 37.07, 1585.0, 288.4, 37.34, 1304.0, 277.0, 37.22, 1225.0, 315.0, 36.87, 1423.0, 310.2, 37.37, 1407.0, 288.9, 37.48, 1297.0, 279.1, 36.44, 1226.0, 192.7, 36.71, 787.1, 190.5, 36.68, 772.2, 205.3, 35.78, 846.0, 304.1, 36.0, 1345.0, 417.5, 36.25, 1944.0, 362.2, 36.74, 1659.0, 313.2, 36.71, 1391.0, 264.2, 35.89, 1128.0, 254.4, 36.02, 1066.0, 261.8, 35.24, 1107.0, 270.8, 35.2, 1151.0, 264.2, 35.09, 1125.0, 254.3, 35.06, 1077.0]


    algs = AIAlgorithm.objects.filter(availability=True)
    
    alg_index = 0

    algorithm_object = registry.algorithms[algs[alg_index].id]

    prediction = algorithm_object.compute_prediction(input_data)
    
    #Insert forecast into db
    p1, p2, p3, p4, p5 = prediction
    pf = PowerForecast.objects.create(timestamp=timestamp,
                                    t1=p1,
                                    t2=p2,
                                    t3=p3,
                                    t4=p4,
                                    t5=p5)