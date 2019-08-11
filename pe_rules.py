from urllib.request import urlopen
from re import compile
from phonology_engine import PhonologyEngine
from subprocess import call

#saknis, vard, gal, kilm
_months = [
    ["SAUS",   "IS",  "Į",  "IO"],
    ["VASAR",  "IS",  "Į",  "IO"],
    ["KOV",    "AS",  "Ą",  "O"],
    ["BALAND", "IS",  "Į",  "ŽIO"],
    ["GEGUŽ",  "Ė",   "Ę",  "ĖS"],
    ["BIRŽEL", "IS",  "Į",  "IO"],
    ["LIEP",   "A",  "Ą",  "OS"],
    ["RUGPJŪ", "TIS", "TĮ", "ČIO"],
    ["RUGSĖJ", "IS",  "Į",  "O"],
    ["SPAL",   "IS",  "Į",  "IO"],
    ["LAPKRI", "TIS", "TĮ", "ČIO"],
    ["GRUOD",  "IS",  "Į",  "ŽIO"],
    ]

_month = ["MĖN", "UO", "ESĮ", "ESIO"]

def get_month(month, mode=0):
    if mode not in range(5):
        raise Exception()
    if month not in range(1, 13):
        raise Exception()

    m = month - 1
    
    if mode == 0:
        result = (_months[m][0] + _months[m][1])
    elif mode == 1:
        result = (_months[m][0] + _months[m][2])
    elif mode == 2:
        result = ("%s%s %s%s" % (_months[m][0], _months[m][3], _month[0], _month[1]))
    elif mode == 3:
        result = ("%s%s %s%s" % (_months[m][0], _months[m][3], _month[0], _month[2]))
    elif mode == 4:
        result = (_months[m][0] + _months[m][3])

    return result.lower()

def get_endings():
    pe = PhonologyEngine()
    pe.phrase_separators = ''

    with urlopen('https://raw.githubusercontent.com/aleksas/phonology_engine/master/native/source/rules.h') as url:
        content = url.read().decode('windows-1257', 'ignore')

    d = {}
    pat = compile(r'"([^,:* -]+)-([^ @]+)@[^@]+@",')
    for match in pat.finditer(content):
        stressed_num = match.group(1)
        ending = match.group(2)
        if stressed_num not in d:
            d[stressed_num] = set([])
        d[stressed_num].add(ending)
    
    for k in d.keys():
        d[k] = list(d[k])

    m = {}
    for i in list(range(20)) + list(range(20, 100, 10)) + [10**p for p in [2,3,6,9]]:
        k = pe.process_and_collapse(str(i), 'ascii_stressed_word')
        m[k] = i

    dd = {}
    for k,v in d.items():
        if k.endswith('AI~') or k.endswith('AI') or k.endswith('Ų'):
            continue
        dd[m[k]] = v
    
    sorted_keys = sorted(dd.keys(), reverse=True)
    return dd, sorted_keys

if __name__ == "__main__":
    endings, sorted_keys = get_endings()
    s = set([v for values in endings.values() for v in values])
    print(s)
