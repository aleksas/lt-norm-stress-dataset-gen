from io import open
from re import sub, compile
from urllib.request import urlopen
from os.path import exists, join
from os import mkdir
from random import randint, sample
from static.get_skaitvardis import get_number_complex_name, Stress

from generators.text_modifiers import modifiers

default_stress = Stress.No

ps = compile(r'[`~^]+')

date_p_1=r'(\d{4}) m\.\s+([a-zą-ž])+\s+(\d+)+\s+d(\.|(ien[a-zą-ž]+))'

tmp_dir = '.'

n1 = compile(r'(.*\d.*)|([XIVCD]{2;})')

FINAL_1 = 'https://github.com/aleksas/liepa_dataset/raw/master/other/stressed/__final_1.txt'

url_content_cache = {}
def get_content(url):
    if url not in url_content_cache:
        with urlopen(url) as content_manager:
            url_content_cache[url] = content_manager.read()

    return url_content_cache[url]

def get_lines(url):
    content_bytes = get_content(url)

    content = content_bytes.decode('utf-8', 'ignore').strip()

    def rep(pattern, repl, content, strict = True):
        content_new = sub(pattern, repl, content)
        if content == content_new and strict:
            raise Exception('"%s" pattern didn\'t match')
        return content_new

    sentence_splitters = [
        # SPLIT SENTENCE PER LINE

        # remove empty lines
        (r'([\r\s]*\n[\r\s]*)+', r'\n'),

        #direct speach
        (r'([!?\.]\s*)\n+(\s*(-|[a-z]))', r'\g<1> \g<2>'),
        (r'("[^"]+\s*)\n(\s*")', r'\g<1> \g<2>'),

        #(r'([^\s\.\?!]+\s)?[\t\r\n ]*([^\s\.\?!]+[\.\?!]+)[\t\r\n ]*', r'\g<1>\g<2>\n'),
        (r'([\.?:]\s*)(-\s*["A-ZĄ-Ž])', r'\g<1>\n\g<2>'),
        (r'\n(\s*[a-zą-ž])', r' \g<1>'),

        # shortened first name
        (r'(\s[A-ZĄ-Ž][a-zą-ž]?\.\s*)\n(\s*[A-ZĄ-Ž])', r'\g<1> \g<2>'),
    
        #numbered lines
        (r'(\n\s*(\d+|([XIV]+))\.?\s*)\n+', r'\g<1> '),

        (r'([a-zą-ž~`^]{3,}[\.!?]+)\s+("?[A-ZĄ-Ž][~`^a-zą-ž]{2,})', r'\g<1>\n\g<2>'),
    ]

    for p,r in sentence_splitters:
        content = rep(p,r,content)

    for l in content.splitlines():
        l = l.strip()
        if l:
            yield l

def generate_senteces(config):
    num_lines = []
    for line in get_lines(FINAL_1):
        if n1.match(line):
            num_lines.append(line)
        else:
            yield ps.sub('', line), line
            yield line, line
        
    while num_lines:
        num_line = num_lines.pop()
        line = num_line
        for p, s_ in modifiers:
            if not isinstance(s_, list):
                s_ = [s_]
            
            for s in s_:
                m = p.search(line)
                if m:
                    line = p.sub(s, line).strip()

        if not n1.match(line):
            yield ps.sub('', num_line), line
            yield ps.sub('', line), line
            yield num_line, line