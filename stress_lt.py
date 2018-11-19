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

"""Data generators for translation data-sets."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import tarfile
from tensor2tensor.data_generators import generator_utils
from tensor2tensor.data_generators import problem
from tensor2tensor.data_generators import text_encoder
from tensor2tensor.data_generators import text_problems
from tensor2tensor.data_generators import translate
from tensor2tensor.utils import registry

import tensorflow as tf

_LTLTSTR_TRAIN_DATASETS = [
    [
        "https://github.com/aleksas/tensor-stressor/raw/master/data/training-parallel-combo-v1.tgz",  # pylint: disable=line-too-long
        ("training-parallel-combo-v1/combination_v1.lt-lt_str.lt",
         "training-parallel-combo-v1/combination_v1.lt-lt_str.lt_str")
    ],
]
_LTLTSTR_TEST_DATASETS = [
    [
        "https://github.com/aleksas/tensor-stressor/raw/master/data/training-parallel-ch-v1.tgz",
        ("training-parallel-ch-v1/chrestomatija_v1.lt-lt_str.lt",
         "training-parallel-ch-v1/chrestomatija_v1.lt-lt_str.lt_str")
    ],
]


def _get_wmt_ltltstr_bpe_dataset(directory, filename):
  """Extract the WMT lt-ltstr corpus `filename` to directory unless it's there."""
  train_path = os.path.join(directory, filename)
  if not (tf.gfile.Exists(train_path + ".ltstr") and
          tf.gfile.Exists(train_path + ".lt")):
    url = ("https://drive.google.com/uc?export=download&id="
           "0B_bZck-ksdkpM25jRUN2X2UxMm8")
    corpus_file = generator_utils.maybe_download_from_drive(
        directory, "wmt16_lt_ltstr.tar.gz", url)
    with tarfile.open(corpus_file, "r:gz") as corpus_tar:
      corpus_tar.extractall(directory)
  return train_path


@registry.register_problem
class TranslateLtltstrWmtBpe32k(translate.TranslateProblem):
  """Problem spec for WMT Lt-Ltstr translation, BPE version."""

  @property
  def vocab_type(self):
    return text_problems.VocabType.TOKEN

  @property
  def oov_token(self):
    return "UNK"

  def generate_samples(self, data_dir, tmp_dir, dataset_split):
    """Instance of token generator for the WMT lt->ltstr task, training set."""
    train = dataset_split == problem.DatasetSplit.TRAIN
    dataset_path = ("train.tok.clean.bpe.32000"
                    if train else "chrest.tok.bpe.32000")
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

    return text_problems.text2text_txt_iterator(train_path + ".lt",
                                                train_path + ".ltstr")


@registry.register_problem
class TranslateLtltstrWmt8k(translate.TranslateProblem):
  """Problem spec for WMT Lt-Ltstr translation."""

  @property
  def approx_vocab_size(self):
    return 2**13  # 8192

  def source_data_files(self, dataset_split):
    train = dataset_split == problem.DatasetSplit.TRAIN
    return _LTLTSTR_TRAIN_DATASETS if train else _LTLTSTR_TEST_DATASETS


@registry.register_problem
class TranslateLtltstrWmt32k(TranslateLtltstrWmt8k):

  @property
  def approx_vocab_size(self):
    return 2**15  # 32768


@registry.register_problem
class TranslateLtltstrWmt32kPacked(TranslateLtltstrWmt32k):

  @property
  def packed_length(self):
    return 256

  @property
  def vocab_filename(self):
    return TranslateLtltstrWmt32k().vocab_filename


@registry.register_problem
class TranslateLtltstrWmt8kPacked(TranslateLtltstrWmt8k):

  @property
  def packed_length(self):
    return 256

  @property
  def vocab_filename(self):
    return TranslateLtltstrWmt8k().vocab_filename


@registry.register_problem
class TranslateLtltstrWmtCharacters(TranslateLtltstrWmt8k):
  """Problem spec for WMT Lt-Ltstr translation."""

  @property
  def vocab_type(self):
    return text_problems.VocabType.CHARACTER