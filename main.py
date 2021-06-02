#*---------------------------------------------------------------------------------------*#
#*----- Auteur :        Aubertin Emmanuel                                           -----*#
#*----- GitHub :        github.com/Athomisos | Twitter : @BlenderAubertin           -----*#
#*----- Description :   Easy apache php and PSQL deploy                             -----*#
#*---------------------------------------------------------------------------------------*#

import os, argparse, random, string, docker, socket, utils
from sys import argv

__author__ = "Aubertin Emmanuel"
__copyright__ = "2021"
__credits__ = ["Aubertin Emmanuel"]
__license__ = "GPL"
__version__ = "1.0.0"



def askAction():
    action = input("""What do you want to do?
        - c (create a new docker)
        - s (start a specific docker)\nInput : """)
    if(action == "c"):
        createDocker()
    elif(action == "s"):
        utils.printLine()
        print("Start specific Docker :")
    else:
        utils.printLine()
        utils.Warn("You must answer c or s, please try again : ")
        return askAction()

def createDocker():
    utils.printLine()
    print("Create new Docker :)")
    inputPort = utils.checkPort(input("Enter the port you wish to use : "))
    containerName = newName()
    print("Name : " + containerName)
    image = checkdb() # without or with DB
    runDocker(image, containerName, inputPort)

def checkdb():
    inputVar = input("Do you want a database in your container? [y/n] ")
    if(inputVar == "yes" or inputVar == "Y" or inputVar == "y"):
        print("Create docker with DB")
        return PSQL_IMAGE
    elif(inputVar == "no" or inputVar == "n" or inputVar == "N"):
        print("Just appache and php7")
        return PHP_IMAGE
    else:
        utils.Warn("You must answer yes or no, please try again.")
        return checkdb()
    

def newName():
    utils.lsdocker()
    docker_name = input("""Enter the name of your container (Q -> quit
                                  R -> Random name): """)
    if(docker_name == "Q" or docker_name == "q"):
        print("Goodbye :)")
        exit()
    elif(docker_name == "R" or docker_name == "r"):
        docker_name = utils.randomStr(8)
    return docker_name

def runDocker(image_name, docker_name, input_port):
    return(DOCKER_CLIENT.containers.run(image_name, name=docker_name, volumes={ SRC_PATH : {'bind': '/var/www/html/', 'mode' : 'rw'} }, ports=input_port))

#--  MAIN --#
utils.checkRoot()

#----|  ArgParse  |----#
parser = argparse.ArgumentParser(description="""
    Easy way to deploy apache, php and PSQL.
    """,
    usage="""
        sudo python3 main.py
    """,
    epilog="version {}, license {}, copyright {}, credits {}".format(__version__,__license__,__copyright__,__credits__))
parser.add_argument('-f','--folder', default=os.getcwd(), type=str, help='Specific src path (./ by default')
#parser.add_argument('-p','--port', default="80", type=str, help='Enter a custom port ')
#parser.add_argument('-n','--name', default=utils.randomStr(8), type=str, help='Enter the name of the container (random name by default)')
#parser.add_argument('-s','--specific', help='If you want set up a specific contianer', action="store_true")
#parser.add_argument('-c','--create', help='Set to true for create a new container', action="store_true")

args = parser.parse_args()

SRC_PATH = args.folder
DOCKER_CLIENT = docker.from_env()
PHP_IMAGE = "php:7.2-apache"
PSQL_IMAGE = "psql"

askAction()

    