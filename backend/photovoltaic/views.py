from venv import create
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

from pytz import timezone
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from .util import (get_time_inteval,
    get_time_range,
    get_string_number,
    generate_forecast_json)

from .serializers import (
    PVDataSerializer,
    PVStringSerializer,
    PVDataMeteorologicalSerializer,
    PVDataPowerSerializer,
    PowerForecastSerializer,
    YieldDaySerializer,
    YieldMonthSerializer,
    YieldYearSerializer,
    YieldMinuteSerializer,
    AlertTresholdSerializer,
    SettingaSerializer)
from .models import (
    PVData,
    PVString,
    PowerForecast,
    YieldDay,
    YieldMonth,
    YieldYear,
    YieldMinute,
    AlertTreshold,
    Settings)

# Create your views here.

class PVDataViewSet(viewsets.ModelViewSet):
    queryset = PVData.objects.all()
    serializer_class = PVDataSerializer

    @action(methods=['GET'], url_path='status', detail=False)
    def pv_system_status(self, request):
        latest_data = PVDataSerializer(PVData.objects.latest('timestamp')).data

        print(latest_data)

        time_now = datetime.now()
        time_data = datetime.strptime(latest_data['timestamp'], '%Y-%m-%dT%H:%M:%S.%f-03:00')
        delta = time_now - time_data
        minutes = delta / timedelta(minutes=1)

        status = 'Normal Operation'
        if(minutes >= 3):
            status = 'Offline'
        else:
            for string in latest_data['strings']:
                if string['voltage_alert'] == 'WA' or string['current_alert'] == 'WA':
                    status = 'Warning Operation'
                if string['voltage_alert'] == 'FT' or string['current_alert'] == 'FT':
                    status = 'Fault Operation'
                    break
        
        json_response = {
            'status': status
        }

        return Response(json_response)

    @action(methods=['GET'], url_path='latest', detail=False)
    def pv_data_latest(self, request):
        latest_data = PVData.objects.latest('timestamp')
        return Response(PVDataSerializer(latest_data).data)

    @action(methods=['GET'], url_path='meteorologicalhistory', detail=False)
    def meteorological_history(self, request):
        now = datetime.now()
        datetime_lte = now.strftime('%Y-%m-%dT%H:%M:%S.%f-03:00')
        yesterday = now - timedelta(days=1)
        datetime_gte = yesterday.strftime('%Y-%m-%dT%H:%M:%S.%f-03:00')
        day_data = PVData.objects.filter(timestamp__gte=datetime_gte, timestamp__lte=datetime_lte)

        return Response(PVDataMeteorologicalSerializer(day_data, many=True).data)

    @action(methods=['GET'], url_path='powerhistory', detail=False)
    def power_history(self, request):
        time_interval = get_time_inteval(request)

        now = datetime.now()
        datetime_lte = now.strftime('%Y-%m-%dT%H:%M:%S.%f-03:00')
        yesterday = now - timedelta(minutes=time_interval)
        datetime_gte = yesterday.strftime('%Y-%m-%dT%H:%M:%S.%f-03:00')
        power_data = PVData.objects.filter(timestamp__gte=datetime_gte, timestamp__lte=datetime_lte)

        return Response(PVDataPowerSerializer(power_data, many=True).data)

    @action(methods=['GET'], url_path='history', detail=False)
    def pv_data_history(self, request):
        time_begin, time_end = get_time_range(request)

        datetime_lte = datetime.strptime(time_begin, '%Y-%m-%dT%H:%M:%S.%f-03:00')
        datetime_gte = datetime.strptime(time_end, '%Y-%m-%dT%H:%M:%S.%f-03:00')
        pv_data = PVData.objects.filter(timestamp__gte=datetime_gte, timestamp__lte=datetime_lte)

        return Response(PVDataSerializer(pv_data, many=True).data)

class PVStringViewSet(viewsets.ModelViewSet):
    queryset = PVString.objects.all()
    serializer_class = PVStringSerializer

    @action(methods=['GET'], url_path='history', detail=False)
    def pv_string_history(self, request):
        number = get_string_number(request)
        time_begin, time_end = get_time_range(request)

        datetime_lte = datetime.strptime(time_begin, '%Y-%m-%dT%H:%M:%S.%f-03:00')
        datetime_gte = datetime.strptime(time_end, '%Y-%m-%dT%H:%M:%S.%f-03:00')
        pv_data = PVString.objects.filter(string_number=number, timestamp__gte=datetime_gte, timestamp__lte=datetime_lte)

        return Response(PVStringSerializer(pv_data, many=True).data)

class PowerForecastViewSet(viewsets.ModelViewSet):
    queryset = PowerForecast.objects.all()
    serializer_class = PowerForecastSerializer

    @action(methods=['GET'], url_path='history', detail=False)
    def forecast_history(self, request):
        time_interval = get_time_inteval(request)

        now = datetime.now()
        datetime_lte = now.strftime('%Y-%m-%dT%H:%M:%S.%f-03:00')
        yesterday = now - timedelta(minutes=time_interval+1)
        datetime_gte = yesterday.strftime('%Y-%m-%dT%H:%M:%S.%f-03:00')
        power_forecast = PowerForecast.objects.filter(timestamp__gte=datetime_gte, timestamp__lte=datetime_lte)

        forecast_json = generate_forecast_json(PowerForecastSerializer(power_forecast, many=True).data)

        return Response(forecast_json)

    @action(methods=['GET'], url_path='history', detail=False)
    def power_forecast_history(self, request):
        time_begin, time_end = get_time_range(request)

        datetime_lte = datetime.strptime(time_begin, '%Y-%m-%dT%H:%M:%S.%f-03:00')
        datetime_gte = datetime.strptime(time_end, '%Y-%m-%dT%H:%M:%S.%f-03:00')
        forecast_data = PowerForecast.objects.filter(timestamp__gte=datetime_gte, timestamp__lte=datetime_lte)

        return Response(PowerForecastSerializer(forecast_data, many=True).data)

class YieldDayViewSet(viewsets.ModelViewSet):
    queryset = YieldDay.objects.all()
    serializer_class = YieldDaySerializer

    @action(methods=['GET'], url_path='now', detail=False)
    def yield_now(self, request):
        yield_today = YieldDay.objects.latest('timestamp')
        return Response(YieldDaySerializer(yield_today).data)

    @action(methods=['GET'], url_path='latest15', detail=False)
    def yield_latest_15(self, request):
        now = datetime.now()
        datetime_lte = now.strftime('%Y-%m-%dT23:59:59.999999-03:00')
        yesterday = now - timedelta(days=15)
        datetime_gte = yesterday.strftime('%Y-%m-%dT00:00:00.000000-03:00')
        yield_days = YieldDay.objects.filter(timestamp__gte=datetime_gte, timestamp__lte=datetime_lte)

        return Response(YieldDaySerializer(yield_days, many=True).data)

    @action(methods=['GET'], url_path='history', detail=False)
    def yield_day_history(self, request):
        time_begin, time_end = get_time_range(request)

        datetime_lte = datetime.strptime(time_begin, '%Y-%m-%dT%H:%M:%S.%f-03:00')
        datetime_gte = datetime.strptime(time_end, '%Y-%m-%dT%H:%M:%S.%f-03:00')
        yield_data = YieldDay.objects.filter(timestamp__gte=datetime_gte, timestamp__lte=datetime_lte)

        return Response(YieldDaySerializer(yield_data, many=True).data)

class YieldMonthViewSet(viewsets.ModelViewSet):
    queryset = YieldMonth.objects.all()
    serializer_class = YieldMonthSerializer

    @action(methods=['GET'], url_path='latest12', detail=False)
    def yield_latest_12(self, request):
        now = datetime.now()
        datetime_lte = now.strftime('%Y-%m-%dT23:59:59.999999-03:00')
        yesterday = now - relativedelta(months=12)
        datetime_gte = yesterday.strftime('%Y-%m-01T00:00:00.000000-03:00')
        yield_months = YieldMonth.objects.filter(timestamp__gte=datetime_gte, timestamp__lte=datetime_lte)

        return Response(YieldMonthSerializer(yield_months, many=True).data)

    @action(methods=['GET'], url_path='history', detail=False)
    def yield_month_history(self, request):
        time_begin, time_end = get_time_range(request)

        datetime_lte = datetime.strptime(time_begin, '%Y-%m-%dT%H:%M:%S.%f-03:00')
        datetime_gte = datetime.strptime(time_end, '%Y-%m-%dT%H:%M:%S.%f-03:00')
        yield_data = YieldMonth.objects.filter(timestamp__gte=datetime_gte, timestamp__lte=datetime_lte)

        return Response(YieldMonthSerializer(yield_data, many=True).data)

class YieldYearViewSet(viewsets.ModelViewSet):
    queryset = YieldYear.objects.all()
    serializer_class = YieldYearSerializer

    @action(methods=['GET'], url_path='latest10', detail=False)
    def yield_latest_10(self, request):
        now = datetime.now()
        datetime_lte = now.strftime('%Y-%m-%dT23:59:59.999999-03:00')
        yesterday = now - relativedelta(months=120)
        datetime_gte = yesterday.strftime('%Y-01-01T00:00:00.000000-03:00')
        yield_year = YieldYear.objects.filter(timestamp__gte=datetime_gte, timestamp__lte=datetime_lte)

        return Response(YieldYearSerializer(yield_year, many=True).data)

    @action(methods=['GET'], url_path='history', detail=False)
    def yield_year_history(self, request):
        time_begin, time_end = get_time_range(request)

        datetime_lte = datetime.strptime(time_begin, '%Y-%m-%dT%H:%M:%S.%f-03:00')
        datetime_gte = datetime.strptime(time_end, '%Y-%m-%dT%H:%M:%S.%f-03:00')
        yield_data = YieldYear.objects.filter(timestamp__gte=datetime_gte, timestamp__lte=datetime_lte)

        return Response(YieldYearSerializer(yield_data, many=True).data)

class YieldMinuteViewSet(viewsets.ModelViewSet):
    queryset = YieldMinute.objects.all()
    serializer_class = YieldMinuteSerializer

    @action(methods=['GET'], url_path='today', detail=False)
    def yield_today(self, request):
        now = datetime.now()
        datetime_lte = now.strftime('%Y-%m-%dT%H:%M:%S.%f-03:00')
        datetime_gte = now.strftime('%Y-%m-%dT00:00:00.000000-03:00')
        yield_today = YieldMinute.objects.filter(timestamp__gte=datetime_gte, timestamp__lte=datetime_lte)

        return Response(YieldMinuteSerializer(yield_today, many=True).data)

    @action(methods=['GET'], url_path='history', detail=False)
    def yield_minute_history(self, request):
        time_begin, time_end = get_time_range(request)

        datetime_lte = datetime.strptime(time_begin, '%Y-%m-%dT%H:%M:%S.%f-03:00')
        datetime_gte = datetime.strptime(time_end, '%Y-%m-%dT%H:%M:%S.%f-03:00')
        yield_data = YieldMinute.objects.filter(timestamp__gte=datetime_gte, timestamp__lte=datetime_lte)

        return Response(YieldMinuteSerializer(yield_data, many=True).data)

class AlertTresholdViewSet(viewsets.ModelViewSet):
    queryset = AlertTreshold.objects.all()
    serializer_class = AlertTresholdSerializer

class SettingsViewSet(viewsets.ModelViewSet):
    queryset = Settings.objects.all()
    serializer_class = SettingaSerializer

    @action(methods=['POST'], url_path='setalertsettings', detail=False)
    def set_alert_settings(self, request):

        st, created = Settings.objects.get_or_create(id=1)

        st.fault_vt_percentile = request.GET.get('fault_vt_percentile', st.fault_vt_percentile)
        st.warning_vt_percentile = request.GET.get('warning_vt_percentile', st.warning_vt_percentile)
        st.delt_vt = request.GET.get('delt_vt', st.delt_vt)

        st.fault_cr_percentile = request.GET.get('fault_cr_percentile', st.fault_cr_percentile)
        st.warning_cr_percentile = request.GET.get('warning_cr_percentile', st.warning_cr_percentile)
        st.delt_cr = request.GET.get('delt_cr', st.delt_cr)

        return Response(status=200)

    @action(methods=['POST'], url_path='setalertactive', detail=False)
    def set_alert_active(self, request):

        st, created = Settings.objects.get_or_create(id=1)

        st.fault_user_active = request.GET.get('fault_user_active', st.fault_user_active)
        st.warning_user_active = request.GET.get('warning_user_active', st.warning_user_active)

        return Response(status=200)

    @action(methods=['POST'], url_path='setretraininginterval', detail=False)
    def set_retraining_interval(self, request):

        st, created = Settings.objects.get_or_create(id=1)

        st.retraining_interval = request.GET.get('retraining_interval', st.retraining_interval)

        return Response(status=200)

    @action(methods=['GET'], url_path='daysleft', detail=False)
    def days_left_alert(self, request):

        st, created = Settings.objects.get_or_create(id=1)

        return Response({'days_left': st.days_left})