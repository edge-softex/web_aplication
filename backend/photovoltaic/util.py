from email import message
import numbers
import pandas as pd
from pytz import timezone
from datetime import datetime, timedelta

from api import settings

from .models import AlertThreshold, Settings, Log

def read_dat_file(filename):
    """Read .dat file, discards some row headers and returns appropriate values.
   
    param filename: path and filename do .dat file
    type filename: str
    
    :rtype: pandas.DataFrame
    :return: a pandas dataframe contatining the data
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
    """Get the value contained in the request and return as an integer.
   
    time_interval: time interval in minutes that the data will be filtered
    type filename: int
    
    :rtype: int
    :return: time interval in minutes that the data will be filtered
    """

    return int(request.GET.get('time_interval', 10))

def get_time_range(request):
    """Get the values contained in the request and return them as strings.
   
    time_begin: initial datetime to filter the data, default is 24 hours less than the current datetime
    type time_begin: str (yyyy-MM-ddTHH:mm:ss.SZ)
    time_end: final datetime to filter the data, default is the current datetime
    type time_end: str (yyyy-MM-ddTHH:mm:ss.SZ)
    
    :rtype: str
    :return: two strings with the start and end timestamp
    """

    time_end = request.GET.get('time_end', stringify_datetime(timestamp_aware()))
    time_begin = request.GET.get('time_begin', stringify_datetime(timestamp_aware() - timedelta(days=1)))
    return time_begin, time_end

def get_string_number(request):
    """Get the value contained in the request and return as an integer.
   
    string_number: number that identifies the queried string
    type string_number: int
    
    :rtype: int
    :return: number that identifies the queried string
    """

    return request.GET.get('string_number', 1)

def generate_forecast_json(data):
    """Transforms the instant power forecast dataset into a json in the format that should be displayed by the frontend.
   
    param data: json set containing the forecast data
    type data: json array
    
    :rtype: json array
    :return: json array in the format that should be displayed by the frontend
    """

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

def createAlertLog(self, alert_severity, alert_type, string_number, value):
    """Generates a log message regarding the activation of an alert.
   
    param alert_severity: indicates which severity of alert has been activated
    type alert_severity: str
    param alert_type: indicates whether the alert was activated by current or voltage
    type alert_type: str
    param string_number: number that identifies the string
    type string_number: int
    param value: voltage or current value that triggered the alert
    type value: float
    """

    if alert_severity == 'FT':
        alert_severity = 'FAULT'
    elif alert_severity == 'WA':
        alert_severity = 'WARNING'

    if alert_type == 'VT':
        alert_type = 'Voltage'
        mu = 'V'
    elif alert_type == 'CR':
        alert_type = 'Current'
        mu = 'A'

    title = 'Alert Activation.'
    message = '{type} on String {number} has reached an {alert} level: {value} {mu}'.format(
        type=alert_type, number=string_number, alert=alert_severity, value=value, mu=mu)
    self.createLog(title, message)

def createLog(self, title, message):
    """Generate a log message.
   
    param title: title which indicates the type of log message
    type title: str
    param message: message with log content 
    type message: str
    """

    log = Log.create(title=title, message=message)
    log.save()


def alert_definition(alert_type, string_number, meteorological_value, value):
    """Evaluates current and voltage value to detect fault.
   
    param alert_type: indicates whether the alert was activated by current or voltage
    type alert_type: str
    param string_number: number that identifies the queried string
    type string_number: int
    param meteorological_value: value of the meteorological variable related to the current or voltage value used in the evaluation
    type meteorological_value: float
    param value: voltage or current value that will be evaluated
    type value: float
    """

    st = Settings.objects.get_or_create(id=1)

    try:
        threshold = AlertThreshold.objects.get(alert_type=alert_type, string_number=string_number, meteorological_value=round(meteorological_value))
        
        alert = 'NR'
        
        if threshold and st.alert_days_active:
            if (value >= threshold.threshold_ft_max or value <= threshold.threshold_ft_min) and st.fault_user_active:
                alert = 'FT'
                createLog(alert, alert_type, string_number, value)
            elif (value >= threshold.threshold_wa_max or value <= threshold.threshold_wa_min) and st.warning_user_active:
                alert = 'WA'
                createLog(alert, alert_type, string_number, value)
            else:
                alert = 'NM'
    except:
        alert = 'NR'

    return alert

def timestamp_aware():
    """Returns the current datetime object with the timezone included.
   
    :rtype: datetime
    :return: current datetime with the timezone
    """
    tz = timezone(settings.TIME_ZONE)
    datetime_aware = tz.localize(datetime.now())

    return datetime_aware

def stringify_datetime(datetime):
    """Stringify a datetime object to standard django format.
    
    param datetime: datetime object to be stringfy
    type datetime: datetime

    :rtype: str
    :return: stringify datetime
    """
    return str(datetime).replace(' ', 'T')
