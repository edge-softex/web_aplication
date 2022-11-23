# """web_application URL Configuration

#     The `urlpatterns` list routes URLs to views. For more information please see:
#         https://docs.djangoproject.com/en/4.0/topics/http/urls/
#     Examples:
#     Function views
#         1. Add an import:  from my_app import views
#         2. Add a URL to urlpatterns:  path('', views.home, name='home')
#     Class-based views
#         1. Add an import:  from other_app.views import Home
#         2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
#     Including another URLconf
#         1. Import the include() function: from django.urls import include, path
#         2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
from email.mime import base
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from photovoltaic import views as photovoltaic_views

api_router = routers.DefaultRouter()
api_router.register(r'users', photovoltaic_views.UserViewSet)
api_router.register(r'accounts', photovoltaic_views.AccountsViewSet, basename='accounts')
api_router.register(r'pvdata', photovoltaic_views.PVDataViewSet)
api_router.register(r'pvstring', photovoltaic_views.PVStringViewSet)
api_router.register(r'powerforecast', photovoltaic_views.PowerForecastViewSet)
api_router.register(r'yieldday', photovoltaic_views.YieldDayViewSet)
api_router.register(r'yieldmonth', photovoltaic_views.YieldMonthViewSet)
api_router.register(r'yieldyear', photovoltaic_views.YieldYearViewSet)
api_router.register(r'yieldminute', photovoltaic_views.YieldMinuteViewSet)
api_router.register(r'alertthreshold', photovoltaic_views.AlertThresholdViewSet)
api_router.register(r'settings', photovoltaic_views.SettingsViewSet)
api_router.register(r'log', photovoltaic_views.LogViewSet)
api_router.register(r'external', photovoltaic_views.ExternalAPIViweSet, basename='external')

external_router = routers.DefaultRouter()
external_router.register(r'apiactions', photovoltaic_views.ExternalAPIViweSet, basename='apiactions')

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(api_router.urls)),
]