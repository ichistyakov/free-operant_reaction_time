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
    global FPSCLOCK, DISPLAYSURF, BASICFONT, KITTY

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((800, 600))
    BASICFONT =  pygame.font.SysFont('Arial', 40)
    pygame.display.set_caption('Stroop task')

    while True:
        experiment()


# Controls flow of the experiment
def experiment():
    global CHANGE_STIMULI

    phase = next(PHASES)
    stimulus = {
        'text': 'white',
        'color': 'white',
        'pos': (400, 300)
    }
    button = {
        'bounds': pygame.Rect(350, 450, 100, 100),
        'color': BUTTON_NORMAL_BACK_COLOR,
        'on_click': None
    }
    CHANGE_STIMULI = pygame.USEREVENT + 1
    pygame.time.set_timer(CHANGE_STIMULI, 1000)

    while True:
        DISPLAYSURF.fill(BACKGROUND)
        # Updates states
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            stimulus = stimuli_handler(event, phase, **stimulus)
            phase = phase_handler(phase, event)
            button = button_handler(event, **button)
        # Draws states
        text_stimuli(**stimulus)
        button_object(**button)
        # Updates screen
        pygame.display.update()
        FPSCLOCK.tick(FPS)


# Check events and updates state of the button
def button_handler(ivent, **kwargs):
    bounds = kwargs['bounds']
    color = kwargs['color']
    on_click = kwargs['on_click']
    if ivent.type == pygame.MOUSEMOTION:
        if bounds.collidepoint(ivent.pos):
            color = BUTTON_HOVER_BACK_COLOR
        else:
            color = BUTTON_NORMAL_BACK_COLOR
    elif ivent.type == pygame.MOUSEBUTTONDOWN:
        if ivent.button == 1:
            if bounds.collidepoint(ivent.pos):
                color = BUTTON_PRESSED_BACK_COLOR
    elif ivent.type == pygame.MOUSEBUTTONUP:
        if ivent.button == 1:
            if bounds.collidepoint(ivent.pos):
                color = BUTTON_HOVER_BACK_COLOR
    new_state = {
        'bounds': bounds,
        'color': color,
        'on_click': on_click
    }
    return new_state


# Generates new stimuli configuration every CHANGE_STIMULI based on current phase or does nothing
def stimuli_handler(ivent, phase, **kwargs):
    text = kwargs['text']
    color = kwargs['color']
    pos = kwargs['pos']
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


# Alternates between values that coded in 'phases' or does nothing. Feel free to add rules here.
def phase_handler(current_state, ivent):
    if ivent.type == KEYDOWN and ivent.key == K_q:
        return next(PHASES)
    else:
        return current_state


# Accepts a dict of parameters and modifies the global surface. This side-effect is intended.
def button_object(**kwargs):
    bounds = kwargs['bounds']
    color = kwargs['color']
    pygame.draw.rect(DISPLAYSURF, color, bounds)


# Modifies the global surface, but this side effect is intended
def text_stimuli(**kwargs):
    pos = kwargs['pos']
    text = kwargs['text']
    color = kwargs['color']
    font = BASICFONT
    text_surface, bounds = get_surface(font, text, COLORDICT.get(color))
    pos = centralize(pos, bounds.width)
    DISPLAYSURF.blit(text_surface, pos)


# Align toward center horizontally
def centralize(pos, width):
    return pos[0] - width // 2, pos[1]


# Converts raw data to the surface
def get_surface(font, text, color):
    text_surface = font.render(text, False, color)
    return text_surface, text_surface.get_rect()


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()