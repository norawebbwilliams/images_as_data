# -*- coding: utf-8 -*-

# 00_functions.py
# Description: This script contains a set of functions used in other 
#				scripts implementing computer vision methods.

import numpy as np
import matplotlib.pyplot as plt
from torchvision import transforms
import torch
import time
from torch.autograd import Variable

def imshow(inp, title=None):
    """
    Description: This function takes a grid of images and shows them, making 
        image visualization easy.    
    Parameters:
        `inp`:      type <torch.FloatTensor> object.
        `title`:    type <list> of strings indicating the labels of the `inp` 
                        images.    
    Output:
        shows the images and their labels (if provided)
    """
    inp = inp.numpy().transpose((1, 2, 0))
    #mean = np.array([0.485, 0.456, 0.406])
    #std = np.array([0.229, 0.224, 0.225])
    #inp = std * inp + mean
    inp = np.clip(inp, 0, 1)
    plt.imshow(inp)
    if title is not None:
        plt.title(title)
    plt.pause(0.001)
    
    
def data_tranform(train = True, mean = [0.485, 0.456, 0.406], 
                  sd = [0.229, 0.224, 0.225],
                  scale = 256, random_crop = 224):
    """
    Description: This function creates an object to transform train and
        test (or only testing) images.    
    Parameters:
        `train`: type <bool> indicating if the object will need to be used
                    to transform training and testing images (=True) or
                    only testing.
        `mean`: type <list> of 3 floats indicating the mean value of the 3 RGB
                    image inputs.
        `sd`: type <list> of 3 floats indicating the standard deviation of 
                    the 3 RGB mean inputs.
        `scale`: type <int> indicating the new size to give to the train and
                    test data (e.g. 256x256 pixel images).
        `random_crop`: type <int> indicating the size of the part of the image
                    really used for training-testing (e.g. 224x224)                    
    Output:
        An object to be used for preprocessing the train and test images        
    Example:
        preprocess = data_transform()        
    """
    if train:
        data_transforms = {
            'train': transforms.Compose([
                transforms.Scale(scale),            
                transforms.RandomSizedCrop(random_crop),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Normalize(mean, sd)
            ]),
            'test': transforms.Compose([
                transforms.Scale(scale),
                transforms.CenterCrop(random_crop),
                transforms.ToTensor(),
                transforms.Normalize(mean, sd)
            ]),
        }
    else:
        data_transforms = transforms.Compose([
            transforms.Scale(scale),
            transforms.CenterCrop(random_crop),
            transforms.ToTensor(),
            transforms.Normalize(mean, sd)
        ])        
    return(data_transforms)

def visualize_model(model, class_names, num_images, dataloaders, use_gpu):
    """
    Description: This function shows N (<num_images>) model predictions (top 
        label + top probability).
    
    Parameters:
        `model`: type <torchvision.models.-modeltype->, the trained model.       
        `num_images`: type <int> indicating the number of random images to show.
        `dataloaders`: type <dict> of a 'train' and a 'test
            torch.utils.data.dataloader.DataLoader.
        `use_gpu`: type <bol> indicating whether CUDA is available.
        
    Output:
        Prints out N predictions
    """
    images_so_far = 0

    for i, data in enumerate(dataloaders['test']):
        inputs, labels = data
        if use_gpu:
            inputs, labels = Variable(inputs.cuda()), Variable(labels.cuda())
        else:
            inputs, labels = Variable(inputs), Variable(labels)

        outputs = model(inputs)
        _, preds = torch.max(outputs.data, 1)

        for j in range(inputs.size()[0]):
            images_so_far += 1
            ax = plt.subplot(num_images//2, 2, images_so_far)
            ax.axis('off')
            ax.set_title('predicted: {}'.format(class_names[preds[j]]))
            imshow(inputs.cpu().data[j])

            if images_so_far == num_images:
                return
