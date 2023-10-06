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
from photovoltaic.ai import (LstmForecaster, DlinearForecaster, AIRegistry)

try:
    registry = AIRegistry()
    
    # name="dlinear forecaster"
    # description="Dlinear model with simple pre- and post-processing, capable of retraining"
    # model_path = "dlinear/model"
    name="lstm forecaster"
    description="LSTM model with simple pre- and post-processing, capable of retraining"
    model_path = "lstm/model.h5"
    #model = DlinearForecaster(model_path)
    model = LstmForecaster(model_path)
    registry.add_algorithm(algorithm_object=model,
                            algorithm_name=name,
                            algorithm_description=description,
                            algorithm_availability=True,
                            algorithm_path = model_path)

    print("Registry created sucessfully!")
except Exception as e:
    print("Exception while loading the algorithms to the registry,", str(e))