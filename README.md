# Coding Challenge App

A coding challenge solution to get the Git Profile for a user/organization

## Install:

Create the virtual environment with conda:
```
conda env create -f environment.yaml
source activate user-profiles
```

Add the requirements:
```
pip install -r requirements.txt
```

## Running the code

### Spin up the service

```
# start up local server
python -m run
```

### Making Requests

```
curl -i "http://127.0.0.1:5000/health-check"
```


## What'd I'd like to improve on...
