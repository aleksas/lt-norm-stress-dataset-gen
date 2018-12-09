# tensor-stressor
tensor2tensor for automatic stressing text in Lithuanian

- Use [EN-DE as example](https://github.com/tensorflow/tensor2tensor/blob/master/tensor2tensor/data_generators/translate_ende.py)  to define LT-LTs problem 
- Use [--t2t_usr_dir](https://github.com/tensorflow/tensor2tensor#adding-your-own-components) parameter to define extra problem search path

# Docker Env

[Instructions](./docker)

# Run trainer & evaluate

## Train 

```bash
PROBLEM=encoder_character_stressor
HPARAMS_SET=transformer_base
MODEL=transformer_encoder
WORKER_GPU=2
HPARAMS="eval_drop_long_sequences=True"

USR_DIR=.
DATA_DIR=$HOME/t2t_data
TMP_DIR=/tmp/t2t_datagen
TRAIN_DIR=$HOME/t2t_train/$PROBLEM/$MODEL-$HPARAMS_SET

mkdir -p $DATA_DIR $TMP_DIR

tensorboard --logdir $TRAIN_DIR &

t2t-trainer \
 --generate_data \
 --problem=$PROBLEM \
 --data_dir=$DATA_DIR \
 --tmp_dir=$TMP_DIR \
 --output_dir=$TRAIN_DIR \
 --t2t_usr_dir=$USR_DIR \
 --hparams_set=$HPARAMS_SET \
 --hparams=$HPARAMS \
 --model=$MODEL \
 --worker_gpu=$WORKER_GPU \
 --eval_drop_long_sequences=True
```

## Evaluate 

```bash

PROBLEM=encoder_character_stressor
HPARAMS=transformer_base
MODEL=transformer_encoder

USR_DIR=.
DATA_DIR=$HOME/t2t_data
TMP_DIR=/tmp/t2t_datagen
TRAIN_DIR=$HOME/t2t_train/$PROBLEM/$MODEL-$HPARAMS

DECODE_FILE=$DATA_DIR/decode_this.txt
DECODE_TO_FILE=$DATA_DIR/decode_result.txt
echo "Laba diena drauai!" > $DECODE_FILE
echo "Viskas bus gerai." >> $DECODE_FILE

BEAM_SIZE=4
ALPHA=0.6

t2t-decoder \
  --data_dir=$DATA_DIR \
  --problem=$PROBLEM \
  --model=$MODEL \
  --hparams_set=$HPARAMS \
  --output_dir=$TRAIN_DIR \
  --t2t_usr_dir=$USR_DIR \
  --decode_hparams="beam_size=$BEAM_SIZE,alpha=$ALPHA" \
  --decode_from_file=$DECODE_FILE \
  --decode_to_file=$DECODE_TO_FILE
```

# References
- [How to train using my own dataset?](https://github.com/tensorflow/tensor2tensor/issues/516)
- [Walkthrough](https://github.com/tensorflow/tensor2tensor/blob/master/README.md#walkthrough)
- [cant train translation on my own data](https://github.com/tensorflow/tensor2tensor/issues/876)
- [Adding your own components](https://github.com/tensorflow/tensor2tensor#adding-your-own-components)
- [Defining the Problem](https://github.com/tensorflow/tensor2tensor/blob/master/docs/new_problem.md)
- [Sequence Tagging with pytorch](https://medium.com/@kolloldas/building-the-mighty-transformer-for-sequence-tagging-in-pytorch-part-i-a1815655cd8)
