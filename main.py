import random
import pygame
import sys
import csv
import os
from math import log, exp
from datetime import datetime
# Custom modules
import config as c


# Controls general flow of the program
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, S_CHANGE_RATE, WRITE_CSV, FILENAME

    # Asks for inputs to create unique filename
    name = str(input("Enter a participant's name: ") or c.DEFAULT_NAME)
    session = str(input("Enter # of a session: ") or c.DEFAULT_SESSION)
    S_CHANGE_RATE = get_float("Enter rate as float (default is 3.0): ", c.DEFAULT_RATE)
    WRITE_CSV = get_bool("Write to csv? [True/False] (default is True): ", c.DEFAULT_WRITE)
    date = datetime.strftime(datetime.now(), "%Y_%b_%d_%H%M")
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    FILENAME = f"{_thisDir}{os.sep}data{os.path.sep}{name}_{session}_{date}.csv"

    # Initialize GUI
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode(c.SCREEN_SIZE)
    SURFWIDTH, SURFHEIGHT = pygame.display.get_surface().get_size()
    BASICFONT = pygame.font.SysFont(c.FONTNAME, c.FONTSIZE)
    pygame.display.set_caption(c.CAPTION)

    # Main routine
    while True:
        experiment()


# Controls flow of the experiment
def experiment():

    phase = {  # Dictionary to store current phase
        'name': next(c.PHASES),
        'id': 1,
    }
    stimuli = c.STIMULI  # Stores global parameters of stimuli for consequent manipulations
    score = 0  # Counts score
    rf_available = True  # Tracks availability of reinforcement
    responses = 0  # Tracks number of responses
    rate = S_CHANGE_RATE  # Stores copy of global S_CHANGE_RATE for consequent manipulations

    pygame.time.set_timer(c.CHANGE_STIMULI, int(1000 / rate))
    while True:
        DISPLAYSURF.fill(c.BACKGROUND)
        buttons = c.BUTTONS[phase['name']]
        # Updates states
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate(FILENAME, c.DATA, WRITE_CSV)
            phase = phase_handler(event, **phase)
            rf_available = reinforcement_refresher(event, rf_available)
            rate = rate_change_handler(event, rate)
            for k in stimuli:
                stimuli[k] = stimuli_handler(event, phase['name'], **stimuli[k])
            for i in buttons:
                buttons[i] = button_state_handler(event, **buttons[i])
                responses, score, rf_available = responses_handler(*[buttons[i][key] for key in ['state', 'reinforced_if']],
                                                                   responses, score, rf_available, **stimuli)
                if buttons[i]['state'] == 'pressed':
                    c.DATA.append([pygame.time.get_ticks()/1000, responses, score, phase['name'], phase['id'], rate])
        # Draws states
        for k in stimuli:
            text_object(**stimuli[k])
        for i in buttons:
            button_object(*[buttons[i][key] for key in ['bounds', 'state', 'color_dict']])
        text_object(text=f"Score: {score}", align=False, **c.SCORE)
        # Updates screen
        pygame.display.update()
        FPSCLOCK.tick(c.FPS)


# Receives current responses count and button state
# Outputs new responses count
def responses_handler(button_state, reinforced_if, responses, count, available, **current_sd_state):
    responses, score, available = responses, count, available
    if button_state == 'pressed':
        responses += 1
        score, available = reinforcement_handler(reinforced_if, score, available, **current_sd_state)
    return responses, score, available


# Receives current reinforcement state and updates availability
def reinforcement_refresher(ivent, available):
    if ivent.type == c.CHANGE_STIMULI:
        available = True
    return available


# Checks button state and updates score
# Only one correct response per stimuli is reinforced
def reinforcement_handler(reinforced_if, count, available, **current_sd_state):
    complex_sd = complex_sd_handler(reinforced_if, **current_sd_state)
    if available and complex_sd:
        count += 1
    else:
        count -= 1
    available = False  # Reinforcement becomes unavailable until nearest stimuli change
    return count, available


# Checks whether criteria for reinforcement are satisfied
# Accepts parameter for check and parameters dictionary
def complex_sd_handler(reinforced_if, **current_sd_state):
    stimuli = [current_sd_state[k]['text'] for k in current_sd_state]
    if all(x == reinforced_if for x in stimuli):
        return True
    else:
        return False


# Receives current state of rate
# Scroll-up: increases rate, scroll-down: decreases rate
def rate_change_handler(ivent, rate):
    rate = rate
    if ivent.type == pygame.MOUSEBUTTONDOWN:
        if ivent.button == 4 or ivent.button == 5:
            if ivent.button == 4:
                # Logarithmic scale prevents negative values
                rate = exp(log(rate) + 0.01)
            if ivent.button == 5:
                rate = exp(log(rate) - 0.01)
            pygame.time.set_timer(c.CHANGE_STIMULI, int(1000 / rate))
    return rate


# Inputs: event, bounds of the button, state of the button
# Outputs: same bounds, but new state if necessary
def button_state_handler(ivent, bounds, state, reinforced_if, color_dict):
    if state == 'pressed' and ivent.type != pygame.MOUSEBUTTONDOWN:
        state = 'hover'
    if ivent.type == pygame.MOUSEMOTION:
        if bounds.collidepoint(ivent.pos):
            state = 'hover'
        else:
            state = 'normal'
    elif ivent.type == pygame.MOUSEBUTTONDOWN:
        if ivent.button == 1:
            if bounds.collidepoint(ivent.pos):
                state = 'pressed'
    new_state = {
        'bounds': bounds,
        'state': state,
        'reinforced_if': reinforced_if,
        'color_dict': color_dict
    }
    return new_state


# Generates new stimuli configuration every CHANGE_STIMULI
# Produced stimuli depend on the current phase
def stimuli_handler(ivent, phase, text, color, pos):
    if ivent.type == c.CHANGE_STIMULI:
        text = random.choice(c.WORDS[phase])
        color = random.choice(c.COLORS)
    new_state = {
        'text': text,
        'color': color,
        'pos': pos
    }
    return new_state


# Receives current phase name and id
# If Q is pressed - returns next name and id from infinite iterator PHASES (defined at the beginning)
def phase_handler(ivent, name, id):
    if ivent.type == pygame.KEYDOWN and ivent.key == pygame.K_q:
        name = next(c.PHASES)
        id += 1
    new_state = {
        'name': name,
        'id': id
    }
    return new_state


# Receives a dict of button parameters and modifies the global surface
# This side effect is intended
def button_object(bounds, state, color_dict):
    color = color_dict.get(state)
    pygame.draw.rect(DISPLAYSURF, color, bounds)


# Receives a dict of stimulus paramaters and modifies the global surface
# This side effect is intended
def text_object(pos, text, color, align=True):
    font = BASICFONT
    text_surface, bounds = get_surface(font, text, c.COLORDICT.get(color, color))
    if align:
        pos = centralize(pos, bounds.width)
    DISPLAYSURF.blit(text_surface, pos)


# Align toward center horizontally
def centralize(pos, width):
    return pos[0] - width // 2, pos[1]


# Converts raw data to the surface
def get_surface(font, text, color):
    text_surface = font.render(text, False, color)
    return text_surface, text_surface.get_rect()


# Finishes program
def terminate(filename, data, write=False):
    if write:
        write_to_csv(filename, data)
    pygame.quit()
    sys.exit()


# Writes input to a csv file
def write_to_csv(filename, data):
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(_thisDir + os.sep + u'data'):
        print(u"Data folder created")
        os.makedirs(_thisDir + os.sep + u'data')
    output_writer = csv.writer(open(filename + '.csv', 'w'), lineterminator='\n')
    for i in range(0, len(data)):
        output_writer.writerow(data[i])


# Functions to ensure correct start of the script
# Converts a string to a boolean, repeats prompt if input is not a boolean
def get_bool(prompt, default):
    while True:
        try:
            return {"true": True, "false": False}[input(prompt).lower() or default]
        except KeyError:
            print("That is not a boolean! Enter True or False")


# Repeats prompt if input is not a float
def get_float(prompt, default):
    while True:
        try:
            return float(input(prompt) or default)
        except ValueError:
            print('That is not a float! Example: 3.0')


# Starts main()
if __name__ == '__main__':
    main()