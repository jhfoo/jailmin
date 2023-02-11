import subprocess

RELEASE_LATEST = '13.1-RELEASE'

def cmdBootstrap(args):
  BaseParams = ['bastille','bootstrap']
  CmdArgs = getattr(args,'CmdArgs')
  if len(CmdArgs) > 0 and CmdArgs[0] == 'latest':
    CmdArgs[0] = RELEASE_LATEST

  result = subprocess.run(BaseParams + CmdArgs, capture_output=True, text=True)
  print (result.stdout)
  print (result.stderr)
