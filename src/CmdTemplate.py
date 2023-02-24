import os
import subprocess
import shutil



def execCmd(args):
  BaseParams = ['bastille','template']
  CmdArgs = getattr(args,'CmdArgs')

  # execute stock Bastille commands
  result = subprocess.run(BaseParams + CmdArgs, capture_output=True, text=True)
  print (result.stdout)
  print (result.stderr)
