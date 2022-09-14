import pandas as pd
from pytz import timezone
from datetime import datetime, timedelta

from api import settings

from .models import AlertTreshold, Settings

def read_dat_file(filename):
    """
    Read .dat file, discards some row headers and returns appropriate values.
    Parameters
    ----------
    filename : string with path and filename do .dat file
    Returns
    -------
    df : pandas.DataFrame
        A pandas dataframe contatining the data.
    """
    df = pd.read_csv(filename, skiprows=3)
    df_aux = pd.read_csv(filename, header=1)
    df.columns = df_aux.columns

    cols_to_drop = ['RECORD', 'Excedente_Avg', 'Compra_Avg']
    for col in cols_to_drop:
        if col in df.columns:
            df = df.drop([col], axis=1)

    for column in df.columns:
        if column != "TIMESTAMP":
            df[column] = df[column].astype('float')
    # Drop column 'RECORD' (if present) because from june 2019 is is no longer used
    return df

def get_time_inteval(request):
    return int(request.GET.get('time_interval', 10))

def get_time_range(request):
    time_end = request.GET.get('time_end', stringify_datetime(timestamp_aware()))
    time_begin = request.GET.get('time_begin', stringify_datetime(timestamp_aware() - timedelta(days=1)))
    return time_begin, time_end

def get_string_number(request):
    return request.GET.get('string_number', 1)

def generate_forecast_json(data):
    length = len(data)

    if length == 0:
        return []

    json_array = []
    for i in range(1, length):
        json_data = {
            'timestamp': data[i]['timestamp'],
            'forecast': data[i-1]['t1']
        }
        json_array.append(json_data)

    latest_data = data[length-1]
    datetime_forecast = datetime.strptime(latest_data['timestamp'], '%Y-%m-%dT%H:%M:%S.%f%z')

    datetime_forecast = datetime_forecast + timedelta(minutes=1)
    json_array.append({
        'timestamp': stringify_datetime(datetime_forecast),
        'forecast': latest_data['t1']
    })

    datetime_forecast = datetime_forecast + timedelta(minutes=1)
    json_array.append({
        'timestamp': stringify_datetime(datetime_forecast),
        'forecast': latest_data['t2']
    })

    datetime_forecast = datetime_forecast + timedelta(minutes=1)
    json_array.append({
        'timestamp': stringify_datetime(datetime_forecast),
        'forecast': latest_data['t3']
    })

    datetime_forecast = datetime_forecast + timedelta(minutes=1)
    json_array.append({
        'timestamp': stringify_datetime(datetime_forecast),
        'forecast': latest_data['t4']
    })

    datetime_forecast = datetime_forecast + timedelta(minutes=1)
    json_array.append({
        'timestamp': stringify_datetime(datetime_forecast),
        'forecast': latest_data['t5']
    })

    return json_array

def alert_definition(alert_type, string_number, meteorological_value, value):
    st = Settings.objects.get_or_create(id=1)

    try:
        threshold = AlertTreshold.objects.get(alert_type=alert_type, string_number=string_number, meteorological_value=round(meteorological_value))
        
        alert = 'NR'
        
        if threshold and st.alert_days_active:
            if (value >= threshold.treshold_ft_max or value <= threshold.treshold_ft_min) and st.fault_user_active:
                alert = 'FT'
            elif (value >= threshold.treshold_wa_max or value <= threshold.treshold_wa_min) and st.warning_user_active:
                alert = 'WA'
            else:
                alert = 'NM'
    except:
        alert = 'NR'

    return alert

def timestamp_aware():
    tz = timezone(settings.TIME_ZONE)
    datetime_aware = tz.localize(datetime.now())

    return datetime_aware

def stringify_datetime(datetime):
    return str(datetime).replace(' ', 'T')
