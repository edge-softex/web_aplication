from photovoltaic.models.aialgorithm import AIAlgorithm

class AIRegistry:
    def __init__(self):
        self.algorithms = {}

    def add_algorithm(self, algorithm_object, algorithm_name,
                    algorithm_description,algorithm_availability, algorithm_path):
        
        defaults = {"name": algorithm_name,
                "description": algorithm_description,
                "availability": algorithm_availability,
                "path": algorithm_path}

        database_object, algorithm_created = AIAlgorithm.objects.update_or_create(id=1,
                defaults=defaults)

        self.algorithms[database_object.id] = algorithm_object    