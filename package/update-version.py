# core
import argparse
# community
import toml
import semver

FILE_TOML = 'pyproject.toml'
FILE_LOCAL_INSTALL_PART = 'install-local'
FILE_USER_INSTALL_PART = 'install-user'

def upgradeVersion(args, ver):
  if args.minor:
    return ver.bump_minor()
  if args.patch:
    return ver.bump_patch()

  # else
  return ver.bump_build()

def updateExecScript(fname, ver):
  infile = open(f"{fname}.template",'r')
  template = infile.read()
  infile.close()

  outfile = open(f"bin/{fname}",'w')
  template = template.replace('__VERSION__',ver)
  outfile.write(template)
  outfile.close()

infile = open(FILE_TOML,'r')
config = toml.loads(infile.read())
infile.close()

parser = argparse.ArgumentParser(
  prog='update-version'
)
parser.add_argument('--minor', action=argparse.BooleanOptionalAction)
parser.add_argument('--build', action=argparse.BooleanOptionalAction)
parser.add_argument('--patch', action=argparse.BooleanOptionalAction)
args = parser.parse_args()

ver = upgradeVersion(args, semver.Version.parse(config['project']['version']))
config['project']['version'] = str(ver)
print (f"New version: {ver}")

outfile = open(FILE_TOML,'w')
outfile.write(toml.dumps(config))
outfile.close()

updateExecScript(FILE_LOCAL_INSTALL_PART), str(ver))
updateExecScript(FILE_USER_INSTALL_PART), str(ver))

# infile = open(f"{FILE_LOCAL_INSTALL_PART}.template",'r')
# template = infile.read()
# infile.close()

# outfile = open(f"bin/{FILE_LOCAL_INSTALL_PART}",'w')
# template = template.replace('__VERSION__',str(ver))
# outfile.write(template)
# outfile.close()
