# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import
import os
import tensorflow as tf
import math

"""
BCL + OMEGA = 180 / 32. + data aug + ms
FLOPs: 1321979063;    Trainable params: 52136440

This is your result for task 1:

    mAP: 0.7197849386403127
    ap of each class:
    plane:0.888767706661227,
    baseball-diamond:0.828813250009659,
    bridge:0.4680099872101205,
    ground-track-field:0.6901660404277621,
    small-vehicle:0.7395262726408154,
    large-vehicle:0.5667009043812319,
    ship:0.7347841545028257,
    tennis-court:0.9071577005837769,
    basketball-court:0.8229722946512178,
    storage-tank:0.8448119293093586,
    soccer-ball-field:0.6186025857112213,
    roundabout:0.6441106031308795,
    harbor:0.628617739475033,
    swimming-pool:0.7122314212831211,
    helicopter:0.7015014896264388

The submitted information is :

Description: RetinaNet_DOTA_DCL_B_3x_20200923_145.8w


This is your result for task 1:

    mAP: 0.7301021435398962
    ap of each class:
    plane:0.8770187842801944,
    baseball-diamond:0.8267941412496465,
    bridge:0.5127762497195772,
    ground-track-field:0.7429087472658292,
    small-vehicle:0.7430367724213736,
    large-vehicle:0.5717593529976157,
    ship:0.7535736625119606,
    tennis-court:0.9066598303041958,
    basketball-court:0.8420467411496289,
    storage-tank:0.85672175425764,
    soccer-ball-field:0.6380583684613818,
    roundabout:0.653533415863242,
    harbor:0.6392204165860068,
    swimming-pool:0.7104658633500178,
    helicopter:0.676958052680133

The submitted information is :

Description: RetinaNet_DOTA_DCL_B_3x_20200923_ms_145.8w

"""

# ------------------------------------------------
VERSION = 'RetinaNet_DOTA_DCL_B_3x_20200923'
NET_NAME = 'resnet101_v1d'  # 'MobilenetV2'
ADD_BOX_IN_TENSORBOARD = True

# ---------------------------------------- System_config
ROOT_PATH = os.path.abspath('../')
print(20*"++--")
print(ROOT_PATH)
GPU_GROUP = "0,1,2"
NUM_GPU = len(GPU_GROUP.strip().split(','))
SHOW_TRAIN_INFO_INTE = 20
SMRY_ITER = 2000
SAVE_WEIGHTS_INTE = 27000 * 3

SUMMARY_PATH = ROOT_PATH + '/output/summary'
TEST_SAVE_PATH = ROOT_PATH + '/tools/test_result'

if NET_NAME.startswith("resnet"):
    weights_name = NET_NAME
elif NET_NAME.startswith("MobilenetV2"):
    weights_name = "mobilenet/mobilenet_v2_1.0_224"
else:
    raise Exception('net name must in [resnet_v1_101, resnet_v1_50, MobilenetV2]')

PRETRAINED_CKPT = ROOT_PATH + '/data/pretrained_weights/' + weights_name + '.ckpt'
TRAINED_CKPT = os.path.join(ROOT_PATH, 'output/trained_weights')
EVALUATE_DIR = ROOT_PATH + '/output/evaluate_result_pickle/'

# ------------------------------------------ Train config
RESTORE_FROM_RPN = False
FIXED_BLOCKS = 1  # allow 0~3
FREEZE_BLOCKS = [True, False, False, False, False]  # for gluoncv backbone
USE_07_METRIC = True

MUTILPY_BIAS_GRADIENT = 2.0  # if None, will not multipy
GRADIENT_CLIPPING_BY_NORM = 10.0  # if None, will not clip

CLS_WEIGHT = 1.0
REG_WEIGHT = 1.0
ANGLE_WEIGHT = 0.5
REG_LOSS_MODE = None
ALPHA = 1.0
BETA = 1.0

BATCH_SIZE = 1
EPSILON = 1e-5
MOMENTUM = 0.9
LR = 5e-4
DECAY_STEP = [SAVE_WEIGHTS_INTE*12, SAVE_WEIGHTS_INTE*16, SAVE_WEIGHTS_INTE*20]
MAX_ITERATION = SAVE_WEIGHTS_INTE*20
WARM_SETP = int(1.0 / 4.0 * SAVE_WEIGHTS_INTE)

# -------------------------------------------- Data_preprocess_config
DATASET_NAME = 'DOTA'  # 'pascal', 'coco'
PIXEL_MEAN = [123.68, 116.779, 103.939]  # R, G, B. In tf, channel is RGB. In openCV, channel is BGR
PIXEL_MEAN_ = [0.485, 0.456, 0.406]
PIXEL_STD = [0.229, 0.224, 0.225]  # R, G, B. In tf, channel is RGB. In openCV, channel is BGR
IMG_SHORT_SIDE_LEN = [800, 400, 600, 1000, 1200]
IMG_MAX_LENGTH = 1200
CLASS_NUM = 15
OMEGA = 180 / 32.
ANGLE_MODE = 0

IMG_ROTATE = True
RGB2GRAY = True
VERTICAL_FLIP = True
HORIZONTAL_FLIP = True
IMAGE_PYRAMID = True

# --------------------------------------------- Network_config
SUBNETS_WEIGHTS_INITIALIZER = tf.random_normal_initializer(mean=0.0, stddev=0.01, seed=None)
SUBNETS_BIAS_INITIALIZER = tf.constant_initializer(value=0.0)
PROBABILITY = 0.01
FINAL_CONV_BIAS_INITIALIZER = tf.constant_initializer(value=-math.log((1.0 - PROBABILITY) / PROBABILITY))
WEIGHT_DECAY = 1e-4
USE_GN = False
FPN_CHANNEL = 256

# ---------------------------------------------Anchor config
LEVEL = ['P3', 'P4', 'P5', 'P6', 'P7']
BASE_ANCHOR_SIZE_LIST = [32, 64, 128, 256, 512]
ANCHOR_STRIDE = [8, 16, 32, 64, 128]
ANCHOR_SCALES = [2 ** 0, 2 ** (1.0 / 3.0), 2 ** (2.0 / 3.0)]
ANCHOR_RATIOS = [1, 1 / 2, 2., 1 / 3., 3., 5., 1 / 5.]
ANCHOR_ANGLES = [-90, -75, -60, -45, -30, -15]
ANCHOR_SCALE_FACTORS = None
USE_CENTER_OFFSET = True
METHOD = 'H'
USE_ANGLE_COND = False
ANGLE_RANGE = 180  # 90 or 180

# --------------------------------------------RPN config
SHARE_NET = True
USE_P5 = True
IOU_POSITIVE_THRESHOLD = 0.5
IOU_NEGATIVE_THRESHOLD = 0.4

NMS = True
NMS_IOU_THRESHOLD = 0.1
MAXIMUM_DETECTIONS = 100
FILTERED_SCORE = 0.05
VIS_SCORE = 0.4


