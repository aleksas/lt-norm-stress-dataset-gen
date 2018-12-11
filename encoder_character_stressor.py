from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import tarfile
import re
import codecs
from tensor2tensor.data_generators import generator_utils
from tensor2tensor.data_generators import problem
from tensor2tensor.data_generators import text_problems
from tensor2tensor.data_generators import text_encoder
from tensor2tensor.layers import modalities
from tensor2tensor.utils import registry

import tensorflow as tf

_STRESS_CLASS_LABELS = [
  '`', # grave 
  '^', # circumflex instead of acute
  '~', # tilde
  '_'  # no stress
]

_CLASS_LABELS_EOS_ID = len(_STRESS_CLASS_LABELS)
_RE_NON_STRESS_PATTERN = re.compile(r'[^\r\n`^~]')
_RE_STRESS_PATTERN = re.compile(r'_([`^~])')

_LTLTSTR_TRAIN_DATASETS = [
  [
    "https://github.com/aleksas/tensor-stressor/raw/master/data/training-parallel-combo-v1.tgz",  # pylint: disable=line-too-long
    ("training-parallel-combo-v1/combination_v1.lt-lt_str.lt",
      "training-parallel-combo-v1/combination_v1.lt-lt_str.lt_str_lbl")
  ],
  [
    "https://github.com/aleksas/tensor-stressor/raw/master/data/training-parallel-ch-v1.tgz",
    ("training-parallel-ch-v1/chrestomatija_v1.lt-lt_str.lt",
      "training-parallel-ch-v1/chrestomatija_v1.lt-lt_str.lt_str_lbl")
  ],
]

def txt_line_iterator(txt_path):
  """Iterate through lines of file."""
  with tf.gfile.Open(txt_path) as f:
    for line in f:
      yield line.strip('\ufeff').strip()

def stressed_text2stress(source_txt_path, labels_txt_path, class_strs):
  content = '\n'.join(txt_line_iterator(source_txt_path))
  content = _RE_NON_STRESS_PATTERN.sub(r"_", content)
  content = _RE_STRESS_PATTERN.sub(r"\1", content)

  with codecs.open(labels_txt_path, 'w', 'UTF-8') as f:
    f.write(content)

def text2class_txt_iterator(source_txt_path, labels_txt_path, class_strs=None):
  """Yield dicts for Text2ClassProblem.generate_samples from lines of files.
  Args:
    source_txt_path: txt file with record per line.
    labels_txt_path: txt file with label per char per line, either as int or str. If
      string, must provide class_strs.
    class_strs: list<str> of class label names. Must be in correct order (i.e.
      ["a", "b", "c"] means that "a" will get class ID 0, "b" ID 1, etc.).
  Yields:
    {"inputs": inputs, "labels": labels}
  """
  if class_strs:
    class_strs = dict([(s, i) for i, s in enumerate(class_strs)])
  for inputs, labels in zip(
      txt_line_iterator(source_txt_path), txt_line_iterator(labels_txt_path)):
    if len(inputs) != len(labels):
      raise Exception('Input and label string lengths do not match')
    if class_strs:
      labels = [class_strs[label] for label in labels]
    else:
      labels = [int(label) for label in labels]

    yield {"inputs": inputs, "labels": labels}

def _get_ltltstr_dataset(directory, filename):
  train_path = os.path.join(directory, filename)
  if not (tf.gfile.Exists(train_path + ".lt_str_lbl")): # generate stress text file from ascii stressed text
    if not tf.gfile.Exists(train_path + ".lt") or not tf.gfile.Exists(train_path + ".lt_str_ascii"):
      for url ,_ in _LTLTSTR_TRAIN_DATASETS:
        corpus_file = generator_utils.maybe_download_from_drive(
            directory, url.split('/')[-1], url)
        with tarfile.open(corpus_file, "r:gz") as corpus_tar:
          corpus_tar.extractall(directory)

    stressed_text2stress(train_path + ".lt_str_ascii", train_path + ".lt_str_lbl", _STRESS_CLASS_LABELS)    
  return train_path

@registry.register_problem
class EncoderCharacterStressor(text_problems.Text2ClassProblem):  
  def source_data_files(self, dataset_split):
    return _LTLTSTR_TRAIN_DATASETS

  def hparams(self, defaults, unused_model_hparams):
    p = defaults
    
    p.loss_multiplier = 2.0

    inputs_encoder = self._encoders["inputs"]

    p.modality = {
        "inputs": modalities.SymbolModality,
        "targets": modalities.ClassLabelModality,
    }
    p.vocab_size = {
        "inputs": inputs_encoder.vocab_size,
        "targets": self.num_classes
    }
  
  def example_reading_spec(self):
    data_fields = {
        "inputs": tf.VarLenFeature(tf.int64),
        "targets": tf.VarLenFeature(tf.int64),
    }
    data_items_to_decoders = None
    return (data_fields, data_items_to_decoders)

  def generate_encoded_samples(self, data_dir, tmp_dir, dataset_split):
    generator = self.generate_samples(data_dir, tmp_dir, dataset_split)
    encoder = self.get_or_create_vocab(data_dir, tmp_dir)
    for sample in generator:
      inputs = encoder.encode(sample["inputs"])
      inputs.append(text_encoder.EOS_ID)
      targets = sample["labels"]
      targets.append(_CLASS_LABELS_EOS_ID)

      yield {"inputs": inputs, "targets": targets}

  @property
  def target_space_id(self):
    return problem.SpaceID.GENERIC

  @property
  def vocab_type(self):
    return text_problems.VocabType.CHARACTER

  @property
  def is_generate_per_split(self):
    return True

  @property
  def num_classes(self):
    return len(_STRESS_CLASS_LABELS) + 1

  def class_labels(self, data_dir):
    del data_dir
    return _STRESS_CLASS_LABELS
  
  def generate_samples(self, data_dir, tmp_dir, dataset_split):
    train = dataset_split == problem.DatasetSplit.TRAIN
    dataset_path = ("training-parallel-combo-v1/combination_v1.lt-lt_str"
                    if train else "training-parallel-ch-v1/chrestomatija_v1.lt-lt_str")
    train_path = _get_ltltstr_dataset(tmp_dir, dataset_path)

    return text2class_txt_iterator(train_path + ".lt",
                                    train_path + ".lt_str_lbl",
                                    _STRESS_CLASS_LABELS)

  
