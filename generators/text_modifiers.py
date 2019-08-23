from random import randint, sample, seed, choice
from static.get_skaitvardis import get_number_complex_name, Stress
from string import ascii_uppercase
from re import compile

seed(0)

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

def rand_few_or_many(max=1000):
    return choice([rand_few(max), rand_many(max)])

stress=Stress.ASCII

# Kiekiniai/ Pagrindiniai

kiek_pagr_dgs_vyr_vard = {
    'category_type':'Kiekiniai',
    'category_subtype':'Pagrindiniai',
    'number':'dgs',
    'gender':'vyr. g.',
    'case':'vard.',
    'stress':stress
}

kiek_pagr_dgs_mot_kilm = {**kiek_pagr_dgs_vyr_vard, 'gender':'mot. g.', 'case':'kilm.'}

kiek_pagr_dgs_vyr_gal = {**kiek_pagr_dgs_vyr_vard, 'case':'gal.'}
kiek_pagr_dgs_vyr_kilm = {**kiek_pagr_dgs_vyr_vard, 'case':'kilm.'}
kiek_pagr_vns_vyr_kilm = {**kiek_pagr_dgs_vyr_kilm, 'number':'vns'}
kiek_pagr_vns_vyr_vard = {**kiek_pagr_dgs_vyr_vard, 'number':'vns'}

kiek_daug_dgs_vyr_vard = {**kiek_pagr_dgs_vyr_vard, 'category_subtype':'Dauginiai'}
kiek_daug_dgs_vyr_kilm = {**kiek_daug_dgs_vyr_vard, 'case':'kilm.'}

kelin_ivard_dgs_vyr_vard = {**kiek_pagr_dgs_vyr_vard, 'category_type':'Kelintiniai', 'category_subtype':'Įvardžiuotiniai'}
kelin_ivard_dgs_vyr_gal = {**kelin_ivard_dgs_vyr_vard, 'case':'gal.'}
kelin_ivard_dgs_vyr_kilm = {**kelin_ivard_dgs_vyr_vard, 'case':'kilm.'}
kelin_ivard_dgs_vyr_inag = {**kelin_ivard_dgs_vyr_vard, 'case':'įnag.'}
kelin_ivard_vns_vyr_gal = {**kelin_ivard_dgs_vyr_gal, 'number':'vns'}
kelin_ivard_vns_vyr_naud = {**kelin_ivard_vns_vyr_gal, 'case':'naud.'}
kelin_ivard_vns_vyr_vard = {**kelin_ivard_vns_vyr_gal, 'case':'vard.'}

kelin_ivard_vns_mot_gal = {**kelin_ivard_dgs_vyr_gal, 'gender':'mot. g.'}
kelin_ivard_vns_mot_kilm = {**kelin_ivard_vns_mot_gal, 'case':'kilm.'}
kelin_ivard_vns_mot_vard = {**kelin_ivard_vns_mot_gal, 'case':'vard.'}
kelin_ivard_vns_mot_inag = {**kelin_ivard_vns_mot_gal, 'case':'įnag.'}

kelin_neivard_dgs_vyr_vard = {**kelin_ivard_dgs_vyr_vard, 'category_subtype':'Neįvardžiuotiniai'}
kelin_neivard_dgs_vyr_kilm = {**kelin_ivard_dgs_vyr_vard, 'case':'kilm.'}
kelin_neivard_dgs_vyr_inag = {**kelin_ivard_dgs_vyr_vard, 'case':'įnag.'}
kelin_neivard_dgs_vyr_gal  = {**kelin_ivard_dgs_vyr_vard, 'case':'gal.'}

kelin_neivard_vns_vyr_kilm = {**kelin_neivard_dgs_vyr_kilm, 'number':'vns'}
kelin_neivard_vns_vyr_viet = {**kelin_neivard_vns_vyr_kilm, 'case':'viet.'}
kelin_neivard_vns_vyr_vard = {**kelin_neivard_vns_vyr_viet, 'case':'vard.'}
kelin_neivard_vns_vyr_gal = {**kelin_neivard_vns_vyr_viet, 'case':'gal.'}

kelin_neivard_dgs_mot_kilm = {**kelin_neivard_dgs_vyr_kilm, 'gender':'mot. g.'}
kelin_neivard_vns_mot_kilm = {**kelin_neivard_dgs_mot_kilm, 'number':'vns'}
kelin_neivard_vns_mot_viet = {**kelin_neivard_vns_mot_kilm, 'case':'kilm.'}
kelin_neivard_vns_mot_gal = {**kelin_neivard_vns_mot_kilm, 'case':'gal.'}

modifiers = [
    (
        compile(r"[„“]"), 
        lambda _: "\""
    ),
    (
        compile(r"–"), 
        lambda _: r"-"
    ),
    (
        compile(r" \d+,5 "), 
        lambda _: r" %s su puse " % (
            get_number_complex_name(value=randint(10,100),**kiek_pagr_dgs_vyr_vard)[0]
        )
    ),
    (
        compile(r" iš daugiau nei \d+ šalių"), 
        lambda _: r" iš daugiau nei %s šalių" % (
            get_number_complex_name(value=randint(2,100), **kiek_pagr_dgs_mot_kilm)[0]
        )
    ),
    (
        compile(r" iš daugiau nei \d+ šalių"), 
        lambda _: r" iš daugiau nei %s šalies" % (
            get_number_complex_name(value=1, **kiek_pagr_dgs_mot_kilm)[0]
        )
    ),
    (
        compile(r"\d+ ar \d+ metu`s"), 
        lambda _: r"%s ar %s metu`s" % ((
            get_number_complex_name(value=randint(2,100), **kiek_pagr_dgs_vyr_gal)[0]
        ),(
            get_number_complex_name(value=randint(2,100), **kiek_pagr_dgs_vyr_gal)[0]
        ))
    ),
    (
        compile(r"prieš \d+ me~tų"), 
        lambda _: r"prieš %s me~tų" % (
            get_number_complex_name(value=randint(10,100), **kiek_pagr_dgs_vyr_kilm)[0]
        )
    ),
    (
        compile(r"kaip \d+ me~tų"), 
        lambda _: r"kaip %s me~tų" % (
            get_number_complex_name(value=randint(10,100), **kiek_pagr_dgs_vyr_kilm)[0]
        )
    ),
    (
        compile(r"\d{2,3} me~tų"), 
        lambda _: r"%s metų" % (
            get_number_complex_name(value=randint(10,999), **kiek_pagr_dgs_vyr_kilm)[0]
        )
    ),
    (
        compile(r"\d+ val\. perio`dui"), 
        lambda _: r"%s valandų perio`dui" % (
            get_number_complex_name(value=randint(10,999), **kiek_pagr_dgs_vyr_kilm)[0]
        )
    ),
    (
        compile(r"\d+ va~landą"), 
        lambda _: r"%s va~landą" % (
            get_number_complex_name(value=randint(1,100), **kelin_neivard_vns_mot_gal)[0]
        )
    ),
    (
        compile(r"\d+ milijo~nai"), 
        lambda _: r"%s milijo~nai" % (
            get_number_complex_name(value=rand_few(), **kiek_pagr_dgs_vyr_vard)[0]
        )
    ),
    (
        compile(r"\d+ tūkst. li`tų"), 
        [
            lambda _: r"%s tū^kstantis li`tų" % get_number_complex_name(value=rand_ones(), **kiek_pagr_vns_vyr_vard)[0],
            lambda _: r"%s tū^kstančiai li`tų" % get_number_complex_name(value=rand_few(), **kiek_pagr_dgs_vyr_vard)[0],
            lambda _: r"%s tū^kstančių li`tų" % get_number_complex_name(value=rand_many(), **kiek_pagr_dgs_vyr_kilm)[0]
        ]
    ),
    (
        compile(r"\d+ tū\^kstančių"), 
        [
            lambda _: r"%s tū^kstančių" % get_number_complex_name(value=rand_many(), **kiek_pagr_dgs_vyr_kilm)[0]
        ]
    ),
    (
        compile(r"\d+ mln. li`tų"), 
        [
            lambda _: r"%s milijo~nas li`tų" % get_number_complex_name(value=rand_ones(), **kiek_pagr_vns_vyr_vard)[0],
            lambda _: r"%s milijo~nai li`tų" % get_number_complex_name(value=rand_few(), **kiek_pagr_dgs_vyr_vard)[0],
            lambda _: r"%s milijo~nų li`tų" % get_number_complex_name(value=rand_many(), **kiek_pagr_dgs_vyr_kilm)[0]
        ]
    ),
    (
        compile(r"\d+ li`tų"), 
        lambda _: r"%s li`tų" % get_number_complex_name(value=rand_many(), **kiek_pagr_dgs_vyr_kilm)[0]
    ),
    (
        compile(r" \d+ litu`s"), 
        lambda _: r" %s litu`s" % get_number_complex_name(value=rand_few_or_many(), **kiek_pagr_dgs_vyr_gal)[0]
    ),
    (
        compile(r"\d+ keleivių"), 
        [
            lambda _: r"%s keleivis" % get_number_complex_name(value=rand_ones(), **kiek_pagr_vns_vyr_vard)[0],
            lambda _: r"%s keleiviai" % get_number_complex_name(value=rand_few(), **kiek_pagr_dgs_vyr_vard)[0],
            lambda _: r"%s keleivių" % get_number_complex_name(value=rand_many(), **kiek_pagr_dgs_vyr_kilm)[0]
        ]
    ),    
    (
        compile(r"\d+ valandas"), 
        lambda _: r"%s valandas" % (
            get_number_complex_name(value=rand_few(),  **kiek_pagr_dgs_vyr_vard)[0]
        )
    ),  
    (
        compile(r"^\d+ (?=[A-ZĄ-Ž][a-zą-ž`~\^])"), 
        lambda _: r"%s " % (
            get_number_complex_name(value=randint(1,50),  **kiek_pagr_dgs_vyr_vard)[0]
        )
    ),
    (
        compile(r"^\d+\."), 
        lambda _: r"%s." % (
            get_number_complex_name(value=randint(2,100), **kiek_pagr_dgs_vyr_vard)[0]
        )
    ),
    (
        compile(r"^\d+\)"), 
        lambda _: r"%s)" % (
            get_number_complex_name(value=randint(2,100), **kiek_pagr_dgs_vyr_vard)[0]
        )
    ),
    (
        compile(r"N[Rr]\. \d+ \"D"), 
        lambda _: r"Nu`meris %s \"D" % (
            get_number_complex_name(value=randint(1,100), **kiek_pagr_dgs_vyr_vard)[0]
        )
    ),
    (
        compile(r"N[Rr]\. \d+-\d+"), 
        lambda _: r"Nu`meris %s - %s" % (
            get_number_complex_name(value=randint(1,100), **kiek_pagr_vns_vyr_vard)[0],
            get_number_complex_name(value=randint(1,100), **kiek_pagr_vns_vyr_vard)[0]
        )
    ),
    (
        compile(r"žr\. \d+ pav."), 
        lambda _: r"žiūrė^kite %s paveikslė~lį" % (
            get_number_complex_name(value=rand_ones(), **kelin_neivard_vns_vyr_gal)[0]
        )
    ),
    (
        compile(r"\(\d+ pav.\)"), 
        lambda _: r"(%s paveikslė~lis)" % (
            get_number_complex_name(value=rand_ones(), **kelin_neivard_vns_vyr_vard)[0]
        )
    ),
    (
        compile(r"žr\."), 
        lambda _: r"žiūrė^kite"
    ),
    (
        compile(r"\d+ dalyje"), 
        lambda _: r"%s dalyje" % (
            get_number_complex_name(value=randint(1,100),**kelin_neivard_vns_mot_viet)[0]
        )
    ),
    (
        compile(r"\d+ dalies"), 
        lambda _: r"%s dalies" % (
            get_number_complex_name(value=randint(1,100),**kelin_neivard_vns_mot_kilm)[0]
        )
    ),
    (
        compile(r"\d+ punkte"), 
        lambda _: r"%s punkte" % (
            get_number_complex_name(value=randint(1,100),**kelin_neivard_vns_vyr_viet)[0]
        )
    ),
    (
        compile(r"\d+ me~tais"), 
        lambda _: r"%s me~tais" % (
            get_number_complex_name(value=randint(10,3000),**kelin_neivard_dgs_vyr_inag)[0]
        )
    ),
    (
        compile(r"\d+-ai~?siais"), 
        lambda _: r"%s" % (
            get_number_complex_name(value=randint(1,3000), **kelin_ivard_dgs_vyr_inag)[0]
        )
    ),
    
    (
        compile(r"\d+ klasėje"), 
        lambda _: r"%s klasėje" % (
            get_number_complex_name(value=randint(1, 20),**kelin_ivard_vns_mot_inag)[0]
        )
    ),
    (
        compile(r"\d{4} me~tų"), 
        lambda _: r"%s me~tų" % (
            get_number_complex_name(value=randint(1000,3000), **kelin_ivard_dgs_vyr_kilm)[0]
        )
    ),
    (
        compile(r"\d+\(\d+\) stra\^ipsnis"), 
        lambda _: r"%s(%s) stra^ipsnis" % ((
            get_number_complex_name(value=randint(1,3000),**kelin_neivard_vns_vyr_vard)[0]
        ),(
            get_number_complex_name(value=randint(2,100), **kiek_pagr_dgs_vyr_vard)[0]
        ))
    ),

    (
        compile(r"\d+ stra\^ipsnio"), 
        lambda _: r"%s stra^ipsnio" % (
            get_number_complex_name(value=randint(1,100),**kelin_neivard_vns_vyr_kilm)[0]
        )
    ),
    (
        compile(r"\d+ stra\^ipsnis"), 
        lambda _: r"%s stra^ipsnis" % (
            get_number_complex_name(value=randint(1,100),**kelin_neivard_vns_vyr_vard)[0]
        )
    ),
    (
        compile(r"\d+ stra\^ipsnio"), 
        lambda _: r"%s stra^ipsnio" % (
            get_number_complex_name(value=randint(1,100),**kelin_neivard_vns_vyr_kilm)[0]
        )
    ),
    (
        compile(r"\d{3,} metu`s"), 
        lambda _: r"%s metu`s" % (
            get_number_complex_name(value=randint(1000,3000), **kelin_ivard_dgs_vyr_gal)[0]
        )
    ),
    (
        compile(r"\d+ dieno~s"), 
        lambda _: r"%s dieno~s" % (
            get_number_complex_name(value=randint(1,100),**kelin_neivard_vns_mot_kilm)[0]
        )
    ),
    (
        compile(r" po \d+ komand"), 
        lambda _: r" po %s komand" % (
            get_number_complex_name(value=randint(10,3000),  **kiek_pagr_dgs_vyr_vard)[0]
        )
    ),
    (
        compile(r" po \d+"), 
        lambda _: r" po %s" % (
            get_number_complex_name(value=randint(10,3000), **kiek_pagr_dgs_vyr_gal)[0]
        )
    ),
    (
        compile(r"\d+-\d+ kartus"), 
        lambda _: r"%s %s kartus" % ((
            get_number_complex_name(value=rand_few(), **kiek_pagr_dgs_vyr_gal)[0]
        ),(
            get_number_complex_name(value=rand_few(), **kiek_pagr_dgs_vyr_gal)[0]
        ))
    ),
    (
        compile(r"\d{4} m. [a-zą-ž]+ \d+ d. įsa~kym"), 
        lambda _: r"%s %s kartus" % ((
            get_number_complex_name(value=rand_few(), **kiek_pagr_dgs_vyr_gal)[0]
        ),(
            get_number_complex_name(value=rand_few(), **kiek_pagr_dgs_vyr_gal)[0]
        ))
    ),
    (
        compile(r"iki \d+ me~tų"), 
        lambda _: r"iki %s me~tų" % (
            get_number_complex_name(value=randint(10,100), **kiek_pagr_dgs_vyr_kilm)[0]
        )
    ),
    (
        compile(r"egužės \d+ dieną"), 
        lambda _: r"egužės %s dieną" % (
            get_number_complex_name(
                value=randint(10,100),**kelin_neivard_vns_vyr_gal)[0]
        )
    ),
    (
        compile(r"\d+-ųjų"), 
        lambda _: "{}".format(
            get_number_complex_name(
                value=randint(1000,3000),**kelin_ivard_dgs_vyr_kilm)[0]
        )
    ),
    (
        compile(r"\d+-ąjį"), 
        lambda _: "{}".format(
            get_number_complex_name(
                value=randint(1,10000),**kelin_ivard_vns_vyr_gal)[0]
        )
    ),
    (
        compile(r"\d+-ąją"), 
        lambda _: "{}".format(
            get_number_complex_name(value=randint(1000,3000),**kelin_ivard_vns_mot_gal)[0]
        )
    ),
    (
        compile(r"\d+-osios"), 
        lambda _: "{}".format(
            get_number_complex_name(value=randint(1,999),**kelin_ivard_vns_mot_kilm)[0]
        )
    ),
    (
        compile(r"\d+-ajam"), 
        lambda _: "{}".format(
            get_number_complex_name(value=randint(1,999),**kelin_ivard_vns_vyr_naud)[0]
        )
    ),
    (
        compile(r"\d+\s+tomas,\s+Nr.\d+"), 
        lambda _: "{} tomas, numeris {}".format(
            get_number_complex_name(value=randint(1,999),**kelin_ivard_vns_vyr_vard)[0],
            get_number_complex_name(value=randint(1,999),**kiek_pagr_vns_vyr_vard)[0]
        )
    ),
    (
        compile(r" [A-Z]-\d+ skyri"), 
        lambda _: "{}-{} skyri".format(
            choice(ascii_uppercase),
            get_number_complex_name(value=randint(1,999),**kiek_pagr_vns_vyr_vard)[0]
        )
    ),
    (
        compile(r" [A-Z]-\d+/[A-Z]-\d+ sky~ri"), 
        lambda _: "{}-{}/{}-{} sky~ri".format(
            choice(ascii_uppercase),
            get_number_complex_name(value=randint(1,999),**kiek_pagr_vns_vyr_vard)[0],
            choice(ascii_uppercase),
            get_number_complex_name(value=randint(1,999),**kiek_pagr_vns_vyr_vard)[0]
        )
    ),
    (
        compile(r" [A-Z]\d+ sky~ri"), 
        lambda _: "{}{} sky~ri".format(
            choice(ascii_uppercase),
            get_number_complex_name(value=randint(1,999),**kiek_pagr_vns_vyr_vard)[0]
        )
    ),
    (
        compile(r"\d+ sky~ri"), 
        lambda _: "{} sky~ri".format(
            get_number_complex_name(value=randint(1,999),**kiek_pagr_vns_vyr_vard)[0]
        )
    ),
    (
        compile(r"\d+-oji"), 
        lambda _: "{}".format(
            get_number_complex_name(value=randint(1,999),**kelin_ivard_vns_mot_vard)[0]
        )
    ),
    (
        compile(r"o \d+ die~ną"), 
        lambda _: "o {} die~ną".format(
            get_number_complex_name(value=randint(1,60),**kelin_ivard_vns_mot_gal)[0]
        )
    ),
    (
        compile(r"\d+ stra\^ipsnio"), 
        lambda _: "{} stra^ipsnio".format(
            get_number_complex_name(value=randint(1,999),**kelin_neivard_vns_vyr_kilm)[0]
        )
    ),
    (
        compile(r"\d+ stra\^ipsnis"), 
        lambda _: "{} stra^ipsnis".format(
            get_number_complex_name(value=randint(1,999),**kelin_neivard_vns_vyr_vard)[0]
        )
    ),
    (
        compile(r"\d+ valandą"),  # metro vns
        lambda _: "{} valandą".format(
            get_number_complex_name(value=rand_ones(),**kelin_neivard_vns_mot_gal)[0]
        )
    ),
    (
        compile(r"\d+-\d+ me~tų"), 
        lambda _: r"%s %s me~tų" % (
            get_number_complex_name(value=randint(1,100),**kiek_daug_dgs_vyr_kilm)[0],                
            get_number_complex_name(value=randint(1,100),**kiek_daug_dgs_vyr_kilm)[0]
        )
    ),
    (
        compile(r"\d+-\d+ tū\^kstančių"), 
        lambda _: r"%s %s tū^kstančių" % (
            get_number_complex_name(value=randint(2,100),**kiek_daug_dgs_vyr_kilm)[0],                
            get_number_complex_name(value=rand_few(),**kiek_daug_dgs_vyr_kilm)[0]
        )
    ),
    (
        compile(r"\d+ tū\^kstančių"), 
        lambda _: r"%s tū^kstančių" % (
            get_number_complex_name(value=rand_few(),**kiek_daug_dgs_vyr_kilm)[0]
        )
    ),
    (
        compile(r"\d+ milijo~nų"), 
        lambda _: r"%s milijo~nų" % (
            get_number_complex_name(value=rand_few(),**kiek_daug_dgs_vyr_kilm)[0]
        )
    ),
    (
        compile(r"prieš \d+ me~tų"), 
        lambda _: r"prieš %s me~tų" % (
            get_number_complex_name(value=randint(10,20) + pow(10, randint(0, 3)), **kiek_daug_dgs_vyr_vard)[0]
        )
    ),
    (
        compile(r"iki \d+ me~tų"), 
        lambda _: r"iki %s me~tų" % (
            get_number_complex_name(value=randint(1,300), **kiek_pagr_dgs_vyr_kilm)[0]
        )
    ),
    (
        compile(r"\d+-erių"), 
        lambda _: "{}".format(
            get_number_complex_name(value=randint(1,200),**kiek_daug_dgs_vyr_kilm)[0]
        )
    ),
    (
        compile(r"nuo \d+ iki \d+"),
        lambda _: r"nuo %s iki %s" % (
            get_number_complex_name(value=randint(2,100),**kiek_daug_dgs_vyr_kilm)[0],
            get_number_complex_name(value=randint(2,100),**kiek_daug_dgs_vyr_kilm)[0]
        )
    ),
    (
        compile(r"\d+ m aukšč?io"),  # metro vns
        lambda _: "{} metrų aukščio".format(
            get_number_complex_name(value=rand_few(), **kiek_pagr_dgs_vyr_kilm)[0]
        )
    ),
    (
        compile(r"\d+ m il~gio"),  # metro vns
        lambda _: "{} me`trų il~gio".format(
            get_number_complex_name(value=rand_few(), **kiek_pagr_dgs_vyr_kilm)[0]
        )
    ),
    (
        compile(r"\d+ valandų"),  # metro vns
        lambda _: "{} valandų".format(
            get_number_complex_name(value=rand_many(), **kiek_pagr_dgs_mot_kilm)[0]
        )
    ),
    (
        compile(r"\d+ minučių"),  # metro vns
        lambda _: "{} minučių".format(
            get_number_complex_name(value=rand_few(), **kiek_pagr_dgs_mot_kilm)[0]
        )
    ),
    (
        compile(r"\d+ me`trų"),  # metro vns
        lambda _: "{} me`trų".format(
            get_number_complex_name(value=rand_few(), **kiek_pagr_dgs_mot_kilm)[0]
        )
    ),
    (
        compile(r"\d+ me`trų"),  # metro vns
        lambda _: "{} me`trų".format(
            get_number_complex_name(value=rand_few(), **kiek_pagr_dgs_mot_kilm)[0]
        )
    ),
    (
        compile(r"\d{4} m\.(?= ((sau~s)|(vas)|(ko\^v)|(bal)|(gegu)|(bir)|(li\^ep)|(rugp)|(rugs)|(spa~l)|(la~pk)|(gru)))"),  # metro vns
        lambda _: "{} me~tų".format(
            get_number_complex_name(value=randint(1,3000), **kelin_ivard_dgs_vyr_kilm)[0]
        )
    ),    
    (
        compile(r"stra\^ipsnio \d+ ir \d+ dalies"), 
        lambda _: "stra^ipsnio {} ir {} dalies".format(
            get_number_complex_name(value=randint(1,100),**kelin_neivard_vns_mot_kilm)[0],
            get_number_complex_name(value=randint(1,100),**kelin_neivard_vns_mot_kilm)[0]
        )
    ),
    (
        compile(r"Nr\. \d+-\d+"), 
        lambda _: "numeris {} {}".format(
            get_number_complex_name(value=randint(1,99),stress=stress)[0],
            get_number_complex_name(value=randint(1,999),stress=stress)[0]
        )
    )
]
