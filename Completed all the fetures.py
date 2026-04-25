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

COLOR_LASER = (1.0, 0.0, 0.2)

# --- GLOBAL STATE ---
is_night = True  
cam_angle = 30.0     
cam_height = 7000.0  
cam_dist = 16000.0   
cam_fov = 120.0       
GRID_LENGTH = 9000   
artifact_spin = 0.0

# --- PLAYER (THIEF) STATE ---
camera_mode = "global"  
thief_x = random.uniform(-2000, 2000) 
thief_y = -8500                       
thief_angle = 90.0                    
is_crouching = False 
is_torch_on = False 
dash_timer = 0

# --- FEATURE 3 (MEMBER 2): DECOY KINEMATICS PHYSICS STATE ---
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

# ADDED NEW CCTV ON THE BACK WALL OF THE ARTIFACT ROOM
cctv_walls = [
    (-3000, -10, 800, 0.0), 
    (3000, -10, 800, 3.14),
    (0, 8950, 800, 0.0) 
]
cctv_time = 0.0

# --- FEATURE 3 (MEMBER 3): PUZZLES & LOOT STATE ---
pressure_plates = [
    {'x': 0, 'y': 2500, 'active': False},
    {'x': -300, 'y': 4000, 'active': False},
    {'x': 300, 'y': 4000, 'active': False}
]

entrance_lasers_active = True
power_box_hacked = False
hack_progress = 0.0
is_hacking = False
artifact_stolen = False
artifact_scale = 2.0
glass_shatter = False
game_won = False
shards = []
for _ in range(120):
    shards.append({
        'x': random.uniform(-150, 150),
        'y': random.uniform(-150, 150),
        'z': random.uniform(100, 500),
        'vx': random.uniform(-25, 25),
        'vy': random.uniform(-25, 25),
        'vz': random.uniform(10, 35)
    })

def reset_game():
    global is_lockdown, lockdown_z, thief_x, thief_y, thief_angle
    global drones, dash_timer, decoy_state, decoy_timer
    global pressure_plates, entrance_lasers_active, power_box_hacked
    global hack_progress, is_hacking, artifact_stolen, artifact_scale, glass_shatter, game_won
    
    is_lockdown = False
    lockdown_z = 1500.0
    thief_x = random.uniform(-2000, 2000) 
    thief_y = -8500                       
    thief_angle = 90.0    
    dash_timer = 0
    decoy_state = 0
    decoy_timer = 0
    
    for p in pressure_plates: p['active'] = False
    entrance_lasers_active = True
    power_box_hacked = False
    hack_progress = 0.0
    is_hacking = False
    artifact_stolen = False
    artifact_scale = 2.0
    glass_shatter = False
    game_won = False
    for s in shards:
        s['x'], s['y'], s['z'] = random.uniform(-150, 150), random.uniform(-150, 150), random.uniform(100, 500)
    
    drones = [
        {'x': -4000, 'y': -3000, 'z': 1200, 'min_x': -5000, 'max_x': -2000, 'min_y': -4000, 'max_y': -1000, 'state': 0, 'speed': 25},
        {'x': 4000, 'y': -5000, 'z': 1000, 'min_x': 2000, 'max_x': 6000, 'min_y': -7000, 'max_y': -3000, 'state': 2, 'speed': 35},
        {'x': 0, 'y': -6000, 'z': 1500, 'min_x': -2000, 'max_x': 2000, 'min_y': -8000, 'max_y': -4000, 'state': 1, 'speed': 30},
        {'x': 0, 'y': -2000, 'z': 1300, 'min_x': -2000, 'max_x': 2000, 'min_y': -3000, 'max_y': -1000, 'state': 2, 'speed': 28}
    ]

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_12):
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

def draw_decoy():
    if decoy_state > 0:
        glPushMatrix()
        glTranslatef(decoy_x, decoy_y, decoy_z) 
        if decoy_state == 1:
            glRotatef(artifact_spin * 5.0, 1, 1, 0)
        glColor3f(0.4, 0.8, 1.0) 
        glutSolidCube(40)
        glPopMatrix()
        
        if is_night:
            glPushMatrix()
            glTranslatef(decoy_x, decoy_y, 0)
            draw_light_pool(80, 0.4, 0.8, 1.0, 5) 
            glPopMatrix()

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

    if is_night and not power_box_hacked:
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
    
    # Yellow Light automatically turns off if power is cut
    if is_night and not power_box_hacked:
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
        if -350 < bx < 350: continue
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

    # Decorative frame over doorway
    glColor3f(0.3, 0.15, 0.05) 
    glPushMatrix()
    glTranslatef(0, 0, 400) 
    glScalef(10.0, 0.5, 8.0) 
    glutSolidCube(100)
    glPopMatrix()
    
    # Lockdown Bars
    if is_lockdown:
        glColor3f(0.05, 0.05, 0.05) 
        for bar_x in range(-450, 500, 100):
            glPushMatrix()
            glTranslatef(bar_x, 0, lockdown_z) 
            gluCylinder(gluNewQuadric(), 15, 15, 1500, 10, 10)
            glPopMatrix()

    # The Inner Wall Architecture (Left and Right sides of the door)
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

    # --- BUG FIX: POWER BOX MOVED TO THE FAR LEFT WALL IN FRONT ---
    glColor3f(*wall_col)
    glPushMatrix()
    glTranslatef(-3500, 6500, 400) # Pillar built against the left side
    glScalef(10.0, 15.0, 8.0) 
    glutSolidCube(100)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-2950, 6500, 400) # Wall-mounted box pops out slightly
    if power_box_hacked:
        glColor3f(0.2, 0.2, 0.2) 
    else:
        glColor3f(0.2, 0.4, 0.9) 
    glScalef(100, 150, 200) # Big industrial electrical box
    glutSolidCube(1)
    glPopMatrix()

    # The Single Wall-Attached Laser Door
    if entrance_lasers_active:
        glColor3f(*COLOR_LASER)
        for lx in range(-250, 300, 100): 
            glPushMatrix()
            glTranslatef(lx, 6000, 0) 
            gluCylinder(gluNewQuadric(), 15, 15, 1500, 10, 10)
            glPopMatrix()

    # Pressure Plates
    for p in pressure_plates:
        glPushMatrix()
        glTranslatef(p['x'], p['y'], 2)
        if p['active']:
            glColor3f(0.1, 0.8, 0.1)  # Green
        else:
            glColor3f(0.8, 0.1, 0.1)  # Red
        glBegin(GL_QUADS)
        glVertex3f(-100, -100, 0); glVertex3f(100, -100, 0)
        glVertex3f(100, 100, 0); glVertex3f(-100, 100, 0)
        glEnd()
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

    # --- FINAL TARGET ARTIFACT & CAGE ---
    glPushMatrix()
    glTranslatef(0, 7500, 0)
    
    # Artifact Pedestal
    glColor3f(0.6, 0.5, 0.1)
    glPushMatrix()
    glTranslatef(0, 0, 100)
    glScalef(2.0, 2.0, 2.0)
    glutSolidCube(100)
    glPopMatrix()
    
    # The Stolen Artifact (Scales down to 0 when stolen)
    if artifact_scale > 0:
        glColor3f(1.0, 0.8, 0.0) 
        glPushMatrix()
        glTranslatef(0, 0, 300)
        glRotatef(artifact_spin, 0, 0, 1)
        glRotatef(artifact_spin * 0.5, 0, 1, 0)
        glScalef(artifact_scale, artifact_scale, artifact_scale)
        gluSphere(gluNewQuadric(), 30, 10, 10)
        gluCylinder(gluNewQuadric(), 40, 40, 20, 10, 10)
        glPopMatrix()
    
    # Glass Box or Shards
    if not glass_shatter:
        glColor3f(0.3, 0.4, 0.5) 
        glPushMatrix()
        glTranslatef(0, 0, 500) 
        glScalef(2.1, 2.1, 0.1)
        glutSolidCube(100)
        glPopMatrix()
        for px, py in [(-100, -100), (100, -100), (-100, 100), (100, 100)]:
            glPushMatrix()
            glTranslatef(px, py, 300)
            glScalef(0.1, 0.1, 4.0) 
            glutSolidCube(100)
            glPopMatrix()
    else:
        glColor3f(0.8, 0.9, 1.0)
        for s in shards:
            glPushMatrix()
            glTranslatef(s['x'], s['y'], s['z'])
            glutSolidCube(12)
            glPopMatrix()
            
    # ALL-AROUND ARTIFACT LASER CAGE
    if not power_box_hacked:
        glColor3f(*COLOR_LASER)
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            lx = math.cos(rad) * 150
            ly = math.sin(rad) * 150
            glPushMatrix()
            glTranslatef(lx, ly, 0)
            gluCylinder(gluNewQuadric(), 8, 8, 800, 10, 10)
            glPopMatrix()
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
            
        if is_night and not power_box_hacked:
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
        else:
            return False

    return True

def keyboardListener(key, x, y):
    global is_night, camera_mode, is_crouching, is_torch_on, thief_x, thief_y, thief_angle, cam_fov
    global dash_timer, decoy_state, decoy_x, decoy_y, decoy_z, decoy_vx, decoy_vy, decoy_vz, decoy_timer
    global is_hacking, artifact_stolen, glass_shatter
    
    try:
        char = key.decode('utf-8').lower()
    except:
        char = ''

    if char == 'r':
        reset_game()
        glutPostRedisplay()
        return

    if is_lockdown or game_won: return

    if char == 't': is_night = not is_night
    elif char == 'v': camera_mode = "first_person" if camera_mode == "global" else "global"
    elif char == 'c': is_crouching = not is_crouching
    elif char == 'f': is_torch_on = not is_torch_on
        
    elif char == 'e':
        if dash_timer <= 0 and not is_crouching:
            dash_timer = 25 
            
    elif char == 'q':
        if decoy_state == 0:
            decoy_state = 1 
            decoy_x = thief_x + math.cos(math.radians(thief_angle)) * 50
            decoy_y = thief_y + math.sin(math.radians(thief_angle)) * 50
            decoy_z = 150.0 
            throw_speed = 150.0
            decoy_vx = math.cos(math.radians(thief_angle)) * throw_speed
            decoy_vy = math.sin(math.radians(thief_angle)) * throw_speed
            decoy_vz = 45.0 
            
    elif char == 'h':
        # Now checks proximity to the NEW far-left wall mounted box
        if math.hypot(thief_x - (-3000), thief_y - 6500) < 450 and not power_box_hacked:
            is_hacking = True
            
    elif char == 'p':
        if math.hypot(thief_x - 0, thief_y - 7500) < 350 and power_box_hacked and not artifact_stolen:
            artifact_stolen = True
            glass_shatter = True
        
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
    if key == GLUT_KEY_LEFT: cam_angle -= 3
    elif key == GLUT_KEY_RIGHT: cam_angle += 3
    elif key == GLUT_KEY_UP: cam_height += 300 
    elif key == GLUT_KEY_DOWN: cam_height -= 300
    glutPostRedisplay()

def idle():
    global artifact_spin, drones, cctv_time, is_lockdown, lockdown_z
    global dash_timer, thief_x, thief_y
    global decoy_state, decoy_x, decoy_y, decoy_z, decoy_vx, decoy_vy, decoy_vz, decoy_timer
    global is_hacking, hack_progress, power_box_hacked, entrance_lasers_active
    global artifact_scale, game_won
    
    artifact_spin += 1.5
    if artifact_spin > 360: artifact_spin -= 360

    if not is_lockdown and not game_won:
        if dash_timer > 0:
            dash_timer -= 1
            next_x = thief_x + math.cos(math.radians(thief_angle)) * 60
            next_y = thief_y + math.sin(math.radians(thief_angle)) * 60
            if is_valid_move(next_x, next_y):
                thief_x, thief_y = next_x, next_y
                
        # DECOY THROW PHYSICS
        if decoy_state == 1:
            decoy_x += decoy_vx
            decoy_y += decoy_vy
            decoy_z += decoy_vz
            decoy_vz -= 3.0 
            if decoy_z <= 20:
                decoy_z = 20
                decoy_state = 2 
                decoy_timer = 250 
        elif decoy_state == 2:
            decoy_timer -= 1
            if decoy_timer <= 0:
                decoy_state = 0 
                
        # --- PLATES DISABLE THE SINGLE WALL LASER DOOR ---
        all_plates_active = True
        for p in pressure_plates:
            if math.hypot(thief_x - p['x'], thief_y - p['y']) < 150:
                p['active'] = True
            if not p['active']:
                all_plates_active = False
        
        if all_plates_active:
            entrance_lasers_active = False
            
        # --- HACKING LOGIC ---
        if is_hacking:
            # Check proximity to the new left-wall power box
            if math.hypot(thief_x - (-3000), thief_y - 6500) > 450:
                is_hacking = False 
            else:
                hack_progress += 0.5
                if hack_progress >= 100:
                    power_box_hacked = True
                    is_hacking = False
                    
        if artifact_stolen and artifact_scale > 0:
            artifact_scale -= 0.04
            if artifact_scale <= 0:
                artifact_scale = 0
                game_won = True
                
        if glass_shatter:
            for s in shards:
                if s['z'] > 10:
                    s['x'] += s['vx']
                    s['y'] += s['vy']
                    s['z'] += s['vz']
                    s['vz'] -= 1.0

        if not power_box_hacked:
            cctv_time += 0.02
            for d in drones:
                if decoy_state == 2:
                    dx, dy = decoy_x - d['x'], decoy_y - d['y']
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

    # --- BUG FIX: POWER CUT DISABLES DRONES, LASERS *AND* ALL CCTVS ---
    if not is_lockdown:
        if not power_box_hacked:
            for d in drones:
                if math.hypot(thief_x - d['x'], thief_y - d['y']) < 400: is_lockdown = True
            
            # Artifact Cage Lasers
            if math.hypot(thief_x - 0, thief_y - 7500) < 160:
                is_lockdown = True

            # CCTV Cameras (Now safely shut off alongside power!)
            for px, py, phase in cctv_pillars:
                dx, dy = thief_x - px, thief_y - py
                if math.hypot(dx, dy) < 1200:
                    facing_angle = 90.0 + math.sin(cctv_time + phase) * 60.0
                    thief_angle_to_cctv = math.degrees(math.atan2(dy, dx))
                    diff = (thief_angle_to_cctv - facing_angle) % 360
                    if diff > 180: diff -= 360
                    if abs(diff) < 30: is_lockdown = True

            for wx, wy, wz, phase in cctv_walls:
                dx, dy = thief_x - wx, thief_y - wy
                if math.hypot(dx, dy) < 1000:
                    facing_angle = -90.0 + math.sin(cctv_time + phase) * 60.0
                    thief_angle_to_cctv = math.degrees(math.atan2(dy, dx))
                    diff = (thief_angle_to_cctv - facing_angle) % 360
                    if diff > 180: diff -= 360
                    if abs(diff) < 30: is_lockdown = True

        # Check the Single Wall Laser Door Collision (Stays active until plates are pressed)
        if entrance_lasers_active:
            if 5950 < thief_y < 6050 and -350 < thief_x < 350:
                is_lockdown = True

    if is_lockdown and lockdown_z > 0:
        lockdown_z -= 60.0
        if lockdown_z < 0: lockdown_z = 0
                
    glutPostRedisplay()

def showScreen():
    if is_lockdown:
        siren_blink = math.sin(cctv_time * 15.0)
        if siren_blink > 0: glClearColor(1.0, 0.0, 0.0, 1.0) 
        else: glClearColor(0.3, 0.0, 0.0, 1.0) 
    else:
        glClearColor(0, 0, 0, 1) 
        
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)

    setupCamera()

    draw_super_massive_floor_and_road()
    draw_outer_field_objects()
    draw_museum_architecture()
    draw_interior_artifacts()
    
    draw_decoy() 
    draw_security_drones() 
    draw_thief()

    glDisable(GL_DEPTH_TEST) 

    # --- BASE HUD ---
    mode = "LOCKDOWN!" if is_lockdown else ("POWER CUT!" if power_box_hacked else "NIGHT" if is_night else "DAY")
    posture = "CROUCH" if is_crouching else "STAND"
    torch = "ON" if is_torch_on else "OFF"
    dash_text = "DASHING!" if dash_timer > 0 else "READY"
    if decoy_state == 1: decoy_text = "FLYING..."
    elif decoy_state == 2: decoy_text = f"ACTIVE ({decoy_timer})"
    else: decoy_text = "READY"
    
    draw_text(10, 720, f"THE ART THIEF'S LASER VAULT | MODE: {mode} | CAM: {camera_mode.upper()}")
    draw_text(10, 700, f"POSTURE: {posture} ('C') | TORCH: {torch} ('F') | DASH: {dash_text} | DECOY: {decoy_text}")
    draw_text(10, 680, "CONTROLS -> W/A/S/D: Sneak | E: DASH | Q: DECOY | Z/X: ZOOM | R: RESTART | ARROWS: Global Cam")

    # --- DYNAMIC PROMPTS ---
    if is_lockdown:
        draw_text(380, 400, "GAME OVER - PRESS 'R' TO RESTART", font=GLUT_BITMAP_TIMES_ROMAN_24)
        
    if game_won:
        draw_text(280, 400, "YOU WIN! THE ARTIFACT IS SECURED!", font=GLUT_BITMAP_TIMES_ROMAN_24)
    elif is_hacking:
        draw_text(400, 400, f"HACKING MAINFRAME: {int(hack_progress)}%", font=GLUT_BITMAP_TIMES_ROMAN_24)
    elif math.hypot(thief_x - (-3000), thief_y - 6500) < 450 and not power_box_hacked:
        draw_text(350, 400, "PRESS AND HOLD 'H' TO HACK POWER BOX", font=GLUT_BITMAP_TIMES_ROMAN_24)
        
    if math.hypot(thief_x - 0, thief_y - 7500) < 350 and power_box_hacked and not artifact_stolen:
        draw_text(350, 400, "PRESS 'P' TO STEAL THE ARTIFACT", font=GLUT_BITMAP_TIMES_ROMAN_24)
        
    glEnable(GL_DEPTH_TEST) 
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH) 
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b" The Art Thief's Laser Vault (3D Stealth Simulator)")
    
    glEnable(GL_DEPTH_TEST)
    
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutIdleFunc(idle)
    
    glutMainLoop()

if __name__ == "__main__":
    main()