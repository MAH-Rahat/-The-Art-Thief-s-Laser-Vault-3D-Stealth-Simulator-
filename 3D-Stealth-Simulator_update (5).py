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
OVERRIDE_BEAM = (0.2, 0.8, 1.0)
ARTIFACT_BEAM = (1.0, 0.86, 0.25)

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
all_oky=True
plate_count = 0
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

# --- PUZZLE / LOOT STATE ---
PLATE_HALF_SIZE = 120.0
PLATE_TRIGGER_RADIUS = 240.0
vault_plate_positions = [
    (-1800.0, 2200.0),
    (1800.0, 2450.0),
    (-1200.0, 4300.0),
    (1200.0, 5200.0),
]
vault_plate_active = [False, False, False, False]
vault_plate_progress = 0
cameras_disabled = False
laser_gate_height = 1500.0

override_box_positions = [
    (-600.0, 2200.0, 180.0),
]
override_box_used = [False]
override_active = False
override_timer = 0
security_freeze_timer = 0
OVERRIDE_DURATION_FRAMES = 360
game_won = False

artifact_x = 0.0
artifact_y = 7500.0
artifact_z = 320.0
artifact_scale = 1.0
artifact_collected = False
artifact_shatter_timer = 0
SHATTER_DURATION_FRAMES = 180
artifact_shards = []
interaction_radius = 900.0

laser_sweeps = [
    {'x': -900.0, 'y': -2900.0, 'span': 1500.0, 'speed': 8.0, 'min_x': -1600.0, 'max_x': -200.0},
    {'x': 900.0, 'y': -2900.0, 'span': 1500.0, 'speed': -8.5, 'min_x': 200.0, 'max_x': 1600.0},
]

def reset_game():
    global is_lockdown, lockdown_z, thief_x, thief_y, thief_angle
    global drones, dash_timer, decoy_state, decoy_timer
    global vault_plate_active, vault_plate_progress, cameras_disabled, laser_gate_height
    global override_box_used, override_active, override_timer, security_freeze_timer
    global game_won
    global artifact_scale, artifact_collected, artifact_shatter_timer, artifact_shards
    global laser_sweeps
    
    is_lockdown = False
    lockdown_z = 1500.0
    thief_x = random.uniform(-2000, 2000) 
    thief_y = -8500                       
    thief_angle = 90.0    
    dash_timer = 0
    decoy_state = 0
    decoy_timer = 0
    vault_plate_active = [False, False, False, False]
    vault_plate_progress = 0
    cameras_disabled = False
    laser_gate_height = 1500.0
    override_box_used = [False]
    override_active = False
    override_timer = 0
    security_freeze_timer = 0
    game_won = False
    artifact_scale = 1.0
    artifact_collected = False
    artifact_shatter_timer = 0
    artifact_shards = []
    laser_sweeps = [
        {'x': -900.0, 'y': -2900.0, 'span': 1500.0, 'speed': 8.0, 'min_x': -1600.0, 'max_x': -200.0},
        {'x': 900.0, 'y': -2900.0, 'span': 1500.0, 'speed': -8.5, 'min_x': 200.0, 'max_x': 1600.0},
    ]
    
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

def get_plate_count():
    return sum(1 for is_active in vault_plate_active if is_active)

def is_vault_unlocked():
    return vault_plate_progress >= len(vault_plate_positions)

def draw_vertical_beam(radius, height, color):
    glColor4f(color[0], color[1], color[2], 0.3)
    quadric = gluNewQuadric()
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)
    gluCylinder(quadric, radius, radius * 0.45, height, 18, 1)
    glPopMatrix()

def draw_rotating_triangle_marker(x, y, z, color, scale=140.0, spin_mul=3.0):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(artifact_spin * spin_mul, 0, 0, 1)
    glColor3f(*color)
    glBegin(GL_TRIANGLES)
    glVertex3f(0, scale, 0)
    glVertex3f(-scale * 0.75, -scale * 0.45, 0)
    glVertex3f(scale * 0.75, -scale * 0.45, 0)
    glEnd()
    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(3.0)
    glBegin(GL_LINE_LOOP)
    glVertex3f(0, scale, 0)
    glVertex3f(-scale * 0.75, -scale * 0.45, 0)
    glVertex3f(scale * 0.75, -scale * 0.45, 0)
    glEnd()
    glPopMatrix()

def draw_pressure_plate_tile(plate_x, plate_y, is_active, is_current_target):
    if is_active:
        outer_color = (0.18, 0.72, 0.28) if not override_active else (0.05, 0.20, 0.08)
        inner_color = (0.28, 0.95, 0.38) if not override_active else (0.08, 0.25, 0.12)
    elif is_current_target:
        outer_color = (0.7, 0.58, 0.16) if not override_active else (0.15, 0.12, 0.03)
        inner_color = (0.96, 0.82, 0.24) if not override_active else (0.20, 0.15, 0.05)
    else:
        outer_color = (0.4, 0.18, 0.18) if not override_active else (0.12, 0.05, 0.05)
        inner_color = (0.58, 0.26, 0.26) if not override_active else (0.15, 0.08, 0.08)

    glColor3f(*outer_color)
    glBegin(GL_QUADS)
    glVertex3f(plate_x - PLATE_HALF_SIZE, plate_y - PLATE_HALF_SIZE, 8)
    glVertex3f(plate_x + PLATE_HALF_SIZE, plate_y - PLATE_HALF_SIZE, 8)
    glVertex3f(plate_x + PLATE_HALF_SIZE, plate_y + PLATE_HALF_SIZE, 8)
    glVertex3f(plate_x - PLATE_HALF_SIZE, plate_y + PLATE_HALF_SIZE, 8)
    glEnd()

    glColor3f(*inner_color)
    glBegin(GL_QUADS)
    glVertex3f(plate_x - 70, plate_y - 70, 10)
    glVertex3f(plate_x + 70, plate_y - 70, 10)
    glVertex3f(plate_x + 70, plate_y + 70, 10)
    glVertex3f(plate_x - 70, plate_y + 70, 10)
    glEnd()

def draw_wire_ring(radius, color, segments=28):
    glColor3f(*color)
    glBegin(GL_LINE_LOOP)
    for i in range(segments):
        angle = math.tau * i / segments
        glVertex3f(math.cos(angle) * radius, math.sin(angle) * radius, 0)
    glEnd()

def draw_override_pulse(x, y, z, is_used):
    pulse_phase = artifact_spin * 0.08
    inner = 80.0 + math.sin(pulse_phase) * 12.0
    outer = 130.0 + math.sin(pulse_phase * 1.4) * 18.0
    glow = (0.2, 0.95, 1.0) if is_used else (0.35, 0.7, 1.0)

    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(90, 1, 0, 0)
    draw_wire_ring(inner, glow)
    draw_wire_ring(outer, (0.8, 0.95, 1.0) if is_used else (0.55, 0.75, 1.0))
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
                # Oishy Jobaida - Darken interior floor when power cut
                if override_active:
                    col_a = (0.05, 0.05, 0.08)  # Dark blue-gray
                    col_b = (0.04, 0.04, 0.07)  # Slightly darker
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

    if is_night and not cameras_disabled:
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
    
    if is_night and not cameras_disabled:
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

def draw_streetlight(x, y):
    glPushMatrix()
    glTranslatef(x, y, 0)
    
    if is_night:
        glPushMatrix()
        direction = 1 if x < 0 else -1
        glTranslatef(direction * 300, 0, 0) 
        draw_light_pool(280, 0.9, 0.9, 0.7, 20) 
        glPopMatrix()

    glColor3f(0.2, 0.2, 0.2)
    gluCylinder(gluNewQuadric(), 15, 10, 800, 10, 10)

    glTranslatef(0, 0, 800)
    direction = 90 if x < 0 else -90 
    glRotatef(direction, 0, 0, 1)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 8, 8, 300, 10, 10) 

    glTranslatef(0, 0, 300)
    if is_night:
        glColor3f(1.0, 1.0, 0.8) 
    else:
        glColor3f(0.3, 0.3, 0.3) 
    gluSphere(gluNewQuadric(), 30, 15, 15)
    glPopMatrix()

def draw_grass_bushes():
    bush_col = NIGHT_BUSH if is_night else DAY_BUSH
    glColor3f(*bush_col)
    for bx, by in bush_positions:
        if -350 < bx < 350:
            continue
        glPushMatrix()
        glTranslatef(bx, by, 0)
        glScalef(1.5, 1.5, 0.8) 
        gluSphere(gluNewQuadric(), 80, 10, 10)
        glPopMatrix()

def draw_outer_field_objects():
    draw_grass_bushes()

    tree_coords = [
        (-4000, -2000), (4000, -2000), (-3000, -6000), (3000, -6000),
        (-6000, -1000), (6000, -1000), (-2000, -8000), (2000, -8000),
        (-5000, -4000), (5000, -4000), (-7000, -7000), (7000, -7000)
    ]
    for tx, ty in tree_coords:
        draw_massive_tree(tx, ty)
        
    for px, py, phase in cctv_pillars:
        draw_cctv_pillar(px, py, phase)

    for sy in range(-1000, -9000, -1500):
        draw_streetlight(-350, sy)
        draw_streetlight(350, sy)

def draw_museum_architecture():
    wall_col = NIGHT_WALL if is_night else DAY_WALL
    glColor3f(*wall_col)
    
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, 0, 0); glVertex3f(-6500, 0, 0)
    glVertex3f(-6500, 0, 1500); glVertex3f(-GRID_LENGTH, 0, 1500)
    
    glVertex3f(-6500, 0, 450); glVertex3f(-5750, 0, 450)
    glVertex3f(-5750, 0, 1500); glVertex3f(-6500, 0, 1500)
    
    glVertex3f(-5750, 0, 0); glVertex3f(-500, 0, 0)
    glVertex3f(-500, 0, 1500); glVertex3f(-5750, 0, 1500)
    
    glVertex3f(500, 0, 0); glVertex3f(GRID_LENGTH, 0, 0)
    glVertex3f(GRID_LENGTH, 0, 1500); glVertex3f(500, 0, 1500)

    glVertex3f(-GRID_LENGTH, 0, 0); glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 1500); glVertex3f(-GRID_LENGTH, 0, 1500)
    
    glVertex3f(GRID_LENGTH, 0, 0); glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 1500); glVertex3f(GRID_LENGTH, 0, 1500)
    
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0); glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 1500); glVertex3f(-GRID_LENGTH, GRID_LENGTH, 1500)

    if is_night:
        glColor3f(NIGHT_WALL[0]*0.8, NIGHT_WALL[1]*0.8, NIGHT_WALL[2]*0.8) 
    else:
        glColor3f(DAY_WALL[0]*0.8, DAY_WALL[1]*0.8, DAY_WALL[2]*0.8)
        
    glVertex3f(-GRID_LENGTH, 0, 1500)
    glVertex3f(GRID_LENGTH, 0, 1500)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 1500)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 1500)
    glEnd()

    for wx, wy, wz, phase in cctv_walls:
        draw_wall_cctv(wx, wy, wz, phase)
    glColor3f(0.3, 0.15, 0.05) 
    glPushMatrix()
    glTranslatef(0, 0, 400) 
    glScalef(10.0, 0.5, 8.0) 
    glutSolidCube(100)
    glPopMatrix()
    if is_lockdown:
        glColor3f(0.05, 0.05, 0.05) 
        for bar_x in range(-450, 500, 100):
            glPushMatrix()
            glTranslatef(bar_x, 0, lockdown_z) 
            gluCylinder(gluNewQuadric(), 15, 15, 1500, 10, 10)
            glPopMatrix()

    glColor3f(*wall_col)
    glPushMatrix()
    glTranslatef(-4650, 6000, 750)
    glScalef(87.0, 1.0, 15.0) 
    glutSolidCube(100)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(4650, 6000, 750)
    glScalef(87.0, 1.0, 15.0) 
    glutSolidCube(100)
    glPopMatrix()

    if laser_gate_height > 5:
        glColor3f(*COLOR_LASER)
        for lx in range(-250, 300, 100): 
            glPushMatrix()
            glTranslatef(lx, 6000, 0) 
            gluCylinder(gluNewQuadric(), 15, 15, laser_gate_height, 10, 10)
            glPopMatrix()

def draw_interior_artifacts():
    box_data = [
        (-2000, 2000, 0), (2000, 2000, 1), (-4000, 4000, 2), 
        (4000, 4000, 3), (-1500, 5000, 4), (1500, 5000, 5)
    ]
    for bx, by, kind in box_data:
        glPushMatrix()
        glTranslatef(bx, by, 0)
        
        glColor3f(0.15, 0.15, 0.15)
        glPushMatrix()
        glTranslatef(0, 0, 100)
        glScalef(2.0, 2.0, 2.0)
        glutSolidCube(100)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0, 0, 250)
        glRotatef(artifact_spin, 0, 0, 1) 
        glRotatef(artifact_spin * 0.5, 0, 1, 0)
        
        if kind == 0:
            glColor3f(0.8, 0.2, 0.2) 
            gluSphere(gluNewQuadric(), 40, 15, 15)
        elif kind == 1:
            glColor3f(0.2, 0.8, 0.2) 
            glutSolidCube(60)
        elif kind == 2:
            glColor3f(0.2, 0.2, 0.8) 
            gluCylinder(gluNewQuadric(), 30, 30, 60, 10, 10)
        elif kind == 3:
            glColor3f(0.8, 0.8, 0.2) 
            gluCylinder(gluNewQuadric(), 40, 0, 80, 10, 10)
        elif kind == 4:
            glColor3f(0.8, 0.4, 0.8) 
            gluSphere(gluNewQuadric(), 30, 10, 10)
            glTranslatef(0, 0, 30)
            gluSphere(gluNewQuadric(), 15, 10, 10)
        else:
            glColor3f(0.4, 0.8, 0.8) 
            glutSolidCube(40)
            glTranslatef(0, 0, 30)
            gluSphere(gluNewQuadric(), 20, 10, 10)
        glPopMatrix()

        glColor3f(0.3, 0.4, 0.5) 
        glPushMatrix()
        glTranslatef(0, 0, 400)
        glScalef(1.9, 1.9, 0.1)
        glutSolidCube(100)
        glPopMatrix()

        for px, py in [(-90, -90), (90, -90), (-90, 90), (90, 90)]:
            glPushMatrix()
            glTranslatef(px, py, 250)
            glScalef(0.1, 0.1, 3.0)
            glutSolidCube(100)
            glPopMatrix()

        glPopMatrix()

def draw_puzzle_and_loot():
    if cameras_disabled:
        for index, (plate_x, plate_y) in enumerate(vault_plate_positions):
            draw_pressure_plate_tile(
                plate_x,
                plate_y,
                vault_plate_active[index],
                index == vault_plate_progress,
            )

    for index, (box_x, box_y, box_z) in enumerate(override_box_positions):
        glPushMatrix()
        glTranslatef(box_x, box_y, box_z)
        # Oishy Jobaida - Darken override box when power cut
        if override_box_used[index]:
            color_box = (0.12, 0.82, 1.0) if not override_active else (0.03, 0.20, 0.25)
            glColor3f(*color_box)
        else:
            color_box = (0.2, 0.35, 1.0) if not override_active else (0.05, 0.08, 0.25)
            glColor3f(*color_box)
        glutSolidCube(110)
        glColor3f(0.08, 0.14, 0.3)
        glPushMatrix()
        glTranslatef(0, -62, 0)
        glScalef(82, 12, 82)
        glutSolidCube(1)
        glPopMatrix()

        color_light = (0.85, 0.9, 1.0) if not override_active else (0.20, 0.22, 0.25)

        glColor3f(0.85, 0.9, 1.0)
        glTranslatef(0, 0, 70)
        glutSolidCube(30)
        glPushMatrix()
        glTranslatef(0, -58, 12)
        if not override_active:
            glColor3f(0.55, 0.9, 1.0 if override_box_used[index] else 0.8)
        else:
            glColor3f(0.12, 0.20, 0.25)
        glScalef(60, 8, 45)
        glutSolidCube(1)
        glPopMatrix()

        glTranslatef(0, 0, 120)
        if override_box_used[index]:
            draw_light_pool(70, 0.2, 0.95, 1.0, 2)
            color_beam = (0.2, 0.9, 1.0) if not override_active else (0.05, 0.20, 0.25)
            glColor3f(*color_beam)
        else:
            draw_light_pool(45, 0.4, 0.6, 1.0, 2)
            glColor3f(0.35, 0.65, 1.0)

        glPushMatrix()
        glTranslatef(0, 0, 210)
        glScalef(24, 24, 220)
        glutSolidCube(1)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0, 0, 65)
        draw_vertical_beam(38 if override_box_used[index] else 18, 420 if override_box_used[index] else 320, OVERRIDE_BEAM)
        glPopMatrix()
        glPopMatrix()

        draw_override_pulse(box_x, box_y, box_z + 18, override_box_used[index])
        if not override_box_used[index]:
            draw_rotating_triangle_marker(box_x, box_y, box_z + 430, (0.35, 0.8, 1.0), 120.0, -3.2)
        elif override_active:
            draw_rotating_triangle_marker(box_x, box_y, box_z + 500, (0.2, 1.0, 1.0), 145.0, 5.0)

    for laser in laser_sweeps:
        glPushMatrix()
        glTranslatef(laser['x'], laser['y'], 160)
        glColor3f(0.22, 0.08, 0.12) if override_active else glColor3f(*COLOR_LASER)
        glScalef(22, laser['span'], 16)
        glutSolidCube(1)
        glPopMatrix()

    if not artifact_collected or artifact_scale > 0.01:
        glPushMatrix()
        glTranslatef(artifact_x, artifact_y, 80)
        glScalef(360, 360, 160)
        glColor3f(0.28, 0.28, 0.32)
        glutSolidCube(1)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(artifact_x, artifact_y, 250)
        glColor4f(0.75, 0.88, 0.96, 0.25)
        glScalef(260, 260, 320)
        glutWireCube(1)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(artifact_x, artifact_y, artifact_z)
        glRotatef(artifact_spin * 6.0, 0, 0, 1)
        glRotatef(artifact_spin * 2.0, 1, 0, 0)
        glScalef(max(artifact_scale, 0.05), max(artifact_scale, 0.05), max(artifact_scale, 0.05))
        # Oishy Jobaida - Darken artifact when power cut
        color_gold = (0.95, 0.82, 0.22) if not override_active else (0.25, 0.20, 0.05)
        glColor3f(*color_gold)
        glutSolidCube(150)
        color_white = (0.9, 0.95, 1.0) if not override_active else (0.20, 0.22, 0.25)
        glColor3f(*color_white)
        glutWireCube(230)
        glPushMatrix()
        glTranslatef(0, 0, -140)
        draw_light_pool(120, 1.0, 0.95, 0.3, 2)
        glPopMatrix()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(artifact_x, artifact_y, 90)
        draw_vertical_beam(22, 360, ARTIFACT_BEAM)
        glPopMatrix()
        draw_rotating_triangle_marker(artifact_x, artifact_y, 520, (1.0, 0.86, 0.25), 130.0, 4.0)

    for shard in artifact_shards:
        glPushMatrix()
        glTranslatef(shard['x'], shard['y'], shard['z'])
        glRotatef(shard['spin'], 1, 1, 0)
        glColor3f(0.7, 0.85, 0.95)
        glScalef(shard['sx'], shard['sy'], shard['sz'])
        glutSolidCube(1)
        glPopMatrix()

def draw_security_drones():
    for d in drones:
        glPushMatrix()
        glTranslatef(d['x'], d['y'], d['z'])
        
        glColor3f(0.2, 0.2, 0.2)
        glPushMatrix()
        glScalef(2.0, 2.0, 0.5)
        glutSolidCube(80)
        glPopMatrix()
        
        glColor3f(0.1, 0.1, 0.1)
        for rx, ry in [(-80, -80), (80, -80), (-80, 80), (80, 80)]:
            glPushMatrix()
            glTranslatef(rx, ry, 0)
            gluCylinder(gluNewQuadric(), 25, 25, 20, 10, 10)
            glPopMatrix()
            
        if is_night:
            glPushMatrix()
            glTranslatef(0, 0, -d['z']) 
            draw_light_pool(400, 0.9, 0.1, 0.1, 100)
            glPopMatrix()
            
        glPopMatrix()

def draw_thief():
    if is_lockdown and lockdown_z == 0 and -500 < thief_x < 500 and thief_y > -100:
        return 

    glPushMatrix()
    glTranslatef(thief_x, thief_y, 0)
    glRotatef(thief_angle - 90, 0, 0, 1)
    
    if is_night and is_torch_on:
        glPushMatrix()
        glTranslatef(40, 600, 0) 
        glScalef(2.0, 3.0, 1.0) 
        draw_light_pool(200, 0.95, 0.85, 0.65, 80) 
        glPopMatrix()

    if camera_mode == "first_person":
        glPopMatrix()
        return 
        
    if dash_timer > 0:
        glScalef(3.0, 3.0, 3.0) 
    else:
        glScalef(3.0, 3.0, 3.0) 

    glColor3f(0.1, 0.1, 0.15) 
    glPushMatrix()
    if is_crouching:
        glTranslatef(0, 15, -10)
        glRotatef(-45, 1, 0, 0) 
    
    glPushMatrix()
    glTranslatef(-15, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 8, 70, 10, 10)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(15, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 8, 70, 10, 10)
    glPopMatrix()
    glPopMatrix() 

    glPushMatrix()
    if is_crouching:
        glTranslatef(0, 15, -30) 
        glRotatef(-30, 1, 0, 0)  

    glColor3f(0.15, 0.15, 0.15) 
    glPushMatrix()
    glTranslatef(0, 5, 110) 
    glRotatef(-15, 1, 0, 0) 
    glScalef(1.1, 0.6, 1.2)
    glutSolidCube(60)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 15, 160) 
    glColor3f(0.9, 0.7, 0.5) 
    gluSphere(gluNewQuadric(), 20, 15, 15)
    glColor3f(0.05, 0.05, 0.05) 
    glTranslatef(0, 0, 5)
    gluSphere(gluNewQuadric(), 21, 15, 15)
    glPopMatrix()

    glColor3f(0.15, 0.15, 0.15)
    glPushMatrix()
    glTranslatef(-40, 5, 130)
    glRotatef(180, 1, 0, 0) 
    gluCylinder(gluNewQuadric(), 8, 6, 80, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(40, 5, 130)
    glRotatef(180, 1, 0, 0) 
    gluCylinder(gluNewQuadric(), 8, 6, 80, 10, 10)
    glPopMatrix()

    glPopMatrix() 
    glPopMatrix() 

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(cam_fov, 1.25, 0.1, 45000) 
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    if camera_mode == "global":
        rad = math.radians(cam_angle)
        x = math.sin(rad) * cam_dist
        y = -math.cos(rad) * cam_dist
        gluLookAt(x, y, cam_height, 0, 2000, 0, 0, 0, 1)
        
    elif camera_mode == "first_person":
        rad = math.radians(thief_angle)
        
        eye_x = thief_x 
        eye_y = thief_y 
        
        cam_z = 220 if is_crouching else 480
        
        target_x = eye_x + math.cos(rad) * 2000
        target_y = eye_y + math.sin(rad) * 2000
        target_z = cam_z - 50 
        
        gluLookAt(eye_x, eye_y, cam_z, target_x, target_y, target_z, 0, 0, 1)

def is_valid_move(nx, ny):
    if nx < -8800 or nx > 8800: return False
    if ny < -8800 or ny > 8800: return False

    if -150 < ny < 150:
        if -6400 < nx < -5850:
            if not is_crouching:
                return False
        elif plate_count>=4 and -500 < nx < 500:
            pass
        else:
            return False

    if 5850 < ny < 6150 and laser_gate_height > 5:
        return False 

    return True

def keyboardListener(key, x, y):
    global is_night, camera_mode, is_crouching, is_torch_on, thief_x, thief_y, thief_angle, cam_fov
    global dash_timer, decoy_state, decoy_x, decoy_y, decoy_z, decoy_vx, decoy_vy, decoy_vz, decoy_timer
    global override_active, override_timer, security_freeze_timer, override_box_used, cameras_disabled
    global game_won
    global artifact_collected, artifact_scale, artifact_shatter_timer, artifact_shards
    
    try:
        char = key.decode('utf-8').lower()
    except:
        char = ''

    if char == 'r':
        reset_game()
        glutPostRedisplay()
        return

    if is_lockdown: return

    if char == 't':
        is_night = not is_night
    elif char == 'v':
        if camera_mode == "global":
            camera_mode = "first_person"
        else:
            camera_mode = "global"
    elif char == 'c':
        is_crouching = not is_crouching
    elif char == 'f':
        is_torch_on = not is_torch_on
        
    elif char == 'e':
        handled_interaction = False
        for index, (box_x, box_y, box_z) in enumerate(override_box_positions):
            if not override_box_used[index] and math.hypot(thief_x - box_x, thief_y - box_y) < interaction_radius:
                override_box_used[index] = True
                override_active = True
                override_timer = OVERRIDE_DURATION_FRAMES
                security_freeze_timer = OVERRIDE_DURATION_FRAMES
                cameras_disabled = True
                artifact_shatter_timer = SHATTER_DURATION_FRAMES
                artifact_shards = []
                for _ in range(26):
                    shard_angle = random.uniform(0.0, math.tau)
                    shard_speed = random.uniform(12.0, 32.0)
                    artifact_shards.append({
                        'x': box_x,
                        'y': box_y,
                        'z': box_z + 70.0,
                        'vx': math.cos(shard_angle) * shard_speed,
                        'vy': math.sin(shard_angle) * shard_speed,
                        'vz': random.uniform(8.0, 24.0),
                        'spin': random.uniform(0.0, 360.0),
                        'rot_speed': random.uniform(4.0, 10.0),
                        'sx': random.uniform(12.0, 30.0),
                        'sy': random.uniform(8.0, 20.0),
                        'sz': random.uniform(5.0, 16.0),
                    })
                handled_interaction = True
                break

        if not handled_interaction and not artifact_collected and math.hypot(thief_x - artifact_x, thief_y - artifact_y) < interaction_radius:
            artifact_collected = True
            artifact_scale = 0.0
            game_won = True

        if not handled_interaction and not artifact_collected and dash_timer <= 0 and not is_crouching:
            dash_timer = 25
            
    # --- UPDATED: TRIGGER THROW PHYSICS ---
    elif char == 'q':
        if decoy_state == 0:
            decoy_state = 1 # State 1: In the air!
            # Spawns exactly at the thief's hand height
            decoy_x = thief_x + math.cos(math.radians(thief_angle)) * 50
            decoy_y = thief_y + math.sin(math.radians(thief_angle)) * 50
            decoy_z = 150.0 
            
            # Give it strong forward speed + upward thrust to create a beautiful arc!
            throw_speed = 150.0
            decoy_vx = math.cos(math.radians(thief_angle)) * throw_speed
            decoy_vy = math.sin(math.radians(thief_angle)) * throw_speed
            decoy_vz = 45.0 
        
    elif char == 'z':
        cam_fov -= 2.0
        if cam_fov < 10.0: cam_fov = 10.0 
    elif char == 'x':
        cam_fov += 2.0
        if cam_fov > 150.0: cam_fov = 150.0 

    elif char == 'w':
        next_x = thief_x + math.cos(math.radians(thief_angle)) * 30
        next_y = thief_y + math.sin(math.radians(thief_angle)) * 30
        if is_valid_move(next_x, next_y):
            thief_x, thief_y = next_x, next_y
    elif char == 's':
        next_x = thief_x - math.cos(math.radians(thief_angle)) * 30
        next_y = thief_y - math.sin(math.radians(thief_angle)) * 30
        if is_valid_move(next_x, next_y):
            thief_x, thief_y = next_x, next_y
    elif char == 'a':
        thief_angle += 5
    elif char == 'd':
        thief_angle -= 5
    
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global cam_angle, cam_height, cam_dist
    if key == GLUT_KEY_LEFT:
        cam_angle -= 3
    elif key == GLUT_KEY_RIGHT:
        cam_angle += 3
    elif key == GLUT_KEY_UP:
        cam_height += 300 
    elif key == GLUT_KEY_DOWN:
        cam_height -= 300
    glutPostRedisplay()

def idle():
    global artifact_spin, drones, cctv_time, is_lockdown, lockdown_z
    global dash_timer, thief_x, thief_y
    global decoy_state, decoy_x, decoy_y, decoy_z, decoy_vx, decoy_vy, decoy_vz, decoy_timer
    global vault_plate_progress, vault_plate_active, laser_gate_height
    global override_timer, security_freeze_timer, override_active
    global game_won
    global artifact_scale, artifact_shatter_timer, artifact_shards, laser_sweeps
    
    artifact_spin += 1.5
    if artifact_spin > 360:
        artifact_spin -= 360
        
    cctv_time += 0.02

    if cameras_disabled and vault_plate_progress < len(vault_plate_positions):
        plate_x, plate_y = vault_plate_positions[vault_plate_progress]
        if math.hypot(thief_x - plate_x, thief_y - plate_y) < PLATE_TRIGGER_RADIUS:
            vault_plate_active[vault_plate_progress] = True
            vault_plate_progress += 1

    if cameras_disabled and is_vault_unlocked():
        laser_gate_height = max(0.0, laser_gate_height - 20.0)

    if override_timer > 0:
        override_timer -= 1
        security_freeze_timer = override_timer
        override_active = True
        if override_timer <= 0:
            override_active = False
            security_freeze_timer = 0
    else:
        override_active = False
        security_freeze_timer = 0

    if not is_lockdown:
        if dash_timer > 0:
            dash_timer -= 1
            next_x = thief_x + math.cos(math.radians(thief_angle)) * 60
            next_y = thief_y + math.sin(math.radians(thief_angle)) * 60
            if is_valid_move(next_x, next_y):
                thief_x, thief_y = next_x, next_y
                
        # --- NEW: CALCULATE DECOY THROW PHYSICS ---
        if decoy_state == 1:
            # It flies through the air using velocity!
            decoy_x += decoy_vx
            decoy_y += decoy_vy
            decoy_z += decoy_vz
            decoy_vz -= 3.0 # GRAVITY pulls it down every frame
            
            # If it hits the floor...
            if decoy_z <= 20:
                decoy_z = 20
                decoy_state = 2 # State 2: Landed!
                decoy_timer = 250 # Start the timer for the drones to investigate
                
        elif decoy_state == 2:
            decoy_timer -= 1
            if decoy_timer <= 0:
                decoy_state = 0 # Disappears

        if security_freeze_timer <= 0:
            for d in drones:
                if decoy_state == 2:
                    dx = decoy_x - d['x']
                    dy = decoy_y - d['y']
                    dist = math.hypot(dx, dy)
                    if dist > d['speed']:
                        d['x'] += (dx / dist) * d['speed']
                        d['y'] += (dy / dist) * d['speed']
                else:
                    if d['state'] == 0:
                        d['x'] += d['speed']
                        if d['x'] >= d['max_x']: d['state'] = 1
                    elif d['state'] == 1:
                        d['y'] += d['speed']
                        if d['y'] >= d['max_y']: d['state'] = 2
                    elif d['state'] == 2:
                        d['x'] -= d['speed']
                        if d['x'] <= d['min_x']: d['state'] = 3
                    elif d['state'] == 3:
                        d['y'] -= d['speed']
                        if d['y'] <= d['min_y']: d['state'] = 0

            for laser in laser_sweeps:
                laser['x'] += laser['speed']
                if laser['x'] <= laser['min_x'] or laser['x'] >= laser['max_x']:
                    laser['speed'] *= -1
                    laser['x'] = max(laser['min_x'], min(laser['x'], laser['max_x']))

    if artifact_shatter_timer > 0:
        artifact_shatter_timer -= 1

    for shard in artifact_shards:
        shard['vx'] *= 0.992
        shard['vy'] *= 0.992
        shard['vz'] -= 1.8
        shard['x'] += shard['vx']
        shard['y'] += shard['vy']
        shard['z'] += shard['vz']
        shard['spin'] += shard['rot_speed']

    if not is_lockdown and not game_won:
        for d in drones:
            dist = math.hypot(thief_x - d['x'], thief_y - d['y'])
            if dist < 400: 
                is_lockdown = True
                        
        if laser_gate_height > 5 and 5900 < thief_y < 6100:
            if not is_crouching:
                for lx in range(-250, 300, 100):
                    if abs(thief_x - lx) < 80:
                        is_lockdown = True

        if not cameras_disabled:
            for px, py, phase in cctv_pillars:
                dx = thief_x - px
                dy = thief_y - py
                if math.hypot(dx, dy) < 1200:
                    facing_angle = 90.0 + math.sin(cctv_time + phase) * 60.0
                    thief_angle_to_cctv = math.degrees(math.atan2(dy, dx))
                    diff = (thief_angle_to_cctv - facing_angle) % 360
                    if diff > 180: diff -= 360
                    if abs(diff) < 30: 
                        is_lockdown = True

            for wx, wy, wz, phase in cctv_walls:
                dx = thief_x - wx
                dy = thief_y - wy
                if math.hypot(dx, dy) < 1000:
                    facing_angle = -90.0 + math.sin(cctv_time + phase) * 60.0
                    thief_angle_to_cctv = math.degrees(math.atan2(dy, dx))
                    diff = (thief_angle_to_cctv - facing_angle) % 360
                    if diff > 180: diff -= 360
                    if abs(diff) < 30:
                        is_lockdown = True

    if is_lockdown and lockdown_z > 0:
        lockdown_z -= 60.0
        if lockdown_z < 0: lockdown_z = 0
                
    glutPostRedisplay()

def showScreen():
    if is_lockdown:
        siren_blink = math.sin(cctv_time * 15.0)
        if siren_blink > 0:
            glClearColor(1.0, 0.0, 0.0, 1.0) 
        else:
            glClearColor(0.3, 0.0, 0.0, 1.0) 
    elif override_active:
        glClearColor(0.0, 0.0, 0.0, 1.0)
    else:
        glClearColor(0, 0, 0, 1) 
        
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) #type: ignore
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)

    setupCamera()

    draw_super_massive_floor_and_road()
    draw_outer_field_objects()
    draw_museum_architecture()
    draw_puzzle_and_loot()
    draw_interior_artifacts()
    
    draw_decoy() 
    draw_security_drones() 
    draw_thief()

    # glDisable(GL_DEPTH_TEST) 
    
    # draw_text(10, 780, "A Random Fixed Position Text")
    # draw_text(10, 760, f"See how the position and variable change?: {rand_var}")

    mode = "LOCKDOWN!" if is_lockdown else ("NIGHT" if is_night else "DAY")
    posture = "CROUCH" if is_crouching else "STAND"
    torch = "ON" if is_torch_on else "OFF"
    dash_text = "DASHING!" if dash_timer > 0 else "READY"
    
    # Update HUD based on the new physics states
    if decoy_state == 1: decoy_text = "FLYING..."
    elif decoy_state == 2: decoy_text = f"ACTIVE ({decoy_timer})"
    else: decoy_text = "READY"
    
    plate_count = get_plate_count()
    draw_text(10, 720, f"THE ART THIEF'S LASER VAULT | MODE: {mode} | CAM: {camera_mode.upper()}")
    draw_text(10, 700, f"POSTURE: {posture} ('C') | TORCH: {torch} ('F') | DASH: {dash_text} | DECOY: {decoy_text}")
    camera_state = "DISABLED" if cameras_disabled else "ACTIVE"
    draw_text(10, 680, f"CAMS: {camera_state} | PLATES: {plate_count}/4 | ARTIFACT: {'RECOVERED' if artifact_collected else 'LOCKED'}")
    draw_text(10, 660, "CONTROLS -> W/A/S/D: Sneak | E: Interact/Dash | Q: DECOY | Z/X: ZOOM | R: RESTART | ARROWS: Global Cam")

    next_plate_hint = "Done"
    if vault_plate_progress < len(vault_plate_positions):
        px, py = vault_plate_positions[vault_plate_progress]
        next_plate_hint = f"({px:.0f},{py:.0f})"
    draw_text(10, 640, f"NEXT PLATE: {next_plate_hint} | OVERRIDE BOX: (-600,2200) | FINAL ARTIFACT: (0,7500)")

    near_override = False
    for index, (box_x, box_y, box_z) in enumerate(override_box_positions):
        if not override_box_used[index] and math.hypot(thief_x - box_x, thief_y - box_y) < interaction_radius:
            near_override = True
            break
    near_artifact = (not artifact_collected) and math.hypot(thief_x - artifact_x, thief_y - artifact_y) < interaction_radius

    if near_override:
        draw_text(10, 620, "[E] Break Override Box: blackout room + freeze drone/laser movement")
    elif not cameras_disabled:
        draw_text(10, 620, "Disable museum cameras first from the in-room override box")
    elif not is_vault_unlocked():
        draw_text(10, 620, "Cameras offline. Activate all 4 pressure plates to open the laser beam door")
    elif near_artifact:
        draw_text(10, 620, "[E] Collect Artifact: mission complete")
    elif laser_gate_height > 5:
        draw_text(10, 620, "Laser beam door opening... stay clear of the red barrier")

    if game_won:
        draw_text(390, 440, "MISSION COMPLETE", font=GLUT_BITMAP_TIMES_ROMAN_24) #type: ignore
        draw_text(335, 410, "YOU STOLE THE ARTIFACT - PRESS 'R' TO RESTART", font=GLUT_BITMAP_HELVETICA_18) #type: ignore

    if is_lockdown:
        draw_text(380, 400, "GAME OVER - PRESS 'R' TO RESTART", font=GLUT_BITMAP_TIMES_ROMAN_24) #type: ignore
        
    glEnable(GL_DEPTH_TEST) 

    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH) #type: ignore
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b" The Art Thief's Laser Vault (3D Stealth Simulator)")
    
    glEnable(GL_DEPTH_TEST)
    
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(None) 
    glutIdleFunc(idle)
    
    glutMainLoop()

if __name__ == "__main__":
    main()
