from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# --- PROFESSIONAL COLOR PALETTE ---
DAY_GRASS_A = (0.35, 0.7, 0.35)   
DAY_GRASS_B = (0.3, 0.65, 0.3)   
DAY_BUSH = (0.25, 0.6, 0.25)      
DAY_ROAD = (0.6, 0.6, 0.6)       
DAY_TRUNK = (0.45, 0.3, 0.15)
DAY_LEAVES = (0.2, 0.6, 0.2)

DAY_WALL = (0.75, 0.75, 0.8)
DAY_FLOOR_A = (0.8, 0.8, 0.85)
DAY_FLOOR_B = (0.75, 0.75, 0.8)
DAY_PILLAR = (0.6, 0.6, 0.65)

NIGHT_GRASS_A = (0.05, 0.15, 0.05)
NIGHT_GRASS_B = (0.04, 0.13, 0.04)
NIGHT_BUSH = (0.03, 0.10, 0.03)
NIGHT_ROAD = (0.2, 0.2, 0.2)
NIGHT_TRUNK = (0.15, 0.1, 0.05)
NIGHT_LEAVES = (0.04, 0.12, 0.04)

NIGHT_WALL = (0.15, 0.15, 0.2)
NIGHT_FLOOR_A = (0.1, 0.1, 0.15)
NIGHT_FLOOR_B = (0.09, 0.09, 0.14)
NIGHT_PILLAR = (0.2, 0.2, 0.25)

VAULT_DOOR = (0.3, 0.35, 0.4)
COLOR_LASER = (1.0, 0.0, 0.2)

# --- GLOBAL STATE ---
is_night = True  
cam_angle = 30.0     
cam_height = 7000.0  
cam_dist = 16000.0   
cam_fov = 120.0       
GRID_LENGTH = 9000   
artifact_spin = 0.0

rand_var = 423

# --- PLAYER (THIEF) STATE ---
camera_mode = "global"  
thief_x = random.uniform(-2000, 2000) 
thief_y = -8500                       
thief_angle = 90.0                    
is_crouching = False 
is_torch_on = False 
dash_timer = 0
