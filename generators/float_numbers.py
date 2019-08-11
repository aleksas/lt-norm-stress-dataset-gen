from random import randint, sample
from math import log10

from static.get_skaitvardis import get_number_complex_name
from static.get_text import rand_ones, rand_few, rand_many

from .utils import generate_values_, increment_stats, default_stress

def generate_float_pairs(config, case='vard.'):
  values = generate_values_(
    config['float_max_pow'], 
    config['float_pow_range'],
    config['float_num_repeat']
  )

  for i in values:
    r = randint(1, 9)
    if r <= 3:
      v = i + randint(0, i)
    elif r <= 6:
      v = randint(0, i)
    elif r <= 8:
      v = i
    else:
      v = 0

    number_name = [get_number_complex_name(value=v, stress=config['stress'])[0], 'ir'] if v else []

    fractions = [
      (rand_ones(), "vns", "vard."),  # viena tūkstantoji
      (rand_few(), "dgs", "vard."), # dvi dešimtosios
      (rand_many(), "dgs", "kilm."),   # dešimt penkioliktųjų
    ]

    for fv, fn, fc in fractions:
      if not fv:
        continue
      fraction_name, _ = get_number_complex_name(
        value=fv, category_type="Kiekiniai",
        category_subtype="Pagrindiniai",
        gender="mot. g.", case=case, stress=config['stress']
      )

      fp = pow(10, int(log10(fv)) + 1)
      
      fraction_size_name, _ = get_number_complex_name(
        value=fp, category_type="Kelintiniai",
        category_subtype="Įvardžiuotiniai", number=fn, 
        gender="mot. g.", case=fc, stress=config['stress']
      )
    
      combined_v = '%d,%d' % (v, fv)
      combined_name = ' '.join(number_name + [fraction_name, fraction_size_name])

      increment_stats()
      
      yield combined_v, combined_name