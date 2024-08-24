# core
import argparse
import importlib.metadata
# custom
import jailmin.CmdConsole as CmdConsole
import jailmin.CmdList as CmdList

def doCli():
  print(f"Jailmin version {importlib.metadata.version('jailmin')}")

  parser = argparse.ArgumentParser(
    prog='jailmin',
    # help='Bastille wrapper'
  )
  cmdparser = parser.add_subparsers(dest='cmd')

  CmdConsole.addParser(cmdparser)
  CmdList.setSubparser(cmdparser)

  args = parser.parse_args()
  print (f"cmd: {args.cmd}")
  if args.cmd:
    args.func(args = args)
  else:
    CmdList.execCmd(args = args)

