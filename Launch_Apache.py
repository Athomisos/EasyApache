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

def lsdocker():
    print("------------------")
    os.system("sudo docker container ls -a")
    print("------------------")

def getDocker(client, docker_name):
    try:
        return(client.containers.get(docker_name))
    except docker.errors.NotFound as e:
        print("Docker name not valide, plz retry")
        return(inputDocker(client))


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

def rmdocker(container, docker_name):
    killdocker(container)
    os.system("sudo docker rm " + docker_name)
    print("The docker is deleted")

def buildport(client, inputPort):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if(s.connect_ex(('localhost', int(inputPort))) == 0):
            print("The port " + inputPort + "is curently not avaible")
            new_port = input("Do you want to asign a new port ?")
            if(new_port == 'y' or new_port == 'yes'):
                futur_port = input("Enter the new port ?")
                return(buildport(client, futur_port))
            elif(new_port == 'n' or new_port == 'no'):
                print("Plz choose one docker and type his name :")
                lsdocker()
                docker_name = input("Enter the docker name :")
                container = getDocker(client, docker_name)
                waiting_actions(client, container)
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
        rmdocker(container, container.name)
        container = inputDocker(client)
        waiting_actions(client, container)
    elif(action == 'RL' or action == 'rl'):
        reloaddocker(container)
    elif(action == 'S' or action == 's'):
        startDocker(container)
    else:
        print("Action not avaible plz retry")
    waiting_actions(client, container)


def inputDocker(client):
    lsdocker()
    docker_name = input("Enter the container name (Q for quit):")
    if(docker_name == "Q" or docker_name == "q"):
        exit()
    else:
        return(getDocker(client, docker_name))
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
parser.add_argument('-s','--specific', help='If you want set up a specific contianer', action="store_true")
parser.add_argument('-c','--create', help='Set to true for create a new container', action="store_true")

#-------------------------------------------------#
# Execute the parser                --------------#
args = parser.parse_args()

#-------------------------------------------------#
# Create Docker client              --------------#
client = docker.from_env()

#-------------------------------------------------#|  main()  |#-------------------------------------------------#

#-------------------------------------------------#
src_path = args.path
port = args.port
image_name = "php:7.2-apache"
if(args.specific):
    waiting_actions(client, inputDocker(client))
elif(args.create):
    docker_name = args.name
    print("Path of src ==> " + src_path)
    checkDocker(client, image_name)
    print("The name of the docker is : ", docker_name)
    protout = buildport(client, port)
    container = runDocker(client, image_name, src_path, docker_name, buildport(client, port))
    waiting_actions(client, container)
else:
    print("You must enter one argument !")

