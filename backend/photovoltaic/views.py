import re

from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import viewsets

from django.contrib.auth.models import User
from django.contrib.auth import login, logout

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from api import settings

from .util import (get_time_inteval,
    get_time_range,
    get_string_number,
    generate_forecast_json,
    timestamp_aware,
    stringify_datetime,
    createLog)

from .tasks import set_data

from .serializers import (
    UserSerializer,
    LoginSerializer,
    PVDataSerializer,
    PVStringSerializer,
    PVDataMeteorologicalSerializer,
    PVDataPowerSerializer,
    PowerForecastSerializer,
    YieldDaySerializer,
    YieldMonthSerializer,
    YieldYearSerializer,
    YieldMinuteSerializer,
    AlertThresholdSerializer,
    SettingaSerializer,
    LogSerializer)

from .models import (
    PVData,
    PVString,
    PowerForecast,
    YieldDay,
    YieldMonth,
    YieldYear,
    YieldMinute,
    AlertThreshold,
    Settings,
    Log)

class DynamicPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 1440

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['GET'], url_path='profile', detail=False)
    def profile(self, request):
        """Returns the data of the logged user.
        
        :rtype: Response
        :return: User (username, email, first_name, last_name)
        """

        return Response(UserSerializer(request.user).data)

    @action(methods=['POST'], url_path='createuser', detail=False)
    def create_user(self, request):
        """Create a new user on the database.

        username: unique text that will be used by the user to login
        type username: str
        first_name: user's first name
        type first_name: str
        last_name: user's last name
        type last_name: str
        email: user's email
        type email: str
        password: secret text used by the user to login
        type password: str
        
        :rtype: Response
        :return: status
        """

        request_data = request.data

        try:
            user = User.objects.create(
                first_name=request_data['first_name'],
                last_name=request_data['last_name'],
                username=request_data['username'],
                email=request_data['email'],
                is_staff=True,
                is_superuser=False,
            )
            user.set_password(request_data['password'])

            user.save()
        except:
            return Response(status=400)

        return Response(status=200)

    @action(methods=['DELETE'], url_path='deactivateuser', detail=False)
    def deactivate_user(self, request):
        """Deactivate the user in the database.

        username: unique text that will be used by the user to login
        type username: str
        
        :rtype: Response
        :return: status
        """

        request_data = request.data

        try:
            user = User.objects.get(username=request_data['username'])
            user.is_active = False
            user.save()
        except:
            return Response(status=400)

        return Response(status=200)

    @action(methods=['POST'], url_path='edituser', detail=False)
    def edit_user(self, request):
        """Change the data of a user that already exists in the database. To not change a data, just provide None.

        username: unique text that will be used by the user to login
        type username: str
        first_name: user's first name
        type first_name: str
        last_name: user's last name
        type last_name: str
        email: user's email
        type email: str
        password: secret text used by the user to login
        type password: str
        
        :rtype: Response
        :return: status
        """

        request_data = request.data

        try:
            user = User.objects.get(username=request_data['username'])
            
            if request_data['new_username']:
                user.username = request_data['new_username']
            if request_data['first_name']:
                user.first_name = request_data['first_name']
            if request_data['last_name']:
                user.last_name = request_data['last_name']
            if request_data['email']:
                user.email = request_data['email']
            if request_data['password']:
                user.set_password(request_data['password'])

            user.save()
        except:
            return Response(status=400)

        return Response(status=200)

class AccountsViewSet(viewsets.ViewSet):

    permission_classes = [permissions.AllowAny]

    @action(methods=['POST'], url_path='login', detail=False)
    def login_(self, request):
        """Perform user login.

        username: unique text that will be used by the user to login
        type username: str
        password: secret text used by the user to login
        type password: str
        
        :rtype: Response
        :return: status
        """

        serializer = LoginSerializer(data=request.data, context={ 'request': request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(status=202)

    @action(methods=['POST'], url_path='logout', detail=False)
    def logout_(self, request):
        """Perform user logout.
        
        :rtype: Response
        :return: status
        """

        logout(request)
        return Response(status=202)

    @action(methods=['GET'], url_path='token', detail=False)
    def get_token(self, request):
        """Returns the user token and system timezone. Used by the Solaire library.

        username: unique text that will be used by the user to login
        type username: str
        password: secret text used by the user to login
        type password: str
        
        :rtype: Response
        :return: token, timezone
        """

        serializer = LoginSerializer(data=request.data, context={ 'request': request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'timezone': settings.TIME_ZONE
        })

class PVDataViewSet(viewsets.ModelViewSet):

    queryset = PVData.objects.all()
    serializer_class = PVDataSerializer
    pagination_class = DynamicPagination

    @action(methods=['GET'], url_path='status', detail=False)
    def pv_system_status(self, request):
        """Returns the PV system status.
        
        :rtype: Response
        :return: status (system status)
        """

        latest_data = PVDataSerializer(PVData.objects.latest('timestamp')).data

        time_now = timestamp_aware()
        time_data = datetime.strptime(latest_data['timestamp'], '%Y-%m-%dT%H:%M:%S.%f%z')
        delta = time_now - time_data
        minutes = delta / timedelta(minutes=1)

        status_string = 'Normal'
        status = 'normaloperation'
        if(minutes >= 3):
            status_string = 'Offline'
            status = 'offline'
        else:
            for string in latest_data['strings']:
                if string['voltage_alert'] == 'WA' or string['current_alert'] == 'WA':
                    status_string = 'Warning'
                    status = 'warning'
                if string['voltage_alert'] == 'FT' or string['current_alert'] == 'FT':
                    status_string = 'Fault'
                    status = 'fault'
                    break
        
        json_response = {
            'status': status,
            'status_string': status_string
        }

        return Response(json_response)

    @action(methods=['GET'], url_path='latest', detail=False)
    def pv_data_latest(self, request):
        """Returns the last received PV system dataset.
        
        :rtype: Response
        :return: PVData (timestamp, irradiance, temperature_pv, temperature_amb, power_avg, strings)
        """

        latest_data = PVData.objects.latest('timestamp')
        return Response(PVDataSerializer(latest_data).data)

    @action(methods=['GET'], url_path='meteorologicalday', detail=False)
    def meteorological_day(self, request):
        """Returns meteorological data for the last 24 hours (max 1440 datasets).
        
        :rtype: Response
        :return: list of PVData (timestamp, irradiance, temperature_pv, temperature_amb)
        """
        now = timestamp_aware()
        datetime_lte = stringify_datetime(now)
        yesterday = now - timedelta(days=1)
        datetime_gte = stringify_datetime(yesterday)
        day_data = PVData.objects.filter(timestamp__gte=datetime_gte, timestamp__lte=datetime_lte)

        meteorological_data = PVDataMeteorologicalSerializer(day_data, many=True).data

        timestamp = [item['timestamp'].split('.')[0] for item in meteorological_data]
        irradiance = [item['irradiance'] for item in meteorological_data]
        temperature_pv = [item['temperature_pv'] for item in meteorological_data]
        temperature_amb = [item['temperature_amb'] for item in meteorological_data]

        data_json = {
            'timestamp': timestamp,
            'irradiance': irradiance,
            'temperature_pv': temperature_pv,
            'temperature_amb': temperature_amb
        }

        return Response(data_json)

    @action(methods=['GET'], url_path='powerday', detail=False)
    def power_day(self, request):
        """Returns the power data and power forecast of the last 24 hours (max 1440 datasets).
        
        :rtype: Response
        :return: list of PVData (timestamp, power_avr)
        """

        time_interval = get_time_inteval(request)

        now = timestamp_aware()
        datetime_lte = stringify_datetime(now)
        yesterday = now - timedelta(minutes=time_interval)
        datetime_gte = stringify_datetime(yesterday)

        power_data = PVData.objects.filter(timestamp__gte=datetime_gte, timestamp__lte=datetime_lte)
        power_json = PVDataSerializer(power_data, many=True).data

        yesterday = now - timedelta(minutes=time_interval+1)
        datetime_gte = stringify_datetime(yesterday)
        
        power_forecast = PowerForecast.objects.filter(timestamp__gte=datetime_gte, timestamp__lte=datetime_lte)
        forecast_json = generate_forecast_json(PowerForecastSerializer(power_forecast, many=True).data)

        power_timestamp = [item['timestamp'].split('.')[0] for item in power_json]
        power_avg = [item['power_avg'] for item in power_json]

        fc_timestamp = [item['timestamp'].split('.')[0] for item in forecast_json]
        forecast = [item['forecast'] for item in forecast_json]

        if(power_timestamp):
            if(power_timestamp[0] != fc_timestamp[0]):
                fc_timestamp.insert(0, power_timestamp[0])

        if(len(fc_timestamp) > len(forecast)):
            forecast.insert(0, 0)

        timestamp_list = []

        for i in range(0, len(power_timestamp)):
            p_datatime = datetime.strptime(power_timestamp[i], '%Y-%m-%dT%H:%M:%S').replace(second=0, microsecond=0)
            power_timestamp[i] = p_datatime
            timestamp_list.append(p_datatime)

        for i in range(0, len(fc_timestamp)):
            fc_datatime = datetime.strptime(fc_timestamp[i], '%Y-%m-%dT%H:%M:%S').replace(second=0, microsecond=0)
            fc_timestamp[i] = fc_datatime
            timestamp_list.append(fc_datatime)

        timestamp_list = sorted(timestamp_list)
        timestamp_list = list(dict.fromkeys(timestamp_list))

        aux_power = [None] * len(timestamp_list)
        aux_forecast = [None] * len(timestamp_list)

        for i in range(0, len(timestamp_list)):
            for j in range(0, len(power_timestamp)):
                if power_timestamp[j] == timestamp_list[i]:
                    aux_power[i] = power_avg[j]
                    break

            for j in range(0, len(fc_timestamp)):
                if fc_timestamp[j] == timestamp_list[i]:
                    aux_forecast[i] = forecast[j]
                    break

        for time in timestamp_list:
            time = stringify_datetime(time).split('.')[0]

        if not timestamp_list:
            timestamp_list = ['None', 'None', 'None', 'None', 'None', 'None']

        if not aux_power:
            aux_power = [0, 0, 0, 0, 0, 0]

        if not aux_forecast:
            aux_forecast = [0, 0, 0, 0, 0, 0]

        data_json = {
            'timestamp': timestamp_list,
            'data': aux_power,
            'forecast': aux_forecast 
        }

        return Response(data_json)

    @action(methods=['GET'], url_path='history', detail=False)
    def pv_data_history(self, request):
        """Returns the PVData set between the given timestamps. By default it returns data for the last 24 hours.

        time_begin: initial datetime to filter the data, default is 24 hours less than the current datetime
        type time_begin: str (yyyy-MM-ddTHH:mm:ss.SZ)
        time_end: final datetime to filter the data, default is the current datetime
        type time_end: str (yyyy-MM-ddTHH:mm:ss.SZ)
        page: number of the page in which the data is separated, default is 1
        type page: int
        
        :rtype: Paginated Response
        :return: list of PVData (timestamp, irradiance, temperature_pv, temperature_amb, power_avg, strings)
        """

        time_begin, time_end = get_time_range(request)

        pv_data = PVData.objects.filter(timestamp__gte=time_begin, timestamp__lte=time_end)
        page = self.paginate_queryset(pv_data)

        if page is not None:
            serializer = PVDataSerializer(page, many=True).data
            return Response(self.get_paginated_response(serializer).data)

        return Response(PVDataSerializer(pv_data, many=True).data)

class PVStringViewSet(viewsets.ModelViewSet):

    queryset = PVString.objects.all()
    serializer_class = PVStringSerializer
    pagination_class = DynamicPagination

    @action(methods=['GET'], url_path='history', detail=False)
    def pv_string_history(self, request):
        """Returns the PVString set between the given timestamps. By default it returns data for the last 24 hours.

        string_number: number that identifies the queried string, default is 1
        type string_number: int
        time_begin: initial datetime to filter the data, default is 24 hours less than the current datetime
        type time_begin: str (yyyy-MM-ddTHH:mm:ss.SZ)
        time_end: final datetime to filter the data, default is the current datetime
        type time_end: str (yyyy-MM-ddTHH:mm:ss.SZ)
        page: number of the page in which the data is separated, default is 1
        type page: int
        
        :rtype: Paginated Response
        :return: list of PVString (name, timestamp, voltage, current, power, volatge_alert, current_alert, string_number)
        """

        number = get_string_number(request)
        time_begin, time_end = get_time_range(request)

        string_data = PVString.objects.filter(string_number=number, timestamp__gte=time_begin, timestamp__lte=time_end)
        page = self.paginate_queryset(string_data)

        if page is not None:
            serializer = PVStringSerializer(page, many=True).data
            return Response(self.get_paginated_response(serializer).data)

        return Response(PVStringSerializer(string_data, many=True).data)

class PowerForecastViewSet(viewsets.ModelViewSet):

    queryset = PowerForecast.objects.all()
    serializer_class = PowerForecastSerializer
    pagination_class = DynamicPagination

    @action(methods=['GET'], url_path='forecastday', detail=False)
    def forecast_day(self, request):
        """Returns the power forecast data of the last x minutes (max 1445 datasets).

        time_interval: time interval in minutes that the data will be filtered, default is 10
        type time_interval: int
        
        :rtype: Response
        :return: list of PowerForecast (timestamp, t1, t2, t3, t4, t5)
        """

        time_interval = get_time_inteval(request)

        now = timestamp_aware()
        datetime_lte = stringify_datetime(now)
        yesterday = now - timedelta(minutes=time_interval+1)
        datetime_gte = stringify_datetime(yesterday)
        power_forecast = PowerForecast.objects.filter(timestamp__gte=datetime_gte, timestamp__lte=datetime_lte)

        forecast_json = generate_forecast_json(PowerForecastSerializer(power_forecast, many=True).data)

        return Response(forecast_json)

    @action(methods=['GET'], url_path='history', detail=False)
    def power_forecast_history(self, request):
        """Returns the PowerForecast set between the given timestamps. By default it returns data for the last 24 hours.

        time_begin: initial datetime to filter the data, default is 24 hours less than the current datetime
        type time_begin: str (yyyy-MM-ddTHH:mm:ss.SZ)
        time_end: final datetime to filter the data, default is the current datetime
        type time_end: str (yyyy-MM-ddTHH:mm:ss.SZ)
        page: number of the page in which the data is separated, default is 1
        type page: int
        
        :rtype: Paginated Response
        :return: list of PowerForecast (timestamp, t1, t2, t3, t4, t5)
        """

        time_begin, time_end = get_time_range(request)

        forecast_data = PowerForecast.objects.filter(timestamp__gte=time_begin, timestamp__lte=time_end)
        page = self.paginate_queryset(forecast_data)

        if page is not None:
            serializer = PowerForecastSerializer(page, many=True).data
            return Response(self.get_paginated_response(serializer).data)

        return Response(PowerForecastSerializer(forecast_data, many=True).data)

class YieldDayViewSet(viewsets.ModelViewSet):

    queryset = YieldDay.objects.all()
    serializer_class = YieldDaySerializer
    pagination_class = DynamicPagination

    @action(methods=['GET'], url_path='now', detail=False)
    def yield_now(self, request):
        """Returns the last yield data.
        
        :rtype: Response
        :return: YieldDay (timestamp, yield_day, yield_day_forecast)
        """

        yield_today = YieldDay.objects.latest('timestamp')
        return Response(YieldDaySerializer(yield_today).data)

    @action(methods=['GET'], url_path='latest10', detail=False)
    def yield_latest_10(self, request):
        """Returns the yield day data of the last 10 days.
        
        :rtype: Response
        :return: list of YieldDay (timestamp, yield_day, yield_day_forecast)
        """

        now = timestamp_aware()
        datetime_lte = stringify_datetime(now)
        yesterday = now - timedelta(days=10)
        datetime_gte = stringify_datetime(yesterday)
        yield_days = YieldDay.objects.filter(timestamp__gte=datetime_gte, timestamp__lte=datetime_lte)
        yield_json = YieldDaySerializer(yield_days, many=True).data[-10: ]

        timestamp = [item['timestamp'].split('T')[0] for item in yield_json]
        yield_ = [item['yield_day'] for item in yield_json]
        yield_day_forecast = [item['yield_day_forecast'] for item in yield_json]

        data_json = {
            'timestamp': timestamp,
            'data': yield_,
            'forecast': yield_day_forecast
        }

        return Response(data_json)

    @action(methods=['GET'], url_path='history', detail=False)
    def yield_day_history(self, request):
        """Returns the YieldDay set between the given timestamps. By default it returns data for the last 24 hours.

        time_begin: initial datetime to filter the data, default is 24 hours less than the current datetime
        type time_begin: str (yyyy-MM-ddTHH:mm:ss.SZ)
        time_end: final datetime to filter the data, default is the current datetime
        type time_end: str (yyyy-MM-ddTHH:mm:ss.SZ)
        page: number of the page in which the data is separated, default is 1
        type page: int
        
        :rtype: Paginated Response
        :return: list of YieldDay (timestamp, yield_day, yield_day_forecast)
        """

        time_begin, time_end = get_time_range(request)

        yield_data = YieldDay.objects.filter(timestamp__gte=time_begin, timestamp__lte=time_end)
        page = self.paginate_queryset(yield_data)

        if page is not None:
            serializer = YieldDaySerializer(page, many=True).data
            return Response(self.get_paginated_response(serializer).data)

        return Response(YieldDaySerializer(yield_data, many=True).data)

class YieldMonthViewSet(viewsets.ModelViewSet):

    queryset = YieldMonth.objects.all()
    serializer_class = YieldMonthSerializer
    pagination_class = DynamicPagination

    @action(methods=['GET'], url_path='latest12', detail=False)
    def yield_latest_12(self, request):
        """Returns the yield month data of the last 12 months.
        
        :rtype: Response
        :return: list of YieldMonth (timestamp, yield_month, yield_month_forecast)
        """

        now = timestamp_aware()
        datetime_lte = re.sub(r'\d\d:\d\d:\d\d.\d+', '23:59:59.999999', stringify_datetime(now))
        yesterday = now - relativedelta(months=12)
        datetime_gte = re.sub(r'\d\dT\d\d:\d\d:\d\d.\d+', '01T00:00:00.000000', stringify_datetime(yesterday))
        yield_months = YieldMonth.objects.filter(timestamp__gte=datetime_gte, timestamp__lte=datetime_lte)

        return Response(YieldMonthSerializer(yield_months, many=True).data)

    @action(methods=['GET'], url_path='history', detail=False)
    def yield_month_history(self, request):
        """Returns the YieldMonth set between the given timestamps. By default it returns data for the last 24 hours.

        time_begin: initial datetime to filter the data, default is 24 hours less than the current datetime
        type time_begin: str (yyyy-MM-ddTHH:mm:ss.SZ)
        time_end: final datetime to filter the data, default is the current datetime
        type time_end: str (yyyy-MM-ddTHH:mm:ss.SZ)
        page: number of the page in which the data is separated, default is 1
        type page: int
        
        :rtype: Paginated Response
        :return: list of YieldMonth (timestamp, yield_month, yield_month_forecast)
        """

        time_begin, time_end = get_time_range(request)

        yield_data = YieldMonth.objects.filter(timestamp__gte=time_begin, timestamp__lte=time_end)
        page = self.paginate_queryset(yield_data)

        if page is not None:
            serializer = YieldMonthSerializer(page, many=True).data
            return Response(self.get_paginated_response(serializer).data)

        return Response(YieldMonthSerializer(yield_data, many=True).data)

class YieldYearViewSet(viewsets.ModelViewSet):

    queryset = YieldYear.objects.all()
    serializer_class = YieldYearSerializer
    pagination_class = DynamicPagination

    @action(methods=['GET'], url_path='latest10', detail=False)
    def yield_latest_10(self, request):
        """Returns the yield year data of the last 10 years.
        
        :rtype: Response
        :return: list of YieldYear (timestamp, yield_year, yield_year_forecast)
        """

        now = timestamp_aware()
        datetime_lte = re.sub(r'\d\d:\d\d:\d\d.\d+', '23:59:59.999999', stringify_datetime(now))
        yesterday = now - relativedelta(months=120)
        datetime_gte = re.sub(r'\d\d-\d\dT\d\d:\d\d:\d\d.\d+', '01-01T00:00:00.000000', stringify_datetime(yesterday))
        yield_year = YieldYear.objects.filter(timestamp__gte=datetime_gte, timestamp__lte=datetime_lte)

        return Response(YieldYearSerializer(yield_year, many=True).data)

    @action(methods=['GET'], url_path='history', detail=False)
    def yield_year_history(self, request):
        """Returns the YieldYear set between the given timestamps. By default it returns data for the last 24 hours.

        time_begin: initial datetime to filter the data, default is 24 hours less than the current datetime
        type time_begin: str (yyyy-MM-ddTHH:mm:ss.SZ)
        time_end: final datetime to filter the data, default is the current datetime
        type time_end: str (yyyy-MM-ddTHH:mm:ss.SZ)
        page: number of the page in which the data is separated, default is 1
        type page: int
        
        :rtype: Paginated Response
        :return: list of YieldYear (timestamp, yield_year, yield_year_forecast)
        """

        time_begin, time_end = get_time_range(request)

        yield_data = YieldYear.objects.filter(timestamp__gte=time_begin, timestamp__lte=time_end)
        page = self.paginate_queryset(yield_data)

        if page is not None:
            serializer = YieldYearSerializer(page, many=True).data
            return Response(self.get_paginated_response(serializer).data)

        return Response(YieldYearSerializer(yield_data, many=True).data)

class YieldMinuteViewSet(viewsets.ModelViewSet):

    queryset = YieldMinute.objects.all()
    serializer_class = YieldMinuteSerializer
    pagination_class = DynamicPagination

    @action(methods=['GET'], url_path='today', detail=False)
    def yield_today(self, request):
        """Returns the yield minute data of the actual day (max 1440 datasets).
        
        :rtype: Response
        :return: list of YieldMinute (timestamp, yield_minute, yield_day_forecast)
        """

        now = timestamp_aware()
        datetime_gte = re.sub(r'\d\d:\d\d:\d\d.\d+', '00:00:00.000000', stringify_datetime(now))
        datetime_lte = re.sub(r'\d\d:\d\d:\d\d.\d+', '23:59:59.999999', stringify_datetime(now))
        yield_today = YieldMinute.objects.filter(timestamp__gte=datetime_gte, timestamp__lte=datetime_lte)
        yield_json = YieldMinuteSerializer(yield_today, many=True).data

        timestamp = [item['timestamp'].split('.')[0] for item in yield_json]
        yield_minute = [item['yield_minute'] for item in yield_json]

        data_json = {
            'timestamp': timestamp,
            'data': yield_minute
        }

        return Response(data_json)

    @action(methods=['GET'], url_path='history', detail=False)
    def yield_minute_history(self, request):
        """Returns the YieldMinute set between the given timestamps. By default it returns data for the last 24 hours.

        time_begin: initial datetime to filter the data, default is 24 hours less than the current datetime
        type time_begin: str (yyyy-MM-ddTHH:mm:ss.SZ)
        time_end: final datetime to filter the data, default is the current datetime
        type time_end: str (yyyy-MM-ddTHH:mm:ss.SZ)
        page: number of the page in which the data is separated, default is 1
        type page: int
        
        :rtype: Paginated Response
        :return: list of YieldMinute (timestamp, yield_minute, yield_day_forecast)
        """

        time_begin, time_end = get_time_range(request)

        yield_data = YieldMinute.objects.filter(timestamp__gte=time_begin, timestamp__lte=time_end)
        page = self.paginate_queryset(yield_data)

        if page is not None:
            serializer = YieldMinuteSerializer(page, many=True).data
            return Response(self.get_paginated_response(serializer).data)

        return Response(YieldMinuteSerializer(yield_data, many=True).data)

class AlertThresholdViewSet(viewsets.ModelViewSet):

    queryset = AlertThreshold.objects.all()
    serializer_class = AlertThresholdSerializer
    pagination_class = DynamicPagination

class SettingsViewSet(viewsets.ModelViewSet):
    
    queryset = Settings.objects.all()
    serializer_class = SettingaSerializer

    @action(methods=['POST'], url_path='setalertsettings', detail=False)
    def set_alert_settings(self, request):
        """Change the alert settings. To not change a data, just provide None.

        fault_vt_percentile: percentile of the threshold calculation for the voltage failure alert
        type fault_vt_percentile: int, 1 to 99
        warning_vt_percentile: percentile of the threshold calculation for the voltage failure alert
        type warning_vt_percentile: int, 1 to 99
        delt_vt: neighborhood of values used in the calculation of voltage thresholds
        type delt_vt: int, greater than 0
        fault_cr_percentile: percentile of the threshold calculation for the current failure alert
        type fault_cr_percentile: int, 1 to 99
        warning_cr_percentile: percentile of the threshold calculation for the current failure alert
        type warning_cr_percentile: int, 1 to 99
        delt_cr: neighborhood of values used in the calculation of current thresholds
        type delt_cr: int, greater than 0
        
        :rtype: Response
        :return: status
        """

        st, created = Settings.objects.get_or_create(id=1)

        try:
            st.fault_vt_percentile = request.data['fault_vt_percentile']
            st.warning_vt_percentile = request.data['warning_vt_percentile']
            st.delt_vt = request.data['delt_vt']

            st.fault_cr_percentile = request.data['fault_cr_percentile']
            st.warning_cr_percentile = request.data['warning_cr_percentile']
            st.delt_cr = request.data['delt_cr']

            st.save()
            createLog(title='System settings changed.',
                    message = '{username} changed alert settings.'.format(username=request.user.username))
        except:
            return Response(status=400)

        return Response(status=200)

    @action(methods=['POST'], url_path='setalertactive', detail=False)
    def set_alert_active(self, request):
        """Change whether alerts are active or not. To not change a data, just provide None.

        fault_user_active: set whether fault alerts are active or not
        type fault_user_active: boolean
        warning_user_active: set whether warning alerts are active or not
        type warning_user_active: boolean
        
        :rtype: Response
        :return: status
        """

        st, created = Settings.objects.get_or_create(id=1)

        try:
            st.fault_user_active = request.data['fault_user_active']
            st.warning_user_active = request.data['warning_user_active']
            st.save()
            createLog(title='System settings changed.',
                    message = '{username} changed whether alerts are active or not.'.format(username=request.user.username))
        except:
            return Response(status=400)

        return Response(status=200)

    @action(methods=['POST'], url_path='setretraininginterval', detail=False)
    def set_retraining_interval(self, request):
        """Change the interval between model retraining.

        retraining_interval: time interval between model training in months, default is 3
        type retraining_interval: int
        
        :rtype: Response
        :return: status
        """

        st, created = Settings.objects.get_or_create(id=1)

        try:
            st.retraining_interval = request.data['retraining_interval']
            st.save()
            createLog(title='System settings changed.',
                    message = '{username} changed the training interval of the models.'.format(username=request.user.username))
        except:
            return Response(status=400)

        return Response(status=200)

    @action(methods=['GET'], url_path='daysleft', detail=False)
    def days_left_alert(self, request):
        """Returns the days left to accumulate enough data to activate alerts.
        
        :rtype: Response
        :return: days_left
        """

        st, created = Settings.objects.get_or_create(id=1)

        return Response({'days_left': st.days_left})

class LogViewSet(viewsets.ModelViewSet):

    queryset = Log.objects.all()
    serializer_class = LogSerializer
    pagination_class = DynamicPagination

    @action(methods=['GET'], url_path='history', detail=False)
    def log_history(self, request):
        """Returns the log set between the given timestamps. By default it returns data for the last 24 hours.

        time_begin: initial datetime to filter the data, default is 24 hours less than the current datetime
        type time_begin: str (yyyy-MM-ddTHH:mm:ss.SZ)
        time_end: final datetime to filter the data, default is the current datetime
        type time_end: str (yyyy-MM-ddTHH:mm:ss.SZ)
        page: number of the page in which the data is separated, default is 1
        type page: int
        
        :rtype: Paginated Response
        :return: list of Log (message, title, created_at)
        """

        time_begin, time_end = get_time_range(request)

        log_data = Log.objects.filter(created_at__gte=time_begin, created_at__lte=time_end)
        page = self.paginate_queryset(log_data)

        if page is not None:
            serializer = LogSerializer(page, many=True).data
            return Response(self.get_paginated_response(serializer).data)

        return Response(LogSerializer(log_data, many=True).data)

class ExternalAPIViweSet(viewsets.ViewSet):

    @action(methods=['POST'], url_path='postdata', detail=False)
    def post_data(self, request):
        """Receives data from the Solaire library for insertion into the system.
        
        :rtype: Response
        :return: status
        """

        request_data = request.data

        try:
            request_data['timestamp']
            request_data['irradiance']
            request_data['temperature_pv']
            request_data['temperature_amb']
            request_data['power_avr']
            request_data['strings']
            request_data['generation']

            set_data.apply_async(args=[request_data], kwargs={}, queue='input_data')
        except:
            return Response(status=400)

        return Response(status=200)