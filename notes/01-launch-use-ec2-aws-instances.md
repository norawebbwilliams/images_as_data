# How to launch and work with EC2-AWS instances

## Introduction

* Training and fine-tuning Convolutional Neural Networks (CNNs) requires high computational power. 
    
* Machines with Graphics Processing Units (GPUs) are well suited for these type of tasks but laptops and desktop computers are rarely equipped with GPUs.
    
* The most common solution is to use cloud computing services such as Amazon Web Services (AWS) and to perform complex computation tasks in the cloud. Many other cloud computer services can be used for this purpose, and you may have access to a high performing computer cluster at your home institution. In these notes we'll focus on using AWS because that's what we use and know better. 

* Before you start, we suggest making sure you have a bash terminal available on your computer. A bash terminal (also referred to as a shell) will look like a command line window -- basically a black screen with a blinking cursor where you enter commands. Mac computers already [come with a bash terminal option](https://macpaw.com/how-to/use-terminal-on-mac). Windows computers often don't, but a you can get one easily by downloading [Git for Windows](https://gitforwindows.org/). Once installed, simply a) click on the Windows or Start icon, b) in the Programs list, open the Git folder, and c) click the option for Git Bash. To open more than one terminal, while keeping the current one open, right click on Git Bash and select "Open in a new window."

## Outline

The goal of this module is to help people set up their own AWS infrastructure to train and fine-tune CNNs so they can implement state-of-the-art computer vision techniques in their own work.

Steps:
1. [Create an AWS account](#1-create-an-aws-account).

2. [Create an EC2 instance](#2-create-an-ec2-instance).

3. [Access your EC2 instance](#3-access-your-ec2-instance).

4. [Run a jupyter notebook server in the instance](#4-run-a-jupyter-notebook-server-in-the-instance).

5. [Connect to the jupyter notebook from your local machine](#5-connect-to-the-jupyter-notebook-from-your-local-machine).

6. [Stopping the EC2 instance](#6-important-stopping-your-ec2-instance).

## 1. Create an AWS account
* Go to [https://aws.amazon.com/](https://aws.amazon.com/) and click on `Create a new AWS account` (upper right corner).

* Fill out the Sign Up form. 

* You will be asked to provide a credit card. New accounts can use some types of EC2 instances and other services for free during the first year. You can learn more about it in [here](https://aws.amazon.com/free/). However, EC2 instances with GPUs are not included in this free tier. A `g2.2xlarge` instance for example costs about $.65/hour (and a `p2.xlarge` instance costs about $.90/h; they both have 1 GPU), but you will be charged only for the time you use it (as long as you remember to stop it when you are done! We'll get to this later, or jump ahead to the last step to learn more).

* For security purposes, AWS highly recommends that you do not log in with as the "root" user (the user you just created, linked to your credit card). AWS suggests that you [create a new user for yourself using their IAM famework](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html). You can give that new user full administrator priviledges. The only AWS element that an IAM administrative user will not be able to see is billing information -- for that you will have to log in as the root user. We won't go into the IAM user step in detail here, as you can do the rest of this module as the root user. However, we highly recommend creating an IAM user by [following the steps in this tutorial](https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started_create-admin-group.html), then signing into AWS as that IAM user going forward. 

* Finally, folks affiliated with a university should consider signing up for [AWS Educate](https://aws.amazon.com/education/awseducate/). Once you apply and are approved, you'll receive free AWS credits (from $30-200 depending on your status). Those credits will be more than enough to cover the AWS services you'll use during this workshop.

## 2. Create an EC2 instance

[What are EC2 instances?](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html) These are servers mantained by AWS that you can use remotely. It's like renting a computer from Amazon for as long as you need it. These computers, however, do not have a keyboard or a mouse, so you'll have to interact with them remotely and programatically from your local machine. We'll give you some hints on how to do this. But first, let's go through how to create an instance with everything already set up to implement state-of-the-art computer vision techniques.

* Sign into your AWS account. Click on `Services` and then on `EC2`. This will bring you to your `EC2 Dashboard`. Now click on the `Instances` option under the Instances menu (left side of the screen). This will bring up your instances board.

* To create a new instance, click on the blue `Launch Instance` button. You'll then have to go through different steps to specify the type of server you want to create:

    - **Step 1: Choose and Amazon Machine Image (AMI).** In here you need to specify the type of operation system (OS) and pre-settings you want installed in your machine. Installing all the needed dependencies for deep learning and computer vision is not an easy task, as several software and hardware requirements need to be met. Lucky for us, other people have already gone through the hassle and have then openly shared their pre-settings! To access these, select the `Community AMIs` from the menu on the left. You'll then see an almost infinite list of AMIs to select from. One that we have already tested and know works well to implement and fine-tune computer vision models in python (e.g. using `PyTorch`) is the `Deep Learning AMI (Ubuntu) Version 3.0 - ami-0a9fac70`. Simply type **ami-0a9fac70** in the search bar and select the only result that will pop up. 
    
    - If you search for **ami-0a9fac70** and nothing comes up, your AWS account is probably looking in the wrong region. This AMI is only available in the `US East (N. Virginia)` region. In the upper right portion of the AWS dashboard, just to the left of the word `Support`, you'll see a dropdown option. If you click on it, you will see a list of all the AWS regions. Make sure that `US East (N. Virginia)` is selected, then search again for **ami-0a9fac70**.
    
    - **Step 2: Choose an Instance Type.** Here you need to specify the type of machine/computer you want. You'll see a lot of types, which vary on several dimensions, such as the memory size and the number of computing nodes (CPUs, GPUs). The `g` and `p` instance types have GPU graphics on them. An affordable option ($.65/h) is to use the `g2.2xlarge` type: it comes with 1 GPU and a decent amount of memory (15Gb). The next affordable option ($.90/h) is the `p2.xlarge`, which also comes with 1 GPU (although more efficent/fast, see this [comparison](https://bitfusion.io/2016/11/03/quick-comparison-of-tensorflow-gpu-performance-on-aws-p2-and-g2-instances/)) and much more memory (61Gb). Once you have selected an instance type, click on `Review and Launch`
    
    - **Step 3,4,5,6.** You can skip these steps for now. If asked, simply leave the default options selected.
    
    - **Step 7: Review.** Click on `Launch`. You'll be asked to "Create a new key pair" (or to "Choose an existing key pair" if you have already launched a EC2 instance using this account). Choose a name for the key pair and click on `Download Key Pair`. This will download a `.pem` file, **save it in a safe place and NEVER lose it**. This file is used to access the instance and if you lose it, you won't be able to ever access it again! For now, you can save the file to your Desktop.
    
    - Once you have downloaded the key and clicked on `Launch Instances`, the instance will be created and started. You can see it active if you go back to the Instances board. It may take a few minutes to finish initializing.
    
    - If you get an error when you try to launch the instance, something like "Launch Failed -- You have requested more instances (1) than your current instance limit of 0 allows for the specified instance type. Please visit http://aws.amazon.com/contact-us/ec2-request to request an adjustment to this limit", you will need to follow the link and request access to these types of instances from AWS support. **It may take a few days to get this permission!!!**. You'll have the option to request some number of this instance type (either `g2.2xlarge` or `p2.xlarge`). We suggest that you request only one instance of the type you've chosen, since that may make the approval process go more quickly. Once you receive approval, go through these steps again to launch your instance.
    
* NOTE: If you get this far in the module and have to stop, **make sure you STOP your EC2 instance** to avoid being charged continuously. See the last step of this guide. 

## 3. Access your EC2 instance.

* Once your EC2 instance has been launched, you can access your instance programmatically. Make sure you are logged in to your AWS account, preferrably as your IAM user, and `start` your EC2 instance if it is `stopped`. You can check whether or not the instance is on by looking at the EC2 Instances board. If the Instance State is `stopped`, right click on the word `stopped`, then hover over the Intstance State option and select `start`. It will ask if you are sure you want to start the instance. 

* Open a bash terminal on your machine. Mac computers already [come with bash terminal](https://macpaw.com/how-to/use-terminal-on-mac). Windows computers often don't, but a you can get one by downloading [Git for Windows](https://gitforwindows.org/): once installed, simply a) click on the Windows or Start icon, b) in the Programs list, open the Git folder, and c) click the option for Git Bash.

* Here is the command you need to type in the bash shell in order to access the EC2 instance: `ssh -i xxxx.pem ubuntu@xx.xxx.xxx.xxx`, where:
    
    - `xxxx.pem` is the path to your key. This could be something like: `/Users/johnsmith/my_key.pem`. If it's the first time you use this key, you'll need to set up the right permission by typing in a bash terminal: `sudo chmod 600 /path/to/my/key.pem`. Otherwise, you'll get the following warning: `WARNING: UNPROTECTED PRIVATE KEY FILE!`.
    - `xx.xxx.xxx.xxx` is the IP of the instance you launched. You can find it in the AWS EC2 Instances dashboard, under the `IPv4 Public IP` column.
    
* The first time you connect to the instance, you'll get a message about the authenticity of the host and asked if you want to proceed. Type 'yes' to continue.
    
* Now you should be connected to the instance! You'll see a message about the environments available, and you may see a note asking you to reboot. You can reboot by typing `sudo reboot`, waiting a few minutes and then re-connecting to the instance using the `ssh` command above.

* To double check that you are in the instance, type the following bash command: `ls`. This will list the files/directories in the home directory. If you created the instance using the suggested AMI, you should see the following: `anaconda3 | Nvidia_Clud_EULA.pdf | src | tutorials`.

* NOTE: If you get this far in the module and have to stop, **make sure you STOP your EC2 instance** to avoid being charged continuously. See the last step of this guide. 


## 4. Run a jupyter notebook server in the instance.

One way to take advantage of the computing power of this instance with a GPU is to write a script locally and then send it to and execute it in the instance. Another more user-friendly option is to run a jupyter notebook server in the instance and then connect to it from your local machine. This will allow you to type code (e.g. Python code) in your machine that will get executed in the instance in sections.

* If you used the suggested AMI when creating the instance, it should be able to run jupyter notebooks already. The current jupyter configuration in the instance has a password that needs to be changed to your password of choice. In order to do so, type the following in the bash terminal connected to the machine: `jupyter notebook password`, hit enter, and then type the desired password twice, as prompted. You will only need to do this one, not every time you run a jupyter notebook.

* Open a new port in the EC2 instance so we can access the jupyter server remotely. You will only need to do this one, not every time you run a jupyter notebook (AWS will remember your new rule about the port). In the AWS EC2 Instances board, click on the `Security Group` of the instance (far-right of your instance row).

* Select the `Inbound` tab in the lower panel and click `Edit`.

* Click on `Add Rule` (make sure you add a new rule, don't change the existing one(s)!) and add a new `Custom TCP` connection, with the following configuration:
    
    - **Type**: Custom TCP
    - **Protocol:** TCP
    - **Port Range:** 8888
    - **Source:** Custom 0.0.0.0/0
    - **Description:** SSH for Admin Desktop

* Click `Save`.

* Launch a jupyter notebook server in the instance. Type the following in the bash terminal connected to the EC2 instance: `jupyter notebook`. It may take a few minutes to launch. Don't close this bash terminal in order to keep the the jupyter server running!

* NOTE: If you get this far in the module and have to stop, **make sure you STOP your EC2 instance** to avoid being charged continuously. See the last step of this guide. 

## 5. Connect to the jupyter notebook from your local machine.

* Connect your local machine to the port in the instance the jupyter notebook is reporting to (port 8888). Note that to do this, you will open a **NEW** bash terminal. Keep the terminal that is running the EC2 instance open (it's the one hosting the jupyter notebook).

    - Mac users: Type the following in a **new** bash terminal: `ssh -i xxxx.pem -L 8157:127.0.0.1:8888 ubuntu@ec2-xx-xxx-xxx-xx.compute-1.amazonaws.com`. You're already know what `xxxx.pem` is. The second set of placeholders (xx-xxx-xxx-xx) refer again to instance's IP. Notice however that in this case the numbers are separated by `-` and not by `.`! Again, you will need to say "yes" to the security question.
    - Windows users: Type the following in a **new** bash terminal: `ssh -i xxxx.pem -L 8888:127.0.0.1:8888 ubuntu@ec2-xx-xxx-xxx-xx.compute-1.amazonaws.com`. You're already know what `xxxx.pem` is. The second set of placeholders (xx-xxx-xxx-xx) refer again to instance's IP. Notice however that in this case the numbers are separated by `-` and not by `.`! Again, you will need to say "yes" to the security question.

* Now connect via your web browser of choice (Firefox, Chrome, etc.) and log in using the password you created earlier. Type the following in a web browser:

    - Mac: https://127.0.0.1:8157 (if this doesn't work, remove the "s" and do simply: http://127.0.0.1:8157)
    - Windows/PC: http://127.0.0.1:8888 

* Congrats! You should now see the file structure in the EC2 instance. Feel free to click around and see what's there!

* After you complete your work with the notebook, **make sure you STOP your EC2 instance** to avoid being charged continuously. See the last step of this guide. 

## 6. Important: Stopping your EC2 instance.

It's very important to stop your EC2 instance when you are done for the day. Otherwise, you will continue to be charged. 

* Save and close your jupyter notebook (if you have one open).

* [Optional] Move any files you need off the EC2 instance and on to your own machine. 

* Go to your EC2 dashboard in AWS. You'll see that under `Instance State` the EC2 instance you've been working with be listed as `running`. Right click on the word `running` and a menu will pop up. Hover over `Instance State` and you will see a series of options. Most often you will want to either `Stop` or `Start` the instance. **If you select `Terminate`, you will delete the entire instance, and you will have to start all over to set up the instance.** If you select `Stop`, the instance will stop running, but you will see this instance, complete with your programs and files, when you log back in. 

* The next time you log in, go back to your EC2 Dashboard and change the `Instance State` to `Start`. Then you can start from step 3 of this guide to log in to the instance. The key file (the `xxxx.pem`) will be the same, but note that the IP address (in the `IPv4 Public IP` column on your Dashboard) will change every time you stop and restart the instance. 




