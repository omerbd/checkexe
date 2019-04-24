# get the file
# move the file into dropbox
# winrm check if the file is there loop in 1st VM
# winrm download the dropbox file to the desired dir
# winrm start the .exec
# winrm start the python final_vers file
# winrm close the VM
# winrm destory the VM
# print 'it's finished. check your mail'
import dropbox
dbx = dropbox.Dropbox("KDiUNCYkxhAAAAAAAAAADMDNQ-0b5iGZ-7hnUnzSVEoMNI-_73GgqXZVky6bm0Hr")
try:
	answer=dbx.files_get_metadata('/abdudi.exe')
except dropbox.exceptions.ApiError:
	print ('no')
