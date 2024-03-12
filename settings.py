import json
import pygame


STRUCTURES = {   # Functions to create different type of orietation
    'L': {
        1: lambda h,v: [(h,v+1),(h,v),(h,v-1),(h+1,v-1)],
        2: lambda h,v: [(h-1,v),(h,v),(h+1,v),(h-1,v-1)],
        3: lambda h,v: [(h,v+1),(h,v),(h,v-1),(h-1,v+1)],
        4: lambda h,v: [(h-1,v),(h,v),(h+1,v),(h+1,v+1)]
    },
    '-L': {
        1: lambda h,v: [(h,v+1),(h,v),(h,v-1),(h-1,v-1)],
        2: lambda h,v: [(h-1,v),(h,v),(h+1,v),(h-1,v+1)],
        3: lambda h,v: [(h,v+1),(h,v),(h,v-1),(h+1,v+1)],
        4: lambda h,v: [(h-1,v),(h,v),(h+1,v),(h+1,v-1)]
    },
    'w': {
        1: lambda h,v: [(h,v+1),(h,v),(h+1,v),(h-1,v)],
        2: lambda h,v: [(h+1,v),(h,v),(h,v+1),(h,v-1)],
        3: lambda h,v: [(h,v-1),(h,v),(h+1,v),(h-1,v)],
        4: lambda h,v: [(h-1,v),(h,v),(h,v+1),(h,v-1)]
    },
    'z': {
        1: lambda h,v: [(h,v+1),(h,v),(h+1,v),(h+1,v-1)],
        2: lambda h,v: [(h+1,v),(h,v),(h,v-1),(h-1,v-1)]
    },
    '-z': {
        1: lambda h,v: [(h,v+1),(h,v),(h-1,v),(h-1,v-1)],
        2: lambda h,v: [(h-1,v),(h,v),(h,v-1),(h+1,v-1)]
    },
    'I': {
        1: lambda h,v: [(h,v-1),(h,v),(h,v+1),(h,v+2)],
        2: lambda h,v: [(h-1,v),(h,v),(h+1,v),(h+2,v)]
    },
    'o': {
        1: lambda h,v: [(h,v+1),(h,v),(h+1,v+1),(h+1,v)]
    }
}

pygame.init()
def font(x: int):
    pygame.init()
    the_font = pygame.font.SysFont("Arial", x)
    return the_font

class Settings:
    BLOCK_SIZE = 22
    V_BOXES = 32
    H_BOXES = 20
    BOARD_SIZE = BLOCK_SIZE*H_BOXES, BLOCK_SIZE*V_BOXES
    WHITE = 255,255,255
    BLACK = 0,0,0
    GRAY = 128,128,128
    RED = 255, 0, 0
    GREEN = 0, 255, 0
    BLUE = 0, 0, 255
    point_per_line = 10
    point_per_level = 50
    frames_per_level = -2
    COLORS = {
        'yello': (255,255,0),
        'lime': (0,255,0),
        'blue': (0,0,255),
        'aqua': (0,255,255),
        'orange': (255,69,0),
        'gray': (128,128,128)
    }
    
    def __init__(self) -> None:
        self.game_unpaused = True
        global font
        self.FONT = font
        self.high_score = 0
        self.game_over = False
        self.gameing_mode = False
        self.starting_mode = True
        self.quiting_mode = False
        self.prev_mode = None
        self.reset_buttons()
        self.set_defaults()
        self.get_high_score()
    
    def set_defaults(self):
        self.point = 0
        self.level = 1
        self.frames_per_action = 12
        self.frames_counter = 0

    def reset_buttons(self):
        self.button_active = {
            'start': False,
            'new game': False,
            'quit game': False,
            'yes' : False,
            'no' : False
        }
    
    def update_score(self):
        self.point += self.point_per_line
        if self.frames_per_action <= 2:
            self.frames_per_action = 2
        elif self.point == self.level*self.point_per_level:
            self.level += 1
            self.frames_per_action += self.frames_per_level
            self.frames_counter = 0
        #print(self.level, self.frames_counter, self.frames_per_action)
    
    def get_high_score(self):
        with open('game_data.json') as game_data_file:
            game_data = json.load(game_data_file)
            self.high_score = game_data['high score']

    def save_high_score(self):
        game_data = {'high score': self.high_score}
        with open('game_data.json', 'w') as game_data_file:
            json.dump(game_data, game_data_file)