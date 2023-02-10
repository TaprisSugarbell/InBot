from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


_config = []


def post_buttons(post_id: int, _mode: str = "safe", _tag_code: str = "0", _has_parent: bool = None):
    _prev_next = []
    _parent = []
    if post_id > 1:
        _prev_next.append(
            InlineKeyboardButton(
                'Prev', f'{_mode}_prev_{_tag_code}_{post_id}'
            )
        )
    if _has_parent:
        _parent.append(
            InlineKeyboardButton(f'Parent', switch_inline_query_current_chat=f'parent:{post_id}')
        )
    _prev_next.append(
        InlineKeyboardButton(
            'Next', f'{_mode}_next_{_tag_code}_{post_id}'
        )
    )
    return InlineKeyboardMarkup(
        [
            _prev_next,
            [
                InlineKeyboardButton(
                    "File", f'{_mode}_file_{_tag_code}_{post_id}'
                )
            ],
            _parent
        ]
    )


