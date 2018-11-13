# A free operant version of Donder's reaction time experiments
Source code from the project 'Fixed-Interval Multiple Schedule of Reinforcement as An Alternative to Reaction Time Measures'

## Requirements
Tested only for Python 3.6</br>
Libraries: `pygame, numpy`

## Installation
Ubuntu 16.04 or later:
```
git clone https://github.com/ichistyakov/free-operant_reaction_time.git
cd ~/free-operant_reaction_time
# Optional: create virtual environment
# Run sudo apt install python3-venv if necessary
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Starting
From venv:
```
python3 main.py
```
If everything is okay, script will prompt several inputs in terminal to create distinct filename and start PyGame GUI
