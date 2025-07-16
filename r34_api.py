# animal-bot/r34_api.py
# author: Ptmasher
# version 1.0

from rule34Py import rule34Py
import random


def get_post(TAGS):
    """Gets random picture from rule34.xxx"""
    # Initialize connection
    client = rule34Py()

    # Define tags

    # Get pictures from host
    result = client.search(tags=TAGS, limit=200)
    # Choose random picture from the page
    postId = random.randint(0,len(result))

    # Return picture
    photo = result[postId].image
    return photo