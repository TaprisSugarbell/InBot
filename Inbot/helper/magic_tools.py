import random
import string


def rankey(
        length: int = 5,
        _string: string = string.hexdigits
):
    return "".join(
        random.choice(
            _string
        ) for _ in range(length)
    )