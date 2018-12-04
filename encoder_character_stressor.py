# coding=utf-8
# Copyright 2018 The Tensor2Tensor Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""IMDB Sentiment Classification Problem."""

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
from tensor2tensor.utils import registry

import tensorflow as tf

_CLASS_LABELS = ['`', '^', '~', ' ']
_RE_PATTERN = re.compile(r' ([`^~])')

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

def encode_class_to_labels_file(source_txt_path, labels_txt_path, class_strs):
  with codecs.open(source_txt_path, 'r', 'UTF-8') as f:
    content = f.read()
  
  content = _RE_PATTERN.sub(r"\1", content)

  with codecs.open(source_txt_path, 'w', 'UTF-8') as f:
    f.write(content)

def text2multiclass_txt_iterator(source_txt_path, labels_txt_path, class_strs=None):
  """Yield dicts for Text2ClassProblem.generate_samples from lines of files.
  Args:
    source_txt_path: txt file with record per line.
    labels_txt_path: txt file with label per char per line, either as int or str. If
      string, must provide class_strs.
    class_strs: list<str> of class label names. Must be in correct order (i.e.
      ["a", "b", "c"] means that "a" will get class ID 0, "b" ID 1, etc.).
  Yields:
    {"inputs": inputs, "label": label}
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
      labels = [int(label) or label in labels]

    yield {"inputs": inputs, "labels": labels}

def _get_wmt_ltltstr_bpe_dataset(directory, filename):
  """Extract the WMT lt-ltstr corpus `filename` to directory unless it's there."""
  train_path = os.path.join(directory, filename)
  if not (tf.gfile.Exists(train_path + ".lt_str_lbl")):
    if not tf.gfile.Exists(train_path + ".lt"):
      for url, files in _LTLTSTR_TRAIN_DATASETS:
        corpus_file = generator_utils.maybe_download_from_drive(
            directory, url.split('/')[-1], url)
        with tarfile.open(corpus_file, "r:gz") as corpus_tar:
          corpus_tar.extractall(directory)

    encode_class_to_labels_file(train_path + ".lt", train_path + ".lt_str_lbl", _CLASS_LABELS)    
  return train_path

@registry.register_problem
class EncoderCharacterStressor(text_problems.Text2ClassProblem):
  def hparams(self, defaults, unused_model_hparams):
    p = defaults
    inputs_encoder = self._encoders["inputs"]
    targets_encoder = self._encoders["targets"]

    p.modality = {
        "inputs": modalities.SymbolModality,
        "targets": modalities.MultiLabelModality,
    }
    p.vocab_size = {
        "inputs": inputs_encoder.vocab_size,
        "targets": targets_encoder.vocab_size,
    }
  
  def source_data_files(self, dataset_split):
    if dataset_split == problem.DatasetSplit.TRAIN:
      return _LTLTSTR_TRAIN_DATASETS
    elif dataset_split == problem.DatasetSplit.EVAL:
      return _LTLTSTR_TRAIN_DATASETS
    else: # if dataset_split == problem.DatasetSplit.TEST:
      return _LTLTSTR_TEST_DATASETS

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
  def dataset_splits(self):
    return [{
        "split": problem.DatasetSplit.TRAIN,
        "shards": 10,
    }, {
        "split": problem.DatasetSplit.EVAL,
        "shards": 1,
    }]

  @property
  def approx_vocab_size(self):
    return 2**13  # 8k vocab suffices for this small dataset.

  @property
  def num_classes(self):
    return len(_CLASS_LABELS)

  def class_labels(self, data_dir):
    del data_dir
    return _CLASS_LABELS
  
  def generate_samples(self, data_dir, tmp_dir, dataset_split):
    """Instance of token generator for the WMT lt->ltstr task, training set."""
    train = dataset_split == problem.DatasetSplit.TRAIN
    dataset_path = ("combination_v1.lt-lt_str"
                    if train else "chrestomatija_v1.lt-lt_str")
    train_path = _get_wmt_ltltstr_bpe_dataset(tmp_dir, dataset_path)

    # Vocab
    vocab_path = os.path.join(data_dir, self.vocab_filename)
    if not tf.gfile.Exists(vocab_path):
      bpe_vocab = os.path.join(tmp_dir, "vocab.bpe.32000")
      with tf.gfile.Open(bpe_vocab) as f:
        vocab_list = f.read().split("\n")
      vocab_list.append(self.oov_token)
      text_encoder.TokenTextEncoder(
          None, vocab_list=vocab_list).store_to_file(vocab_path)

    return text2multiclass_txt_iterator(train_path + ".lt",
                                        train_path + ".lt_str_lbl",
                                        _CLASS_LABELS)

  
