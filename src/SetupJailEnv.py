# core lib
import subprocess

# public lib
import psutil




def getOptionInput(text, default = '', IsYesNo = True, IsYesDefault = False, IsNoDefault = False):
  if default == '':
    if IsYesNo:
      if IsYesDefault:
        OptionStr = 'Y/n'
      elif IsNoDefault:
        OptionStr = 'y/N'
      else:
        OptionStr = ''
  else:
    OptionStr = default

  while True:
    resp = input (text + ' [{}]'.format(OptionStr)).lower()
    if resp == '':
      if IsYesDefault:
        resp = 'y'
        break
      elif IsNoDefault:
        resp = 'n'
        break
      elif not default == '':
        resp = default
        break
    else:
      if default != '':
        return resp
      elif IsYesNo:
        if resp == 'y' or resp == 'n':
          break
      else:
        break

  return resp

def execShell(cmd):
  proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
  while True:
    line = proc.stdout.readline()
    print (line.strip())
    PollResult = proc.poll()
    # print (PollResult)
    if line == '' and PollResult is not None:
      break

def do():
  print ('Interfaces: ', end='')
  interfaces = []
  for intf in psutil.net_if_addrs().keys():
    if not intf == 'lo0':
      interfaces.append(intf)

  print ('OK')
  for intf in interfaces:
    print ('- {}'.format(intf))

  resp = getOptionInput('Update rc.conf?', IsYesDefault=True)
  if resp == 'y':
    BridgeAddress = getOptionInput('- Bridge address?', default='192.168.100.1/24')
    execShell('./bin/install-rc.conf {}'.format(BridgeAddress))

  # resp = getOptionInput('Restart network?', IsYesDefault=True)
  # if resp == 'y':
  #   execShell('sudo service netif restart')