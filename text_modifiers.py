from random import randint, sample, seed
from static.get_skaitvardis import get_number_complex_name, Stress
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

stress=Stress.ASCII

# Kiekiniai/ Pagrindiniai

param_group_0 = {
    'category_type':'Kiekiniai',
    'category_subtype':'Pagrindiniai',
    'number':'dgs',
    'gender':'vyr. g.',
    'case':'vard.',
    'stress':stress
}

param_group_1 = {**param_group_0, 'gender':'mot. g.', 'case':'kilm.'}

param_group_2 = {**param_group_0, 'case':'gal.'}
param_group_3 = {**param_group_0, 'case':'kilm.'}
param_group_4 = {**param_group_3, 'number':'vns'}
param_group_5 = {**param_group_0, 'number':'vns'}

modifiers = [
    (
        compile(r" \d+,5 "), 
        lambda _: r" %s su puse " % (
            get_number_complex_name(value=randint(10,100),**param_group_0)[0]
        )
    ),
    (
        compile(r" iš daugiau nei \d+ šalių"), 
        lambda _: r" iš daugiau nei %s šalių" % (
            get_number_complex_name(value=randint(2,100), **param_group_1)[0]
        )
    ),
    (
        compile(r" iš daugiau nei \d+ šalių"), 
        lambda _: r" iš daugiau nei %s šalies" % (
            get_number_complex_name(
                value=1, **param_group_1)[0]
        )
    ),
    (
        compile(r"\d+ ar \d+ metus"), 
        lambda _: r"%s ar %s metus" % ((
            get_number_complex_name(value=randint(2,100), **param_group_2)[0]
        ),(
            get_number_complex_name(value=randint(2,100), **param_group_2)[0]
        ))
    ),
    (
        compile(r"prieš \d+ metų"), 
        lambda _: r"prieš %s metų" % (
            get_number_complex_name(value=randint(10,100), **param_group_3)[0]
        )
    ),
    (
        compile(r"kaip \d+ metų"), 
        lambda _: r"kaip %s metų" % (
            get_number_complex_name(value=randint(10,100), **param_group_3)[0]
        )
    ),
    (
        compile(r"\d{2,3} metų"), 
        lambda _: r"%s metų" % (
            get_number_complex_name(value=randint(10,999), **param_group_3)[0]
        )
    ),
    (
        compile(r"\d+ milijonai"), 
        lambda _: r"%s milijonai" % (
            get_number_complex_name(value=rand_few(), **param_group_0)[0]
        )
    ),
    (
        compile(r"\d+ tūkst. litų"), 
        [
            lambda _: r"%s tūkstis litų" % get_number_complex_name(value=rand_ones(), **param_group_5)[0],
            lambda _: r"%s tūkstčiai litų" % get_number_complex_name(value=rand_few(), **param_group_0)[0],
            lambda _: r"%s tūkstčių litų" % get_number_complex_name(value=rand_many(), **param_group_3)[0]
        ]
    ),    
    (
        compile(r"\d+ valandas"), 
        lambda _: r"%s valandas" % (
            get_number_complex_name(
                value=rand_few(),  **param_group_0)[0]
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
                case='vard.',
                stress=stress)[0]
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
                case='vard.',
                stress=stress)[0]
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
                case='vard.',
                stress=stress)[0]
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
                case='vard.',
                stress=stress)[0]
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
                case='kilm.',
                stress=stress)[0]
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
                case='viet.',
                stress=stress)[0]
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
                case='kilm.',
                stress=stress)[0]
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
                case='viet.',
                stress=stress)[0]
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
                case='vard.',
                stress=stress)[0]
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
                case='kilm.',
                stress=stress)[0]
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
                case='įnag.',
                stress=stress)[0][0]
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
                case='kilm.',
                stress=stress)[0]
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
                case='vard.',
                stress=stress)[0]
        ),(
            get_number_complex_name(
                value=randint(2,100),
                category_type='Kiekiniai',
                category_subtype='Pagrindiniai',
                number='dgs',
                gender='vyr. g.',
                case='vard.',
                stress=stress)[0]
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
                case='gal.',
                stress=stress)[0]
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
                case='kilm.',
                stress=stress)[0]
        )
    ),
    (
        compile(r" po \d+ komand"), 
        lambda _: r" po %s komand" % (
            get_number_complex_name(value=randint(10,3000),  **param_group_0)[0]
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
                case='gal.',
                stress=stress)[0]
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
                case='gal.',
                stress=stress)[0]
        ),(
            get_number_complex_name(
                value=rand_few(),
                category_type='Kiekiniai',
                category_subtype='Pagrindiniai',
                number='dgs',
                gender='vyr. g.',
                case='gal.',
                stress=stress)[0]
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
                case='gal.',
                stress=stress)[0]
        ),(
            get_number_complex_name(
                value=rand_few(),
                category_type='Kiekiniai',
                category_subtype='Pagrindiniai',
                number='dgs',
                gender='vyr. g.',
                case='gal.',
                stress=stress)[0]
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
                case='kilm.',
                stress=stress)[0]
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
                case='gal.',
                stress=stress)[0]
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
                case='kilm.',
                stress=stress)[0],
                
            get_number_complex_name(
                value=randint(1,100),
                category_type='Kiekiniai',
                category_subtype='Dauginiai',
                number='dgs',
                gender='vyr. g.',
                case='kilm.',
                stress=stress)[0]
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
                case='kilm.',
                stress=stress)[0],
                
            get_number_complex_name(
                value=rand_few(),
                category_type='Kiekiniai',
                category_subtype='Dauginiai',
                number='dgs',
                gender='vyr. g.',
                case='kilm.',
                stress=stress)[0]
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
                case='kilm.',
                stress=stress)[0]
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
                case='vard.',
                stress=stress)[0]
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
                case='kilm.',
                stress=stress)[0]
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
                case='kilm.',
                stress=stress)[0]
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
                case='gal.',
                stress=stress)[0]
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
                case='kilm.',
                stress=stress)[0]
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
                case='gal.',
                stress=stress)[0]
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
                case='kilm.',
                stress=stress)[0]
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
                case='naud.',
                stress=stress)[0]
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
                case='vard.',
                stress=stress)[0]
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
                case='gal.',
                stress=stress)[0]
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
                case='kilm.',
                stress=stress)[0],
                
            get_number_complex_name(
                value=randint(2,100),
                category_type='Kiekiniai',
                category_subtype='Dauginiai',
                number='dgs',
                gender='vyr. g.',
                case='kilm.',
                stress=stress)[0]
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
                case='kilm.',
                stress=stress)[0]
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
                case='kilm.',
                stress=stress)[0]
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
                case='kilm.',
                stress=stress)[0]
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
                case='gal.',
                stress=stress)[0]
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
                case='kilm.',
                stress=stress)[0]
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
                case='kilm.',
                stress=stress)[0]
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
                case='kilm.',
                stress=stress)[0]
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
                case='kilm.',
                stress=stress)[0]
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
                case='kilm.',
                stress=stress)[0],
            get_number_complex_name(
                value=randint(1,100),
                category_type='Kelintiniai',
                category_subtype='Neįvardžiuotiniai',
                number='vns',
                gender='mot. g.',
                case='kilm.',
                stress=stress)[0]
        )
    ),
    (
        compile(r"Nr\. \d+-\d+"), 
        lambda _: "numeris {} {}".format(
            get_number_complex_name(value=randint(1,99),
                stress=stress)[0],
            get_number_complex_name(value=randint(1,999),
                stress=stress)[0]
        )
    )
]
