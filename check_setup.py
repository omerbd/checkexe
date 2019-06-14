# Omer Ben David
# May 2019, Israel

import os
import shutil
import subprocess
import sys
import smtplib
import time
import dropbox
import socket
from tkinter import messagebox

# a recurring error in deleting files
DELETING_ERROR = (FileNotFoundError, OSError)


def input_check(exe_path, mail_name):
    """ Checking if the input the user is getting in is correct (the mail and the path of the cheked .exe file"""
    if exe_path == '' and os.path.exists(exe_path):
        if mail_name == '':  # if both inputs are blank
            return "You didn't enter both parameters. please try again"
        return "You didn't enter any exe path.please try again."  # if only the path is blank
    if mail_name == '':  # if the mail is blank
        return "You didn't enter any mail name. please try again."
    point = exe_path.find('.')
    extension = exe_path[point:]
    if extension != '.exe':
        return "The file is not an .exe. Please try again"
    is_valid = mail_name.find('@gmail.com')
    if is_valid < 0 or is_valid == 0:  # if there is no '@gmail.com', find function will return -1
        return 'mail is not valid. please try again'
    slash = mail_name.find("\\")
    if slash != -1:
        return "ERROR you used the oppsite slash in your path. Please try again."
    return True  # if all the conditions are OK

def drop_upload(exe_path, exe_name):
    dbx = dropbox.Dropbox(
        "KDiUNCYkxhAAAAAAAAAADMDNQ-0b5iGZ-7hnUnzSVEoMNI-_73GgqXZVky6bm0Hr")
    with open(exe_path, 'rb') as f:
        dbx.files_upload(f.read(), '/CheckExe/'+str(exe_name))


def delete_files():
    """Delete all the files that are left after the VM finishes its job."""
    try:
        subprocess.check_output('python c:/sandbox/vm/bin/delete_files.py')
    except DELETING_ERROR:
        print('CheckExe could not delete those files.')


def vagrant_start():
    """Starts the VM. """
    init_cmd = 'vagrant init checkexebox.box'
    up_cmd = 'vagrant up'
    try:
        space = shutil.disk_usage("c:/")  # check how much room is in the disk
        free_gb = space.free/(2**30)
        if free_gb < 30:
            messagebox.showwarning("CheckExe 1.0.0",'You need at least 30gb free space. you have '+str(free_gb))
            sys.exit()
        try:
            subprocess.check_output(init_cmd, shell=True)
            messagebox.showinfo("CheckExe 1.0.0",'init done')
            try:
                os.remove('Vagrantfile')  # delete the wrong Vagrantfile
                try:
                    # copies the correct Vagrantfile into the folder
                    shutil.copyfile('c:/sandbox/Vagrantfile',
                                    'c:/sandbox/vm/Vagrantfile')
                    messagebox.showinfo("CheckExe 1.0.0",'init moved')
                    messagebox.showinfo("CheckExe 1.0.0",'15-30 seconds from now you will not be able to exit because vagrant will be locked.')
                    try:
                        subprocess.check_output(up_cmd, shell=True)
                        messagebox.showinfo("CheckExe 1.0.0",'vm up')
                    except subprocess.CalledProcessError:
                        messagebox.showerror("CheckExe 1.0.0",
                            "CheckExe can't get the virtual machine up. Please try again.")
                        try:
                            delete_files()
                        except DELETING_ERROR as error:
                            print(error)
                except (OSError, FileNotFoundError) as Vagrantfile_error:
                    messagebox.showerror("CheckExe 1.0.0",
                        "CheckExe can't move the correct Vagrantfile into the folder.")
            except OSError:
                messagebox.showerror("CheckExe 1.0.0","CheckExe can't delete the current Vagrantfile")
        except subprocess.CalledProcessError:
            messagebox.showerror("CheckExe 1.0.0","Vagrant init failed.Please try again")
            sys.exit()
    except Exception as space_error:
        print(space_error)


def destroy_vagrant():
    """The VM is destroyed after the end of its use."""
    try:
        subprocess.check_output('python c:/sandbox/vm/bin/destroy.py')
    except (socket.error) as e:
        pass


def winrm_failed():
    """If winrm connection failes mid-through, this proc will delete all of the 'leftovers' and destroy the machine."""
    try:
        delete_files()
        try:
            destroy_vagrant()
        except Exception as destroy_error:
            print(destroy_error)
    except DELETING_ERROR:
        pass
    sys.exit()


def winrm_call(mail_name, exe_name):
    """Downloads the file into the machine, runs it and then compiles a report on its internet activity."""
    drop_cmd = "vagrant winrm -c 'python C:\\sandbox\\drop_down.py /checkexe/"+exe_name+"'"
    run_cmd = "vagrant winrm -c 'C:\\users\\vagrant\\documents\\check.exe'"
    report_cmd = "vagrant winrm -c 'python C:\\sandbox\\vm_inside_functions.py " + \
        mail_name+" check'"
    try:
        # downloads the file from dropbox
        subprocess.check_output(drop_cmd, shell=True)
        messagebox.showinfo("CheckExe 1.0.0",'The file was downloaded.')
        try:
            # runs the machine. it is Popen and not check_output because the latter is a blocking function
            subprocess.Popen(run_cmd)
            messagebox.showinfo("CheckExe 1.0.0",'The file is running.')
            try:
                # prints the message from vm_inside_functions and compiles the report
                report_message = subprocess.check_output(
                    report_cmd, shell=True)
                messagebox.showinfo("CheckExe 1.0.0",report_message.decode("utf-8"))
            except subprocess.CalledProcessError:
                messagebox.showerror("CheckExe 1.0.0","CheckExe have failed to make a report.")
                # uses the proc for situations where the winrm commands or winrm connection failed.
                winrm_failed()
            except (SMTPAuthenticationError, Microsoft.PowerShell.Commands) as email_error:
                messagebox.showerror("CheckExe 1.0.0",'Your email was invalid. Please try again')
                winrm_failed()
        except subprocess.CalledProcessError:
            messagebox.showerror("CheckExe 1.0.0","CheckExe couldn't run the file inside the virtual machine.")
            winrm_failed()
    except (subprocess.CalledProcessError, dropbox.exceptions.ApiError) as dropbox_error:
        messagebox.showerror("CheckExe 1.0.0","CheckExe can't download the file from Dropbox into the virtual machine. Please try again.")
        winrm_failed()


def main():
        try:
            subprocess.check_output('python c:/sandbox/vm/bin/delete_files.py')
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass
        try:
            # the path of the file you want to check
            # the mail to which the report will be sent
            #mail_name = input('please enter your gmail address: ')
            exe_path=sys.argv[1]
            mail_name=sys.argv[2]
            check=(input_check(exe_path,mail_name))
            if check==True:
                messagebox.showinfo("CheckExe 1.0.0","Welcome to CheckExe, a powerful tool that lets you know if you should run the program you just received! To exit, press CTRL+C.")
                exe_split = exe_path.split('/')
                exe_name = exe_split[-1]  # extract the name from the path
                try:
                    drop_upload(exe_path, exe_name)
                    try:
                        vagrant_start()
                        time.sleep(15)
                        try:
                            winrm_call(mail_name, exe_name)
                            time.sleep(60)
                            try:
                                subprocess.check_output(
                                    'python c:/sandbox/vm/bin/destroy.py')
                                try:
                                    subprocess.check_output(
                                        'python c:/sandbox/vm/bin/delete_files.py')
                                    messagebox.showinfo("CheckExe 1.0.0",'CheckExe is done with its check. Have a plesant day!')
                                except (subprocess.CalledProcessError, FileNotFoundError, OSError) as error:
                                    pass
                            except (subprocess.CalledProcessError, FileNotFoundError, OSError) as error:
                                pass
                        except Exception as winrm_error:
                            print(winrm_error)
                    except Exception as vagrant_error:
                        print(vagrant_error)
                except FileNotFoundError:
                    messagebox.showerror("CheckExe 1.0.0",
                        'CheckExe cannot copy the file into Dropbox. Check if you entered the path correctly.')
                except dropbox.exceptions.ApiError:
                    messagebox.showerror("CheckExe 1.0.0",
                        "CheckExe can't upload your file to DropBox. Please try again.")
                    delete_files()
            else:
                messagebox.showerror("CheckExe 1.0.0", check)
        except KeyboardInterrupt:
            delete_files()
            destroy_vagrant()
            time.sleep(10)
            messagebox.showwarning("CheckExe 1.0.0", "You exited CheckExe. Do not pay attention to the Vagrant Message.")
            sys.exit()
        except IndexError:
            messagebox.showerror("CheckExe 1.0.0","You didn't enter all the parameters. Please try again.")
            sys.exit()


if __name__ == "__main__":
    main()
