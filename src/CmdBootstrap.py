import os
import subprocess
import shutil

RELEASE_LATEST = '13.1-RELEASE'
LIST_RELEASE = 'release'
LIST_ALL = 'all'
LIST_TEMPLATE = 'template'
DIR_CACHE = '/usr/local/bastille/cache'
DIR_RELEASES = '/usr/local/bastille/releases'
DIR_TEMPLATES = '/usr/local/bastille/templates'
DIR_ZFS_BASE = 'zroot/bastille'
BOOTSTRAP_CMD_LATEST = 'latest'
BOOTSTRAP_CMD_LIST = ['list', 'ls']
BOOTSTRAP_CMD_DELETE = ['delete', 'del']

def listReleases():
  releases = os.listdir(DIR_RELEASES)
  releases.sort()
  print ('Bootstrapped releases ({})'.format(len(releases)))

  for release in releases:
    print ('- {}'.format(release))  

def listTemplates():
  templates = os.listdir(DIR_TEMPLATES)
  templates.sort()
  print ('Bootstrapped templates ({})'.format(len(templates)))

  for template in templates:
    print ('- {}'.format(template))  


def listBootstrap(args):
  # list releases by default
  context = LIST_RELEASE
  if len(args) > 0:
    if args[0] == LIST_TEMPLATE:
      context = LIST_TEMPLATE
    elif args[0] == LIST_ALL:
      context = LIST_ALL

  if context == LIST_RELEASE or context == LIST_ALL:
    listReleases()
  if context == LIST_TEMPLATE or context == LIST_ALL:
    if context == LIST_ALL:
      print ('')
    listTemplates()

def rmZfsPath(ZfsDelPath):
  result = subprocess.run(['zfs', 'destroy', '-r', ZfsDelPath], 
    capture_output=True, text=True)
  print (result.stdout)
  print (result.stderr)

def deleteBootstrap(args):
  if len(args) < 2:
    print ('Missing argument(s): Expect [release|template] [release/template name]')
    return
  if not args[0] in [LIST_RELEASE, LIST_TEMPLATE]:
    print ('Unknown first argument: Expect [release|template]')
    return

  TargetDir = DIR_RELEASES if args[0] == LIST_RELEASE else DIR_TEMPLATES
  subfolder = args[1]
  if subfolder in os.listdir(TargetDir):
    print (TargetDir + '/' + subfolder)

    if args[0] == LIST_RELEASE:
      rmZfsPath(DIR_ZFS_BASE + '/cache/' + subfolder)
      shutil.rmtree(DIR_CACHE + '/' + subfolder)

      rmZfsPath(DIR_ZFS_BASE + '/releases/' + subfolder)
      shutil.rmtree(DIR_RELEASES + '/' + subfolder)
  else:
    print ('Missing release or template: {}'.format(subfolder))

  

def cmdBootstrap(args):
  BaseParams = ['bastille','bootstrap']
  CmdArgs = getattr(args,'CmdArgs')
  if len(CmdArgs) > 0:
    cmd = CmdArgs.pop(0)
    if cmd == BOOTSTRAP_CMD_LATEST:
      CmdArgs.insert(0, RELEASE_LATEST) 
    elif cmd in BOOTSTRAP_CMD_LIST:
      listBootstrap(CmdArgs)
      return
    # iced until learnt how to remove ../releases and ../templates
    # elif cmd in BOOTSTRAP_CMD_DELETE:
    #   deleteBootstrap(CmdArgs)
      return
    elif cmd in BOOTSTRAP_CMD_DELETE:
      deleteBootstrap(CmdArgs)
      return
    else:
      # legacy cmd args: put the cmd back into CmdArgs
      CmdArgs.insert(0, cmd) 

  # execute stock Bastille commands
  result = subprocess.run(BaseParams + CmdArgs, capture_output=True, text=True)
  print (result.stdout)
  print (result.stderr)
