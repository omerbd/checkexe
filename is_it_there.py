import os
import sys
file_path=sys.argv[1]
exists = os.path.isfile(str(file_path))
if exists:
	print (True)