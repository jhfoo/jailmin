#!/usr/local/bin/python3.8
# core modules
from ast import parse
from curses import has_key
from importlib.resources import path
import os
import sys
import pathlib

def appendLibPath():
  # Assumes lib/ is relative to actual jailmin.py, not the soft link
  # in future this should be moved to /usr/local/bin/jailminlib/
  BinFullFilename = __file__
  if os.path.islink(BinFullFilename):
    BinFullFilename = os.readlink(BinFullFilename)
  AppPath = str(pathlib.Path(os.path.join(os.path.dirname(BinFullFilename), '..')).resolve())
  sys.path.append(AppPath)

  sys.path.append('/usr/local/etc/jailmin/packages')

appendLibPath()

# custom
import jailminlib.logger as logger
import jailminlib.init as init
import jailminlib.BastilleAdapter as BastilleAdapter
import jailminlib.CliParser as CliParser
import jailminlib.statebuilder as statebuilder

JailManager = BastilleAdapter.BastilleAdapter ()

logger.onlyConsole()
init.validateRoot()

CurrentJailState = statebuilder.getCurrentState(JailManager)
CliParser.execCli(CliParser.parseCli(), JailManager, CurrentJailState)


