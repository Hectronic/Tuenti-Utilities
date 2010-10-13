#Created by hectronic
#V. 0.4 alpha
#I don't have decided the license yet. Temporally all rigths reserved

import LoginScreen
import TuentiAPI
import Status
class Main():
    '''
    classdocs
    '''
    api = TuentiAPI.API()
    def logScreen(self):
        log = LoginScreen.LoginScreen()
        log.main()
        email, password = log.getCredentials()
        log.__del__()
        self.api = TuentiAPI.API()
        self.api.handleCookies()
        self.api.login(email, password)
        sts = Status.changeStatusScreen(self)
        sts.main()
        status = sts.getCredentials()
        
        print "Email %s .Password %s" % (email, password)
        image = self.api.getNextPhoto();
        print image
        image = self.api.getNextPhoto();
        print image
    
    def changeStatus(self, msg):
        self.api.changeStatus(msg)
        
    def __init__(self):
        '''
        Constructor
        '''
       #Log=LoginScreen()
       #Log.main()
        
if __name__ == "__main__":
    main = Main()
    main.logScreen()
