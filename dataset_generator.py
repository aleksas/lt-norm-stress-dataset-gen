from os import makedirs
from os.path import isfile, join, exists
from errno import EEXIST
from random import sample, seed, choices, choice
from codecs import open
from subprocess import call
from json import dump
from re import compile

from static.get_skaitvardis import Stress
from static.get_zodis import get_cases

from generators.utils import stats
from generators.numbers import generate_number_pairs
from generators.float_numbers import generate_float_pairs
from generators.small_numbers import generate_small_number_pairs, generate_small_number_linked_pairs
from generators.numbers_with_units import generate_float_unit_pairs, generate_number_unit_pairs
from generators.dates import generate_years, generate_months, generate_dates

from utils import remove_stress

import py_compile
py_compile.compile('dataset_generator.py')

# 871341 %
# aštuoni šimtai septyniasdešimt >> missing VIENAS <<< tūkstantis trys šimtai keturiasdešimt vienas procentas  .

def generate_pairs(config):

  def glue_vals(glue_options, vals, strvals):
    glue = [] + choices(glue_options, k=len(vals)) + []

    v  = ''.join([a+b for a,b in zip(vals, glue)])
    vs = ''.join([a+b for a,b in zip(strvals, glue)])

    return v, vs

  unused = []
  vals, strvals = [], []
  pair_count = 0
  avg_vs_len = 0

  glue_options = generate_glue_options()

  pair_generators = []
  pair_generators += [generate_years(config), generate_months(config), generate_dates(config)]
  pair_generators += [generate_number_pairs(config)]
  pair_generators += [generate_number_unit_pairs(config)]
  pair_generators += [generate_float_pairs(config)]
  pair_generators += [generate_float_unit_pairs(config)]
  pair_generators += [generate_small_number_pairs(config)]
  pair_generators += [generate_small_number_linked_pairs(config)]

  while len(pair_generators) > 0 or len(unused) > 0:
    if len(unused) > 0:
      pair = unused.pop()
    else:
      generator = choice(pair_generators)
      pair = next(generator, None)

      if not pair:
        pair_generators.remove(generator)
        continue
      
    val, norm_val = pair
    
    mix = (
      [val] * config['mix_val_weight_val'] + 
      [remove_stress(norm_val, config['stress'])] * config['mix_val_weight_norm'] +
      [norm_val] * config['mix_val_weight_norm_stress'])

    val = choice(mix)
    vals.append(val)
    strvals.append(norm_val)  
    
    v, vs = glue_vals(glue_options, vals, strvals)
    vs_len = len(vs)

    pop = vs_len >= config['max_len']

    avg_vs_len_ = avg_vs_len + (vs_len - avg_vs_len)/(pair_count + 1)

    false_stop = [False] * int(config['max_len'] - avg_vs_len_) # don't stop if current avg less than hanlf len
    true_stop = [True] * max(0, config['max_len'] - len(false_stop))

    stop_here = len(vals) > 0 and choice(true_stop + false_stop)

    if pop or stop_here:
      if pop:
        vals.pop()
        strvals.pop()
        unused.append(pair)

      if len(vals) == 0:
        raise Exception()

      v, vs = glue_vals(glue_options, vals, strvals)
      
      vals.clear()
      strvals.clear()
      
      yield v, vs

      avg_vs_len += (len(vs) - avg_vs_len)/(pair_count + 1)
      pair_count += 1
    else:
      continue
  
  if len(vals) > 0:
    v, vs = glue_vals(glue_options, vals, strvals)
    yield v, vs

def generate_dataset(config):
  #max_pow = config['max_pow']
  #thrs_rnd_add = config['thrs_rnd_add']
  directory = config['directory']

  num_fname = 'num2text_num_p8_v7.txt' #% (max_pow, thrs_rnd_add)
  txt_fname = 'num2text_txt_p8_v7.txt' #% (max_pow, thrs_rnd_add)

  subdirectory = 'num2text-p8-v7' #% (max_pow, thrs_rnd_add)
  subdirectory_path = join(directory, subdirectory)
  number_file, text_file = join(subdirectory_path, num_fname), join(subdirectory_path, txt_fname)
  config_file = join(subdirectory_path, 'config.json')
  stats_file = join(subdirectory_path, 'stats.json')

  if not isfile(number_file) or not isfile(text_file):
    if not exists(subdirectory_path):
        try:
            makedirs(subdirectory_path)
        except OSError as e:
            if e.errno != EEXIST:
                raise e

    with open(config_file, 'w') as fp:
      dump(config, fp, indent=3)

    preview_count = 0
    with open(number_file, 'w') as nf:
      with open(text_file, 'w', 'UTF-8') as tf:
        for pair in generate_pairs(config):
            nf.write(pair[0].strip() + '\n')
            tf.write(pair[1].strip() + '\n')

            if preview_count < config['preview']:
              print(pair[0])
              print(pair[1])
              print()
              preview_count += 1

    with open(stats_file, 'w') as fp:
      dump(stats, fp, indent=3)

    print ('Save data into %s and %s files intto %s' % (number_file, text_file, directory))

  return number_file, text_file, subdirectory

def generate_glue_options(space_size=3):
  sep_chars_a = ' ;\t'
  sep_chars_b = '.,'
  a = [' ' * pre + sc + ' ' * post for pre in range(space_size) for post in range(space_size) for sc in sep_chars_a]
  b = [' ' * pre + sc + ' ' * post for pre in range(space_size) for post in range(1, space_size) for sc in sep_chars_b]
  return a + b

def generate_tar_script(subdirectory):
  call(["tar", "-zcvf", "%s.tar.gz" % subdirectory, "%s/" % subdirectory])
  call(["mv", "num2text-p8-v7.tar.gz", "data/num2text-p8_5-v7.tar.gz"])
  call(["rm", "-r", "num2text-p8-v7"])

if __name__ == "__main__":
  seed(0)

  config = {
    'max_len': 512,
    'max_pow': 9,
    'pow_range': 3,
    'num_repeat': 1,
    'float_max_pow': 7,
    'float_pow_range': 2,
    'float_num_repeat': 1,
    'num_unit_max_pow': 7,
    'num_unit_pow_range': 3,
    'num_unit_repeat': 1,
    'thrs_rnd_add': 7,
    'thrs_ending_add': 5,
    'mix_val_weight_val': 20,
    'mix_val_weight_norm': 4,
    'mix_val_weight_norm_stress': 1,
    'small_num': 100,
    'small_num_repeat': 6000,
    'small_linked_num_repeat': 5000,
    'num_duplicate_p': 1,
    'years': list(range(1, 3600)),
    'years_repeat': 2,
    'months': list(range(12)),
    'days': list(range(1, 32)),
    'days_repeat': 1,
    'date_cases': get_cases(),
    'stress': Stress.ASCII,
    'preview': 100,
    'directory': '.'
  }

  _, _, subdirectory = generate_dataset(config)
  generate_tar_script(subdirectory)
