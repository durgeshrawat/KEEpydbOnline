from msilib.schema import Error
import pyrebase
import os
import urllib

class realtimedatabase:
    def __init__(self,authtoken):
        try:
            firebase = pyrebase.initialize_app(authtoken)
            self.auth= firebase.auth()
            self.storage=firebase.storage()
        except Exception as e:
            print(e)

    def login(self,email,password):
        try:
            info=self.auth.sign_in_with_email_and_password(email=email, password=password,)
            if info["registered"]==True:
                return True
        except Exception as getaddrinfo :
            raise Error(getaddrinfo)
    
    def adduser(self,email,password,name="KEEpydb-Client"):
        try:
            print(self.auth.create_user_with_email_and_password(email,password))
        except Exception as getaddrinfo :
            raise Error(getaddrinfo)

    #Storage
    def upload(self,filename,cloudfilename,returnurl=False):
        self.storage.child(cloudfilename).put(filename)
        if returnurl==True:
            return self.storage.child(cloudfilename).get_url(None)
    
    def geturl(self,cloudfilename):
        return self.storage.child(cloudfilename).get_url(None)


    def download(self,cloudfilename,path,filename):
        self.storage.child(cloudfilename).download(path,filename)

    def readfile(self,cloudfilename,decode=True):
        cloudfilename1=''
        for j in str(cloudfilename):
            if j == '.':
                cloudfilename1+='/'
            else:
                cloudfilename1+=j

        url=self.geturl(cloudfilename1)
        f=urllib.request.urlopen(url).read()
        if decode==True:
            return f.decode()
        else:
            return f

    def isobject(self,objectname):
        try:
            url=self.geturl(objectname)
            f=urllib.request.urlopen(url).read()
            return True
        except:
            return False
    def createobject(self,objectname):
        objectname=str(objectname+"/ObjectHandle")
        with open("objectHandle","w") as f:
            f.write("This is an <KEEpydbObject>")
        self.upload("objectHandle",objectname)
        os.system("del objectHandle")
        return True

    def pushdata(self,varname,data): #fileobjectclassname[object class name],variablename[filename],data
        varname1=''
        for j in varname:
            if j == '.':
                varname1+='/'
            else:
                varname1+=j
        with open("objectfile","w") as f:
            f.write(str(data))
        self.upload('objectfile',varname1,data)     #filename,cloudfilename
        os.system("del objectfile")
        return True
        
    def objectcall(self,objectname):
        return self.readfile(objectname)

