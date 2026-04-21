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

# --- FEATURE 3: DECOY KINEMATICS PHYSICS STATE ---
# State: 0 = Ready, 1 = Thrown (In Air), 2 = Landed (Drones Chasing)
decoy_state = 0 
decoy_x = 0.0
decoy_y = 0.0
decoy_z = 0.0
decoy_vx = 0.0
decoy_vy = 0.0
decoy_vz = 0.0
decoy_timer = 0

bush_positions = [(random.uniform(-8000, 8000), random.uniform(-8500, -100)) for _ in range(150)]

# --- SECURITY SYSTEMS STATE ---
is_lockdown = False
lockdown_z = 1500.0 

drones = [
    {'x': -4000, 'y': -3000, 'z': 1200, 'min_x': -5000, 'max_x': -2000, 'min_y': -4000, 'max_y': -1000, 'state': 0, 'speed': 25},
    {'x': 4000, 'y': -5000, 'z': 1000, 'min_x': 2000, 'max_x': 6000, 'min_y': -7000, 'max_y': -3000, 'state': 2, 'speed': 35},
    {'x': 0, 'y': -6000, 'z': 1500, 'min_x': -2000, 'max_x': 2000, 'min_y': -8000, 'max_y': -4000, 'state': 1, 'speed': 30},
    {'x': 0, 'y': -2000, 'z': 1300, 'min_x': -2000, 'max_x': 2000, 'min_y': -3000, 'max_y': -1000, 'state': 2, 'speed': 28},
]

cctv_pillars = [
    (-3500, -2500, 0.0), (3500, -2500, 3.14), 
    (-4500, -6000, 1.5), (4500, -6000, 4.5)
]
cctv_walls = [
    (-3000, -10, 800, 0.0), (3000, -10, 800, 3.14)
]

cctv_time = 0.0

