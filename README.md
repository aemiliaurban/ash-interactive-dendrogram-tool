# Ash

## Navigating Ash

A brief tutorial can be found on [youtube](https://www.youtube.com/watch?v=WLfB4a4UlKg).

## Navigating Ash
Data upload can be tested with the iris dataset which can be found in ash/common/iris_sample_data.

## How to run Ash via Docker
Commands ought to be run from the root of the repo. Alternatively, you can adjust the paths.

### Build the image:
```
docker build . -t ash --no-cache 
```
### Run the container:
```
docker run -p 8050:8050 ash 
```

## How to run Ash locally from the source
Ash supports python3.10. Make sure you have it installed on your machine.
It can be installed with homebrew:
```
brew install python@3.10
```
OPTIONAL: creating a virtual environment (highly recommended):
```
python3.10 -m venv venv
```
Activate the virtual environment
```
source venv/bin/activate
```
Install requirements:
```
pip install -r requirements.txt
```
Run the app:
Before running the app, make sure you are in the ash directory (relative paths).
```
python app.py
```

## How to install the Ash package 
It is possible to use parts of Ash as a package. The dendrogram splitting function and the data parsing function are available.

[Link to PyPI](https://pypi.org/project/ash-dendro/)

### Build the image:
```
pip install ash-dendro
```

