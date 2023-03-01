import subprocess
import CmdUtil

def execCmd(args):
  # print (args)
  MatchedJailId = CmdUtil.matchJailId(args.JailId)
  if MatchedJailId == None:
    print ('Invalid or ambiguous jail id')
    return

  child = subprocess.Popen(['bastille','restart', MatchedJailId],
    shell=False,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    universal_newlines=True)
  while child.poll() is None:
    line = child.stdout.readline().strip()
    if line == '':
      continue
    print (line)

  # result = subprocess.run(['bastille','restart', MatchedJailId], capture_output=True, text=True)
  # print (result.stdout)
  # print (result.stderr)



