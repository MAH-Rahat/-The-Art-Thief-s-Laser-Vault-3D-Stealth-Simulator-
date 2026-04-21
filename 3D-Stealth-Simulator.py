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

def reset_game():
    global is_lockdown, lockdown_z, thief_x, thief_y, thief_angle
    global drones, dash_timer, decoy_state, decoy_timer
    
    is_lockdown = False
    lockdown_z = 1500.0
    thief_x = random.uniform(-2000, 2000) 
    thief_y = -8500                       
    thief_angle = 90.0    
    dash_timer = 0
    decoy_state = 0
    decoy_timer = 0
    
    drones = [
        {'x': -4000, 'y': -3000, 'z': 1200, 'min_x': -5000, 'max_x': -2000, 'min_y': -4000, 'max_y': -1000, 'state': 0, 'speed': 25},
        {'x': 4000, 'y': -5000, 'z': 1000, 'min_x': 2000, 'max_x': 6000, 'min_y': -7000, 'max_y': -3000, 'state': 2, 'speed': 35},
        {'x': 0, 'y': -6000, 'z': 1500, 'min_x': -2000, 'max_x': 2000, 'min_y': -8000, 'max_y': -4000, 'state': 1, 'speed': 30},
        {'x': 0, 'y': -2000, 'z': 1300, 'min_x': -2000, 'max_x': 2000, 'min_y': -3000, 'max_y': -1000, 'state': 2, 'speed': 28}
    ]

# STRICT TEMPLATE COMPLIANCE
def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_12): #type: ignore
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 870)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_light_pool(radius, r, g, b, z_height):
    glColor3f(r, g, b)
    glPushMatrix()
    glTranslatef(0, 0, z_height)
    glScalef(1.0, 1.0, 0.01) 
    gluSphere(gluNewQuadric(), radius, 20, 20)
    glPopMatrix()

# --- UPDATED: DRAW DYNAMIC FLYING DECOY ---
def draw_decoy():
    if decoy_state > 0:
        # Draw the physical stone/cube
        glPushMatrix()
        glTranslatef(decoy_x, decoy_y, decoy_z) 
        
        # If it's flying in the air, make it tumble and spin!
        if decoy_state == 1:
            glRotatef(artifact_spin * 5.0, 1, 1, 0)
            
        glColor3f(0.4, 0.8, 1.0) 
        glutSolidCube(40)
        glPopMatrix()
        
        # Draw the tracking light/shadow explicitly clamped to the floor!
        if is_night:
            glPushMatrix()
            glTranslatef(decoy_x, decoy_y, 0)
            draw_light_pool(80, 0.4, 0.8, 1.0, 5) # Z=5 so it sits on the road/grass perfectly
            glPopMatrix()

# --- ENVIRONMENT FUNCTIONS ---
def draw_super_massive_floor_and_road():
    glBegin(GL_QUADS)
    for i in range(-GRID_LENGTH, GRID_LENGTH, 400): 
        for j in range(-GRID_LENGTH, GRID_LENGTH, 400):
            if j < 0:
                col_a = NIGHT_GRASS_A if is_night else DAY_GRASS_A
                col_b = NIGHT_GRASS_B if is_night else DAY_GRASS_B
            else:
                col_a = NIGHT_FLOOR_A if is_night else DAY_FLOOR_A
                col_b = NIGHT_FLOOR_B if is_night else DAY_FLOOR_B
            
            if ((i // 400) + (j // 400)) % 2 == 0:
                glColor3f(*col_a)
            else:
                glColor3f(*col_b)
                
            glVertex3f(i, j, 0)
            glVertex3f(i + 400, j, 0)
            glVertex3f(i + 400, j + 400, 0)
            glVertex3f(i, j + 400, 0)

    road_col = NIGHT_ROAD if is_night else DAY_ROAD
    glColor3f(*road_col)
    glVertex3f(-300, -GRID_LENGTH, 5) 
    glVertex3f(300, -GRID_LENGTH, 5)
    glVertex3f(300, 0, 5)
    glVertex3f(-300, 0, 5)
    glEnd()

def draw_massive_tree(x, y):
    trunk_col = NIGHT_TRUNK if is_night else DAY_TRUNK
    leaves_col = NIGHT_LEAVES if is_night else DAY_LEAVES
    
    glPushMatrix()
    glTranslatef(x, y, 0)
    glColor3f(*trunk_col)
    gluCylinder(gluNewQuadric(), 80, 50, 600, 10, 10)
    
    glTranslatef(0, 0, 600)
    glColor3f(*leaves_col)
    gluSphere(gluNewQuadric(), 350, 15, 15)
    glPopMatrix()

def draw_cctv_pillar(x, y, phase_offset):
    col = NIGHT_PILLAR if is_night else DAY_PILLAR
    glPushMatrix()
    glTranslatef(x, y, 0)
    
    glColor3f(*col)
    gluCylinder(gluNewQuadric(), 20, 20, 1000, 10, 10) 
    
    glTranslatef(0, 0, 1010)
    
    local_angle = math.sin(cctv_time + phase_offset) * 60.0
    glRotatef(local_angle, 0, 0, 1) 
    
    glColor3f(0.5, 0.5, 0.5)
    glutSolidCube(40) 
    
    glColor3f(0.2, 0.2, 0.2)
    glPushMatrix()
    glTranslatef(0, 20, 0)
    glRotatef(-90, 1, 0, 0) 
    gluCylinder(gluNewQuadric(), 10, 15, 30, 10, 10)
    glPopMatrix()

    if is_night:
        glPushMatrix()
        glTranslatef(0, 0, -970) 
        glColor3f(0.8, 0.8, 0.2) 
        
        glBegin(GL_QUADS)
        glVertex3f(0, 0, 0)         
        glVertex3f(-600, 1200, 0)  
        glVertex3f(600, 1200, 0)
        glVertex3f(600, 1200, 0) 
        glEnd()
        glPopMatrix()

    glPopMatrix()

def draw_wall_cctv(x, y, z, phase_offset):
    glPushMatrix()
    glTranslatef(x, y, z)
    
    glColor3f(0.3, 0.3, 0.3)
    glutSolidCube(30)
    
    glTranslatef(0, -20, 0) 
    
    local_angle = math.sin(cctv_time + phase_offset) * 60.0
    glRotatef(local_angle, 0, 0, 1) 
    
    glColor3f(0.5, 0.5, 0.5)
    glutSolidCube(40) 
    
    glColor3f(0.2, 0.2, 0.2)
    glPushMatrix()
    glTranslatef(0, -20, 0)
    glRotatef(90, 1, 0, 0) 
    gluCylinder(gluNewQuadric(), 10, 15, 30, 10, 10)
    glPopMatrix()
    
    if is_night:
        glPushMatrix()
        glTranslatef(0, 0, -z + 60) 
        glColor3f(0.8, 0.8, 0.2) 
        
        glBegin(GL_QUADS)
        glVertex3f(0, 0, 0)
        glVertex3f(-500, -1000, 0) 
        glVertex3f(500, -1000, 0)
        glVertex3f(500, -1000, 0) 
        glEnd()
        glPopMatrix()

    glPopMatrix()
