# Microservice Beny.

# Сreate and activate a virtual environment: 
```
python -m venv venv
source venv/bin/activate
export PYTHONPATH=$PWD
```
# Install all requirements:
```pip install -r requirements.txt```
# Run project:
python app/main.py

# App using swagger. Go to the /docs to see all endpoints:
```http://0.0.0.0:8000/docs```
# DB:
```Uses motor v2.2.0 for mongodb. By deafault is connected to mongodb://localhost:27017```