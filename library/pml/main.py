from pmlauncher import pml, mlogin, mlaunchoption
import subprocess
import os
import sys
import platform
from PyQt5.QtWidgets import QMessageBox, QInputDialog,QWidget, QLineEdit
import keyring


class LoginDialog(QWidget):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)
        #self.setSize

    def login(self):
        login, ok = QInputDialog.getText(self, "Minecraft Login", "Username:")
        if ok and login:
            password, ok =  QInputDialog.getText(self, "Minecraft Login", "Password:", QLineEdit.Password)
            if ok and password:
                return login,password
                

def runminecraft(forge_version):
    MAGIC_USERNAME_KEY = 'ADELLPHI_USERNAME'
    APP_ID = 'ADELLPHI'  

    if platform.system() == 'Windows':
      appData = os.getenv('APPDATA')
      p = appData + "\\.minecraft\\"
    elif platform.system() == "Darwin":
      appData = str(Path.home())
      p = appData + "/Library/Application Support/minecraft/"
    elif platform.system() == "Linux":
      appData = str(Path.home())
      p = appData + "/.minecraft/"
    
    #check if login is saved, otherwise prompt using dialog
    login = ""
    password = ""
    login = keyring.get_password(APP_ID, MAGIC_USERNAME_KEY)
    if (login):
        password = keyring.get_password(APP_ID, login)  

    if not (login or password):
        login,password = LoginDialog().login()
        keyring.set_password(APP_ID, MAGIC_USERNAME_KEY, login)
        keyring.set_password(APP_ID, login, password)


    

    # initialize
    #p = os.environ["appdata"] + "\\.minecraft"  # windows default game directory
    #p = os.getcwd() + "/game"
    #p = os.path.abspath("/home/myu/.minecraft")
    if (not password):
        QMessageBox.information(None, "Adellphi", "You must login")
        return
        

    pml.initialize(p)
    print("Initialized in " + pml.getGamePath())
    from .pycraft import authentication
    auth = authentication.AuthenticationToken()
    auth.authenticate(login, password)

    session = mlogin.session()  # set session object
    session.username = auth.profile.name
    session.uuid = auth.profile.id_
    session.access_token = auth.access_token


    inputVersion = forge_version
    # get profiles
    #profiles = pml.updateProfiles()
    #for item in profiles:
        #print(item.name)

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

