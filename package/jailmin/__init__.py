# core
import argparse
import importlib.metadata
# custom
import jailmin.CmdConsole as CmdConsole

def cmdList(args):
  print ('list')

def doCli():
  print(f"Jailmin version {importlib.metadata.version('jailmin')}")

  parser = argparse.ArgumentParser(
    prog='jailmin',
    # help='Bastille wrapper'
  )
  cmdparser = parser.add_subparsers(dest='cmd')

  CmdConsole.addParser(cmdparser)

  ListParser = cmdparser.add_parser('list', 
    help='overloaded Bastille list command', 
  )
  ListParser.set_defaults(func=cmdList)

  args = parser.parse_args()
  args.func(args)

  print (f"cmd: {args.cmd}")