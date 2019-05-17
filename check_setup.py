# Omer Ben David
# May 2019, Israel

import os
import shutil
import subprocess
import sys
import smtplib
import time
import dropbox

DELETING_ERROR= (FileNotFoundError, OSError)  # a recurring error in deleting files

def input_check(exe_path, mail_name):
	""" Checking if the input the user is getting in is correct (the mail and the path of the cheked .exe file"""
	if exe_path=='':
		if mail_name=='': # if both inputs are blank
			return "You didn't enter both parameters. please try again"
		return "You didn't enter any exe path.please try again." # if only the path is blank
	if mail_name=='': # if the mail is blank
		return "You didn't enter any mail name. please try again."
	is_valid=mail_name.find('@gmail.com')
	if is_valid<0 or is_valid==0: # if there is no '@gmail.com', find function will return -1
		return 'mail is not valid. please try again'
	slash=mail_name.find("\\")
	if slash!=-1:
		return "ERROR you used the oppsite slash in your path. Please try again."
	return True # if all the conditions are OK


def delete_files():
	"""Delete all the files that are left after the VM finishes its job."""
	try:
		shutil.rmtree('c:/sandbox/.vagrant')
		try:
			shutil.rmtree('c:/sandbox/vm/.vagrant')
			try:
				os.remove('Vagrantfile')
			except DELETING_ERROR:
				pass
		except DELETING_ERROR:
			pass
	except DELETING_ERROR:
		pass

def vagrant_start():
	"""Starts the VM. """
	init_cmd='vagrant init vmpackage.box'
	up_cmd='vagrant up'
	try:
		space =shutil.disk_usage("c:/") # check how much room is in the disk
		free_gb=space.free/(2**30)
		if free_gb<30:
			print ('you need at least 30gb free space. you have '+str(free_gb))
			sys.exit()
		try:
			subprocess.check_output(init_cmd, shell=True)
			print ('init done')
			try:
				os.remove('Vagrantfile') # delete the wrong Vagrantfile
				try:
					shutil.copyfile('c:/sandbox/Vagrantfile', 'c:/sandbox/vm/Vagrantfile') # copies the correct Vagrantfile into the folder
					print ('init moved')
					try:
						subprocess.check_output(up_cmd, shell=True)
						print ('vm up')
					except subprocess.CalledProcessError:
						print ("CheckExe can't get the virtual machine up. Please try again.")
						try:
							delete_files()
						except DELETING_ERROR as error:
							print (error)
				except (OSError, FileNotFoundError) as Vagrantfile_error:
					print ("CheckExe can't move the correct Vagrantfile into the folder.")
			except OSError:
				print ("CheckExe can't delete the current Vagrantfile")
		except subprocess.CalledProcessError:
			print ("Vagrant init failed.Please try again")
			sys.exit()
	except Exception as space_error:
		print (space_error)


def destroy_vagrant():
	"""The VM is destroyed after the end of its use."""
	halt_cmd="vagrant halt"
	dest_cmd="vagrant destroy -f"
	try: # first you halt the machine so it won't be forced
		subprocess.check_output(halt_cmd, shell=True)
		try: # and then you destroy the machine and all of its files
			subprocess.check_output(dest_cmd, shell=True)
		except subprocess.CalledProcessError:
			print ('Vagrant cannot destroy itself.')
	except subprocess.CalledProcessError:
		print ('Vagrant canno halt.')	

def winrm_failed():
	"""If winrm connection failes mid-through, this proc will delete all of the 'leftovers' and destroy the machine."""
	try:
		delete_files()
		try:
			destroy_vagrant()
		except Exception as destroy_error:
			print (destroy_error)
	except DELETING_ERROR:
		pass
	sys.exit()

def winrm_call(mail_name, exe_name):
	"""Downloads the file into the machine, runs it and then compiles a report on its internet activity."""
	drop_cmd="vagrant winrm -c 'python C:\\sandbox\\drop_down.py /"+exe_name+"'"
	run_cmd="vagrant winrm -c 'C:\\users\\vagrant\\documents\\check.exe'"
	report_cmd="vagrant winrm -c 'python C:\\sandbox\\vm_inside_functions.py "+mail_name+" check'"
	try:
		subprocess.check_output(drop_cmd, shell=True) # downloads the file from dropbox
		print ('The file was downloaded.')
		try:
			subprocess.Popen(run_cmd) # runs the machine. it is Popen and not check_output because the latter is a blocking function
			print ('The file is running.')
			try:
				print(subprocess.check_output(report_cmd, shell=True)) # prints the message from vm_inside_functions and compiles the report
			except subprocess.CalledProcessError:
				print ("CheckExe have failed to make a report.")
				winrm_failed() # uses the proc for situations where the winrm commands or winrm connection failed.
			except (SMTPAuthenticationError,Microsoft.PowerShell.Commands) as email_error:
				print ('Your email was invalid. Please try again')
				winrm_failed()
		except subprocess.CalledProcessError:
			print ("CheckExe couldn't run the file inside the virtual machine.")
			winrm_failed()
	except (subprocess.CalledProcessError, dropbox.exceptions.ApiError) as dropbox_error:
		print ("CheckExe can't download the file from Dropbox into the virtual machine. Please try again.")
		winrm_failed()
			
def main():
	exe_path =input('please enter the path of the exe you want to check, with only / between folders: ') # the path of the file you want to check
	mail_name=input('please enter your gmail address: ') # the mail to which the report will be sent
	check=input_check(exe_path, mail_name) # cheking the input
	if check==True: # if the input is OK
		exe_split=exe_path.split('/')
		exe_name=exe_split[-1] # extract the name from the path
		try:
			shutil.copyfile(exe_path, 'C:\\Users\\kodi\\Dropbox\\Apps\\CheckExe\\'+exe_name) # copy the .exe into dropbox
			try:
				vagrant_start()
				try:
					winrm_call(mail_name,exe_name)
					try:
						destroy_vagrant()
						try:
							delete_files()
						except subprocess.CalledProcessError:
							pass
					except subprocess.CalledProcessError:
						print ('Vagrant cannot destroy itself.')
				except Exception as winrm_error:
					print (winrm_error)
			except Exception as vagrant_error:
				print (vagrant_error)
		except FileNotFoundError:
			print ('CheckExe cannot copy the file into Dropbox. Check if you entered the path correctly.')
		except PermissionError:
			print ("You cannot use the file you tried to check because you don't have permission. Please try again.")
	else:
		print (check)
		
		
if __name__=="__main__":
	main()
