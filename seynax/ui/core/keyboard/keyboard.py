import re
import tkinter

from utils.attributes.string_utils import blank

translations = {
    'CTRL': 'Control',
    '+':    'KP_Add',
    '-': 'KP_Subtract'
}


def translate(keys: str) -> str:
    keys = keys.lower()
    keys = re.sub('\s+', '', keys)
    splits = keys.split('+')

    if len(splits) > 1 and not blank(splits[1]):
        for split in splits:
            for name, value in translations.items():
                keys = keys.replace(split, split.replace(name.lower(), value))
    else:
        for name, value in translations.items():
            keys = keys.replace(name.lower(), value)

    return '<' + keys.replace('+', '-') + '>'
