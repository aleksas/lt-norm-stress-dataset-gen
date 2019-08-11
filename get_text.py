from io import open
from re import sub, compile
from urllib.request import urlopen
from os.path import exists, join
from os import mkdir
from random import randint, sample
from static.get_skaitvardis import get_number_complex_name, Stress

default_stress = Stress.No

ps = compile(r'[`~^]+')

date_p_1=r'(\d{4}) m\.\s+([a-zą-ž])+\s+(\d+)+\s+d(\.|(ien[a-zą-ž]+))'

tmp_dir = '.'

n1 = compile(r'(.*\d.*)|([XIVCD]{2;})')

tens = list(range(20, 100, 10)) + [0]
many = list(range(10, 21)) + list(range(30, 100, 10))

def rand_ones(max=1000):
    if max < 100:
        raise ValueError()

    f100 = randint(0, max//100) * 100
    return 1 + sample(tens, 1)[0] + f100

def rand_few(max=1000):
    if max < 100:
        raise ValueError()

    f10 = sample(tens, 1)[0]
    f100 = randint(0, max//100) * 100

    return randint(2,9) + f10 + f100

def rand_many(max=1000):
    if max < 100:
        raise ValueError()
        
    f100 = randint(0, max//100) * 100

    return sample(many, 1)[0] + f100

def split_lines():
    filename = '__final_1.txt'
    tmp_path = join(tmp_dir, filename)
    content_bytes = None

    if not exists(tmp_path):
        if not exists(tmp_dir):
            mkdir(tmp_dir)
            
        with urlopen('https://github.com/aleksas/liepa_dataset/raw/master/other/stressed/__final_1.txt') as url:
            with open(tmp_path, 'wb') as f:
                content_bytes = url.read()
                f.write(content_bytes)

    if not content_bytes:
        with open(tmp_path, 'rb') as f:
            content_bytes = f.read()

    context = {}
    context['content'] = content_bytes.decode('utf-8', 'ignore')
    context['content'] = context['content'].strip()

    def rep(pattern, repl):
        debug = True
        content_new = sub(pattern, repl, context['content'])
        if debug and context['content'] == content_new:
            raise Exception()
        context['content'] = content_new

    rep(r'([^\s\.\?!]+\s)?[\t\r\n ]*([^\s\.\?!]+[\.\?!]+)[\t\r\n ]*', r'\g<1>\g<2>\n')
    rep(r'([\t\r\n ]+[IVX]+\.)\n+', r' \g<1> ')
    rep(r'([!?\.]\s*)\n+(\s*(-|[a-z]))', r'\g<1> \g<2>')
    rep(r'("[^"]+\s*)\n(\s*")', r'\g<1> \g<2>')
    rep(r'([\.?:]\s*)(-\s*["A-ZĄ-Ž])', r'\g<1>\n\g<2>')
    rep(r'\n(\s*[a-zą-ž])', r'\g<1>')
    
    # shortened first name
    rep(r'(\s[A-ZĄ-Ž][a-zą-ž]?\.\s*)\n(\s*[A-ZĄ-Ž])', r'\g<1> \g<2>')

    # nr.
    #rep(r'Nr\.\s*\n', r'Nr\.')

    #numbered lines
    rep(r'(\n\s*((\d+)|([XIV]+))\.?\s*)\n', r'\g<1> ')
    rep(r'(\n\s*\d+\s*)\n', r'\g<1> ')

    rep(r'\n([,\)\]\}])', r'\g<1>')

    #rep(r'^([IVX]+\.)\n+', r'\g<1> ')
    #rep(r'^([A-ZĄ-Ž]\.)\n+', r'\g<1> ')
    #rep(r'([\t\r\n ]+[A-ZĄ-Ž]\.)\n+', r' \g<1> ')
    #rep(r'([a-zą-ž])\n([0-9a-zą-ž,:])', r'\g<1> \g<2>')
    #rep(r'\n([a-zą-ž,:])', r' \g<1>')
    #rep(r'\n([\)\]])', r'\g<1>')
    #rep(r'(Nr\.)\n((\d)|([IXVM\d]))', r'\g<1> \g<2>')
    #rep(r'(\s*((pab)|([dD]r)|(Šv))\.\s*)\n(\s*[A-ZĄ-Ž])', r'\g<1> \g<2>')
    #rep(r'(\d+\.)\n(\d+)', r'\g<1> \g<2>')
    #rep(r'\n\s*(")\s*\n', r'\g<1>\n')
    #rep(r' +', r' ')
    ##rep(r'\n+', r'\n')
    #rep(r'\n\s*(\d+\.)\s*\n', r'\n\g<1> ')
    #rep(r'(\n[“”])|(„\n)', r'"')
    #rep(r'(mln\.)\n+((JAV\s)|(Lit)|([Ll]t\.?))', r'\g<1> \g<2>')
    #rep(r'(\d+\s+val.)\s*\n+\s*(\d+\s+min.)\n', r'\g<1> \g<2>')
    #rep(r'(Sh\.)\n+(Abe)', r'\g<1> \g<2>')
    #rep(r'(\s+\d+\s+d\.)\n+(([A-ZĄ-Ža-zą-ž]+\s*){2,6})(įstatymo)', r'\g<1> \g<2> \g<4>')

    for l in context['content'].splitlines():
        l = l.strip()
        if l:
            yield l

modifiers = [
    (
        compile(r" \d+,5 "), 
        lambda _: r" %s su puse " % (
            get_number_complex_name(
                value=randint(10,100),
                category_type='Kiekiniai',
                category_subtype='Pagrindiniai',
                number='dgs',
                gender='vyr. g.',
                case='vard.')[0]
        )
    ),
    (
        compile(r" iš daugiau nei \d+ šalių"), 
        lambda _: r" iš daugiau nei %s šalių" % (
            get_number_complex_name(
                value=randint(2,100),
                category_type='Kiekiniai',
                category_subtype='Pagrindiniai',
                number='dgs',
                gender='mot. g.',
                case='kilm.')[0]
        )
    ),
    (
        compile(r"\d+ straipsnio"), 
        lambda _: r"%s straipsnio" % (
            get_number_complex_name(
                value=randint(1,100),
                category_type='Kelintiniai',
                category_subtype='Neįvardžiuotiniai',
                number='vns',
                gender='vyr. g.',
                case='kilm.')[0]
        )
    ),
    (
        compile(r"\d+ dalyje"), 
        lambda _: r"%s dalyje" % (
            get_number_complex_name(
                value=randint(1,100),
                category_type='Kelintiniai',
                category_subtype='Neįvardžiuotiniai',
                number='vns',
                gender='mot. g.',
                case='viet.')[0]
        )
    ),
    (
        compile(r"\d+ dalies"), 
        lambda _: r"%s dalies" % (
            get_number_complex_name(
                value=randint(1,100),
                category_type='Kelintiniai',
                category_subtype='Neįvardžiuotiniai',
                number='vns',
                gender='mot. g.',
                case='kilm.')[0]
        )
    ),
    (
        compile(r"\d+ punkte"), 
        lambda _: r"%s punkte" % (
            get_number_complex_name(
                value=randint(1,100),
                category_type='Kelintiniai',
                category_subtype='Neįvardžiuotiniai',
                number='vns',
                gender='vyr. g.',
                case='viet.')[0]
        )
    ),
    (
        compile(r"\d+ straipsnis"), 
        lambda _: r"%s straipsnis" % (
            get_number_complex_name(
                value=randint(1,100),
                category_type='Kelintiniai',
                category_subtype='Neįvardžiuotiniai',
                number='vns',
                gender='vyr. g.',
                case='vard.')[0]
        )
    ),
    (
        compile(r"\d+ straipsnio"), 
        lambda _: r"%s straipsnio" % (
            get_number_complex_name(
                value=randint(1,100),
                category_type='Kelintiniai',
                category_subtype='Neįvardžiuotiniai',
                number='vns',
                gender='vyr. g.',
                case='kilm.')[0]
        )
    ),
    (
        compile(r"\d+ ar \d+ metus"), 
        lambda _: r"%s ar %s metus" % ((
            get_number_complex_name(
                value=randint(2,100),
                category_type='Kiekiniai',
                category_subtype='Pagrindiniai',
                number='dgs',
                gender='vyr. g.',
                case='gal.')[0]
        ),(
            get_number_complex_name(
                value=randint(2,100),
                category_type='Kiekiniai',
                category_subtype='Pagrindiniai',
                number='dgs',
                gender='vyr. g.',
                case='gal.')[0]
        ))
    ),
    (
        compile(r" iš daugiau nei \d+ šalių"), 
        lambda _: r" iš daugiau nei %s šalies" % (
            get_number_complex_name(
                value=1,
                category_type='Kiekiniai',
                category_subtype='Pagrindiniai',
                number='vns',
                gender='mot. g.',
                case='kilm.')[0]
        )
    ),
    (
        compile(r"prieš \d+ metų"), 
        lambda _: r"prieš %s metų" % (
            get_number_complex_name(
                value=randint(10,100),
                category_type='Kiekiniai',
                category_subtype='Pagrindiniai',
                number='dgs',
                gender='vyr. g.',
                case='kilm.')[0]
        )
    ),
    (
        compile(r"kaip \d+ metų"), 
        lambda _: r"kaip %s metų" % (
            get_number_complex_name(
                value=randint(10,100),
                category_type='Kiekiniai',
                category_subtype='Pagrindiniai',
                number='dgs',
                gender='vyr. g.',
                case='kilm.')[0]
        )
    ),
    (
        compile(r"\d+ metais"), 
        lambda _: r"%s metais" % (
            get_number_complex_name(
                value=randint(10,3000),
                category_type='Kelintiniai',
                category_subtype='Neįvardžiuotiniai',
                number='dgs',
                gender='vyr. g.',
                case='įnag.')[0][0]
        )
    ),
    (
        compile(r"\d{4} metų"), 
        lambda _: r"%s metų" % (
            get_number_complex_name(
                value=randint(1000,3000),
                category_type='Kelintiniai',
                category_subtype='Įvardžiuotiniai',
                number='dgs',
                gender='vyr. g.',
                case='kilm.')[0]
        )
    ),
    (
        compile(r"\d{2,3} metų"), 
        lambda _: r"%s metų" % (
            get_number_complex_name(
                value=randint(10,999),
                category_type='Kiekiniai',
                category_subtype='Pagrindiniai',
                number='dgs',
                gender='vyr. g.',
                case='kilm.')[0]
        )
    ),
    (
        compile(r"\d+ milijonai"), 
        lambda _: r"%s milijonai" % (
            get_number_complex_name(
                value=rand_few(),
                category_type='Kiekiniai',
                category_subtype='Pagrindiniai',
                number='dgs',
                gender='vyr. g.',
                case='vard.')[0]
        )
    ),
    (
        compile(r"\d+ tūkst. litų"), 
        [
            lambda _: r"%s tūkstis litų" % (
                get_number_complex_name(
                    value=rand_ones(),
                    category_type='Kiekiniai',
                    category_subtype='Pagrindiniai',
                    number='vns',
                    gender='vyr. g.',
                    case='vard.')[0]),
            lambda _: r"%s tūkstčiai litų" % (
                get_number_complex_name(
                    value=rand_few(),
                    category_type='Kiekiniai',
                    category_subtype='Pagrindiniai',
                    number='dgs',
                    gender='vyr. g.',
                    case='vard.')[0]),
            lambda _: r"%s tūkstčių litų" % (
                get_number_complex_name(
                    value=rand_many(),
                    category_type='Kiekiniai',
                    category_subtype='Pagrindiniai',
                    number='dgs',
                    gender='vyr. g.',
                    case='kilm.')[0])
        ]
    ),    
    (
        compile(r"\d+ valandas"), 
        lambda _: r"%s valandas" % (
            get_number_complex_name(
                value=rand_few(),
                category_type='Kiekiniai',
                category_subtype='Pagrindiniai',
                number='dgs',
                gender='mot. g.',
                case='gal.')[0]
        )
    ),
    (
        compile(r"^\d+\."), 
        lambda _: r"%s." % (
            get_number_complex_name(
                value=randint(2,100),
                category_type='Kiekiniai',
                category_subtype='Pagrindiniai',
                number='dgs',
                gender='vyr. g.',
                case='vard.')[0]
        )
    ),
    (
        compile(r"^\d+\."), 
        lambda _: r"%s." % (
            get_number_complex_name(
                value=1,
                category_type='Kiekiniai',
                category_subtype='Pagrindiniai',
                number='vns',
                gender='vyr. g.',
                case='vard.')[0]
        )
    ),
    (
        compile(r"^\d+\)"), 
        lambda _: r"%s)" % (
            get_number_complex_name(
                value=randint(2,100),
                category_type='Kiekiniai',
                category_subtype='Pagrindiniai',
                number='dgs',
                gender='vyr. g.',
                case='vard.')[0]
        )
    ),
    (
        compile(r"^\d+\)"), 
        lambda _: r"%s)" % (
            get_number_complex_name(
                value=1,
                category_type='Kiekiniai',
                category_subtype='Pagrindiniai',
                number='vns',
                gender='vyr. g.',
                case='vard.')[0]
        )
    ),
    (
        compile(r"\d+\(\d+\) straipsnis"), 
        lambda _: r"%s %s straipsnis" % ((
            get_number_complex_name(
                value=randint(1,3000),
                category_type='Kelintiniai',
                category_subtype='Neįvardžiuotiniai',
                number='vns',
                gender='vyr. g.',
                case='vard.')[0]
        ),(
            get_number_complex_name(
                value=randint(2,100),
                category_type='Kiekiniai',
                category_subtype='Pagrindiniai',
                number='dgs',
                gender='vyr. g.',
                case='vard.')[0]
        ))
    ),
    (
        compile(r"\d{3,} metus"), 
        lambda _: r"%s metus" % (
            get_number_complex_name(
                value=randint(1000,3000),
                category_type='Kelintiniai',
                category_subtype='Įvardžiuotiniai',
                number='dgs',
                gender='vyr. g.',
                case='gal.')[0]
        )
    ),
    (
        compile(r"\d+ dienos"), 
        lambda _: r"%s dienos" % (
            get_number_complex_name(
                value=randint(1,100),
                category_type='Kelintiniai',
                category_subtype='Neįvardžiuotiniai',
                number='vns',
                gender='mot. g.',
                case='kilm.')[0]
        )
    ),
    (
        compile(r" po \d+ komand"), 
        lambda _: r" po %s komand" % (
            get_number_complex_name(
                value=randint(10,3000),
                category_type='Kiekiniai',
                category_subtype='Pagrindiniai',
                number='dgs',
                gender='mot. g.',
                case='gal.')[0]
        )
    ),
    (
        compile(r" po \d+"), 
        lambda _: r" po %s" % (
            get_number_complex_name(
                value=randint(10,3000),
                category_type='Kiekiniai',
                category_subtype='Pagrindiniai',
                number='dgs',
                gender='vyr. g.',
                case='gal.')[0]
        )
    ),
    (
        compile(r"\d+-\d+ kartus"), 
        lambda _: r"%s %s kartus" % ((
            get_number_complex_name(
                value=rand_few(),
                category_type='Kiekiniai',
                category_subtype='Pagrindiniai',
                number='dgs',
                gender='vyr. g.',
                case='gal.')[0]
        ),(
            get_number_complex_name(
                value=rand_few(),
                category_type='Kiekiniai',
                category_subtype='Pagrindiniai',
                number='dgs',
                gender='vyr. g.',
                case='gal.')[0]
        ))
    ),
    (
        compile(r"\d{4} m. [a-zą-ž]+ \d+ d. įsakym"), 
        lambda _: r"%s %s kartus" % ((
            get_number_complex_name(
                value=rand_few(),
                category_type='Kiekiniai',
                category_subtype='Pagrindiniai',
                number='dgs',
                gender='vyr. g.',
                case='gal.')[0]
        ),(
            get_number_complex_name(
                value=rand_few(),
                category_type='Kiekiniai',
                category_subtype='Pagrindiniai',
                number='dgs',
                gender='vyr. g.',
                case='gal.')[0]
        ))
    ),
    (
        compile(r"iki \d+ metų"), 
        lambda _: r"iki %s metų" % (
            get_number_complex_name(
                value=randint(10,100),
                category_type='Kiekiniai',
                category_subtype='Pagrindiniai',
                number='dgs',
                gender='vyr. g.',
                case='kilm.')[0]
        )
    ),
    (
        compile(r"egužės \d+ dieną"), 
        lambda _: r"egužės %s dieną" % (
            get_number_complex_name(
                value=randint(10,100),
                category_type='Kelintiniai',
                category_subtype='Neįvardžiuotiniai',
                number='vns',
                gender='vyr. g.',
                case='gal.')[0]
        )
    ),
    (
        compile(r"\d+-\d+ metų"), 
        lambda _: r"%s %s metų" % (
            get_number_complex_name(
                value=randint(1,100),
                category_type='Kiekiniai',
                category_subtype='Dauginiai',
                number='dgs',
                gender='vyr. g.',
                case='kilm.')[0],
                
            get_number_complex_name(
                value=randint(1,100),
                category_type='Kiekiniai',
                category_subtype='Dauginiai',
                number='dgs',
                gender='vyr. g.',
                case='kilm.')[0]
        )
    ),
    (
        compile(r"\d+-\d+ tūkstančių"), 
        lambda _: r"%s %s tūkstančių" % (
            get_number_complex_name(
                value=randint(2,100),
                category_type='Kiekiniai',
                category_subtype='Dauginiai',
                number='dgs',
                gender='vyr. g.',
                case='kilm.')[0],
                
            get_number_complex_name(
                value=rand_few(),
                category_type='Kiekiniai',
                category_subtype='Dauginiai',
                number='dgs',
                gender='vyr. g.',
                case='kilm.')[0]
        )
    ),
    (
        compile(r"\d+ tūkstančių"), 
        lambda _: r"%s tūkstančių" % (
            get_number_complex_name(
                value=rand_few(),
                category_type='Kiekiniai',
                category_subtype='Dauginiai',
                number='dgs',
                gender='vyr. g.',
                case='kilm.')[0]
        )
    ),
    (
        compile(r"prieš \d+ metų"), 
        lambda _: r"prieš %s metų" % (
            get_number_complex_name(
                value=randint(10,20) + pow(10, randint(0, 3)),
                category_type='Kiekiniai',
                category_subtype='Dauginiai',
                number='dgs',
                gender='vyr. g.',
                case='vard.')[0]
        )
    ),
    (
        compile(r"iki \d+ metų"), 
        lambda _: r"iki %s metų" % (
            get_number_complex_name(
                value=randint(1,300),
                category_type='Kelintiniai',
                category_subtype='Pagrindiniai',
                number='dgs',
                gender='vyr. g.',
                case='kilm.')[0]
        )
    ),
    (
        compile(r"\d+-ųjų"), 
        lambda _: "{}".format(
            get_number_complex_name(
                value=randint(1000,3000),
                category_type='Kelintiniai',
                category_subtype='Įvardžiuotiniai',
                number='dgs',
                gender='vyr. g.',
                case='kilm.')[0]
        )
    ),
    (
        compile(r"\d+-ąjį"), 
        lambda _: "{}".format(
            get_number_complex_name(
                value=randint(1,10000),
                category_type='Kelintiniai',
                category_subtype='Įvardžiuotiniai',
                number='vns',
                gender='vyr. g.',
                case='gal.')[0]
        )
    ),
    (
        compile(r"\d+-erių"), 
        lambda _: "{}".format(
            get_number_complex_name(
                value=randint(1,200),
                category_type='Kiekiniai',
                category_subtype='Dauginiai',
                number='dgs',
                gender='vyr. g.',
                case='kilm.')[0]
        )
    ),
    (
        compile(r"\d+-ąją"), 
        lambda _: "{}".format(
            get_number_complex_name(
                value=randint(1000,3000),
                category_type='Kelintiniai',
                category_subtype='Įvardžiuotiniai',
                number='vns',
                gender='mot. g.',
                case='gal.')[0]
        )
    ),
    (
        compile(r"\d+-osios"), 
        lambda _: "{}".format(
            get_number_complex_name(
                value=randint(1,999),
                category_type='Kelintiniai',
                category_subtype='Įvardžiuotiniai',
                number='vns',
                gender='mot. g.',
                case='kilm.')[0]
        )
    ),
    (
        compile(r"\d+-ajam"), 
        lambda _: "{}".format(
            get_number_complex_name(
                value=randint(1,999),
                category_type='Kelintiniai',
                category_subtype='Įvardžiuotiniai',
                number='vns',
                gender='vyr. g.',
                case='naud.')[0]
        )
    ),
    (
        compile(r"\d+-oji"), 
        lambda _: "{}".format(
            get_number_complex_name(
                value=randint(1,999),
                category_type='Kelintiniai',
                category_subtype='Įvardžiuotiniai',
                number='vns',
                gender='mot. g.',
                case='vard.')[0]
        )
    ),
    (
        compile(r"o \d+ dieną"), 
        lambda _: "o {} dieną".format(
            get_number_complex_name(
                value=randint(1,60),
                category_type='Kelintiniai',
                category_subtype='Įvardžiuotiniai',
                number='vns',
                gender='mot. g.',
                case='gal.')[0]
        )
    ),
    (
        compile(r"nuo \d+ iki \d+"),
        lambda _: r"nuo %s iki %s" % (
            get_number_complex_name(
                value=randint(2,100),
                category_type='Kiekiniai',
                category_subtype='Dauginiai',
                number='dgs',
                gender='vyr. g.',
                case='kilm.')[0],
                
            get_number_complex_name(
                value=randint(2,100),
                category_type='Kiekiniai',
                category_subtype='Dauginiai',
                number='dgs',
                gender='vyr. g.',
                case='kilm.')[0]
        )
    ),
    (
        compile(r"\d+ straipsnio"), 
        lambda _: "{} straipsnio".format(
            get_number_complex_name(
                value=randint(1,999),
                category_type='Kelintiniai',
                category_subtype='Neįvardžiuotiniai',
                number='vns',
                gender='vyr. g.',
                case='kilm.')[0]
        )
    ),
    (
        compile(r"\d+ m aukšč?io"),  # metro vns
        lambda _: "{} metrų aukščio".format(
            get_number_complex_name(
                value=rand_few(),
                category_type='Kiekiniai',
                number='dgs',
                gender='vyr. g.',
                case='kilm.')[0]
        )
    ),
    (
        compile(r"\d+ m ilgio"),  # metro vns
        lambda _: "{} metrų ilgio".format(
            get_number_complex_name(
                value=rand_few(),
                category_type='Kiekiniai',
                number='dgs',
                gender='vyr. g.',
                case='kilm.')[0]
        )
    ),
    (
        compile(r"\d+ valandą"),  # metro vns
        lambda _: "{} valandą".format(
            get_number_complex_name(
                value=rand_ones(),
                category_type='Kelintiniai',
                category_subtype='Neįvardžiuotiniai',
                number='vns',
                gender='mot. g.',
                case='gal.')[0]
        )
    ),
    (
        compile(r"\d+ valandų"),  # metro vns
        lambda _: "{} valandą".format(
            get_number_complex_name(
                value=rand_few(),
                category_type='Kiekiniai',
                number='dgs',
                gender='mot. g.',
                case='kilm.')[0]
        )
    ),
    (
        compile(r"\d+ minučių"),  # metro vns
        lambda _: "{} minučių".format(
            get_number_complex_name(
                value=rand_few(),
                category_type='Kiekiniai',
                number='dgs',
                gender='mot. g.',
                case='kilm.')[0]
        )
    ),
    (
        compile(r"\d+ metrų"),  # metro vns
        lambda _: "{} metrų".format(
            get_number_complex_name(
                value=rand_few(),
                category_type='Kiekiniai',
                number='dgs',
                gender='mot. g.',
                case='kilm.')[0]
        )
    ),
    (
        compile(r"\d+ metrų"),  # metro vns
        lambda _: "{} metrų".format(
            get_number_complex_name(
                value=rand_few(),
                category_type='Kiekiniai',
                number='dgs',
                gender='mot. g.',
                case='kilm.')[0]
        )
    ),
    (
        compile(r"straipsnio \d+ ir \d+ dalies"), 
        lambda _: "straipsnio {} ir {} dalies".format(
            get_number_complex_name(
                value=randint(1,100),
                category_type='Kelintiniai',
                category_subtype='Neįvardžiuotiniai',
                number='vns',
                gender='mot. g.',
                case='kilm.')[0],
            get_number_complex_name(
                value=randint(1,100),
                category_type='Kelintiniai',
                category_subtype='Neįvardžiuotiniai',
                number='vns',
                gender='mot. g.',
                case='kilm.')[0]
        )
    ),
    (
        compile(r"Nr\. \d+-\d+"), 
        lambda _: "numeris {} {}".format(
            get_number_complex_name(value=randint(1,99))[0],
            get_number_complex_name(value=randint(1,999))[0]
        )
    )
]

if __name__ == '__main__':
    num_lines = set([])
    with open('__final_1.split.txt', 'w', encoding="utf8") as f_out:
        for line in split_lines():
            f_out.write(line + '\n')
            line = ps.sub('', line)
            if n1.match(line):
                num_lines.add(line)

    num_lines = list(num_lines)
    num_lines.sort()
    
    with open('__final_1.split.num.txt', 'w', encoding="utf8") as fn_out:
        for line in num_lines:
            fn_out.write(line + '\n')
        
    with open('__final_1.split.num.up.txt', 'w', encoding="utf8") as fn_out:
        while num_lines:
            line = num_lines.pop()
            if "kovo 17 dieną" in line:
                line = line
            for p, s_ in modifiers:
                if not isinstance(s_, list):
                    s_ = [s_]
                
                for s in s_:
                    m = p.search(line)
                    if m:
                        line = p.sub(s, line).strip()
                        line = line[0].upper() + line[1:]

            if n1.match(line):
                fn_out.write(line + '\n')