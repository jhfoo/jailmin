# import core
# from lib2to3.pytree import Base
import os
import pathlib
import re
import shutil
import subprocess

# import oss
import yaml

# import custom
import jailminlib.util as util
import jailminlib.logger as logger

PATH_BASE = '/usr/local/bastille'

def stageReset():
  shutil.rmtree(PATH_BASE + '/temp')
  os.makedirs(PATH_BASE + '/temp/templates')

def stageTemplate(TemplateName, varfile):
  TemplatePath = PATH_BASE + '/' + TemplateName
  TemplateTempParentPath = PATH_BASE + '/temp/templates'
  
  logger.debug('TemplatePath: {}'.format(TemplatePath))
  logger.debug('TemplateTempParentPath: {}'.format(TemplateTempParentPath))

  # validate Bastillefile exists
  BastilleFile = TemplatePath + '/Bastillefile'
  if not pathlib.Path(BastilleFile).is_file():
    raise Exception ('Missing file: {}'.format(BastilleFile))

  # os.makedirs(TemplateTempParentPath)
  # duplicate orig template to temp folder  
  output = subprocess.run(['cp','-r',TemplatePath, TemplateTempParentPath], encoding='utf8', capture_output=True)
  logger.debug ('STDOUT cp: {}'.format(str(output.stdout)))

  TempTemplatePath = PATH_BASE + '/temp/' + TemplateName
  StagedFileContent = stageBastillefile(TempTemplatePath, varfile)
  logger.debug ('Bastillefile {}:\n{}'.format(TempTemplatePath, StagedFileContent))

def stageBastillefile(TemplatePath, varfile):
  FullBastillefile = TemplatePath + '/Bastillefile'
  if not pathlib.Path(FullBastillefile).is_file():
    raise Exception('Invalid Bastillefile path: {}'.format(FullBastillefile))

  InFile = open(FullBastillefile,'r')
  lines = []
  line = InFile.readline()
  while line:
    match = re.match(r'^include\s+(\S+)', line, re.IGNORECASE)
    if match:
      DependentTemplate = match.group(1)
      lines.append('INCLUDE temp/' + DependentTemplate)
      stageTemplate(DependentTemplate, varfile)
      # ret += parseFile(BasePath + '/' + match.group(1) + '/Bastillefile', BasePath)
    else:
      lines.append(line.strip())

    line = InFile.readline()

  InFile.close()

  ret = '\n'.join(lines)
  Outfile = open(FullBastillefile,'w')
  Outfile.write(ret)
  Outfile.close()

  return ret

def parseFile(fname, BasePath):
  if not pathlib.Path(fname).is_file():
    raise Exception('Invalid Bastillefile path: {}'.format(fname))

  InFile = open(fname,'r')
  ret = []
  line = InFile.readline()
  while line:
    match = re.match(r'^include\s+(\S+)', line, re.IGNORECASE)
    if match:
      ret += parseFile(BasePath + '/' + match.group(1) + '/Bastillefile', BasePath)
    else:
      ret.append(line.strip())

    line = InFile.readline()

  InFile.close()

  return ret

def parseVarfile(fname):
  if not pathlib.Path(fname).is_file():
    print ('Missing varfile {}'.format(fname))
    return

  infile = open(fname,'r')
  ret = yaml.load(infile, Loader=yaml.Loader)
  infile.close()
  return ret

def applyVarfile(BastilleFile, VarDict):
  for key in VarDict:
    BastilleFile = re.sub(r'ARG\s+{}\s*=.+'.format(key), 'ARG {} = {}'.format(key, VarDict[key]), BastilleFile, flags=re.IGNORECASE)

  return BastilleFile

