import pygame
import pytmx

DATA_FOLDER = "data/"
FONT_FOLDER = "data/fonts/"
DATABASE_FOLDER = "data/db/"
MUSIC_FOLDER = "data/music/"
SOUNDS_FOLDER = "data/sfx/"
LEVELS_FOLDER = "data/levels/maps/"


def load_image(filename: str) -> "pygame":
    image = pygame.image.load(f"{DATA_FOLDER}{filename}")
    return image


def load_font(filename: str) -> "pygame":
    font = f"{FONT_FOLDER}{filename}"
    return font


def load_level(filename: str) -> "pygame":
    level = pytmx.load_pygame(f"{LEVELS_FOLDER}{filename}.tmx")
    return level


def load_music(filename: str) -> "pygame":
    music = f"{MUSIC_FOLDER}{filename}"
    return music


def load_sound(filename: str) -> "pygame":
    sound = f"{SOUNDS_FOLDER}{filename}"
    return sound


def load_db(filename: str) -> "pygame":
    db = f"{DATABASE_FOLDER}{filename}"
    return db


def init_music() -> None:
    pygame.mixer.init()


def play_music(music_filename: str) -> None:
    pygame.mixer.music.load(load_music(music_filename))
    pygame.mixer.music.play(-1)
    

def stop_music() -> None:
    pygame.mixer.music.stop()


def play_sound(sound_filename: str) -> None:
    sound = pygame.mixer.Sound(load_sound(sound_filename))
    sound.play()
