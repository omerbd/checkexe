"# CheckExe"
# Omer Ben David
# May 2019

# Description:
A simple tool aimed at people with little knowledge in viruses and in monitoring internet data who want to check a .exe file that may harm their computer.

# Installing:
using the batch file included here (will be included later as of 17/5/2019)
if the batch is not prepared yet, please follow:
1. Create a sandbox dir in C:/
2. move the Vagrantfile into it
3. create a vm dir inside the sandbox dir
4. Move the .box file into it and the check_setup.py
5. create a bin dir inside the vm dir and move destroy.py and delete_files.py in there

# How to use:
1.Download the package <br />
2. Use the batch file to install (will be added later) <br />
3. Click the check_setup.py and enter the path of the .exe you want to check and your mail <br />
4. Wait for the message that says that you're done and check the results in your mail <br />


# Notes:
- Do note that you can play with the Vagrantfile memory. The default is 8gb ram for it to run as smoothly as possible, but it won't work on computers with max 8 giga ram and might be problematic on computers with less that 16gb.
