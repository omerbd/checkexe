import dropbox
import sys
#FILE='/check.exe'
FILE=sys.argv[1]
print (FILE)
dbx = dropbox.Dropbox("KDiUNCYkxhAAAAAAAAAADMDNQ-0b5iGZ-7hnUnzSVEoMNI-_73GgqXZVky6bm0Hr")
with open("check.exe", "wb") as f: # name of the sent file
    metadata, res = dbx.files_download(path=str(FILE)) # name of the file you actually send
    f.write(res.content)
