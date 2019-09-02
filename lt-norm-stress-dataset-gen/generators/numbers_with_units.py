from random import randint, sample
from math import log10
from static.get_skaitvardis import get_number_complex_name, Stress
from static.get_zodis import get_complex_name
from generators.text_modifiers import rand_ones, rand_few, rand_many

from .utils import generate_values_, increment_stats, default_stress
from .float_numbers import generate_float_pairs

unit_expansions = [
  ('%', None, 'procentas', None, 'vyr. g.'),
  ('°C', None, 'laipsnis', ('celsijus', 'vns', 'kilm.'), 'vyr. g.'),
  ('°F', None, 'laipsnis', ('farenheitas', 'vns', 'kilm.'), 'vyr. g.'),
  (['€', ' EUR'], None, 'euras', None, 'vyr. g.'),
  (['$', ' USD'], 'JAV', 'doleris', None, 'vyr. g.')
]

# 871341 %
# aštuoni šimtai septyniasdešimt >> missing VIENAS <<< tūkstantis trys šimtai keturiasdešimt vienas procentas  .

def get_units(case='vard.', number='vns', stress=default_stress, force=False):
  for units, prefix, word, postfix, gender in unit_expansions:
    if not isinstance(units, list):
      units = [units]
    
    word_name = get_complex_name(
      value=word, category_type='All',
      number=number, case=case, stress=stress
    )

    res = []
    if prefix:
      res.append(prefix)
    res.append(word_name)
    if postfix:
      postfix_name = get_complex_name(
        value=postfix[0], category_type='All',
        number=postfix[1], case=postfix[2], stress=stress
      )
      res.append(postfix_name)
    res = ' '.join(res)
    
    for unit in units:
      if case == "vard." or force:
        yield unit, res, gender

      yield res, res, gender

def generate_float_unit_pairs(config, case='vard.'):
    for combined_v, combined_name in generate_float_pairs(config, case):
      for a, b, _ in get_units(number='vns', case='kilm.', stress=config['stress'], force=True):
        glue = sample(['', ' ', '  '], 1)[0] 

        increment_stats()
        yield combined_v + glue + a, combined_name + ' ' + b

def generate_number_unit_pairs(config, case='vard.'):
  values = generate_values_(
    config['num_unit_max_pow'], 
    config['num_unit_pow_range'],
    config['num_unit_repeat']
  )

  for i in values:
    if randint(0,20) != 0:
      continue
      
    i = max(1000, i)
    for c in ["vard.","kilm.","naud.","gal.","įnag.","viet."]:
      numbers = [
        (rand_ones(i), "vns", c, c),
        (rand_few(i),  "dgs", c, c),
        (rand_many(i), "dgs", c, "kilm."),
        (0, "dgs", c, "kilm."),
      ]

      for value, unit_number, unit_case, number_case in numbers:
        if value == 0:
          if randint(0,250) != 0:
            continue

        for unit, unit_name, gender in get_units(number=unit_number, case=unit_case, stress=config['stress']):
          value_name, _ = get_number_complex_name(
            value=value, category_type="Kiekiniai",
            category_subtype="Pagrindiniai",
            gender=gender, case=number_case, stress=config['stress']
          )

          increment_stats()

          yield str(value) + ' ' + unit, value_name + ' ' + unit_name
