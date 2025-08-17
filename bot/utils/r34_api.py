import random

from rule34Py import rule34Py


def get_post(tags: list[str]) -> str:
    """Gets random picture from rule34.xxx"""

    client = rule34Py()

    search_result = client.search(tags=tags, limit=1000)
    post_id = random.randint(0, len(search_result))

    photo = search_result[post_id].image
    if not photo:
        raise Exception
    return photo