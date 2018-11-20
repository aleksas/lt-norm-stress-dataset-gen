# tensor-stressor
tensor2tensor for automatic stressing text in Lithuanian

- Use [EN-DE as example](https://github.com/tensorflow/tensor2tensor/blob/master/tensor2tensor/data_generators/translate_ende.py)  to define LT-LTs problem 
- Use [--t2t_usr_dir](https://github.com/tensorflow/tensor2tensor#adding-your-own-components) parameter to define extra problem search path

# Docker Env

## Start CPU only container
[DockerHub](https://hub.docker.com/r/bitspeech/tensor2tensor/), [GitHub](https://github.com/BitSpeech/docker)

> docker run -it -p 8888:8888 bitspeech/tensor2tensor:1.6.6 /bin/bash

## Start GPU (CUDA) container

Install nvidia-docker and run

> nvidia-docker run -it -p 8888:8888 bitspeech/tensor2tensor:1.6.6-gpu /bin/bash

# Run trainer

```bash
USR_DIR=.
PROBLEM=translate_ltltstr_wmt32k
DATA_DIR=$HOME/t2t_data
OUTPUT_DIR=$HOME/train/ltltstr
TMP_DIR=/tmp/t2t_datagen
HPARAMS=transformer_base
MODEL=transformer

mkdir -p $DATA_DIR $TMP_DIR

tensorboard --logdir $TRAIN_DIR &

t2t-trainer \
 --generate_data \
 --problem=$PROBLEM \
 --data_dir=$DATA_DIR \
 --tmp_dir=$TMP_DIR \
 --output_dir=$OUTPUT_DIR \
 --t2t_usr_dir=$USR_DIR \
 --hparams_set=$HPARAMS \
 --model=$MODEL
```

# References
- [How to train using my own dataset?](https://github.com/tensorflow/tensor2tensor/issues/516)
- [Walkthrough](https://github.com/tensorflow/tensor2tensor/blob/master/README.md#walkthrough)
- [cant train translation on my own data](https://github.com/tensorflow/tensor2tensor/issues/876)
- [Adding your own components](https://github.com/tensorflow/tensor2tensor#adding-your-own-components)
- [Defining the Problem](https://github.com/tensorflow/tensor2tensor/blob/master/docs/new_problem.md)
