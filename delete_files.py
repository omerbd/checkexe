import shutil
import os
try:
    shutil.rmtree('c:/sandbox/.vagrant')
    shutil.rmtree('c:/sandbox/vm/.vagrant')
    os.remove('Vagrantfile')
except (FileNotFoundError, OSError):
    pass
except KeyboardInterrupt:
    pass