import subprocess
import time
dest_cmd = "vagrant destroy -f"
try:
    subprocess.check_output("vagrant winrm -c 'shutdown -s -t 0'")
    print ('shutdown')
    time.sleep(15)
    subprocess.check_output(dest_cmd)
    print ('destroy')
except subprocess.CalledProcessError:
    pass
except socketError:
    pass
