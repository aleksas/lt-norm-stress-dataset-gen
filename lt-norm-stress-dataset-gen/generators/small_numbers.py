from random import randint, sample

from .utils import increment_stats
from .numbers import gen_pair_with_ending

from static.get_skaitvardis import get_number_complex_name

def generate_small_values_linked_pairs(config):
  small_linked_num_repeat = config['small_linked_num_repeat']

  options = [
    (range(1, 10), [0, 2, 3], [0, 2, 3, 5, 7]),
    (range(10, 100), [0, 3], [0, 3, 5, 7]),
    (range(10, 100), [0, 5], [0, 5, 7, 9])
    ]

  for _ in range(small_linked_num_repeat):
    for o in options:
      for i in o[0]:
        p1 = sample(o[1], 1)[0]
        p2 = sample(o[2], 1)[0]
        j = i * pow(10, p1)
        i += pow(10, p2) 
        yield i, j
      
def generate_small_values(config):
  small_num = config['small_num']
  small_num_repeat = config['small_num_repeat']

  for _ in range(small_num_repeat):
    for i in range(small_num):
      yield i

def generate_small_number_linked_pairs(config):
  small_pair_values = generate_small_values_linked_pairs(config)

  for i, j in small_pair_values:
    
    number_name_i, _ = get_number_complex_name(value=i, stress=config['stress'])
    number_name_j, _ = get_number_complex_name(value=j, stress=config['stress'])

    i, j = str(i), str(j) 
    i_s, j_s = number_name_i, number_name_j

    increment_stats()
    yield ('%s %s' % (i, j)), ('%s %s' % (i_s, j_s))

def generate_small_number_pairs(config):
  thrs_ending_add = config['thrs_ending_add']

  small_values = generate_small_values(config)

  #add additional <50 numbers, 1000 times each 
  for i in small_values:
    v = randint(0, i)
    
    gen_dup = randint(1, 100) < config['num_duplicate_p']

    v, vs = gen_pair_with_ending(v, thrs_ending_add, config['stress'])

    increment_stats()
    yield v, vs
    
    if gen_dup:
      increment_stats()
      yield v, vs