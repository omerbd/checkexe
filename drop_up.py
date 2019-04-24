import shutil
PATH= input("please enter the path of the file you want to check:")
try:
	shutil.move(PATH, 'C:/Users/kodi/Dropbox/Apps/CheckExe/check.exe')
	print ("OK")
except Exception:
	print ("ERROR")