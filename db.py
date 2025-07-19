# animal-bot/bot.py
# author: kefiiiiir
# version 1.0

import json
import os
from aiogram.types import Message

user_points = {}

POINTS_FILE = "user_points.json"

def load_points():
    """Loads user points to user_points dict"""
    global user_points
    if os.path.exists(POINTS_FILE):
        try:
            with open(POINTS_FILE, 'r') as f:
                user_points = json.load(f)
        except:
            user_points = {}

def save_points():
    """Saves user points from user_points dict to json"""
    with open(POINTS_FILE, 'w') as f:
        json.dump(user_points, f)


async def add_points(message: Message):
    user_id = str(message.from_user.id)
    check_user_exists(user_id) 
    user_points[user_id] += 1
    save_points()

async def deduct_points(message: Message, points: int):
    user_id = str(message.from_user.id)
    check_user_exists(user_id) 
    user_points[user_id] -= points
    save_points()

def check_user_exists(user_id: str):
    if not user_id:
        return
    if user_id not in user_points:
        user_points[user_id] = 0