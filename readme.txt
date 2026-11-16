========================================================================
                     DUNGEON QUEST: THE LOST RELICS
               A Pygame Zero Roguelike Adventure Game
========================================================================

1. ABOUT THE PROJECT
--------------------
"Dungeon Quest: The Lost Relics" is an original top-down Roguelike dungeon
crawler game built using Pygame Zero (pgzero). The player guides a hero
through a dangerous dungeon, avoiding patrolling monsters to recover three
ancient crystals and reach the mystical escape portal.


2. LIBRARIES USED
-----------------
In strict compliance with the project specifications, ONLY the following
libraries and modules are used:

  * pgzero / pgzrun  - Pygame Zero game framework and engine
  * pygame.Rect      - Exceptionally allowed Rect class from Pygame
  * math             - Python Standard Library (trigonometry and distance)
  * random           - Python Standard Library

No other external or disallowed libraries are used.


3. SYSTEM REQUIREMENTS & INSTALLATION
-------------------------------------
* Python 3.8 to 3.12 (Python 3.10 recommended)
* Pygame Zero and Pygame:

  To install the required dependencies, run:
      pip install pgzero pygame


4. HOW TO RUN THE PROJECT
-------------------------
Navigate to the project root directory in your terminal:

    cd /path/to/game

You can run the project using either of the following commands:

    Method A (Pygame Zero Runner):
        pgzrun main.py

    Method B (Direct Python execution):
        python3 main.py


5. GAME CONTROLS
----------------
* Move Hero:  Arrow Keys (Up, Down, Left, Right) or WASD (W, A, S, D)
* Menu Click: Left Mouse Click on interactive buttons


6. GAMEPLAY & OBJECTIVES
------------------------
* The Hero starts in the safe entrance hall with 3 Health Hearts.
* Infiltrate the dungeon and retrieve all 3 ancient crystals.
* Once all 3 crystals are collected, the magical Exit Portal unlocks.
* Step into the unlocked portal to WIN the game.
* If the Hero collides with an enemy, 1 heart is lost, accompanied by a
  damage sound effect, slight knockback, and a temporary invulnerability
  flicker.
* If health drops to 0, the game ends in GAME OVER (Defeat).


7. KEY FEATURES & REQUIREMENT COMPLIANCE
----------------------------------------
* Main Menu with Interactive Buttons:
  - "Start Game" button launches the game session.
  - "Sound & Music: ON / OFF" toggle button dynamically mutes or resumes
    both background music and all sound effects.
  - "Exit" button cleanly terminates the application.

* Two Distinct Enemies with Dedicated Patrol Areas:
  - Enemy 1 (Skeleton Guard): Patrols horizontally back and forth in the
    western corridor; pursues the hero if the hero enters its corridor;
    strictly confined within its assigned patrol territory.
  - Enemy 2 (Dungeon Specter): Floats in a sinusoidal hover path within
    the eastern chamber; pursues the hero if the hero enters its room;
    strictly confined within its assigned chamber territory.

* Sprite Animations (Idle & Movement):
  - Every character (Hero, Skeleton Guard, Dungeon Specter) features
    cyclical multi-frame animations (4 distinct frames each):
    - Idle animation: breathing, eye blinking, jaw clacking, hovering tail waving.
    - Movement animation: distinct leg stepping, arm swinging, spectral swooping.
  - The exit portal also features a continuous 4-frame rotating vortex.

* Audio & Sound Effects:
  - Background music track ("theme.mp3") sourced from mixkit.co.
  - Sound effects (gem collection, enemy hit/damage, victory fanfare, defeat
    game over, UI button click) sourced from mixkit.co.

* Object-Oriented Programming (OOP) Architecture:
  - Custom classes extending Pygame Zero's Actor:
    - AnimatedCharacter(Actor): Base class for cycling multi-frame animations.
    - Hero(AnimatedCharacter): Handles movement, input, and wall collisions.
    - Enemy(AnimatedCharacter): Base enemy class with patrol area clamping.
    - SkeletonEnemy(Enemy): Implements corridor patrol and pursuit.
    - SpecterEnemy(Enemy): Implements hovering sine-wave movement.
    - MenuButton: Reusable clickable UI button component.

* Clean Code & PEP8 Standards:
  - Meaningful English naming for variables, functions, and classes.
  - PEP8 compliant structure, formatting, and docstrings.
