
#***************************************************************************************#
#*----- Auteur :        Aubertin Emmanuel                                           ****#
#*----- Description :   script pour creer un docker apche simplement                ****#
#*----- GitHub :        https://github.com/Athomisos | Twitter : @BlenderAubertin   ****#
#***************************************************************************************#


import os, argparse, random, string, docker, socket
from sys import argv

#-------------------------------------------------#|  Function  |#-------------------------------------------------#
def createName():
    letters = string.ascii_lowercase
    outputName = ''.join(random.choice(letters) for i in range(8))
    return(outputName)

def checkDocker(client, nameOfImage):
    print("Cheking " + nameOfImage + " image ....")
    client.images.pull(nameOfImage)
    print("Image is ok :)")

def getDocker(client, docker_name):
    return(client.containers.get(docker_name))

def killdocker(container):
    print("Extinction of the docker in progress ...")
    container.stop()
    print("The docker is kill.")

def restartdocker(container):
    print("Extinction of the docker in progress ...")
    container.restart()
    print("The docker is up now.")

def startDocker(container):
    print("Your container is starting")
    container.start()
    print("Container is up now.")

def reloaddocker(container):
    print("Reloading of the docker in progress ...")
    container.relaod()
    print("Reload Finish :)")

def rmdocker(container):
    killdocker(container)
    print("The docker is deleted")

def buildport(inputPort):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if(s.connect_ex(('localhost', int(inputPort))) == 0):
            print("The port " + inputPort + "is curently not avaible")
            new_port = input("Do you want to asign a new port ?")
            if(new_port == 'y' or new_port == 'yes'):
                return(buildport(new_port))
        else:
            return({"80/tcp" : str(inputPort)})

def runDocker(client, Inimage_name, Insrc_path, Indocker_name, Ininput_port):
    return(client.containers.run(Inimage_name, name=Indocker_name, volumes={ Insrc_path : {'bind': '/var/www/html/', 'mode' : 'rw'} }, ports=Ininput_port))

def initstart(client, docker_name):
    try:
        container = getDocker(client, docker_name)
        startDocker(container)
        return(container)
    except docker.errors.NotFound as e:
        print("Docker name not valide, plz retry")
        print(os.popen('sudo docker container ls -a').read())
        retry_name = input("plz enter a valid name : ")
        return(initstart(client, retry_name))

def waiting_actions(client, container):
    action = input("Wath do you want do ? \nS (Start) | R (Restart) | K (Kill) | RM (Delete) | RL (reload) | Q (Quit)")
    if(action == 'R' or action == 'r'):
        restartdocker(container)
    elif(action == 'Q' or action == 'q'):
        print("Goodbye\n")
        exit()
    elif(action == 'K' or action == 'k'):
        killdocker(container)
    elif(action == 'RM' or action == 'rm'):
        rmdocker(container)
    elif(action == 'RL' or action == 'rl'):
        reloaddocker(container)
    elif(action == 'S' or action == 's'):
        docker_name = input("Enter the name of the docker : ")
        initstart(client, docker_name)
    else:
        print("Action not avaible plz retry")
    waiting_actions(client, container)

#-------------------------------------------------#|  ArgParse  |#-------------------------------------------------#
#-------------------------------------------------#
# Create the parser                 --------------#
parser = argparse.ArgumentParser(description='Easy way to deploy apache')

#-------------------------------------------------#
# Add new arguments                 --------------#
#-- Spotify username
parser.add_argument('-P','--path', default=os.getcwd(), type=str, help='Enter src path (here by default)')
parser.add_argument('-p','--port', default="80", type=str, help='Enter a custom port, for you computer (WARNING POSSIBLE CONFLICT)')
parser.add_argument('-n','--name', default=createName(), type=str, help='Enter the name of the container (random name by default)')
parser.add_argument('-s','--start', help='Set to true for start a specifique container', action="store_true")

#-------------------------------------------------#
# Execute the parser                --------------#
args = parser.parse_args()

#-------------------------------------------------#
# Create Docker client              --------------#
client = docker.from_env()

#-------------------------------------------------#|  main()  |#-------------------------------------------------#

#-------------------------------------------------#
# const                             --------------#
src_path = args.path
docker_name = args.name
port = args.port
image_name = "php:7.2-apache"
if(args.start):
    container = initstart(client, docker_name)
else:
    print("Path of src ==> " + src_path)
    checkDocker(client, image_name)
    print("The name of the docker is : ", docker_name)
    protout = buildport(port)
    container = runDocker(client, image_name, src_path, docker_name, buildport(port))

waiting_actions(client, container)