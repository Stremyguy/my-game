import pygame
import sqlite3

from characters import RockSleeper, FlyingVirus, Boss


def load_characters_from_db(db_path: str, screen: "pygame") -> dict:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
                   SELECT c.id, c.name, i.x, i.y, i.level_id 
                   FROM characters_ids c JOIN characters_info i ON c.id = i.id
                   """)
    characters_data = cursor.fetchall()
    
    characters = {}
    
    for char in characters_data:
        char_id, name, x, y, level_id = char
        position = (x, y)
        
        if name == "Sleeper":
            character = RockSleeper(position=position, screen=screen)
        elif name == "Onyx":
            character = FlyingVirus(position=position, screen=screen)
        elif name == "Boss":
            character = Boss(position=position, screen=screen)
        else:
            continue
        
        if level_id not in characters:
            characters[level_id] = []
        characters[level_id].append(character)
    
    conn.close()
    return characters
