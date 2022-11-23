from dataclasses import fields
from pyexpat import model
from django.contrib.auth import authenticate
from rest_framework import serializers

from django.contrib.auth.models import User
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
    Log,
    AIAlgorithm
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class PVStringSerializer(serializers.ModelSerializer):
    class Meta:
        model = PVString
        fields = ['name', 'timestamp', 'voltage', 'current', 'power', 'voltage_alert', 'current_alert', 'string_number']

class PVDataSerializer(serializers.ModelSerializer):
    strings = PVStringSerializer(read_only=True, many=True)

    class Meta:
        model = PVData
        fields = ['timestamp', 'irradiance', 'temperature_pv', 'temperature_amb', 'power_avg', 'strings']

class PVDataMeteorologicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PVData
        fields = ['timestamp', 'irradiance', 'temperature_pv', 'temperature_amb']

class PVDataPowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PVData
        fields = ['timestamp', 'power_avg']

class PowerForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = PowerForecast
        fields = ['timestamp', 't1', 't2', 't3', 't4', 't5']

class YieldDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = YieldDay
        fields = ['timestamp', 'yield_day', 'yield_day_forecast']

class YieldMonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = YieldMonth
        fields = ['timestamp', 'yield_month', 'yield_month_forecast']

class YieldYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = YieldYear
        fields = ['timestamp', 'yield_year', 'yield_year_forecast']

class YieldMinuteSerializer(serializers.ModelSerializer):
    class Meta:
        model = YieldMinute
        fields = ['timestamp', 'yield_minute', 'yield_day_forecast']

class AlertThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertThreshold
        fields = ['id', 'alert_type', 'string_number', 'meteorological_value', 'threshold_wa_max', 'threshold_wa_min', 'threshold_ft_max', 'threshold_ft_min']

class SettingaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ['id', 'fault_vt_percentile', 'warning_vt_percentile', 'delt_vt', 'fault_cr_percentile', 'warning_cr_percentile', 'delt_cr',
                'fault_user_active', 'warning_user_active', 'alert_days_active', 'days_left', 'retraining_interval']

class LoginSerializer(serializers.Serializer):
    """
        This serializer defines two fields for authentication:
        * username
        * password.
        It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'

class AIAlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIAlgorithm
        read_only_fields = ("id", "name", "description","created_at")
        fields = ("id", "name", "description", "availability", "update",  "created_at")