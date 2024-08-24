import json
import os
import re
import subprocess
import shutil
import jailmin.CmdUtil as CmdUtil

def execCmd(args):
  # print (args)

  result = subprocess.run(
    CmdUtil.elevatePermissions(args, ['bastille','list','-a']),
    capture_output = True)

  FieldNames = []
  jails = []
  if result.returncode == 0:
    for idx, line in enumerate(result.stdout.decode('utf-8').splitlines()):
      if idx == 0:
        for FieldName in re.split(r'\s+', line):
          # print (f'field: {FieldName}')
          FieldNames.append(FieldName)
      else:
        # print (f'New line')
        rec = {}
        for idx, FieldValue in enumerate(re.split(r'\s+', line)):
          FieldName = FieldNames[idx]
          if FieldNames[idx] != '':
            rec[FieldNames[idx]] = FieldValue 
            # print (f'field: {FieldValue}')
        jails.append(rec)
  else:
    print (result.stderr)

  if 'json' in args and args.json:
    print (json.dumps(jails, indent=2))
  else:
    print(result.stdout.decode('utf-8'))

  return jails

def setSubparser(cmdparser):
  ListParser = cmdparser.add_parser('list', 
    help='overloaded Bastille list command', 
  )
  ListParser.add_argument('-j', '--json', default = False, action='store_true')
  ListParser.set_defaults(func=execCmd)
