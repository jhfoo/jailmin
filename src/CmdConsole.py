import os
import subprocess
import shutil
import CmdUtil

def execCmd(args):
  # print (args)

  MatchedJailId = CmdUtil.matchJailId(args.JailId)
  if MatchedJailId == None:
    print ('Invalid or ambiguous jail id')
    return

  print (f'Matched jail: {MatchedJailId}')
  result = subprocess.run(['bastille','console', MatchedJailId])
  print (result.stdout)
  print (result.stderr)