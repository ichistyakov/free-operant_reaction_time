import random, itertools, pygame, sys
# Custom modules
import colors as c
from pygame.locals import *


FPS = 60
WORDS = ['white', 'red', 'green', 'blue']
COLORS = ['white', 'red', 'green', 'blue']
PHASES = itertools.cycle(['A', 'B'])
BACKGROUND = c.BLACK
BUTTON_NORMAL_BACK_COLOR = c.RED1
BUTTON_HOVER_BACK_COLOR = c.RED2
BUTTON_PRESSED_BACK_COLOR = c.RED3
COLORDICT = {
    'white': c.WHITE,
    'red': c.RED1,
    'green': c.GREEN,
    'blue': c.BLUE
}


# Controls general flow of the program
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((800, 600))
    BASICFONT =  pygame.font.SysFont('Arial', 40)
    pygame.display.set_caption('Stroop task')

    while True:
        experiment()


# Controls flow of the experiment
def experiment():
    global CHANGE_STIMULI, DATA

    CHANGE_STIMULI = pygame.USEREVENT + 1
    DATA = ['time', 'responses', 'phase_name', 'phase_id']
    phase = {
        'name': next(PHASES),
        'id': 1,
    }
    button = {
        'bounds': pygame.Rect(350, 450, 100, 100),
        'state': 'normal'
    }
    stimuli = {
        'left': {
            'text': 'white',
            'color': 'white',
            'pos': (300, 300)
        },
        'right': {
            'text': 'white',
            'color': 'white',
            'pos': (500, 300)
        }
    }
    reinforcement = {
        'count': 0,
        'available': True
    }

    pygame.time.set_timer(CHANGE_STIMULI, 1000)
    while True:
        DISPLAYSURF.fill(BACKGROUND)
        # Updates states
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            phase = phase_handler(event, **phase)
            for k in stimuli:
                stimuli[k] = stimuli_handler(event, phase['name'], **stimuli[k])
            button = button_state_handler(event, **button)
            reinforcement = reinforcement_handler(button['state'], 'color', **reinforcement, **stimuli)
        # Draws states
        for k in stimuli:
            text_object(**stimuli[k])
        button_object(**button)
        text_object((100, 100), f"Score: {reinforcement['count']}", 'white', align=False)
        # Updates screen
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def reinforcement_refresher(ivent, **current_rf_state):
    count = current_rf_state['count']
    available = current_rf_state['available']
    if ivent.type == CHANGE_STIMULI:
        available = True
    new_state = {
        'count': count,
        'available': available
    }
    return new_state


# Checks button state and updates score. Only one correct response per stimuli is reinforced.
def reinforcement_handler(button_state, key, count, available, **current_sd_state):
    complex_sd = complex_sd_handler(key, **current_sd_state)
    if available and complex_sd:
        if button_state == 'pressed':
            count += 1
            available = False  # Reinforcement becomes unavailable until nearest stimuli change
    new_state = {
        'count': count,
        'available': available
    }
    return new_state


# Checks whether criteria for reinforcement are satisfied
# Accepts parameter for check and parameters dictionary
def complex_sd_handler(key, **current_sd_state):
    stimuli = [current_sd_state[k][key] for k in current_sd_state]
    if all(x == stimuli[0] for x in stimuli):
        return True
    else:
        return False


# Checks events and updates the state of the button
def button_state_handler(ivent, **current_state):
    bounds = current_state['bounds']
    state = current_state['state']
    if ivent.type == pygame.MOUSEMOTION:
        if bounds.collidepoint(ivent.pos):
            state = 'hover'
        else:
            state = 'normal'
    elif ivent.type == pygame.MOUSEBUTTONDOWN:
        if ivent.button == 1:
            if bounds.collidepoint(ivent.pos):
                state = 'pressed'
    elif ivent.type == pygame.MOUSEBUTTONUP:
        if ivent.button == 1:
            if bounds.collidepoint(ivent.pos):
                state = 'hover'
    new_state = {
        'bounds': bounds,
        'state': state
    }
    return new_state


# Generates new stimuli configuration every CHANGE_STIMULI
# Produced stimuli depend on the current phase
def stimuli_handler(ivent, phase, **stim_parameters):
    text = stim_parameters['text']
    color = stim_parameters['color']
    pos = stim_parameters['pos']
    if ivent.type == CHANGE_STIMULI:
        if phase == 'A':
            text = random.choice(WORDS)
            color = text
        elif phase == 'B':
            text = random.choice(WORDS)
            color = random.choice(COLORS)
        else:
            text = 'Something wrong with phases!'
            color = 'white'
    new_state = {
        'text': text,
        'color': color,
        'pos': pos
    }
    return new_state


# Receives current phase name and id
# If Q is pressed - returns next name and id from infinite iterator PHASES (defined at the beginning)
def phase_handler(ivent, **current_state):
    name = current_state['name']
    id = current_state['id']
    if ivent.type == KEYDOWN and ivent.key == K_q:
        name = next(PHASES)
        id += 1
    new_state = {
        'name': name,
        'id': id
    }
    return new_state


# Receives a dict of button parameters and modifies the global surface
# This side effect is intended
def button_object(**kwargs):
    bounds = kwargs['bounds']
    state = kwargs['state']
    color_dict = {
        'normal': BUTTON_NORMAL_BACK_COLOR,
        'hover': BUTTON_HOVER_BACK_COLOR,
        'pressed': BUTTON_PRESSED_BACK_COLOR,
        'relaxed': BUTTON_HOVER_BACK_COLOR
    }
    color = color_dict.get(state)
    pygame.draw.rect(DISPLAYSURF, color, bounds)


# Receives a dict of stimulus paramaters and modifies the global surface
# This side effect is intended
def text_object(pos, text, color, align=True):
    font = BASICFONT
    text_surface, bounds = get_surface(font, text, COLORDICT.get(color))
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
def terminate():
    pygame.quit()
    sys.exit()

# Starts program
if __name__ == '__main__':
    main()