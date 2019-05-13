# -*- coding: utf-8 -*-
"""
Created on Thurs, April 26 11:36:13 2018
Purpose: Example Python script for detecting celebrties with Rekognition
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

# For Code Ocean:
rekog_results_dir = '../../results/'

# Path to where your images are
rekog_images_dir = 'path_to_where_your_images_are'
# e.g.:
#rekog_images_dir = 'C:/Users/Nora/Desktop/auto_tagger_example/data/'

# For Code Ocean:
rekog_images_dir = '../../autotagger_data/'

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
#with open('path_to_your_saved_AWS_access_keys.csv', newline='') as csvfile:

# e.g.:
#with open('C:/Users/Nora/Desktop/auto_tagger_example/keys/AWS_personal_nora_admin_credentials.csv', newline='') as csvfile:
# For Code Ocean
with open('../../keys/AWS_personal_nora_admin_credentials.csv', newline='') as csvfile:
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
          
holder_content_celeb = []

### Looping
for imageFile in local_images:

    with open(rekog_images_dir + imageFile, 'rb') as image:
        response = client.recognize_celebrities(Image={'Bytes': image.read()})
    
    print('Detecting faces for ' + imageFile)
    
    ## If no celebrites detected, still save the API info:
    if len(response['CelebrityFaces']) == 0:
        print ("No Celebrities Detected")
        temp_dict = {}
        temp_dict["image_id"] = imageFile
        temp_dict["celeb_full_response"] = ""
        temp_dict["celeb_num"] = ""
        temp_dict["celeb_urls"] = ""
        temp_dict["celeb_name"] = ""
        temp_dict["celeb_id"] = ""
        temp_dict["celeb_face_data"] = ""
        temp_dict["celeb_face_conf"] = ""
        temp_dict["celeb_match_conf"] = ""
        temp_dict['celeb_metadata'] = response['ResponseMetadata']  
        holder_content_celeb.append(temp_dict)
    
    ## If celebrities are detected, save a dictionary for each celebrity:
    else:
        celeb_counter = 1
        
        for face in response['CelebrityFaces']:
            print (face['Name'] + ' : ' + str(face['MatchConfidence']))
            
            temp_dict = {}
            temp_dict["image_id"] = imageFile
            temp_dict["celeb_full_response"] = face 
            temp_dict["celeb_num"] = celeb_counter
            temp_dict["celeb_urls"] = face['Urls']
            temp_dict["celeb_name"] = face['Name']
            temp_dict["celeb_id"] = face['Id']
            temp_dict["celeb_face_data"] = face['Face']
            temp_dict["celeb_face_conf"] = face['Face']['Confidence']
            temp_dict["celeb_match_conf"] = face['MatchConfidence']
            temp_dict['celeb_metadata'] = response['ResponseMetadata']
            celeb_counter += 1
            holder_content_celeb.append(temp_dict)

###########
# Write out the results to a csv
with open(rekog_results_dir + 'awsrekognition_celeb_detect.csv', 'w', newline = '') as csvfile:
    fieldnames = ['image_id', 'celeb_full_response',
                  'celeb_num', 'celeb_urls',
                  'celeb_name', 'celeb_id',
                  'celeb_face_data', 'celeb_face_conf', 
                  'celeb_match_conf', 'celeb_metadata']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for entry in holder_content_celeb:
        writer.writerow(entry)
        
