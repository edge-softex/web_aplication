# Softex - Photovoltaic forecaster
This repository contains everything needed to deploy and run the project.  
  
## Development  
To run the application in a development environment, simply use the command:  
  
```  
docker-compose up  
```  
If the images for the containers aren't created already, the ```up``` command will create them automatically. Changes like new requirements or changes in the build process (Dockerfile) require a rebuild, for that you should use the ```docker-compose build``` command.
  
If this is your first time deploying the project, you should follow the steps below in order to setup your database and Django application:  
1. Run the command ```docker-compose run --rm backend /bin/bash```.
2. Migrate the database, run the command ```python manage.py migrate```. 
2. Create a superuser, run the ```python manage.py createsuperuser``` command to create one.
3. Download one of the following files and place it in backend/photovoltiac/fixtures:
   - All years (795 MB) - https://drive.google.com/file/d/1Ne9b_Mv0qp1ImplhGeUuO4pvkTM0-J6P/view?usp=sharing
   - 2021 (286 MB) - https://drive.google.com/file/d/1iTPnPmYXK7hf_k4qasRIPR1ih7nu6j6w/view?usp=sharing
4. Load backup data, run ```python manage.py loaddata base_name.json``` to load it into your database.  