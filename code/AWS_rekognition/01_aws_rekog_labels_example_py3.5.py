# -*- coding: utf-8 -*-
"""
Created on Thurs, April 26 11:36:13 2018
Purpose: Example Python script for detecting labels with Rekognition
"""

import csv
import boto3 
import pickle
import os

########### Paths
### MUST ADJUST HERE (1/2)
# Path to where your want to save the resulting labels
rekog_results_dir = 'path_to_where_you_want_to_save_labels'
# e.g.:
#rekog_results_dir = 'C:/Users/Nora/Desktop/auto_tagger_example/results/'

# Path to where your images are
rekog_images_dir = 'path_to_where_your_images_are'
# e.g.:
#rekog_images_dir = 'C:/Users/Nora/Desktop/auto_tagger_example/data/'

########### Connect to AWS Rekognition API
# Read in your personal keys
# You can hard code your access key ID and secret key ID into the script, 
# but this is not recommended

personal_access_key = "your_personal_access_key"
secret_access_key = "your_secret_access_key"

# Instead we recommend storing your keys securely in a csv or text file.
# For example, if you have saved your keys in a csv:

credentials = []

### MUST ADJUST HERE (2/2)
with open('path_to_your_saved_AWS_access_keys.csv', newline='') as csvfile:

# e.g.:
#with open('C:/Users/Nora/Desktop/auto_tagger_example/keys/AWS_personal_nora_admin_credentials.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        credentials.append(row)

personal_access_key = credentials[0]['Access key ID']
secret_access_key = credentials[0]['Secret access key']

# Initialize the boto client to access the Rekogniton api
client=boto3.client('rekognition','us-east-1', # or choose the best region for your work, 
                                               # e.g. the location of your S3 bucket if using that method to store images
                    aws_access_key_id = personal_access_key, 
                    aws_secret_access_key = secret_access_key) 


########### Create a list of images to pass through API
# Make a list of all the images in the rekog_data_dir you created
local_images = os.listdir(rekog_images_dir)

########### Loop each image through the celebrity recognition api
          
##### Detect labels
## 
holder_labels = []

for imageFile in local_images:
    with open(rekog_images_dir + imageFile, 'rb') as image:
            response = client.detect_labels(Image={'Bytes': image.read()})
    
    print('Detected labels for ' + imageFile)
    
    ## If no labels detected, still save the info:
    if len(response['Labels']) == 0:
        print ("No Labels Detected")
        temp_dict = {}
        temp_dict["image_id"] = imageFile
        temp_dict["full_detect_labels_response"] = response
        temp_dict["label_num"] = ''
        temp_dict["label_str"] = ''
        temp_dict["label_conf"] = ''
        temp_dict["label_orient_correct"] = response['OrientationCorrection']
        holder_labels.append(temp_dict)   
    
    else:
        
        label_counter = 1
        
        for label in response['Labels']:
            print (label['Name'] + ' : ' + str(label['Confidence']))
            temp_dict = {}
            temp_dict["image_id"] = imageFile
            temp_dict["full_detect_labels_response"] = response
            temp_dict["label_num"] = label_counter
            temp_dict["label_str"] = label['Name']
            temp_dict["label_conf"] = label['Confidence']
            temp_dict["label_orient_correct"] = response['OrientationCorrection']
            label_counter +=1 # update for the next label
            holder_labels.append(temp_dict)
          
len(holder_labels)

###########
# Write out the results to a csv
with open(rekog_results_dir + 'awsrekognition_detect_labels.csv', 'w', newline = '') as csvfile:
    fieldnames = ['image_id', 'full_detect_labels_response',
                  'label_num', 'label_str',
                  'label_conf', 'label_orient_correct'
                  ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader() 
    for entry in holder_labels:
        writer.writerow(entry)
        
