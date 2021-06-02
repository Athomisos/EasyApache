#*---------------------------------------------------------------------------------------*#
#*----- Auteur :        Aubertin Emmanuel                                           -----*#
#*----- GitHub :        github.com/Athomisos | Twitter : @BlenderAubertin           -----*#
#*----- Description :   All utils class and function                                -----*#
#*---------------------------------------------------------------------------------------*#

import os, string, random, socket

__author__ = "Aubertin Emmanuel"
__copyright__ = "2021"
__credits__ = ["Aubertin Emmanuel"]
__license__ = "GPL"
__version__ = "1.0.0"

CLIENT_OS = os.uname().sysname



class printColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def Err(s):
    print(printColors.FAIL + printColors.BOLD + "ERROR : " + printColors.ENDC + s)
    exit()

def Warn(s):
    print(printColors.WARNING + printColors.BOLD + "WARNING : " + printColors.ENDC + s)

def is_root():
    if(CLIENT_OS == 'Linux'):
        return os.geteuid() == 0
    else:
        return None # Uncode for the moment

def checkRoot():
    if(not is_root()):
        Err("You must be root !")

def randomStr(length):
    letters = string.ascii_lowercase
    s = ''.join(random.choice(letters) for i in range(length))
    return s

def printLine():
    for i in range(0, os.get_terminal_size().columns):
        print("-", end="")

def checkPort(inputPort):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if(s.connect_ex(('127.0.0.1', int(inputPort))) == 0):
            Warn("The port " + inputPort + " is curently not avaible, please try again")
            anwser = input("Do you want to asign a new port ? [Y/N] ")
            if(anwser == 'y' or anwser == 'yes' or anwser == 'Y'):
                port = input("Enter the new port ?")
                return(checkPort(port))
            elif(anwser == 'N' or anwser == 'no' or anwser == 'n'):
                Err("You must enter a avaible port !\nGoodbye :)")
            else:
               return(checkPort(inputPort))
        else:
            print("Port is" + printColors.OKGREEN + printColors.BOLD + " avaible" + printColors.ENDC)
            return {"80/tcp" : str(inputPort)}

def lsdocker():
    print(printColors.BOLD + "List of all container :" + printColors.ENDC)
    os.system("sudo docker container ls -a")
    print("------------------")