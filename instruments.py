import pygame
import pytmx

DATA_FOLDER = "data/"
MUSIC_FOLDER = "data/music/"
LEVELS_FOLDER = "data/levels/maps/"


def load_image(filename: str) -> "pygame":
    image = pygame.image.load(f"{DATA_FOLDER}{filename}")
    return image


def load_level(filename: str) -> "pygame":
    level = pytmx.load_pygame(f"{LEVELS_FOLDER}{filename}.tmx")
    return level


def load_music(filename: str) -> "pygame":
    music_path = f"{MUSIC_FOLDER}{filename}"
    return music_path
