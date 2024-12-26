# core
import argparse
# community
import toml
import semver

FILE_TOML = 'pyproject.toml'
FILE_LOCAL_INSTALL_PART = 'install-local'
FILE_USER_INSTALL_PART = 'install-user'

def upgradeVersion(ver):
  args = getArgs()

  if args.minor:
    return ver.bump_minor()
  if args.patch:
    return ver.bump_patch()

  # else
  return ver.bump_build()

def updateExecScript(fname, ver):
  template = ''
  with open(f"conf/template/{fname}",'r') as infile:
    template = infile.read()

  with open(f"bin/{fname}",'w') as outfile:
    template = template.replace('__VERSION__',ver)
    outfile.write(template)

def getArgs():
  parser = argparse.ArgumentParser(
    prog='update-version'
  )
  parser.add_argument('--minor', action=argparse.BooleanOptionalAction)
  parser.add_argument('--build', action=argparse.BooleanOptionalAction)
  parser.add_argument('--patch', action=argparse.BooleanOptionalAction)
  return parser.parse_args()

def getNewVersion():
  infile = open(FILE_TOML,'r')
  config = toml.loads(infile.read())
  infile.close()

  ver = upgradeVersion(semver.Version.parse(config['project']['version']))

  config['project']['version'] = str(ver)
  print (f"New version: {ver}")

  outfile = open(FILE_TOML,'w')
  outfile.write(toml.dumps(config))
  outfile.close()

  return ver

ver = getNewVersion()
updateExecScript(FILE_LOCAL_INSTALL_PART, str(ver))
updateExecScript(FILE_USER_INSTALL_PART, str(ver))

