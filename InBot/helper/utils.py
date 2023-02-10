import os
import random
import string
from typing import Any
from .mongo_connect import *

tc = Mongo(URI, "DanbooruBot", "tag_code")


def rankey(
        length: int = 5,
        _string: string = string.hexdigits
):
    return "".join(
        random.choice(_string) for _ in range(length)
    )


def create_folder(folder_name: Any = None, temp_folder: str = rankey()):
    _user_id = "" if folder_name is None else f"Downloads/{folder_name}/" if temp_folder else f"Downloads/{folder_name}"

    tmp_directory = f"./{_user_id}{temp_folder}/"
    if not os.path.isdir(tmp_directory):
        os.makedirs(tmp_directory, exist_ok=True)
    return tmp_directory


async def tag_code(_tags: str):
    _c = await confirm(
        tc,
        {
            "tags": _tags
        }
    )
    if _c:
        _c = _c[0]
        _tags_code = _c["tags_code"]
    else:
        _tags_code = rankey(8)
        await add_(
            tc,
            {
                "tags": _tags,
                "tags_code": _tags_code
            }
        )
    return _tags_code

