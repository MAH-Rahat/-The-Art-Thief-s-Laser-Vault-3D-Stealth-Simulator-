# Extended DAY and NIGHT color palette
DAY_BUSH = (0.25, 0.6, 0.25)              # Bush foliage color during daytime
NIGHT_BUSH = (0.03, 0.10, 0.03)           # Bush foliage color during nighttime

# Vault structure colors for better visual hierarchy
DAY_WALL = (0.75, 0.75, 0.8)              # Light gray vault walls (day)
NIGHT_WALL = (0.15, 0.15, 0.2)            # Dark blue vault walls (night)

DAY_FLOOR_A = (0.8, 0.8, 0.85)            # First floor tile color (day)
DAY_FLOOR_B = (0.75, 0.75, 0.8)           # Alternate floor tile (day)
NIGHT_FLOOR_A = (0.1, 0.1, 0.15)          # First floor tile color (night)
NIGHT_FLOOR_B = (0.09, 0.09, 0.14)        # Alternate floor tile (night)

DAY_PILLAR = (0.6, 0.6, 0.65)             # Pillar color (day)
NIGHT_PILLAR = (0.2, 0.2, 0.25)           # Pillar color (night)

# Puzzle system special effect colors
# Pressure Plate & Vault Door visual
VAULT_DOOR = (0.3, 0.35, 0.4)             # Heavy blue-gray vault door
#- System Overrides: Laser threat visual
COLOR_LASER = (1.0, 0.0, 0.2)             # Red laser beam color
#- System Overrides: Power box beam color
OVERRIDE_BEAM = (0.2, 0.8, 1.0)           # Cyan beam for override boxes
# Artifact Retrieval: Artifact highlight beam
ARTIFACT_BEAM = (1.0, 0.86, 0.25)         # Gold beam for artifact
# --- PLAYER MOVEMENT CONSTANTS ---
WORLD_STEP = 100.0              # Distance player moves per W/S key press
DASH_DISTANCE = 280.0           # Distance covered during dash ability
DASH_DURATION = 8.0 / 60.0      # Dash animation duration in seconds (8 frames at 60 FPS)

# --- DECOY MECHANICS CONSTANTS ---
DECOY_LANDED_DURATION = 5.0     # Time decoy stays on ground before disappearing (5 seconds)

# --- VAULT PUZZLE CONSTANTS ---
# Pressure Plate Vault Door System
PLATE_HALF_SIZE = 120.0         # Half-width of pressure plate tiles
PLATE_TRIGGER_RADIUS = 240.0    # Radius at which player triggers pressure plates
# System Override & Artifact Retrieval Systems
OVERRIDE_DURATION = 6.0         # How long override effects last when hacking a box
SHATTER_DURATION = 3.0          # How long artifact shattering animation plays

# --- VAULT ROOM BOUNDARY CONSTANTS ---
# These define the exact dimensions of the vault chamber for collision detection
ROOM_LEFT = -1780.0             # Left wall of vault room
ROOM_RIGHT = 1780.0             # Right wall of vault room
ROOM_BACK = -3060.0             # Back wall of vault room
ROOM_FRONT = -820.0             # Front exterior wall of vault room
ROOM_INNER_FRONT = -900.0       # Inner front boundary of vault room
ROOM_DOOR_LEFT = -540.0         # Left edge of doorway
ROOM_DOOR_RIGHT = 540.0         # Right edge of doorway
ROOM_DOOR_OUTER_Y = -700.0      # Outer Y boundary of doorway

# ================== NEW PLAYER STATE VARIABLES ======================================
is_crouching = False            # Whether player is in crouch mode (reduces height, sound)
dash_timer = 0                  # Countdown timer for dash animation effect
is_torch_on = False             # Whether player has turned on a light torch

# =============== NEW PUZZLE & LOOT SYSTEM STATE VARIABLES ===========================

# --- PRESSURE PLATE VAULT PUZZLE STATE ---
# Pressure Plate Vault Door: Sequential floor tiles must be triggered in order
vault_plate_positions = [
    (-1500.0, -4500.0),    # Plate 0 position
    (1100.0, -4250.0),     # Plate 1 position
    (-650.0, -3600.0),     # Plate 2 position
    (1450.0, -3350.0),     # Plate 3 position
]
# Pressure Plate State Tracking
vault_plate_active = [False, False, False, False]
# Pressure Plate Progress Tracking
vault_plate_progress = 0
# Animated Vault Door (slides upward on Z-axis when plates complete)
vault_door_z = 0.0
# --- SYSTEM OVERRIDE HACK STATE ---
#System Overrides: Hack blue power boxes to freeze security and darken room
override_box_positions = [
    (-3200.0, -2400.0, 180.0),     # Left override box
    (3200.0, -2400.0, 180.0),      # Right override box
]
override_box_used = [False, False]
# Override Active Flag (controls darkness and security freeze)
override_active = False
# Override Timer (6 second freeze duration)
override_timer = 0
security_freeze_timer = 0
# --- ARTIFACT RETRIEVAL STATE ---
#Artifact Retrieval: Rotating loot that shrinks and shatters when stolen
artifact_x = 0.0                # X-coordinate of artifact in vault
artifact_y = -2600.0            # Y-coordinate of artifact in vault
artifact_z = 320.0              # Z-coordinate (height) of artifact

# Artifact Shrink Animation (visual feedback when stolen)
artifact_scale = 1.0
# Artifact Collected Flag (starts shrinking and shattering)
artifact_collected = False
# Shattering Animation Timer (3 second duration)
artifact_shatter_timer = 0
# Artifact Shattering Physics (26 glass shards fall with gravity/damping)
artifact_shards = []
# Interaction System (for override boxes and artifact)
interaction_radius = 900.0


#Security Drones (freeze when override is active)
security_drones = [
    {
        'x': -1800.0, 'y': -3300.0, 'z': 320.0,     # Position
        'vx': 8.0, 'vy': 0.0,                        # Velocity components
        'axis': 'x',                                  # Primary movement axis
        'min_x': -3000.0, 'max_x': -600.0,          # X-axis bounds
        'min_y': -3300.0, 'max_y': -3300.0,         # Y-axis bounds
    },
    {
        'x': 1800.0, 'y': -3000.0, 'z': 360.0,      # Position
        'vx': 0.0, 'vy': 7.0,                        # Velocity components
        'axis': 'y',                                  # Primary movement axis
        'min_x': 1800.0, 'max_x': 1800.0,           # X-axis bounds
        'min_y': -3600.0, 'max_y': -2200.0,         # Y-axis bounds
    },
]

#  Laser Sweeps (freeze when override is active)
laser_sweeps = [
    {
        'x': -900.0, 'y': -2900.0,                   # Position
        'span': 1500.0,                              # Length of laser sweep
        'speed': 45.0,                               # Speed moving across room
        'min_x': -1600.0, 'max_x': -200.0,          # Movement bounds
    },
    {
        'x': 900.0, 'y': -2900.0,                    # Position
        'span': 1500.0,                              # Length of laser sweep
        'speed': -50.0,                              # Speed (negative = opposite direction)
        'min_x': 200.0, 'max_x': 1600.0,            # Movement bounds
    },
]

# Pressure Plate Vault Door: Collision helper for puzzle placement
def is_plate_area_clear(x, y):
    for plate_x, plate_y in vault_plate_positions:
        if math.hypot(x - plate_x, y - plate_y) < 650.0:
            return False
    return True


def generate_bush_positions():
    positions = []
    while len(positions) < 50:
        bush_x = random.uniform(-8000, 8000)
        bush_y = random.uniform(-8500, -100)
        if is_plate_area_clear(bush_x, bush_y):
            positions.append((bush_x, bush_y))
    return positions


def get_forward_vector():
    angle_rad = math.radians(thief_angle)
    return math.sin(angle_rad), math.cos(angle_rad)


def move_thief(distance):
    global thief_x, thief_y
    fx, fy = get_forward_vector()
    next_x = thief_x + fx * distance
    next_y = thief_y + fy * distance
    if can_move_to(thief_x, thief_y, next_x, next_y):
        thief_x = next_x
        thief_y = next_y

def is_inside_vault_room(x, y):
    return ROOM_LEFT <= x <= ROOM_RIGHT and ROOM_BACK <= y <= ROOM_INNER_FRONT


def is_in_room_shell(x, y):

    return ROOM_LEFT <= x <= ROOM_RIGHT and ROOM_BACK <= y <= ROOM_FRONT


def is_in_room_doorway(x, y):
    return ROOM_DOOR_LEFT <= x <= ROOM_DOOR_RIGHT and ROOM_INNER_FRONT <= y <= ROOM_DOOR_OUTER_Y

def can_cross_room_door(old_x, old_y, new_x, new_y):
    if not is_vault_unlocked():
        return False
    if not (ROOM_DOOR_LEFT <= old_x <= ROOM_DOOR_RIGHT and ROOM_DOOR_LEFT <= new_x <= ROOM_DOOR_RIGHT):
        return False
    crossed_into_room = old_y > ROOM_INNER_FRONT and new_y <= ROOM_INNER_FRONT
    crossed_out_of_room = old_y <= ROOM_INNER_FRONT and new_y > ROOM_INNER_FRONT
    return crossed_into_room or crossed_out_of_room
def can_move_to(old_x, old_y, new_x, new_y):
    old_inside = is_inside_vault_room(old_x, old_y)
    new_inside = is_inside_vault_room(new_x, new_y)

    if old_inside != new_inside:
        return can_cross_room_door(old_x, old_y, new_x, new_y)

    if is_in_room_shell(new_x, new_y) and not new_inside and not is_in_room_doorway(new_x, new_y):
        return False

    return True
#System Overrides & Artifact Retrieval: Glowing beam indicators
def draw_vertical_beam(radius, height, color):

    glColor4f(color[0], color[1], color[2], 0.3)
    quadric = gluNewQuadric()
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)
    gluCylinder(quadric, radius, radius * 0.45, height, 18, 1)
    glPopMatrix()


#- System Overrides & Artifact Retrieval: Interactive element markers
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


#  Pressure Plate Vault Door: Progress tracking for HUD display
def get_plate_count():

    return sum(1 for is_active in vault_plate_active if is_active)


#Pressure Plate Vault Door: Checks if all 4 plates are triggered
def is_vault_unlocked():

    return vault_plate_progress >= len(vault_plate_positions)


# Pressure Plate Vault Door: Renders color-coded floor tiles (Red/Gold/Green)
def draw_pressure_plate_tile(plate_x, plate_y, is_active, is_current_target):
    if is_active:
        outer_color = (0.18, 0.72, 0.28)
        inner_color = (0.28, 0.95, 0.38)
    elif is_current_target:
        outer_color = (0.7, 0.58, 0.16)
        inner_color = (0.96, 0.82, 0.24)
    else:
        outer_color = (0.4, 0.18, 0.18)
        inner_color = (0.58, 0.26, 0.26)

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


# System Overrides: Animated ring pulses around power boxes
def draw_wire_ring(radius, color, segments=28):

    glColor3f(*color)
    glBegin(GL_LINE_LOOP)
    for i in range(segments):
        angle = math.tau * i / segments
        glVertex3f(math.cos(angle) * radius, math.sin(angle) * radius, 0)
    glEnd()
# System Overrides: Visual pulse animation for power boxes
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

def draw_vault_features():

    # Room colors change based on override state
    room_dark = (0.03, 0.03, 0.04) if override_active else (0.12, 0.13, 0.16)
    room_mid = (0.08, 0.09, 0.12) if override_active else (0.18, 0.2, 0.24)
    trim = (0.18, 0.2, 0.24) if override_active else (0.3, 0.32, 0.36)

    # Main vault chamber
    glPushMatrix()
    glTranslatef(0, -1900, 760)
    glScalef(3600, 2200, 1520)
    glColor3f(*room_dark)
    glutWireCube(1)
    glPopMatrix()

    # Side walls
    for wall_x in (-1700, 1700):
        glPushMatrix()
        glTranslatef(wall_x, -1900, 760)
        glScalef(160, 2200, 1520)
        glColor3f(*room_mid)
        glutSolidCube(1)
        glPopMatrix()

    # Back wall
    glPushMatrix()
    glTranslatef(0, -2980, 760)
    glScalef(3560, 160, 1520)
    glColor3f(*room_mid)
    glutSolidCube(1)
    glPopMatrix()

    # Ceiling
    glPushMatrix()
    glTranslatef(0, -1900, 1520)
    glScalef(3560, 2200, 120)
    glColor3f(*room_mid)
    glutSolidCube(1)
    glPopMatrix()

    # Front walls (left and right of doorway)
    for front_x in (-1180, 1180):
        glPushMatrix()
        glTranslatef(front_x, -820, 760)
        glScalef(1200, 160, 1520)
        glColor3f(*room_mid)
        glutSolidCube(1)
        glPopMatrix()

    # Door frame trim
    glPushMatrix()
    glTranslatef(0, -820, 1340)
    glScalef(1160, 160, 360)
    glColor3f(*trim)
    glutSolidCube(1)
    glPopMatrix()

    # Pressure Plate Vault Door: Checkered floor pattern in vault
    glBegin(GL_QUADS)
    for x in range(-1800, 1800, 600):
        for y in range(-4200, -2400, 600):
            if ((x // 600) + (y // 600)) % 2 == 0:
                if override_active:
                    glColor3f(0.06, 0.06, 0.08)
                else:
                    glColor3f(0.16, 0.18, 0.24)
            else:
                if override_active:
                    glColor3f(0.05, 0.05, 0.07)
                else:
                    glColor3f(0.12, 0.14, 0.2)
            glVertex3f(x, y, 4)
            glVertex3f(x + 600, y, 4)
            glVertex3f(x + 600, y + 600, 4)
            glVertex3f(x, y + 600, 4)
    glEnd()

    # Pressure Plate Vault Door: Render all 4 plates with state-based colors
    for index, (plate_x, plate_y) in enumerate(vault_plate_positions):
        draw_pressure_plate_tile(
            plate_x,
            plate_y,
            vault_plate_active[index],
            index == vault_plate_progress,
        )

    # Steps leading to vault
    for step_index in range(4):
        glPushMatrix()
        glTranslatef(0, -650 + step_index * 180, 40 + step_index * 5)
        glScalef(700 + step_index * 120, 120, 40)
        glColor3f(0.35, 0.35, 0.4)
        glutSolidCube(1)
        glPopMatrix()

    #Pressure Plate Vault Door: Animates upward on Z-axis when puzzle complete
    glPushMatrix()
    glTranslatef(0, -820, vault_door_z + 650)
    glScalef(1080, 120, 1280)
    glColor3f(*VAULT_DOOR)
    glutSolidCube(1)
    glPopMatrix()

    # Door frame outline
    glPushMatrix()
    glTranslatef(0, -760, 650)
    glScalef(1160, 40, 1320)
    glColor3f(*trim)
    glutWireCube(1)
    glPopMatrix()

    #System Overrides: Blue wall-mounted power boxes with pulsing effects
    for index, (box_x, box_y, box_z) in enumerate(override_box_positions):
        # Box main body
        glPushMatrix()
        glTranslatef(box_x, box_y, box_z)
        if override_box_used[index]:
            glColor3f(0.12, 0.82, 1.0)
        else:
            glColor3f(0.2, 0.35, 1.0)
        glutSolidCube(110)

        # Box base
        glColor3f(0.08, 0.14, 0.3)
        glPushMatrix()
        glTranslatef(0, -62, 0)
        glScalef(82, 12, 82)
        glutSolidCube(1)
        glPopMatrix()

        # Box display
        glColor3f(0.85, 0.9, 1.0)
        glTranslatef(0, 0, 70)
        glutSolidCube(30)
        glPushMatrix()
        glTranslatef(0, -58, 12)
        glColor3f(0.55, 0.9, 1.0 if override_box_used[index] else 0.8)
        glScalef(60, 8, 45)
        glutSolidCube(1)
        glPopMatrix()

        # Vertical beam from box
        glTranslatef(0, 0, 120)
        if override_box_used[index]:
            draw_light_pool(70, 0.2, 0.95, 1.0, 2)
            glColor3f(0.2, 0.9, 1.0)
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

        # Pulse animation around box
        draw_override_pulse(box_x, box_y, box_z + 18, override_box_used[index])
        if not override_box_used[index]:
            draw_rotating_triangle_marker(box_x, box_y, box_z + 430, (0.35, 0.8, 1.0), 120.0, -3.2)
        elif override_active:
            draw_rotating_triangle_marker(box_x, box_y, box_z + 500, (0.2, 1.0, 1.0), 145.0, 5.0)

    # System Overrides: Security drones freeze when override is active
    for drone in security_drones:
        glPushMatrix()
        glTranslatef(drone['x'], drone['y'], drone['z'])
        glRotatef(artifact_spin * 2.0, 0, 0, 1)
        if override_active:
            glColor3f(0.12, 0.22, 0.28)
        else:
            glColor3f(0.25, 0.75, 1.0)
        glutSolidCube(90)
        glColor3f(0.05, 0.2, 0.3 if not override_active else 0.18)
        glTranslatef(0, 0, -40)
        glutSolidCube(40)
        glPopMatrix()

    # System Overrides: Laser barriers freeze when override is active
    for laser in laser_sweeps:
        glPushMatrix()
        glTranslatef(laser['x'], laser['y'], 160)
        if override_active:
            glColor3f(0.22, 0.08, 0.12)
        else:
            glColor3f(*COLOR_LASER)
        glScalef(22, laser['span'], 16)
        glutSolidCube(1)
        glPopMatrix()

    # Artifact Retrieval: Rotating artifact in protective case
    if not artifact_collected or artifact_scale > 0.01:
        # Artifact Retrieval: Protective glass case base
        glPushMatrix()
        glTranslatef(artifact_x, artifact_y, 80)
        glScalef(360, 360, 160)
        glColor3f(0.28, 0.28, 0.32)
        glutSolidCube(1)
        glPopMatrix()

        #Artifact Retrieval: Wireframe case visualization
        glPushMatrix()
        glPushMatrix()
        glTranslatef(artifact_x, artifact_y, 250)
        glColor4f(0.75, 0.88, 0.96, 0.25)
        glScalef(260, 260, 320)
        glutWireCube(1)
        glPopMatrix()

        # Artifact Retrieval: Continuously rotating gold artifact shrinks when stolen
        glPushMatrix()
        glTranslatef(artifact_x, artifact_y, artifact_z)
        glRotatef(artifact_spin * 6.0, 0, 0, 1)
        glRotatef(artifact_spin * 2.0, 1, 0, 0)
        glScalef(max(artifact_scale, 0.05), max(artifact_scale, 0.05), max(artifact_scale, 0.05))
        glColor3f(0.95, 0.82, 0.22)
        glutSolidCube(150)
        glColor3f(0.9, 0.95, 1.0)
        glutWireCube(230)
        glPushMatrix()
        glTranslatef(0, 0, -140)
        draw_light_pool(120, 1.0, 0.95, 0.3, 2)
        glPopMatrix()
        glPopMatrix()

        #Artifact Retrieval: Golden beam highlights artifact location
        glPushMatrix()
        glTranslatef(artifact_x, artifact_y, 90)
        draw_vertical_beam(22, 360, ARTIFACT_BEAM)
        glPopMatrix()
        draw_rotating_triangle_marker(artifact_x, artifact_y, 520, (1.0, 0.86, 0.25), 130.0, 4.0)

    #Artifact Retrieval: 26 glass shards fall with gravity and air resistance
    for shard in artifact_shards:
        glPushMatrix()
        glTranslatef(shard['x'], shard['y'], shard['z'])
        glRotatef(shard['spin'], 1, 1, 0)
        glColor3f(0.7, 0.85, 0.95)
        glScalef(shard['sx'], shard['sy'], shard['sz'])
        glutSolidCube(1)
        glPopMatrix()
