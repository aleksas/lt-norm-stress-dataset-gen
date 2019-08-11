from static.get_skaitvardis import get_number_complex_name
from static.get_zodis import get_complex_name
from random import choice, randint

from .utils import increment_stats, default_stress

def get_dates(year, month=None, day=None, case='vard.', stress=default_stress):
  if day and case == 'įnag.' or (not month and not day):
    case = 'vard.'

  if not month:
    case = 'vard.'
    
    number_name, _ = get_number_complex_name(
      value=year, category_type='Kelintiniai',
      category_subtype='Įvardžiuotiniai', gender='vyr. g.',
      number='dgs', case=case, stress=stress
    )

    word_name = get_complex_name(
      value='metai', category_type='All',
      number='dgs', case=case, stress=stress
    )
    
    yield "%d m." % year, number_name + ' ' + word_name
  else:
    number_name, _ = get_number_complex_name(
      value=year, category_type='Kelintiniai',
      category_subtype='Įvardžiuotiniai', gender='vyr. g.',
      number='dgs', case='kilm.', stress=stress
    )

    word_name = get_complex_name(
      value='metai', category_type='All',
      number='dgs', case='kilm.', stress=stress
    )
    
    y_in, y_out = ("%d m. " % year), (number_name + ' ' + word_name + ' ')
      
    if not day:
      m = get_complex_name(
        value=month, category_type="Month",
        number='vns', case=case, stress=stress)

      yield y_in + m, y_out + m

    else:
      m = get_complex_name(
        value=month, category_type="Month",
        number='vns', case='kilm.', stress=stress)
        
      ym_in = y_in + m
      ym_out = y_out + m

      number_name, _ = get_number_complex_name(
        value=day, category_type='Kelintiniai',
        category_subtype='Įvardžiuotiniai', gender='mot. g.',
        number='vns', case=case, stress=stress
      )

      word_name = get_complex_name(
        value='diena', category_type='All',
        number='vns', case=case, stress=stress
      )

      ymd_in = [
        (ym_in + choice(['', ' ']) + str(day) + choice(['', ' ']) + word_name)
      ]

      if case == 'vard.':
        ymd_in += [
          (ym_in + str(day) + ' d.'),
          ("%d-%d-%d" % (year, month, day)),
          ("%d-%02d-%02d" % (year, month, day))
        ]

      ymd_out = ym_out + ' ' + number_name + ' ' + word_name

      yield choice(ymd_in), ymd_out

def generate_years(config):
  for case in config['date_cases']:
    for _ in range(config['years_repeat']):
      for _ in range(len(config['years'])):
        y = choice(config['years'])
        for y_pair in get_dates(y, case=case,stress=config['stress']):

          increment_stats()

          yield y_pair

def generate_months(config):
  for case in config['date_cases']:
    for _ in range(len(config['years'])):
      y = choice(config['years'])
      for _ in range(len(config['months'])):
        m = choice(config['months'])
        if randint(1, 10) <= 6:
          continue
          
        for m_pair in get_dates(y, m, case=case, stress=config['stress']):

          increment_stats()

          yield m_pair

def generate_dates(config):
  for case in config['date_cases']:
    for _ in range(config['days_repeat']):
      for _ in range(len(config['years'])):
        y = choice(config['years'])
        for _ in range(len(config['months'])):
          m = choice(config['months'])
          for _ in range(len(config['days'])):
            d = choice(config['days'])
            for d_pair in get_dates(y, m, d, case=case, stress=config['stress']):
              if randint(1, 10) <= 8:
                continue

              increment_stats()

              yield d_pair