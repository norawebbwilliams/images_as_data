#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import print_function, division
"""
01-training-all-models.py
Purpose: To train 7 binary visual classifiers predicting images with protesting
             crowds, John Legend, and triggering sadness, enthusiasm, anger, 
             disgust, and fear. A pre-trained Convolutinal Neural Net 
             predicting the 1,000 ImageNet classes (ResNet18) is adpated to 
             predict binary outcomes by replacing the last 1,000-weights 
             fully-connected layer by a 2-weights one; and fine-tuned on new 
             training data. The resulting models are saved in a './models/' 
             directory and then used in another notebook to asses model 
             precision and recall. This is part of the piece on computer 
             vision and politics that we are preparing for Cambridge Elements.
"""

# - in this data directory there are 7 folders, one with the train-test images 
#     of each classifier. Each of these directories has a 'train' and 'test' 
#     subdirectory, and each of these two subdirectories has a 'negative' and 
#     'positive' subsubdirectories with the True Negative and True Positive 
#     images to train each classifier.
DATA_PATH = '/home/ubuntu/VPG/PROJECTS/cambridge_elements/data/'

# - the path to a script with several FUNCTIONS we use in this script
FUNCTIONS_PATH = '/home/ubuntu/VPG/PROJECTS/cambridge_elements/notebooks/'

# RESEARCHER CHOICES
# Which sets of data do you want to train a model for? 
# If left empty, code with train for all directories in the DATA_PATH directory
model_list = [] #CHECK APSA 2018 options are 'protest', 'legend', 'enthusiasm', 'anger', 'fear', 'sadness'

# Fine-tuning specification
num_classes = 2 # Enter the number of classes you are training for
set_report_num = 10 # Enter how often you wish the program to report back as it iterates

# Hyperparameters

hyperparam_combo_num = 1 # Use this to keep track of which version of hyperparameters you are using 

set_learn_rate = 0.0001 # Enter the desired learning rate
set_momentum = .9 # Enter the desired momentum
set_step_size = 7 # Enter the desired step size
set_gamma = 0.1 # Enter the desired gamma
set_iterations = 5 # Enter the desired number of iterations
set_batch_size = 4 # Enter the desired batch size



# PACKAGES
#from __future__ import print_function, division
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import torchvision
from torchvision import datasets, models
import matplotlib.pyplot as plt
import numpy as np
plt.ion()   # interactive mode
import os
import pickle
import json


# LOAD FUNCTIONS
os.chdir(FUNCTIONS_PATH)
exec(open('00_functions.py', "rb").read())

# MODEL TRAINING
# - a list of models to train, if not set by researcher above
if len(model_list) == 0:
	model_list = os.listdir(DATA_PATH)
	model_list = [m for m in model_list if m not in ['.DS_Store', 'MODELS', 'ACCURACY']]
	model_list.sort()

# Report which models are being trained
print(model_list)

# Specifying some objects that will be the same for trianing the 7 models
# - preprocessing to be applied to the images. See '00_functions.py' script
#   for more details on the 'data_transform()' function
preprocess = data_tranform()
# - checking if the machine has GPUs
use_gpu = torch.cuda.is_available()

# - how often (every how many iterations) should the loop print/report accuracy
report_num = set_report_num

# Iterate through the datasets and build binary image classifiers.
counter_models = 0
total_models = len(model_list)
for model_str in model_list:
    #================================================================
    # INITIALIZE MODEL
    #================================================================
    # - load a pretrained model from TorchVision: ResNet18
    model = models.resnet18(pretrained=True)

    # - check number of features in last fully connected layer
    num_ftrs = model.fc.in_features 

    # - change the output layer from 1,000 classes to a binary outcome
    model.fc = nn.Linear(num_ftrs, num_classes) # For ResNet18, last step is 512 -> 2
    
    #================================================================
    # MODEL HYPER-PARAMETERS
    #================================================================
    # - specify some model hyperparameters
    criterion = nn.CrossEntropyLoss() # loss function
    optimizer = optim.SGD(model.parameters(), 
                             lr=set_learn_rate, 
                             momentum=set_momentum) # how to perform optimization
    scheduler = lr_scheduler.StepLR(optimizer, 
                                           step_size=set_step_size, 
                                           gamma=set_gamma) # how to update learning rate    
    # - number of iterations
    iter_num = set_iterations

    #================================================================
    # PRE-PROCESSING
    #================================================================
    # - update counter and report progress
    counter_models += 1
    print('Training Model %s of %s: %s'%(counter_models, total_models, model_str.upper()))
    print('=================================\n')
    
    # - specify the path to data for this particular classifier
    model_path = '%s/%s/'%(DATA_PATH, model_str)
    # - specifying where the train and test images are
    image_datasets = {x: datasets.ImageFolder(os.path.join(model_path, x),
                                              preprocess[x])
                      for x in ['train', 'test']}

    # - creating an object to easily load the train and test images
    dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=4,
                                                 shuffle=True)
                  for x in ['train', 'test']}

    # - getting some extra information such as the size of the dataset and the
    #       class number
    dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'test']}
    class_names = image_datasets['train'].classes
    
    # - specify whether to use gpu 
    if use_gpu:
        model = model.cuda()
        
    #================================================================
    # MODEL ESTIMATION
    #================================================================
    # - check the size of the train and test sets
    dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'test']}
    
    # - initialize a time object so we can check how long the training 
    #   takes
    since = time.time()
    
    # - initialize a matrix of weights (model parameters) and accuracy
    #   object where we'll save the weights and accuracy info for the
    #   most accurate weights-configuration
    best_model_wts = model.state_dict()
    best_acc = 0.0
    best_precision = 0.0
    best_recall = 0.0
    loss_progress = []  
    acc_progress = []

    # - 
    for iteration in range(iter_num):
        if iteration % report_num == 0:
            print('Iteration {}/{}'.format(iteration, iter_num - 1))
            print('-' * 10)

        # - each iteration has a training and testing phase
        for phase in ['train', 'test']:
            if phase == 'train':
                scheduler.step() # update model weights
                model.train(True)  # set model to training mode
            else:
                model.train(False)  # set model to evaluate mode

            running_loss = 0.0
            running_corrects = 0
            running_preds = []
            running_labels = []

            # - iterate over data: in training iteration we
            #   iterate through groups of 4 train and 4 test
            #   images.
            for data in dataloaders[phase]:
                # - get the inputs
                inputs, labels = data

                # - transform data and labels into PyTorch variables
                if use_gpu:
                    inputs = Variable(inputs.cuda())
                    labels = Variable(labels.cuda())
                else:
                    inputs, labels = Variable(inputs), Variable(labels)

                # - gradients back to 0 (re-calculated in each iteration)
                optimizer.zero_grad()

                # - forward propagation: applying dot products
                outputs = model(inputs)
                _, preds = torch.max(outputs.data, 1)
                preds_int_list = list(preds)
                labels_int_list = list(labels.data)                
                loss = criterion(outputs, labels)

                # (only in training phase)
                # - backward propagation: calculate loss and gradients
                if phase == 'train':
                    loss.backward()
                    optimizer.step()

                # - calculate accuracy statistics
                running_loss += loss.data[0]
                running_corrects += torch.sum(preds == labels.data)
                running_preds = running_preds + preds_int_list
                running_labels = running_labels + labels_int_list
            
            iter_loss = running_loss / dataset_sizes[phase]
            iter_acc = running_corrects / dataset_sizes[phase]
            if sum(running_preds) > 0:
                iter_recall = sum([1 for i in range(0, len(running_preds)) if 
                                      running_preds[i] == 1 and 
                                      running_labels[i] == 1]) / float(sum(running_labels)) 
                iter_precision = sum([1 for i in range(0, len(running_preds)) if 
                                         running_preds[i] == 1 and 
                                         running_labels[i] == 1]) / float(sum(running_preds))
            else:
                iter_recall = 0
                iter_precision = 0
            
            # - report training progress once every N (e.g. 10) iterations
            if iteration % report_num == 0:
                print('{} Loss:{:.4f} Acc:{:.4f} Precision:{:.4f} Recall:{:.4f}\n'.format(
                    phase, iter_loss, iter_acc, iter_precision, iter_recall))

            # - if this iteration's results are the best so far,
            #   saving a copy of this best model
            if phase == 'test' and iter_acc > best_acc:
                best_acc = iter_acc
                best_precision = iter_precision
                best_recall = iter_recall
                best_model_wts = model.state_dict()                
            if phase == 'test':
                # - keep track of the evolution of the loss and accuracy
                loss_progress.append(iter_loss)
                acc_progress.append(iter_acc)
            
        # - if the accuracy is already pretty high, move to next
        #   classifier
        if best_acc > 0.95 and best_precision > 0.95 and best_recall > 0.95:
            print('... reached good model accuracy, moving to next model.')
            break
    
    # - check how long it took to estimate the model and report
    #   time and results for the most accurate model weights
    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(
        time_elapsed // 60, time_elapsed % 60))
    print('Best val Acc: {:4f}\n\n'.format(best_acc))    
    
    # - use the best model to predict labels for the whole
    #   test set and calculate precision and recall of the
    #   binary classifier   
    

    # - save the best model weights and accuracy
    model.load_state_dict(best_model_wts)
    torch.save(model, '%s/MODELS/%s.pth'%(DATA_PATH, model_str + '_' + str(hyperparam_combo_num)))
    accuracy_summary = {'acc':best_acc,
					      'precision':best_precision,
                          'recall':best_recall,
    					  'lr':set_learn_rate,
    					  'momentum':set_momentum,
    					  'step_size':set_step_size,
    					  'gamma':set_gamma,
    					  'max_iters':set_iterations,
    					  'batch_size':set_batch_size, 
                          'acc_progress':acc_progress,
                          'loss_progress':loss_progress
                          }
    json.dump(accuracy_summary, open('%s/ACCURACY/%s.json'%(DATA_PATH, model_str + '_' + str(hyperparam_combo_num)), 'w'))


# At the end you can plot the loss progression:
plt.plot(loss_progress)
plt.ylabel('loss')
plt.show()
