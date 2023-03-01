import os
import subprocess
import shutil
import yaml

def execStockTemplateCmd(params):
  BaseParams = ['bastille','template']

  result = subprocess.run(BaseParams + params, capture_output=True, text=True)
  print (result.stdout)
  print (result.stderr)

def execCmd(args):

  print (args)
  if args.vars == None:
    # execute stock Bastille commands
    # BaseParams.append(args.JailId)
    # BaseParams.append(args.TemplatePath)
    execStockTemplateCmd([args.JailId, args.TemplatePath])
  else:
    # copy template folder to temp/
    PATH_TEMPLATES = '/usr/local/bastille/templates/'
    PATH_TEMP = PATH_TEMPLATES + 'kungfoo/temp'

    # prepare temp dir
    shutil.rmtree(PATH_TEMP, ignore_errors=True)
    os.mkdir(PATH_TEMP)

    CopySource = PATH_TEMPLATES + args.TemplatePath
    print (f'CP: {CopySource} -> {PATH_TEMP}')

    result = subprocess.run(['cp', '-R', CopySource + '/', PATH_TEMP], 
      capture_output=True, text=True)
    print (result.stdout)
    print (result.stderr)

    # apply variables to Bastillefile
    # slurp in original file
    hInfile = open(PATH_TEMP + '/Bastillefile','r')
    BastilleFile = hInfile.read()
    hInfile.close()

    # load variable file
    hVarFile = open(args.vars[0],'r')
    vars = yaml.safe_load(hVarFile)
    hVarFile.close()

    # global variable replace
    for key in vars.keys():
      BastilleFile = BastilleFile.replace(f'${key}', vars[key])
      print (f'key: {key} -> {vars[key]}')
    print (BastilleFile)

    # update Bastillefile in temp folder
    hOutFile = open(PATH_TEMP + '/Bastillefile','w')
    hOutFile.write(BastilleFile)
    hOutFile.close()

    execStockTemplateCmd([args.JailId, 'kungfoo/temp'])

    # housekeeping
    # shutil.rmtree(PATH_TEMP)
