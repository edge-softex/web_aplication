from django.db import models

class AIAlgorithm(models.Model):
    '''
    The MLAlgorithm represent the ML algorithm object.

    Attributes:
        name: The name of the algorithm.
        description: The short description of how the algorithm works.
        availability: If the algorithm is available or not (True or False).
        update: If there is a new version of the model available or not (True or False).
        created_at: The date when MLAlgorithm was created.
    '''
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1000)
    availability = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)