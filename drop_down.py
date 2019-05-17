import dropbox
import sys
import os
dbx = dropbox.Dropbox("KDiUNCYkxhAAAAAAAAAADMDNQ-0b5iGZ-7hnUnzSVEoMNI-_73GgqXZVky6bm0Hr") # dropbox API demands a registered token for it to work
try:
	FILE=sys.argv[1]
	file_name=FILE[1:] # extracts the / from the name
	with open(file_name, "wb") as f: # name of the sent file
		try:
			metadata, res = dbx.files_download(path=str(FILE)) # name of the file you actually send
			f.write(res.content)
		except dropbox.exceptions.ApiError:
			print ("Dropbox API doesn't work. please try again.")
except dropbox.stone_validators.ValidationError:
	print ('please add / before the name of the file to be at full compliance with dropbox API')
	os.remove(file_name)
except IndexError:
	print ("you didn't put any file name")
