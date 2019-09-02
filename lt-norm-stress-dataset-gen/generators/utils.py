from static.get_skaitvardis import Stress
from sys import _getframe

default_stress = Stress.No

stats = {}

def increment_stats():
  fn =  _getframe(1).f_code.co_name

  if fn not in stats:
    stats[fn] = 0
  stats[fn] += 1

def generate_values_(max_pow, pow_range, num_repeat):
  for _ in range(num_repeat):
    last = 0
    step = 0
    for p in range(0, max_pow):
      start = last + step
      end = int(pow(10, p + 1))
      step = max(1, pow(10, max(0, p - pow_range)))
      for i in range(start, end, step):
        last = i
        yield i

def generate_values(config):
  return generate_values_(
          config['max_pow'],
          config['pow_range'],
          config['num_repeat']
        )