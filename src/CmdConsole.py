import os
import subprocess
import shutil
import CmdUtil

def execCmd(args):
  # print (args)
  CmdArgs = getattr(args,'CmdArgs')
  JailName = CmdArgs[0]

  MatchedJailId = CmdUtil.matchJailId(JailName)
  if MatchedJailId == None:
    print ('Invalid or ambiguous jail id')
    return

  result = subprocess.run(['bastille','console', MatchedJailId])
  print (result.stdout)
  print (result.stderr)