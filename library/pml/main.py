from pmlauncher import pml, mlogin, mlaunchoption
import subprocess
import os
import sys
import platform


def runminecraft(forge_version):
    if platform.system() == 'Windows':
      appData = os.getenv('APPDATA')
      p = appData + "\\.minecraft\\"
    elif platform.system() == "Darwin":
      appData = str(Path.home())
      p = appData + "/Library/Application Support/minecraft/"
    elif platform.system() == "Linux":
      appData = str(Path.home())
      p = appData + "/.minecraft/"
    
    # initialize
    #p = os.environ["appdata"] + "\\.minecraft"  # windows default game directory
    #p = os.getcwd() + "/game"
    #p = os.path.abspath("/home/myu/.minecraft")
    pml.initialize(p)
    print("Initialized in " + pml.getGamePath())
    from .pycraft import authentication
    auth = authentication.AuthenticationToken()
    auth.authenticate("", "")

    session = mlogin.session()  # set session object
    session.username = auth.profile.name
    session.uuid = auth.profile.id_
    session.access_token = auth.access_token


    inputVersion = forge_version
    # get profiles
    profiles = pml.updateProfiles()
    for item in profiles:
        print(item.name)

    #inputVersion = input("input version : ")    

    # download event handler
    # filekind : library , minecraft, index, resource
    def downloadEvent(x):
        pass
        #print(x.filekind + " - " + x.filename + " - " + str(x.currentvalue) + "/" + str(x.maxvalue))


    pml.downloadEventHandler = downloadEvent

    # download profile and create argument
    args = pml.startProfile(inputVersion, 
                            xmx_mb=1024,
                            session=session,

                            launcher_name="pml",  # option
                            server_ip="",
                            jvm_args="",
                            screen_width=0,
                            screen_height=0)


    # start process
    with open("args.txt", "w") as f:  # for debug
        f.write(args)
    print(args)

    mc = subprocess.Popen("java " + args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=pml.getGamePath(), shell=True)

    print("launched!")


    # write output
    with mc.stdout as gameLog:
        while True:
            try:
                line = gameLog.readline()
                if not line:
                    break
                print(line.decode(sys.getdefaultencoding()))
            except:
                pass

    if mc.returncode:
        print(f"Client returned {mc.returncode}!")

