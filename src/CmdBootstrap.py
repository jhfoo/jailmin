import os
import subprocess

RELEASE_LATEST = '13.1-RELEASE'
LIST_RELEASE = 'release'
LIST_ALL = 'all'
LIST_TEMPLATE = 'template'
DIR_RELEASES = '/usr/local/bastille/releases'
DIR_TEMPLATES = '/usr/local/bastille/templates'

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

def cmdBootstrap(args):
  BaseParams = ['bastille','bootstrap']
  CmdArgs = getattr(args,'CmdArgs')
  if len(CmdArgs) > 0:
    if CmdArgs[0] == 'latest':
      CmdArgs[0] = RELEASE_LATEST
    elif CmdArgs[0] == 'list' or CmdArgs[0] == 'ls':
      CmdArgs.pop(0)
      listBootstrap(CmdArgs)

  result = subprocess.run(BaseParams + CmdArgs, capture_output=True, text=True)
  print (result.stdout)
  print (result.stderr)
