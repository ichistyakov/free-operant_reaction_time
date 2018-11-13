import itertools
import pygame
# Custom modules
import colors as c

COLORDICT = {
    'white': c.WHITE
}
# GUI parameters
BACKGROUND = c.BLACK
FPS = 60
FONTNAME = 'Arial'
FONTSIZE = 40
CAPTION = 'Reaction time experiment'
SCREEN_SIZE = (800, 600)
# Session parameters
DEFAULT_NAME = 'A_girl_has_no_name'
DEFAULT_SESSION = 'Infinity'
DEFAULT_RATE = 3.0
DEFAULT_WRITE = True
# Experimental set-up
# Possible text stimuli
WORDS = {
    'A': [u'', u'A'],
    'B': ['A', 'B'],
    'C': ['A', 'B']
}
# Possible colors of text stimuli
COLORS = ['white']
# Possible phases
PHASES = itertools.cycle(['A', 'B', 'C'])
# Response options
BUTTONS = {
    'A': {
        'first': {
            'bounds': pygame.Rect(350, 450, 100, 100),
            'state': 'normal',
            'reinforced_if': 'A',
            'color_dict': {
                'normal': c.RED1,
                'hover': c.RED2,
                'pressed': c.RED3,
            }
        }
    },
    'B': {
        'first': {
            'bounds': pygame.Rect(250, 450, 100, 100),
            'state': 'normal',
            'reinforced_if': 'A',
            'color_dict': {
                'normal': c.RED1,
                'hover': c.RED2,
                'pressed': c.RED3,
            }
        },
        'second': {
            'bounds': pygame.Rect(450, 450, 100, 100),
            'state': 'normal',
            'reinforced_if': 'B',
            'color_dict': {
                'normal': c.GREEN1,
                'hover': c.GREEN2,
                'pressed': c.GREEN3,
            }
        }
    },
    'C': {
        'first': {
            'bounds': pygame.Rect(350, 450, 100, 100),
            'state': 'normal',
            'reinforced_if': 'A',
            'color_dict': {
                'normal': c.RED1,
                'hover': c.RED2,
                'pressed': c.RED3,
            }
        }
    }
}
# Stimuli presented
STIMULI = {
    'first': {
        'text': u'',
        'color': 'white',
        'pos': (400, 300)
    }
}
# Score counter
SCORE = {
    'pos': (100, 100),
    'color': 'white'
}
# Custom event to trigger changes in stimuli
CHANGE_STIMULI = pygame.USEREVENT + 1
# List to store collected data
DATA = [['time', 'responses', 'score', 'phase_name', 'phase_id', 'rate']]