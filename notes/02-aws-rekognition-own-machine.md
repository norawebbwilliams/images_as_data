# Getting started with AWS Rekognition

## Introduction

* AWS Rekognition is one of many available image auto-tagging services. There are other options from Microsoft, Google, IBM, Clarifai, etc. All of these are probably using a trained CNN, but most keep their algorithms proprietary so it is hard to know for sure (which is one of the downsides of using these services!). Note that these services may also retain your images and any generated labels, so proceed with caution in terms of privacy and other ethical concerns. We work with AWS here simply because it fits best into the workshop framework, where we use other AWS services. 

* Each of these services offers an GUI (graphical user interface, you'll hear it pronouced like "gooey") online, where you can upload your own images to test out the service. You can find the AWS demo [here](https://console.aws.amazon.com/rekognition/home?region=us-east-1#/label-detection), though note you'll have to be logged into your AWS accont for it to work. Of course, uploading images one-by-one and recording each demo response is tedious. Accessing the Rekognition API with python is much more efficient.

* Rekognition offers multiple image-tagging calls. In our workshop, we highlight two services: (1) Object and Scene Detection and (2) Celebrity Recognition. See [here](https://aws.amazon.com/rekognition/image-features/) for the full list of available Rekognition calls (content moderation, text extraction, etc.).

* Rekognition currently offers free tier access, up to 5,000 API calls per month. Note that Object/Scene Detection and Celebrity Recognition are each separate API calls, so if you run both of the demo process on 2,500 images, you'll have used all your free calls for the month. After that, you will be charged per image call according to the [latest pricing](https://aws.amazon.com/rekognition/pricing/).

* IMPORTANT: Using Rekognition involves making keys that are used to access the service via an API. Anyone who has access to your keys can use them, so you should keep them secure. For example: don't push your keys to Github! 

* We are going to demonstrate how to use Rekognition from your own computer, not from a cloud instance. The module assumes that you have Python 3.5 or higher available on your computer. If not, you can still practice the set up, but the provided scripts won't run for you (though with some small fixes they will work with Python 2.x). Need to install Python on your machine? We recommend using [Anaconda](https://www.anaconda.com/download/). If you are starting from scratch, install the version that starts with 3.x (Python 2.7 works but will soon be unsupported).

* Before you start, we suggest making sure you have a bash terminal available on your computer. A bash terminal (also referred to as a shell) will look like a command line window -- basically a black screen with a blinking cusror where you enter commands. Mac computers already [come with a bash terminal option](https://macpaw.com/how-to/use-terminal-on-mac). Windows computers often don't, but a you can get one easily by downloading [Git for Windows](https://gitforwindows.org/). Once installed, simply a) click on the Windows or Start icon, b) in the Programs list, open the Git folder, and c) click the option for Git Bash. To open more than one terminal, while keeping the current one open, right click on Git Bash and select "Open in a new window."
 
## Outline

Steps:

1. [Set up a project folder on your computer](#1-set-up-a-project-folder)

2. [Create an AWS account](#2-create-an-aws-account).

3. [Create an IAM user](#3-create-an-iam-user)

4. [Get and save security keys for your IAM account](#4-get-and-save-keys).

5. [Install boto3](#5-access-your-ec2-instance).

6. [Download the repo with sample AWS scripts](#6-clone-repo)

7. Optional: [Get a nice text editor](#7-get-a-nice-text-editor)

8. Optional: [Install Jupyer Notebook](#8-install-jupyter-notebook)

## 1. Set up a project folder

* It helps for organization to create a dedicated directory/folder on your computer for this task. Create a new directory and name it 'auto_tagger_example'. You can create it wherever you like (Desktop, Documents, etc.). For the demo, we have this directory saved on the Desktop.  

* Within the new directory, create a subfolder named 'keys'. 

## 2. Create an AWS account

See the [Step 1 of the first module](https://github.com/norawebbwilliams/cambridge_elements/blob/master/notes/01-launch-use-ec2-aws-instances.md) and follow those instructions to create an AWS account.


## 3. Create an IAM user

* If you haven't already, create an IAM user for yourself with administrative access, [following the steps in this tutorial](https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started_create-admin-group.html). The easiest option in the tutorial is "Creating an Administrator IAM User and Group (Console)." Make note of the username and password for your newly created admin user.

* Signing in to AWS as an IAM user looks a bit different than logging in as the root user. On your IAM dashboard in AWS, you'll see the heading "IAM users sign-in link:" followed by a web address, e.g. `https://XXXXXXXX.signin.aws.amazon.com/console` where `XXXXXXXX` is your AWS account number. Bookmark or otherwise save this link somewhere you will remember it. When you log in as an IAM user, you will start from this page. 

* Log out of your AWS root account and log in again as your IAM user. Remember to start from the IAM users sign-in link that you saved in the previous step.

## 4. Get and save keys

* To generate keys for an IAM user (like the user you just made that has administrator access), go to your AWS console (practice logging in as your IAM user!), click on `Sevices` and select `IAM` (look under `Security, Identity & Compliance`).

* Click on `Users` and then click on the name of your IAM administrator user. Finally, click on `Security credentials`.

* Click on the `Create access key` button. If this button is greyed out, it likely means that you already have two sets of keys generated (look below the button). You can delete one of the existing keys, which will allow you to create a new pair.  

* A window will pop up saying "Success!" and giving you the option to download a .csv file with the new access key. **MAKE SURE YOU DOWNLOAD THIS FILE NOW. If you don't, you will have to generate a new set of keys.** 

* Save the .csv file (it will be named something like 'accessKeys.csv') to the 'keys' subfolder in the project 'auto_tagger_example' folder/directory you created in Step 1. You can save the file with a more memorable filename, if you'd like.  


## 5. Install boto3

* This is a python module that facilitates access to all AWS API services (e.g. Rekognition, Mechanical Turk, etc.). You can install it using the command `pip install boto3` in your bash terminal.

* If you have multiple versions of python on your computer, make sure you install `boto3` in the 3.5+ environment. 


## 6. Clone or download the repo

We have made sample python scripts and image examples available in a separate Github repo. 

* Go to the repo (in a new tab or window), [available here](https://github.com/norawebbwilliams/image_autotaggers).

* Clone or download the image_autotaggers repo by clicking on the green button at the top right of the repo that says "Clone or download". If you are new to Github, the easiest option is to download the repo by clicking "Download ZIP." More advanced users can clone the repo directly to the 'auto_tagger_example' directory you created in Step 1.

* Open up the zipped file you downloaded and save the `data`, `code`, `notebooks` and `results` folders to the 'auto_tagger_example' directory you created in Step 1.


## 7. Get a nice text editor

Optional: To run the practice scripts, you will need to make some adjustments to the sample python scripts that you just downloaded from the repo (they are in the `code` directory). You can open these python scripts with any text editor (e.g. Notepad), but some editors will automatically format the results in a way that makes them easier to work with. There are may good options for text editors. This author likes [Sublime](https://www.sublimetext.com/), which you can download for free.


## 8. Install Jupyter Notebook

Optional: If you want to edit and run scripts using the jupyter notebook interface, you'll need to make sure you have it installed on your computer. If you originally installed python on your computer using Anaconda, you've already got it installed. If not, or to learn more, follow the steps [here](http://jupyter.org/install). 

You can check to see if you have it installed by opening a bash terminal and typing `jupyter notebook`.
