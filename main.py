"""Dungeon Quest: The Lost Relics.

A top-down Roguelike dungeon game built with Pygame Zero.
"""
import math
import random
from pygame import Rect
from pgzero.actor import Actor
import pgzrun

WIDTH = 800
HEIGHT = 600
TITLE = "Dungeon Quest: The Lost Relics"

STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
STATE_WIN = "win"

game_state = STATE_MENU
audio_enabled = True
portal_active = False
portal_frame = 0
portal_timer = 0.0


class AnimatedCharacter(Actor):
    """Base class for characters with multi-frame idle and move animations."""

    def __init__(self, idle_frames, move_frames, pos):
        super().__init__(idle_frames[0], pos)
        self.idle_frames = idle_frames
        self.move_frames = move_frames
        self.is_moving = False
        self.frame_index = 0
        self.anim_timer = 0.0
        self.anim_speed = 0.15

    def update_animation(self, dt):
        """Cycle through animation frames continuously based on motion."""
        self.anim_timer += dt
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0.0
            frames = self.move_frames if self.is_moving else self.idle_frames
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.image = frames[self.frame_index]

    def set_moving(self, moving):
        """Switch animation sequence smoothly when movement state changes."""
        if self.is_moving != moving:
            self.is_moving = moving
            self.frame_index = 0
            self.anim_timer = 0.0
            frames = self.move_frames if moving else self.idle_frames
            self.image = frames[0]


class Hero(AnimatedCharacter):
    """Player hero with input movement, health, and collision handling."""

    def __init__(self, pos):
        idle = [f"hero_idle_{i}" for i in range(4)]
        walk = [f"hero_walk_{i}" for i in range(4)]
        super().__init__(idle, walk, pos)
        self.speed = 3.5
        self.max_hp = 3
        self.hp = 3
        self.invulnerable_timer = 0.0

    def move(self, dx, dy, dungeon_walls):
        """Move hero with sliding collision response against walls."""
        moving = dx != 0 or dy != 0
        self.set_moving(moving)
        if not moving:
            return

        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        self.x += dx * self.speed
        box = Rect(self.x - 14, self.y - 14, 28, 28)
        for wall in dungeon_walls:
            if box.colliderect(wall):
                self.x = (wall.left - 14) if dx > 0 else (wall.right + 14)

        self.y += dy * self.speed
        box = Rect(self.x - 14, self.y - 14, 28, 28)
        for wall in dungeon_walls:
            if box.colliderect(wall):
                self.y = (wall.top - 14) if dy > 0 else (wall.bottom + 14)

    def take_damage(self):
        """Deduct HP and grant temporary invulnerability."""
        if self.invulnerable_timer <= 0.0:
            self.hp -= 1
            self.invulnerable_timer = 1.2
            return True
        return False

    def update(self, dt):
        """Update invulnerability cooldown and sprite animation."""
        if self.invulnerable_timer > 0.0:
            self.invulnerable_timer = max(0.0, self.invulnerable_timer - dt)
        self.update_animation(dt)


class Enemy(AnimatedCharacter):
    """Base enemy class with patrol area constraint."""

    def __init__(self, idle_frames, move_frames, pos, patrol_area, speed):
        super().__init__(idle_frames, move_frames, pos)
        self.patrol_area = patrol_area
        self.speed = speed

    def clamp_to_area(self):
        """Ensure enemy never leaves its assigned territory."""
        self.x = max(self.patrol_area.left + 16,
                     min(self.patrol_area.right - 16, self.x))
        self.y = max(self.patrol_area.top + 16,
                     min(self.patrol_area.bottom - 16, self.y))


class SkeletonEnemy(Enemy):
    """Armored skeleton guard patrolling the western hallway."""

    def __init__(self, pos, patrol_area):
        idle = [f"skeleton_idle_{i}" for i in range(4)]
        walk = [f"skeleton_walk_{i}" for i in range(4)]
        super().__init__(idle, walk, pos, patrol_area, 1.8)
        self.direction = 1

    def update(self, dt, player):
        """Patrol corridor or chase player within assigned area."""
        if self.patrol_area.collidepoint(player.pos):
            dx = player.x - self.x
            dy = player.y - self.y
            dist = math.hypot(dx, dy)
            self.x += (dx / dist) * self.speed if dist > 2 else 0
            self.y += (dy / dist) * self.speed if dist > 2 else 0
            self.set_moving(dist > 2)
        else:
            self.x += self.direction * self.speed
            self.set_moving(True)
            if self.x >= self.patrol_area.right - 20:
                self.direction = -1
            elif self.x <= self.patrol_area.left + 20:
                self.direction = 1

        self.clamp_to_area()
        self.update_animation(dt)


class SpecterEnemy(Enemy):
    """Floating phantom hovering within the eastern chamber."""

    def __init__(self, pos, patrol_area):
        idle = [f"ghost_idle_{i}" for i in range(4)]
        move = [f"ghost_move_{i}" for i in range(4)]
        super().__init__(idle, move, pos, patrol_area, 2.0)
        self.center_x, self.center_y = pos
        self.angle = 0.0

    def update(self, dt, player):
        """Hover along sine-wave path or chase player within chamber."""
        self.angle += 1.8 * dt
        if self.patrol_area.collidepoint(player.pos):
            dx = player.x - self.x
            dy = player.y - self.y
            dist = math.hypot(dx, dy)
            self.x += (dx / dist) * self.speed if dist > 2 else 0
            self.y += (dy / dist) * self.speed if dist > 2 else 0
            self.set_moving(dist > 2)
        else:
            self.x = self.center_x + math.cos(self.angle) * 70
            self.y = self.center_y + math.sin(self.angle * 2.0) * 45
            self.set_moving(True)

        self.clamp_to_area()
        self.update_animation(dt)


class MenuButton:
    """Clickable UI button with border and text."""

    def __init__(self, rect, text):
        self.rect = rect
        self.text = text

    def draw(self):
        """Draw button rectangle and centered text."""
        screen.draw.filled_rect(self.rect, (42, 52, 78))
        screen.draw.rect(self.rect, (100, 140, 210))
        screen.draw.text(self.text, center=self.rect.center, fontsize=24,
                         color=(255, 255, 255), shadow=(1, 1),
                         scolor=(10, 10, 20))

    def is_clicked(self, pos):
        """Return True if mouse click position falls inside button rect."""
        return self.rect.collidepoint(pos)


# Dungeon Environment
walls = [
    Rect(30, 50, 740, 16),
    Rect(30, 574, 740, 16),
    Rect(30, 50, 16, 540),
    Rect(754, 50, 16, 540),
    Rect(390, 66, 16, 230),
    Rect(110, 310, 420, 16),
    Rect(570, 340, 16, 170),
]

skeleton_area = Rect(110, 140, 270, 160)
specter_area = Rect(416, 130, 330, 170)

hero = Hero((100, 480))
skeleton = SkeletonEnemy((220, 220), skeleton_area)
specter = SpecterEnemy((580, 210), specter_area)
portal = Actor("portal_0", (700, 110))

crystals = [
    Actor("crystal", (240, 210)),
    Actor("crystal", (580, 220)),
    Actor("crystal", (670, 480)),
]
total_crystals = len(crystals)

button_start = MenuButton(Rect(260, 240, 280, 48), "Start Game")
button_audio = MenuButton(Rect(260, 306, 280, 48), "Sound & Music: ON")
button_exit = MenuButton(Rect(260, 372, 280, 48), "Exit")

button_play_again = MenuButton(Rect(260, 300, 280, 48), "Play Again")
button_menu = MenuButton(Rect(260, 366, 280, 48), "Main Menu")


def reset_game():
    """Reset player, enemies, crystals and portal for a new run."""
    global portal_active, crystals
    hero.x, hero.y = 100, 480
    hero.hp = hero.max_hp
    hero.invulnerable_timer = 0.0
    hero.set_moving(False)

    skeleton.x, skeleton.y = 220, 220
    skeleton.direction = 1

    specter.x, specter.y = 580, 210
    specter.angle = 0.0

    crystals = [
        Actor("crystal", (240, 210)),
        Actor("crystal", (580, 220)),
        Actor("crystal", (670, 480)),
    ]
    portal_active = False


def toggle_audio():
    """Toggle background music and sound effects on or off."""
    global audio_enabled
    audio_enabled = not audio_enabled
    if audio_enabled:
        button_audio.text = "Sound & Music: ON"
        music.play("theme")
    else:
        button_audio.text = "Sound & Music: OFF"
        music.stop()


def update(dt):
    """Update game entities, collisions, and state transitions."""
    global game_state, portal_active, portal_timer, portal_frame

    if game_state != STATE_PLAYING:
        return

    dx = (1 if keyboard.right or keyboard.d else 0) - (
        1 if keyboard.left or keyboard.a else 0
    )
    dy = (1 if keyboard.down or keyboard.s else 0) - (
        1 if keyboard.up or keyboard.w else 0
    )
    hero.move(dx, dy, walls)
    hero.update(dt)

    skeleton.update(dt, hero)
    specter.update(dt, hero)

    portal_timer += dt
    if portal_timer >= 0.12:
        portal_timer = 0.0
        portal_frame = (portal_frame + 1) % 4
        portal.image = f"portal_{portal_frame}"

    hero_box = Rect(hero.x - 16, hero.y - 16, 32, 32)
    for crystal in crystals[:]:
        if hero_box.colliderect(Rect(crystal.x - 14, crystal.y - 14, 28, 28)):
            crystals.remove(crystal)
            if audio_enabled:
                sounds.gem.play()

    if len(crystals) == 0:
        portal_active = True

    for enemy in (skeleton, specter):
        if hero_box.colliderect(Rect(enemy.x - 14, enemy.y - 14, 28, 28)):
            if hero.take_damage():
                if audio_enabled:
                    sounds.hit.play()
                if hero.hp <= 0:
                    game_state = STATE_GAME_OVER
                    music.stop()
                    if audio_enabled:
                        sounds.gameover.play()
                    return

    if portal_active and hero_box.colliderect(
        Rect(portal.x - 20, portal.y - 20, 40, 40)
    ):
        game_state = STATE_WIN
        music.stop()
        if audio_enabled:
            sounds.win.play()


def draw_overlay(title, subtitle, title_color, buttons, hint=""):
    """Render translucent backdrop, text banner, and buttons."""
    screen.draw.filled_rect(Rect(0, 0, WIDTH, HEIGHT), (14, 18, 28, 230))
    screen.draw.text(title, center=(WIDTH // 2, 130), fontsize=52,
                     color=title_color, shadow=(2, 2), scolor=(5, 5, 10))
    screen.draw.text(subtitle, center=(WIDTH // 2, 185), fontsize=22,
                     color=(210, 225, 245))
    for btn in buttons:
        btn.draw()
    if hint:
        screen.draw.text(hint, center=(WIDTH // 2, 500), fontsize=18,
                         color=(140, 160, 190))


def draw():
    """Render all graphics, tiles, HUD, and interface overlays."""
    screen.clear()

    for x in range(30, 770, 40):
        for y in range(50, 580, 40):
            screen.blit("tile_floor", (x, y))

    screen.draw.rect(skeleton_area, (60, 40, 50))
    screen.draw.rect(specter_area, (40, 55, 70))

    for wall in walls:
        for wx in range(wall.left, wall.right, 40):
            for wy in range(wall.top, wall.bottom, 40):
                screen.blit("tile_wall", (wx, wy))

    portal.draw()
    for crystal in crystals:
        crystal.draw()

    skeleton.draw()
    specter.draw()

    if hero.invulnerable_timer <= 0.0 or int(hero.invulnerable_timer * 10) % 2 == 0:
        hero.draw()

    # Top HUD
    screen.draw.filled_rect(Rect(0, 0, WIDTH, 48), (20, 22, 32))
    screen.draw.line((0, 48), (WIDTH, 48), (50, 60, 80))

    for i in range(hero.max_hp):
        screen.blit("heart_full" if i < hero.hp else "heart_empty",
                    (20 + i * 28, 12))

    collected = total_crystals - len(crystals)
    status_text = f"Crystals: {collected}/{total_crystals}"
    if portal_active:
        status_text += " - PORTAL UNLOCKED!"
    screen.draw.text(status_text, (130, 14), fontsize=22,
                     color=(120, 225, 255))

    audio_text = "AUDIO: ON" if audio_enabled else "AUDIO: OFF"
    screen.draw.text(audio_text, (680, 14), fontsize=20, color=(180, 190, 210))

    if game_state == STATE_MENU:
        draw_overlay("DUNGEON QUEST",
                     "Collect all 3 ancient crystals to unlock the escape portal!",
                     (255, 215, 60), [button_start, button_audio, button_exit],
                     "Controls: Arrow Keys or WASD to move")
    elif game_state == STATE_GAME_OVER:
        draw_overlay("GAME OVER",
                     "The dungeon monsters overwhelmed you!",
                     (240, 60, 60), [button_play_again, button_menu])
    elif game_state == STATE_WIN:
        draw_overlay("VICTORY!",
                     "You recovered all crystals and escaped alive!",
                     (80, 240, 140), [button_play_again, button_menu])


def on_mouse_down(pos):
    """Handle mouse button clicks across game screens."""
    global game_state

    if game_state == STATE_MENU:
        if button_start.is_clicked(pos):
            if audio_enabled:
                sounds.click.play()
            reset_game()
            game_state = STATE_PLAYING
            if audio_enabled and not music.is_playing("theme"):
                music.play("theme")
        elif button_audio.is_clicked(pos):
            toggle_audio()
            if audio_enabled:
                sounds.click.play()
        elif button_exit.is_clicked(pos):
            raise SystemExit(0)

    elif game_state in (STATE_GAME_OVER, STATE_WIN):
        if button_play_again.is_clicked(pos):
            if audio_enabled:
                sounds.click.play()
            reset_game()
            game_state = STATE_PLAYING
            if audio_enabled and not music.is_playing("theme"):
                music.play("theme")
        elif button_menu.is_clicked(pos):
            if audio_enabled:
                sounds.click.play()
            game_state = STATE_MENU
            if audio_enabled and not music.is_playing("theme"):
                music.play("theme")


pgzrun.go()
