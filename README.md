# A free operant version of Donder's reaction time experiments
Source code from the project 'Fixed-Interval Multiple Schedule of Reinforcement as An Alternative to Reaction Time Measures'

## Description
A free operant replication of Donder's reaction time experiments based on the description by Ardi Roelofs (2018).</br>
### Schedule of reinforcement
Fixed-interval multiple schedule of reinforcement is a compound schedule of reinforcement consisting of two or more basic schedules of reinforcement (elements) that occur in an alternating random sequence; interval between two consecutive changes is fixed; a discriminative stimulus is correlated with the presence or absence of each element of the schedule, and reinforcement is delivered for meeting the response requirements of the element in effect at any time.
### Structure of the experiment
Current script consists of 2 schedules: basic fixed-interval multiple schedule of reinforcement (*a* and *c* from Roelofs, 2018) and concurrent fixed-interval multiple schedule of reinforcement (*b*). Basic FI MULT consist of two schedules - responses increase or decrease score. During *a* responding is reinforced when A is present and punished when A is absent; *b* - reinforced when A is present and punished when B is absent. During *c* two response options available, red and green buttons; when A is present - red button is reinforced and green is punished, when B is present - correlations are opposite.
### Flow control
Q changes phase values over `itertools.cycle(['A', 'B', 'C'])`, where A, B and C correspond to aforementioned experimental conditions.</br>
Scrolling changes interval. Scroll-up increases rate of alternation and scroll-down reduces it.

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
