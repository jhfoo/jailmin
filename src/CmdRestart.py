import subprocess

def cmdRestart(args):
  # print (args)
  MatchedJailId = matchJailId(args.jailname)
  if MatchedJailId == None:
    print ('Invalid or ambiguous jail id')
    return

  result = subprocess.run(['bastille','restart', MatchedJailId], capture_output=True, text=True)
  print (result.stdout)
  print (result.stderr)



