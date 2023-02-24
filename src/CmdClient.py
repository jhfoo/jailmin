import paramiko
import os
import pathlib
import random


# defaults if not in environment
FILE_RSA = os.environ['JAILMIN_KEY_PRIVATE'] if 'JAILMIN_KEY_PRIVATE' in os.environ else '/usr/home/jhfoo/.ssh/id_rsa'
PATH_ARTIFACTS = os.environ['JAILMIN_PATH_ARTIFACTS'] if 'JAILMIN_PATH_ARTIFACTS' in os.environ else '/usr/home/jhfoo/jailmin-artifacts/'
DEPLOY_HOST = os.environ['JAILMIN_DEPLOY_HOST'] if 'JAILMIN_DEPLOY_HOST' in os.environ else 'penn.node.consul'
DEPLOY_USER = os.environ['JAILMIN_DEPLOY_USER'] if 'JAILMIN_DEPLOY_USER' in os.environ else 'jhfoo'
DEPLOY_PORT = os.environ['JAILMIN_DEPLOY_PORT'] if 'JAILMIN_DEPLOY_PORT' in os.environ else 3003

def getSshClient():
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
      DEPLOY_HOST,
      username=DEPLOY_USER,
      pkey=paramiko.RSAKey.from_private_key_file(FILE_RSA),
    )
  
    return client

def autoCreateArtifactPath(sftp):
  # create dir if not avail
  try:
    sftp.listdir(path=PATH_ARTIFACTS)
  except:
    try:
      # too many sub-folders to create: give up
      sftp.mkdir(PATH_ARTIFACTS)
    except Exception as err:
      raise FileNotFoundError('Cannot create remote folder: ' + PATH_ARTIFACTS)

def createUniqueFolder(sftp):
  LETTERS = 'abcdefghijklmnopqrstuvwxyz0123456789'
  names = {}

  for item in sftp.listdir_attr(path=PATH_ARTIFACTS):
    names[item.filename] = True

  FolderName = ''
  while (True):
    # generate a name
    NAME_LENGTH = 8
    FolderName = ''

    for i in range(NAME_LENGTH):
      FolderName += LETTERS[random.randint(0, len(LETTERS)-1)]

    if not FolderName in names:
      break
    # line = 'DIR' if stat.S_ISDIR(item.st_mode) else 'FILE'
    # line += ' ' + item.filename
    # print (line)
  return PATH_ARTIFACTS + FolderName + '/'

def prepareRemoteFolder(sftp):
  autoCreateArtifactPath(sftp)
  FolderName = createUniqueFolder(sftp)
  print (FolderName)
  sftp.mkdir (FolderName)
  return FolderName

def execCmd(args):
  print ('CmdClient.execCmd()')

  SshClient = getSshClient()
  sftp = SshClient.open_sftp()
  FolderName = prepareRemoteFolder(sftp)
  print ('Remote folder: {}'.format(FolderName))

  for file in args.CmdArgs:
    print (file)
    if not pathlib.Path(file).is_file():
      raise FileNotFoundError('Missing artifact: {}'.format(file))

    # else
    JustFilename = os.path.basename(file)
    print ('Uploading: {} -> {}'.format(JustFilename, FolderName + JustFilename))
    sftp.put(file, FolderName + JustFilename)      

  # sftp.rmdir(FolderName)      
  SshClient.close()
