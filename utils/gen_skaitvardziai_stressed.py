
from static.get_skaitvardis import get_all_number_names
from phonology_engine import PhonologyEngine
from json import dumps
from re import sub, compile

pe = PhonologyEngine()
clear_stress_p = compile(r'[\^~`]')
regex_replacements = [
    (r'\s*\n*\s*((("[^"]+")|(null)),?)\s*\n\s*', r'\g<1>'),
    (r'(\n\s*)("Default":"[^"]+",)"', r'\g<1>\g<2>\g<1>"'),
    (r'jonas"', 'jo~nas"'),
    (r'jono"', 'jo~no"'),
    (r'jonui"', 'jo~nui"'),
    (r'joną"', 'jo~ną"'),
    (r'jonu"', 'jonu`"'),
    (r'jone"', 'jone`"'),
    (r'jonai"', 'jo~nai"'),
    (r'jonų"', 'jo~nų"'),
    (r'jonams"', 'jo~nams"'),
    (r'jonus"', 'jonu`s"'),
    (r'jonais"', 'jo~nais"'),
    (r'jonuose"', 'jo~nuose"'),
]

def convert(d):
    skip_keys = ['Variations']

    if isinstance(d, dict):
        converted = {}
        for k, v in d.items():
            converted[k] = v if k in skip_keys else convert(v)
        return converted
    elif isinstance(d, str):
        return d
    elif isinstance(d, list):
        if len(d) > 0 and isinstance(d[0], str):
            res = ['']
            s0 = d[0]

            for s in d[1:]:
                s = pe.process_and_collapse(s0 + s, word_format='ascii_stressed_word').lower()
                res.append(s)

            return res
        else:
            return convert(d)
    else:
        raise Exception()

data = convert(get_all_number_names())

with open('raw/skaitvardziai.stressed.json', "w", encoding="utf-8") as fp:
    content = dumps(data, ensure_ascii=False,  indent=3)
    for pattern, replacement in regex_replacements:
        content = sub(pattern, replacement, content)
    fp.write(content)