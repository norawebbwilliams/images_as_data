# Getting started with AWS Rekognition

## Introduction

* AWS Rekognition is one of many available image auto-tagging services. There are other options from Microsoft, Google, IBM, Clarifai, etc. All of these are probably using a trained CNN, but most keep their algorithms proprietary so it is hard to know for sure (which is one of the downsides of using these services!). Note that these services may also retain your images and any generated labels, so proceed with caution in terms of privacy and other ethical concerns. 

* Each of these services offers an GUI (graphical user interface, you'll hear it pronouced like "gooey") online, where you can upload your own images to test out the service. You can find the AWS demo [here](https://console.aws.amazon.com/rekognition/home?region=us-east-1#/label-detection), though note you'll have to be logged into your AWS accont for it to work. Of course, uploading images one-by-one and recording each demo response is tedious. Accessing the Rekognition API with python is much more efficient.

* Rekognition offers multiple image-tagging calls. In our workshop, we highlight two services: (1) Object and Scene Detection and (2) Celebrity Recognition. See [here](https://aws.amazon.com/rekognition/image-features/) for the full list of available Rekognition calls (content moderation, text extraction, etc.).

* Rekognition currently offers free tier access, up to 5,000 API calls per month. Note that Object/Scene Detection and Celebrity Recognition are each separate API calls, so if you run both of the demo process on 2,500 images, you'll have used all your free calls for the month. After that, you will be charged per image call according to the [latest pricing](https://aws.amazon.com/rekognition/pricing/).

* IMPORTANT: Using Rekognition involves making keys that are used to access the service via an API. Anyone who has access to your keys can use them, so you should keep them secure. For example: don't push your keys to Github or a public Code Ocean capsule! 


## Outline

Steps:

1. [Set up a project folder on your computer](#1-set-up-a-project-folder)

2. [Create an AWS account](#2-create-an-aws-account).

3. [Create an IAM user](#3-create-an-iam-user)

4. [Get and save security keys for your IAM account](#4-get-and-save-keys).


## 1. Set up a project folder

* It always helps to create a dedicated directory/folder on your computer for new tasks. Create a new directory and name it 'auto_tagger_example'. You can create it wherever you like (Desktop, Documents, etc.). For our demos, we usually have this directory saved on the Desktop.  

* Within the new directory, create a subfolder named 'keys'. 

## 2. Create an AWS account

* Go to [https://aws.amazon.com/](https://aws.amazon.com/) and click on `Create a new AWS account` (upper right corner).

* Fill out the Sign Up form. 

* You will be asked to provide a credit card. New accounts can use some types of AWS services for free during the first year. You can learn more about it in [here](https://aws.amazon.com/free/). As mentioned above, Rekognition currently give you 5,000 free image API calls per month. After that, you will be charged per image call according to the [latest pricing](https://aws.amazon.com/rekognition/pricing/). 


* Finally, folks affiliated with a university should consider signing up for [AWS Educate](https://aws.amazon.com/education/awseducate/), if available. Once you apply and are approved, you'll receive free AWS credits (from $30-200 depending on your status). 


## 3. Create an IAM user

* For security purposes, AWS highly recommends that you do not log in with as the "root" user (the user you just created, linked to your credit card). Instead, create an IAM user for yourself with administrative access, [following the steps in this tutorial](https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started_create-admin-group.html). The easiest option in the tutorial is "Creating an Administrator IAM User and Group (Console)." Make note of the username and password for your newly created admin user.

* Signing in to AWS as an IAM user looks a bit different than logging in as the root user. On your IAM dashboard in AWS, you'll see the heading "IAM users sign-in link:" followed by a web address, e.g. `https://XXXXXXXX.signin.aws.amazon.com/console` where `XXXXXXXX` is your AWS account number. Bookmark or otherwise save this link somewhere you will remember it. When you log in as an IAM user, you will start from this page. 

* Log out of your AWS root account and log in again as your IAM user. Remember to start from the IAM users sign-in link that you saved in the previous step.

## 4. Get and save keys

* To generate keys for an IAM user (like the user you just made that has administrator access), go to your AWS console (practice logging in as your IAM user!), click on `Sevices` and select `IAM` (look under `Security, Identity & Compliance`).

* Click on `Users` and then click on the name of your IAM administrator user. Finally, click on `Security credentials`.

* Click on the `Create access key` button. If this button is greyed out, it likely means that you already have two sets of keys generated (look below the button). You can delete one of the existing keys, which will allow you to create a new pair.  

* A window will pop up saying "Success!" and giving you the option to download a .csv file with the new access key. **MAKE SURE YOU DOWNLOAD THIS FILE NOW. If you don't, you will have to generate a new set of keys.** 

* Save the .csv file (it will be named something like 'accessKeys.csv') to the 'keys' subfolder in the project 'auto_tagger_example' folder/directory you created in Step 1. You can save the file with a more memorable filename, if you'd like.  


