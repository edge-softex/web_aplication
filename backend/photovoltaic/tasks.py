from calendar import month
from email.policy import default
from celery import shared_task

from datetime import datetime, timedelta
from dateutil.relativedelta import *
from pytz import timezone
import random
import re

import pandas as pd
import numpy as np

import tensorflow as tf

from api import settings

from .util import read_dat_file, stringify_datetime, timestamp_aware, alert_definition, convert_ambient_temp_to_pv, get_estimated_power

from photovoltaic.models import PVData, PVString, PowerForecast, IrradianceForecast, AmbientTemperatureForecast, PVModuleTemperatureForecast, YieldDay, YieldMonth, YieldYear, YieldMinute, AlertThreshold, Settings, Log, AIAlgorithm
from photovoltaic.serializers import PVDataSerializer

from api.wsgi import registry

import time

def createLog(self, exc, task_id, args, kwargs, einfo):
    log = Log.create(title='Backend system error.', message='Task execution error {task}: {einfo}'.format(task=task_id, einfo=einfo))
    log.save()

@shared_task(bind=True, max_retries=3, on_failure=createLog)
def simulate_input(self):
    """Simulates data entry to perform system tests."""

    tz = timezone(settings.TIME_ZONE)
    datetime_now = tz.localize(datetime.now())
    datetime_string = str(datetime_now).replace(' ', 'T')
    
    df = read_dat_file('./photovoltaic/fixtures/{}.dat'.format(datetime_now.day))
    #df = read_dat_file('./photovoltaic/fixtures/test_day_actual.dat')

    index = datetime_now.hour*60 + datetime_now.minute

    df_row = df.iloc[[index]]

    # s1 = PVString.objects.create(name='S1 ' + datetime_string, 
    #                             timestamp=datetime_now,
    #                             voltage=df_row['Tensao_S1_Avg'],
    #                             current=df_row['Corrente_S1_Avg'],
    #                             power=df_row['Potencia_S1_Avg'],
    #                             voltage_alert=np.random.choice(['NM', 'WA', 'FT'], p=[0.88, 0.10, 0.02]),
    #                             current_alert=np.random.choice(['NM', 'WA', 'FT'], p=[0.88, 0.10, 0.02]),
    #                             string_number=1)
    
    # s2 = PVString.objects.create(name='S2 ' + datetime_string,
    #                             timestamp=datetime_now,
    #                             voltage=df_row['Tensao_S2_Avg'],
    #                             current=df_row['Corrente_S2_Avg'],
    #                             power=df_row['Potencia_S2_Avg'],
    #                             voltage_alert=np.random.choice(['NM', 'WA', 'FT'], p=[0.83, 0.15, 0.02]),
    #                             current_alert=np.random.choice(['NM', 'WA', 'FT'], p=[0.83, 0.15, 0.02]),
    #                             string_number=2)

    data = PVData.objects.create(timestamp=datetime_now,
                                irradiance=df_row['Radiacao_Avg'],
                                temperature_pv=df_row['Temp_Cel_Avg'],
                                temperature_amb=df_row['Temp_Amb_Avg'],
                                power_avg=df_row['Potencia_FV_Avg'])

    # data.strings.set([s1, s2])

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

    # power1 = float(df.iloc[[index+1]]['Potencia_FV_Avg'])
    # power2 = float(df.iloc[[index+2]]['Potencia_FV_Avg'])
    # power3 = float(df.iloc[[index+3]]['Potencia_FV_Avg'])
    # power4 = float(df.iloc[[index+4]]['Potencia_FV_Avg'])
    # power5 = float(df.iloc[[index+5]]['Potencia_FV_Avg'])

    #instant_power_forecast.apply_async(args=[], kwargs={}, queue='run_models')
    estimated_instant_power_forecast.apply_async(args=[], kwargs={}, queue='run_models')

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
                                    power_avg=power1,
                                    t1=power1 + random.uniform(0, 1.0),
                                    t2=power2 + random.uniform(0.3, 1.3),
                                    t3=power3 + random.uniform(0.6, 1.6),
                                    t4=power4 + random.uniform(0.9, 1.9),
                                    t5=power5 + random.uniform(1.2, 2.2))


@shared_task(bind=True, max_retries=3, on_failure=createLog)
def calculate_alerts_thresholds(self):
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
                    
                    alert_th, created = AlertThreshold.objects.get_or_create(alert_type='CR', string_number=string_number+1, meteorological_value=value)
                    alert_th.threshold_ft_max = th[0]
                    alert_th.threshold_ft_min = th[1]
                    alert_th.threshold_wa_max = th[2]
                    alert_th.threshold_wa_min = th[3]
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

                    alert_th, created = AlertThreshold.objects.get_or_create(alert_type='VT', string_number=string_number+1, meteorological_value=value)
                    alert_th.threshold_ft_max = th[0]
                    alert_th.threshold_ft_min = th[1]
                    alert_th.threshold_wa_max = th[2]
                    alert_th.threshold_wa_min = th[3]
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
    data_time = datetime.strptime(request_data['timestamp'], '%Y-%m-%dT%H:%M:%S.%f%z')

    if(data_time.microsecond == 0):
        data_time = data_time + timedelta(milliseconds=0.001)

    # if request_data['temperature_pv'] is not None:
    #     temperature = request_data['temperature_pv']
    # elif request_data['temperature_amb'] is not None:
    #     temperature = request_data['temperature_amb']
    # else:
    #     temperature = 0

    # if request_data['irradiance'] is not None:
    #     irradiance = request_data['irradiance']
    # else:
    #     irradiance = 0 

    # for string in request_data['strings']:
    #     if string['power'] is None and string['voltage'] is not None and string['current'] is not None:
    #         string_power = string['voltage'] * string['current']
    #     else:
    #         string_power = string['power']
    #     string_obj = PVString.objects.create(name='S' + str(string['string_number']) + ' ' + request_data['timestamp'], 
    #                             timestamp=stringify_datetime(data_time),
    #                             voltage=string['voltage'],
    #                             current=string['current'],
    #                             power=string_power,
    #                             voltage_alert=alert_definition('VT', string['string_number'], temperature, string['voltage']),
    #                             current_alert=alert_definition('CR', string['string_number'], irradiance, string['current']),
    #                             string_number=string['string_number'])
    #     strings_ref.append(string_obj)
    
    temp_pv_estimate = convert_ambient_temp_to_pv(request_data['temperature_amb'], request_data['irradiance'])

    data = PVData.objects.create(timestamp=stringify_datetime(data_time),
                                irradiance=request_data['irradiance'],
                                temperature_pv=temp_pv_estimate,
                                temperature_amb=request_data['temperature_amb'],
                                humidity=request_data['humidity'],
                                wind_speed=request_data['wind_speed'],
                                wind_direction=request_data['wind_direction'],
                                rain=request_data['rain'],
                                open_circuit_voltage=request_data['ocv'],
                                short_circuit_current=request_data['scc'])

    # data.strings.set(strings_ref)

    day = data_timestamp.split('T')[0] + "T00:00:00.000000-03:00"
    yield_day, created = YieldDay.objects.get_or_create(timestamp=day)

    if request_data['generation'] is None and request_data['power_avg'] is None:
        power = 0
        energy = 0
    elif request_data['generation'] is None and request_data['power_avg'] is not None:
        power = request_data['power_avg']
        energy = request_data['power_avg']*(1/60)/1000
    elif request_data['generation'] is not None and request_data['power_avg'] is None:
        energy = request_data['generation'] - yield_day.yield_day
        power = energy*60*1000
    else:
        power = request_data['power_avg']
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

    estimated_instant_power_forecast.apply_async(args=[], kwargs={}, queue='run_models')

@shared_task(bind=True, max_retries=3, on_failure=createLog)
def instant_power_forecast(self):
    """ Function that uses a neural network model to process 120 minutes of irradiance, temperature of the PV module and instant power data to forecasts 5 minute of instant power. Then saves it in the database.
    """
    
    algs = AIAlgorithm.objects.filter(availability=True)

    alg_index = 0
    
    algorithm_object = registry.algorithms[algs[alg_index].id]
    
    if  algorithm_object.update == True:
        algorithm_object.update_model("lstm/model.h5")

    tz = timezone(settings.TIME_ZONE)
    datetime_now = tz.localize(datetime.now())
    
    datetime_gte = datetime_now - timedelta(minutes=120)
    data = PVData.objects.filter(timestamp__gte=datetime_gte, timestamp__lte=datetime_now).order_by('timestamp')
    
    timestamp = list(data.values_list('timestamp', flat=True))
    irradiance = list(data.values_list('irradiance', flat=True))
    temperature_pv = list(data.values_list('temperature_pv', flat=True))
    power_avg = list(data.values_list('power_avg', flat=True))

    input_data = irradiance+temperature_pv+power_avg

    if len(input_data) != 360:
        input_data = input_data + [0]*(360 - len(input_data)) 
 
    prediction = algorithm_object.compute_prediction(input_data)
 
    #Insert forecast into db
    p1, p2, p3, p4, p5 = prediction
    pf = PowerForecast.objects.create(timestamp=timestamp[-1],
                                    power_avg=power_avg[-1],
                                    t1=p1,
                                    t2=p2,
                                    t3=p3,
                                    t4=p4,
                                    t5=p5)
    
@shared_task(bind=True, max_retries=3, on_failure=createLog)

def estimated_instant_power_forecast(self):
    """ Function that uses a neural network model (LSTM or Dlinear) to process 120 minutes of irradiance and ambient temperature to forecasts 5 minute of the same input features. Then uses this forecasts to estimate the next 5 minutes of PV instant power. Finally saves it in the database.
    """
    algs = AIAlgorithm.objects.filter(availability=True)

    alg_index = 0
    
    algorithm_object = registry.algorithms[algs[alg_index].id]
    
    if  algorithm_object.update == True:
        algorithm_object.update_model(algs[alg_index].path)

    tz = timezone(settings.TIME_ZONE)
    datetime_now = tz.localize(datetime.now())
    
    datetime_gte = datetime_now - timedelta(minutes=120)
    data = PVData.objects.filter(timestamp__gte=datetime_gte, timestamp__lte=datetime_now).order_by('timestamp')
    
    timestamp = list(data.values_list('timestamp', flat=True))
    irradiance = list(data.values_list('irradiance', flat=True))
    temperature_amb = list(data.values_list('temperature_amb', flat=True))
    power_avg = list(data.values_list('power_avg', flat=True))

    input_data = irradiance+temperature_amb

    required_input_lenght = len(algorithm_object.input_labels) * algorithm_object.input_steps
    if len(input_data) != required_input_lenght:
        input_data = input_data + [0.0]*(required_input_lenght - len(input_data)) 

    prediction = algorithm_object.compute_prediction(input_data)
        
    irr = [0 if i < 0 else i for i in prediction[:,0]]
    amb_temp = [0 if i < 0 else i for i in prediction[:,1]]

    pv_temp = [convert_ambient_temp_to_pv(a, b) for a,b in zip(amb_temp,irr)]

    instant_power = [get_estimated_power(a, b) for a,b in zip(irr, pv_temp)]
    
    p1, p2, p3, p4, p5 = instant_power

    #Insert forecast into db
    # pf = PowerForecast.objects.create(timestamp=timestamp[-1], power_avg=power_avg[-1], t1=p1, t2=p2, t3=p3, t4=p4, t5=p5)
    # irrf = IrradianceForecast.objects.create(timestamp=timestamp[-1], t1=irr[0], t2=irr[1], t3=irr[2], t4=irr[3], t5=irr[4])
    # ambtempf = AmbientTemperatureForecast.objects.create(timestamp=timestamp[-1], t1=amb_temp[0], t2=amb_temp[1], t3=amb_temp[2], t4=amb_temp[3], t5=amb_temp[4])
    # pvtempf = PVModuleTemperatureForecast.objects.create(timestamp=timestamp[-1], t1=pv_temp[0], t2=pv_temp[1], t3=pv_temp[2], t4=pv_temp[3], t5=pv_temp[4])

    
@shared_task(bind=True, max_retries=3, on_failure=createLog)
def model_retraining(self):
    """ Function that retrains the neural network then calls the "model_updating" task.
    """
    st, created = Settings.objects.get_or_create(id=1)    
    
    tz = timezone(settings.TIME_ZONE)
    datetime_now = tz.localize(datetime.now())

    datetime_gte = datetime_now +relativedelta(months=-st.retraining_interval)

    df = pd.DataFrame.from_records(PVData.objects.filter(timestamp__gte=datetime_gte, timestamp__lte=datetime_now).values())
    
    algs = AIAlgorithm.objects.all()
    
    alg_index = 0

    algorithm_object = registry.algorithms[algs[alg_index].id]
    
    if not df.empty:
        algorithm_object.retraining(df)
        model_updating.apply_async(args=[], kwargs={}, queue='run_models')
    else:
        print("Training skiped")


    
@shared_task(bind=True, max_retries=3, on_failure=createLog)
def model_updating(self):
    """ Function that indicates that the neural network model needs to be updated in the "instant_power_forecast" task.
    """
    algs = AIAlgorithm.objects.all()
    
    alg_index = 0

    algorithm_object = registry.algorithms[algs[alg_index].id]
    
    algorithm_object.update = True
