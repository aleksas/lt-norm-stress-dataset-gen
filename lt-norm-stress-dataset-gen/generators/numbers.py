from random import randint, choice

from .utils import generate_values, increment_stats
from static.get_skaitvardis import get_number_complex_name, get_number_forms, Stress

def gen_pair_with_ending(x, threshold, stress):
  complex_name, number_splits = get_number_complex_name(value=x, stress=stress)

  if x != 0 and randint(1, 10) <= threshold:
    last_split_num = number_splits[-1][0]
    name_splits = complex_name.split()[:-1]
    number_forms = get_number_forms(stress)[0][last_split_num]
    all_number_forms_no, unique_paths = get_number_forms(Stress.No)
    number_forms_no = all_number_forms_no[last_split_num]

    path = choice(unique_paths[last_split_num])

    _, ending = number_forms_no[path]
    name, _ = number_forms[path]

    name_splits.append(name)
  
    return '%d-%s' % (x, ending), ' '.join(name_splits)
  else:
    return str(x), complex_name

def generate_number_pairs(config):
  thrs_ending_add = config['thrs_ending_add']

  values = generate_values(config)

  for i in values:
    r = randint(1, 9)
    if r <= 3:
      v = i + randint(0, i)
    elif r <= 6:
      v = randint(0, i)
    else:
      v = i

    gen_dup = randint(1, 100) < config['num_duplicate_p']

    v, number_name = gen_pair_with_ending(v, thrs_ending_add, stress=config['stress'])

    increment_stats()
    yield v, number_name

    if gen_dup:
      increment_stats()
      yield v, number_name