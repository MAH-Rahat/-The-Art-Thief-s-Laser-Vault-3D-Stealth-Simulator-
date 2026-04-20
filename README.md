<div align="center">

# 🏛️ The Art Thief's Laser Vault (3D Stealth Simulator)

*A coordinate-driven stealth and puzzle engine where players evade dynamic security systems and manipulate kinematic physics to breach a high-security vault.*

</div>

## 📜 Project Overview
Welcome to the ultimate heist. This 3D stealth and puzzle simulator drops players into a high-security museum room to steal a heavily guarded artifact. The environment is highly dynamic, requiring the player to dodge moving security systems, utilize movement mechanics, and interact with the environment to open the vault. 

Built entirely from scratch, this engine relies exclusively on fundamental 3D transformations (`glTranslate`, `glRotate`, `glScale`), primitive geometric shapes, and coordinate-based collision logic without relying on advanced external physics libraries.

---

## 🎮 Controls

| Key | Action |
| :--- | :--- |
| **W / S** | Sneak Forward / Backward |
| **A / D** | Rotate Player View |
| **E** | Execute Quick-Dash |
| **Q** | Throw Hologram Decoy (Kinematic Physics) |
| **C** | Toggle Crouch / Stand |
| **F** | Toggle Flashlight |
| **T** | Toggle Day / Night Mode |
| **V** | Switch Camera (First-Person / Global) |
| **Z / X** | Zoom In / Zoom Out |
| **R** | Restart / Reset Game |
| **Arrow Keys** | Move Global Camera |

---

## ✨ Key Features & Mechanics

### 🚨 Dynamic Security Systems & Hazards
* **🔪 Sweeping Laser Grids:** Navigate past highly lethal, thin red laser cylinders that continuously sweep back and forth across the facility hallways.
* **🚁 The Patrol Drone:** Evade floating, geometric security drones that endlessly patrol the room in predetermined square paths, hunting for intruders.
* **⛓️ The Lockdown Sequence:** Precision is everything. If a laser or drone detects your coordinates, the room flashes blood-red and heavy iron bars slam down from the ceiling to permanently block the exits.

### 🥷 Player Stealth Mechanics
* **🚷 Crouch Compression:** Instantly compress the player's hitbox by 50% on the Y-axis using `glScalef` to silently slip underneath sweeping laser grids without tripping the alarms.
* **⚡ Kinematic Quick-Dash:** Execute a rapid forward translation to blast past fast-moving drones, complete with a dynamic Z-axis elongation for a slick "speed blur" effect.
* **🧊 Hologram Decoy Physics:** Press 'Q' to throw a glowing decoy cube. The throw utilizes real parabolic kinematics (velocity and gravity). Once the stone hits the floor, patrol drones break their path to investigate the impact zone.

### 🧩 Puzzles & The Loot
* **🟩 Pressure Plate Vault Door:** Locate and trigger specific floor squares to turn them green; activating the full sequence physically slides the massive vault door open along the Z-axis.
* **🔌 System Overrides:** Hack blue wall-mounted power boxes to plunge the room into darkness and temporarily freeze all drone and laser coordinate translations.
* **💎 Artifact Retrieval:** Grab the continuously rotating target artifact to trigger a dynamic sequence where the loot shrinks away and its protective glass case dramatically shatters into falling geometric shards.

---
