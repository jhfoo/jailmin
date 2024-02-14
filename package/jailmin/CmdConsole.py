import os
import subprocess
import shutil
import jailmin.CmdUtil as CmdUtil

def execCmd(args):
  # print (args)

  MatchedJailId = CmdUtil.matchJailId(args.JailId)
  if MatchedJailId == None:
    print ('Invalid or ambiguous jail id')
    return

  print (f'Applying CONSOLE cmd: {MatchedJailId}')

  result = subprocess.run(CmdUtil.elevatePermissions(args, ['bastille','console', MatchedJailId]))
  print (result.stdout)
  print (result.stderr)

def addParser(parser):
  ConsoleParser = parser.add_parser('console', 
    help='overloaded Bastille console command', 
  )
  ConsoleParser.add_argument('JailId')
  ConsoleParser.set_defaults(func=execCmd)
