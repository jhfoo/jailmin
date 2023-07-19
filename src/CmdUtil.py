# core
import os
import subprocess
import re
# custom
import Bastille

def guessJail(JailPart):
  jails = Bastille.getAllJails()

  ret = []
  for JailId in jails:
    if JailPart in JailId.lower():
      ret.append(JailId)

  if len(ret) == 0:
    return None
  elif len(ret) == 1:
    return ret[0]
  else:
    return ret

def setRcConf(key, value):
  ExitCode = os.system(f'sysrc {key}="{value}"')
  if ExitCode != 0:
    raise Exception(f'Unexpected exit code: {ExitCode}')
  # print (ExitCode)

def readRcConf():
  ret = {}

  RcConf = open('/etc/rc.conf','r')
  for line in RcConf.readlines():
    if line.startswith('bastille_'):
      matches = re.match('bastille_(?P<key>.+?)\s*=\s*"(?P<value>.+)"',line)
      if matches.group('key') == 'list':
        ret[matches.group('key')] = matches.group('value').split(' ')
      else:
        ret[matches.group('key')] = matches.group('value')

  RcConf.close()

  return ret

def matchJailId(TestJailId):
  jails = getJails()
  for JailId in jails.keys():
    # exact match
    if TestJailId == JailId: 
      return TestJailId

  # no exact match: try best guess
  PossibleJailId = None
  for JailId in jails.keys():
    # exact match
    if JailId.startswith(TestJailId): 
      # check if there's another possibility
      if PossibleJailId != None:
        # more than one possibility: return None
        return None
      PossibleJailId = JailId

  return PossibleJailId

def getJails():
  result = subprocess.run(['bastille','list'], capture_output=True, text=True)
  ret = {}
  for line in str(result.stdout).splitlines():
    words = line.split()
    if words[0] != 'JID':
      JailInfo = {
        'id': words[0]
      }
      offset = 0 if len(words) == 3 else 1      
      JailInfo['hostname'] = words[offset + 1]
      JailInfo['path'] = words[offset + 2]

      ret[JailInfo['id']] = JailInfo

  # print (ret)

  print (result.stderr)
  return ret