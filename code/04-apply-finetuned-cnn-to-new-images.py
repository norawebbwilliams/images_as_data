#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Purpose: load a previously fine-tuned model and use it to make predictions for images.

"""

# MODULES
#=====================================================================
from __future__ import print_function, division
import torch
import torch.nn as nn
from torch.autograd import Variable
from torchvision import datasets, models
import matplotlib.pyplot as plt
from PIL import Image
plt.ion()   # interactive mode
import os
import csv

# PATHS & CONSTANTS
#=============================================================================
IMG_DIR = 'path_to_images_to_classify'
MODEL_PATH = 'path_to_model'
RESULTS_PATH = 'path_to_save_predictions'

# - the path to a script with several FUNCTIONS we use in this script
FUNCTIONS_PATH = 'path_to_saved_functions'

# LOAD FUNCTIONS
os.chdir(FUNCTIONS_PATH)
exec(open('00_functions.py', ''rb'').read())

# DATA
#====================================================================
# - load fine-tuned model: in our case, a fine-tuned  
#       version of ResNet18.
model = models.resnet18(pretrained = True)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 2)
model.load_state_dict(torch.load(MODEL_PATH))

# - loading a set of images to classify 
img_list = os.listdir(IMG_DIR)
dataset = []
for img_file in img_list:
    img = Image.open('%s%s'%(IMG_DIR, img_file)).convert('RGB')
    dataset.append(img)


# DATA WRANGLING
#====================================================================
# - specifying the transformation-preprocessing to apply to the images
preprocess = data_tranform(train = False)

# - checking if the machine has GPUs and enabling GPU computing if so
use_gpu = torch.cuda.is_available()

# MAIN: Perform Predictions
#====================================================================
# - iterate through loaded images
output_data = []
counter = 0
for img in dataset:
    # This puts together text for reference document
    new_entry = {}
    var = Variable(preprocess(img).unsqueeze(0))
    pred = model(var)
    probs, indeces = nn.Softmax()(pred).data.sort()
    _, final_guess = torch.max(pred.data, 1)
    out_probs = re.sub('\\n ', '', str(probs))
    out_probs = re.sub('\\n\[*.*', '', out_probs)
    out_final_guess = re.sub('\\n ', '', str(final_guess))
    out_final_guess = re.sub('\\n\[*.*', '', out_final_guess)
    new_entry['probs'] = out_probs
    new_entry['final_guess'] = int(out_final_guess)
    new_entry['true_value'] = dataset_filelist[counter][1]
    new_entry['filename'] = dataset_filelist[counter][0]
    print(new_entry)
    output_data.append(new_entry)

with open(os.path.join(RESULTS_PATH, 'results.csv'), 'w') as csvfile:
        w = csv.DictWriter(csvfile, output_data[0].keys())
        w.writeheader()
        w.writerows(output_data)
