<div align="center">

# ⚔️ DUNGEON QUEST: THE LOST RELICS 💎

**An Action-Packed 2D Retro Roguelike Dungeon Crawler Engine**

[![Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Engine](https://img.shields.io/badge/Engine-Pygame%20Zero-FF4B4B?style=for-the-badge&logo=game-and-watch&logoColor=white)](https://pygame-zero.readthedocs.io/)
[![Architecture](https://img.shields.io/badge/Architecture-Object--Oriented%20(OOP)-4CAF50?style=for-the-badge)](https://en.wikipedia.org/wiki/Object-oriented_programming)
[![Style Guide](https://img.shields.io/badge/Code%20Style-PEP%208-blue?style=for-the-badge)](https://www.python.org/dev/peps/pep-0008/)
[![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](LICENSE)

<br/>

> **"Delve into the shadowy depths, outsmart ancient sentinels, collect the three mystic crystals, and unlock the celestial gateway to victory."**

<br/>

[Key Features](#-key-features) •
[Tech Stack](#-tech-stack) •
[Quick Start](#-quick-start) •
[Controls](#-controls) •
[Game Architecture](#-architecture--oop-design) •
[Entity Specifications](#-entities--ai-mechanics)

</div>

---

## 📖 Overview

**Dungeon Quest: The Lost Relics** is a fast-paced, grid-aligned 2D Roguelike built with **Pygame Zero**. Designed with clean object-oriented architecture, the game incorporates state-machine orchestration, responsive continuous animation cycles, area-bounded AI navigation, and retro arcade audio feedback.

---

## ✨ Key Features

* **🏰 Procedural-Feel Dungeon Layout:** Navigate interconnected chambers, protected corridors, and alcoves separated by solid stone masonry.
* **🌀 Multi-Frame Sprite Animation Engine:** Full 4-frame cyclical animations for idle (breathing, eye blinking, jaw clacking, spectral hovering) and movement (leg strides, arm swings, floating swoops).
* **🧠 Zone-Bound Adaptive AI:** Monsters patrol their designated territories with precision and dynamically initiate pursuit when the hero crosses their perimeter.
* **🎵 Immersive Dynamic Audio:** Looping 8-bit chiptune background score paired with synchronized sound effects for coin pickups, impact hurt, defeat, victory fanfare, and tactile UI clicks.
* **⚡ Production-Grade HUD & Menus:** Interactive main menu with real-time audio toggle, live health hearts display, crystal recovery tracker, and seamless zero-leak restart flow.
* **🛡️ Collision & Damage Grace Period:** Smooth sliding collisions along dungeon walls with invulnerability flicker frames preventing instant defeat spikes.

---

## 🛠️ Tech Stack

```
┌─────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                      │
│            Game State Machine • Menu System • HUD           │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                       ENTITIES LAYER                        │
│   Hero (Input/Physics) • Skeleton (Patrol) • Specter (Sine)  │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                     CORE ENGINE ENGINE                      │
│        Pygame Zero (pgzero) • Actor Base • Game Loop        │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                    UNDERLYING PLATFORM                      │
│          Python 3.10+ • SDL2 Backend • Pygame Mixer         │
└─────────────────────────────────────────────────────────────┘
```

| Technology | Role | Description |
|:---|:---|:---|
| 🐍 **Python 3.8 - 3.12** | Core Runtime | High-level language powering the core game loop and logic. |
| 🎮 **Pygame Zero (`pgzero`)** | Game Framework | Event dispatching, screen drawing, sprite handling, and sound playback. |
| 📐 **Pygame `Rect`** | Collision Math | AABB collision detection, containment tests, and hitbox geometry. |
| 🧮 **Standard `math` & `random`** | Trigonometry & AI | Distance calculations, trigonometric floating flight paths, and angle steps. |

---

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have **Python 3.8+** installed:
```bash
python3 --version
```

### 2. Clone the Repository
```bash
git clone https://github.com/HarnishSavsani/Dungeon-Quest.git
cd Dungeon-Quest
```

### 3. Install Dependencies
Install Pygame Zero and its underlying runner:
```bash
pip install pgzero pygame
```

### 4. Launch the Game
You can launch the game using either standard Pygame Zero runner or direct Python execution:

```bash
# Method A: Using Pygame Zero CLI Runner (Recommended)
pgzrun main.py

# Method B: Direct Python Execution
python3 main.py
```

---

## 🕹️ Controls

| Input | Action | Notes |
|:---:|:---|:---|
| <kbd>W</kbd> / <kbd>▲</kbd> | Move Up | Smooth multi-directional movement |
| <kbd>S</kbd> / <kbd>▼</kbd> | Move Down | Diagonals normalized (`0.7071`) |
| <kbd>A</kbd> / <kbd>◀</kbd> | Move Left | Wall collision sliding response |
| <kbd>D</kbd> / <kbd>▶</kbd> | Move Right | Automatic sprite walk cycling |
| 🖱️ **Left Click** | Interact | Click UI buttons (Start, Sound Toggle, Exit, Replay) |

---

## 👾 Entities & AI Mechanics

### 1. 🛡️ The Hero
* **Health:** 3 Hearts (Max HP = 3).
* **Movement:** Normalized vector displacement with wall sliding physics.
* **Invulnerability:** 1.2-second post-damage grace period with visual alpha flickering.
* **Animation:**
  * **Idle:** `hero_idle_0` → `hero_idle_3` (4 frames: breathing, posture settling, eye blink).
  * **Walk:** `hero_walk_0` → `hero_walk_3` (4 frames: leg strides, arm counter-swings).

### 2. 💀 Skeleton Knight (Corridor Sentinel)
* **Domain:** Western Hallway (`Rect(110, 140, 270, 160)`).
* **Behavior:** Patrols horizontally across its corridor. If the hero enters its territory, it engages pursuit. Clamped strictly to its zone.
* **Animation:**
  * **Idle:** `skeleton_idle_0` → `skeleton_idle_3` (4 frames: ribcage shifts, jaw clacking, eye socket glow).
  * **Walk:** `skeleton_walk_0` → `skeleton_walk_3` (4 frames: bony leg strides, weapon sway).

### 3. 👻 Dungeon Specter (Ethereal Phantom)
* **Domain:** Eastern Chamber (`Rect(416, 130, 330, 170)`).
* **Behavior:** Floats in a continuous sinusoidal flight trajectory using trigonometric mathematics:
  $$\Delta x = \cos(\theta) \times 70, \quad \Delta y = \sin(2\theta) \times 45$$
  Initiates ethereal pursuit upon hero intrusion; clamped strictly within its chamber.
* **Animation:**
  * **Idle:** `ghost_idle_0` → `ghost_idle_3` (4 frames: hovering bob, waving wispy tail).
  * **Move:** `ghost_move_0` → `ghost_move_3` (4 frames: swooping shroud, trailing spectral aura).

---

## 🏗️ Architecture & OOP Design

The codebase strictly adheres to object-oriented programming principles:

```python
Actor (Pygame Zero Builtin)
 └── AnimatedCharacter
      ├── Hero             # Controls player input, damage states, wall collisions
      └── Enemy            # Base enemy class enforcing zone clamp constraints
           ├── SkeletonEnemy   # Linear patrol & corridor engagement
           └── SpecterEnemy    # Sinusoidal trajectory & ethereal pursuit

MenuButton                 # Standalone reusable UI component for menus & modals
```

---

## 📂 Project Structure

```text
Dungeon-Quest/
├── images/                 # Pixel-art visual assets (PNG format, lowercase)
│   ├── hero_idle_*.png     # Hero idle cycle (4 frames)
│   ├── hero_walk_*.png     # Hero walk cycle (4 frames)
│   ├── skeleton_idle_*.png # Skeleton idle cycle (4 frames)
│   ├── skeleton_walk_*.png # Skeleton walk cycle (4 frames)
│   ├── ghost_idle_*.png    # Specter idle cycle (4 frames)
│   ├── ghost_move_*.png    # Specter move cycle (4 frames)
│   ├── portal_*.png        # Rotating vortex exit portal (4 frames)
│   ├── crystal.png         # Collectible mystical relics
│   ├── heart_full.png      # Active health container
│   ├── heart_empty.png     # Depleted health container
│   ├── tile_floor.png      # Dungeon cobblestone texture
│   └── tile_wall.png       # Masonry boundary block
├── sounds/                 # 16-bit PCM WAV audio effects (Mixkit.co)
│   ├── click.wav           # Responsive UI tactile button feedback
│   ├── gem.wav             # Sparkling crystal recovery chime
│   ├── hit.wav             # Heavy impact damage crunch
│   ├── win.wav             # Triumphant victory fanfare
│   └── gameover.wav        # Descending minor defeat jingle
├── music/                  # Background soundtracks
│   └── theme.mp3           # Looping retro chiptune dungeon theme
├── main.py                 # Core game engine, entities, loop & state handlers
├── readme.txt              # Standardized plain text specification document
├── .gitignore              # Production-grade Git ignore filter
└── README.md               # GitHub presentation & documentation
```

---

## 🏆 Game Rules & Objectives

1. **Infiltrate:** Enter the dungeon from the safe entrance hall.
2. **Recover:** Collect all **3 ancient mystical crystals** guarded by the sentinels.
3. **Survive:** Avoid contact with patrolling monsters. Collisions deduct 1 heart from your health pool.
4. **Escape:** Recovering all 3 crystals activates the dimensional exit portal. Step into the swirling vortex to achieve **VICTORY**!

---

<div align="center">

Made with ❤️ by [Harnish Savsani](https://github.com/HarnishSavsani)

*Crafted with Python, Pygame Zero, and Passion for Retro Game Development.*

</div>
