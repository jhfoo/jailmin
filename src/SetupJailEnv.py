# core lib
import re
import subprocess

# public lib
import psutil




def getOptionInput(text, default = None, IsYesNo = True, IsYesDefault = False, IsNoDefault = False, choices = None):
  if default == None:
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
      # no selection: use default if set
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
      # custom input
      # must choose from list
      if not choices == None:
        if resp in choices:
          return resp
        else:
          print ('Options: {}'.format(choices))
      elif default != None:
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

def updatePfConf(BridgeSubnet, InternetInterface):
  infile = open('/etc/pf.conf', 'r')
  lines = [
    '# JAILMIN START: do not edit',
    'WANIF = "{}"'.format(InternetInterface),
    'JAILNET = "{}"'.format(BridgeSubnet),
    'nat on $WANIF inet from { $JAILNET } to any -> {$WANIF}',
    '# JAILMIN END: do not edit',
  ]

  isSkipLine = False
  for line in infile.readlines():
    if re.search('# JAILMIN START', line):
      isSkipLine = True
    elif re.search('# JAILMIN END', line):
      isSkipLine = False
    elif not isSkipLine:    
      lines.append(line.strip())
  infile.close()

  outfile = open('/etc/pf.conf','w')
  for line in lines:
    outfile.write(line + '\n')
  outfile.close()

  execShell('pfctl -f /etc/pf.conf')

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
    BridgeSubnet = getOptionInput('- Bridge subnet?', default='192.168.100.0/24')
    InternetInterface = getOptionInput('- Internet interface?', default=interfaces[0], choices=interfaces)
    execShell('./bin/install-rc.conf {}'.format(BridgeAddress))
    updatePfConf(BridgeSubnet = BridgeSubnet, InternetInterface = InternetInterface)

  # resp = getOptionInput('Restart network?', IsYesDefault=True)
  # if resp == 'y':
  #   execShell('sudo service netif restart')