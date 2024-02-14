# core
import os
import subprocess
import re
# custom
import jailmin.Bastille as Bastille

def elevatePermissions(args, cmds):
  cmds.insert(0,'sudo')
  return cmds

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
  IDX_JID = 0
  IDX_STATE = 1
  IDX_IP = 2
  IDX_ADDRESS = 3
  IDX_HOSTNAME = 4
  IDX_RELEASE = 5
  IDX_PATH = 6

  result = subprocess.run(elevatePermissions(None,['bastille','list','-a']) , capture_output=True, text=True)
  ret = {}
  for line in str(result.stdout).splitlines():
    words = line.split()
    # print (f"{words}")
    if words[IDX_JID] != 'JID':
      JailInfo = {
        'id': words[IDX_JID]
      }
      JailInfo['hostname'] = words[IDX_HOSTNAME]
      JailInfo['path'] = words[IDX_PATH]
      JailInfo['state'] = words[IDX_STATE]

      ret[JailInfo['id']] = JailInfo

    # print (ret)

  print (result.stderr)
  return ret