import os
import sys


def validateRoot():
  """Confirms process has root privileges"""
  if os.getuid() != 0:
    print ('INSUFFICIENT PRIVILEGES: jailmin requires root privileges to run some commmands (eg. iocage). Run jail as root or use sudo')
    sys.exit(1)