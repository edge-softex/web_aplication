"""
WSGI config for web_application project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

application = get_wsgi_application()

# AI registry
from photovoltaic.ai import (LstmPowerForecaster, AIRegistry)

try:
    registry = AIRegistry()
    
    lstm = LstmPowerForecaster("lstm/model.h5")
    # add to AI registry
    registry.add_algorithm(algorithm_object=lstm,
                            algorithm_name="lstm power forecaster",
                            algorithm_description="Lstm model with simple pre- and post-processing, capable of retraining",
                            algorithm_availability=True)
except Exception as e:
    print("Exception while loading the algorithms to the registry,", str(e))