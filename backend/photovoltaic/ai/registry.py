from photovoltaic.models.aialgorithm import AIAlgorithm

class AIRegistry:
    def __init__(self):
        self.algorithms = {}

    def add_algorithm(self, algorithm_object, algorithm_name,
                    algorithm_description,algorithm_availability):
        
        # get algorithm
        database_object, algorithm_created = AIAlgorithm.objects.get_or_create(
                name=algorithm_name,
                description=algorithm_description,
                availability=algorithm_availability)

        # add to registry
        self.algorithms[database_object.id] = algorithm_object    