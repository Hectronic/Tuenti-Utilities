#Created by hectronic
#V. 0.4 alpha
#I don't have decided the license yet. Temporally all rigths reserved

import ClientForm
import urllib2
import sys
import os

    
class API():
    uri = "http://m.tuenti.com/"
    profile = "?m=profile&func=my_profile"
    messages = "?m=messaging"
    friends = "?m=friends"
    sitios = "?m=local"
    photo = ""
    url = ""
    images = "http://imagenes2.tuenti.net"
    imagesDir = "photos"
    photonumber = 0
    

    def getData(self):
        name = raw_input("Type your email: ");
        password = raw_input("Type your password: ");
        return name, password
    
    def getMsg(self):
        msg = raw_input("Status message: ")
        return msg
    
    def doRequest(self, request):
        request.add_header('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Ubuntu/10.04 Chromium/6.0.472.53')
        page = urllib2.urlopen(request)
        return page
    
    def getHTML(self, url):
        request = urllib2.Request(url)
        page = self.doRequest(request)
        html = page.read()
        page.close
        return html
    
    def getPhotosPage(self, page):
        ini = page.find('collection_key=')
        fin = page.find('">Fotos en las que salgo<')
        photo = page[ini:fin]
        return photo
    
    def login(self, email, password):
        url = self.uri
        request = urllib2.Request(url)
        page = self.doRequest(request)
        forms = ClientForm.ParseResponse(page, backwards_compat=False)
        form = forms[0]
        form.find_control("remember").items[0].selected = False#Desactivamos el recordar, por lo que pueda pasar
        form["tuentiemail"] = email
        form["password"] = password
        request = form.click()
        page.close()
        page = self.doRequest(request)
        url = self.uri + self.profile
        html = self.getHTML(url)
        self.photo = "?m=photos&func=view_tagged_photo&" + self.getPhotosPage(html)
        return page
    
    #Maneja las cookies de forma mas o menos automatica
    def handleCookies(self):
        cookie_h = urllib2.HTTPCookieProcessor()  
        opener = urllib2.build_opener(cookie_h)  
        urllib2.install_opener(opener)
         
    def getBigPhotoURL(self, photo):
        ini = photo.find('/i/')
        fin = photo.find('.jpg')
        photo = photo[ini - 4:fin + 4]
        ini = photo.find('/i')
        fin = photo.find('br.75.75')
        photo1 = photo[ini:fin]
        photo2 = photo[fin + 8:]
        photo = self.images + photo1 + "600" + photo2
        return photo
        
    def getNextPage(self, html):
        ini = html.find('>Siguiente')
        fin = html.find('"><img src="http://thumbs')
        if (fin == -1):
            fin = html.find('"><img src="http://cd')
        photo = html[ini:fin]
        ini = photo.find('collection_key')
        photo = photo[ini:fin]
        return photo
    
    def getPhoto(self, html):
        ini = html.find('http://thumbs')
        if (ini != -1): 
            fin = html.find('.jpg')
            image = html[ini:fin + 4]
            image = self.getBigPhotoURL(image)
        else:
            ini = html.find('http://cd')
            fin = html.find('.jpg')
            image = html[ini:fin + 4]
        return image
    
    def createDir(self, name):
        if not os.path.isdir(name):
            os.mkdir(name)
        os.chdir(name)    
    
    def save(self, entrada, formato, link):
        try:
            fp = open (entrada + formato, "wb+")
        except:
            print  "File couldn't be write"
            sys.exit(0)
            
        data = urllib2.urlopen(link)
        fp.write(data.read())
        fp.close()
            
    def downloadPhoto(self, image):
        ini = image.rfind("/") + 1
        fin = len(image) - 6
        name = image[ini:fin]
        self.save(name, ".jpg", image)
               
    def changeStatus(self, msg):
        url = self.uri
        request = urllib2.Request(url)
        page = self.doRequest(request)
        forms = ClientForm.ParseResponse(page, backwards_compat=False)
        form = forms[0]
        form["status"] = msg
        request = form.click()
        page.close()
        self.doRequest(request)
   
    def getNextPhoto(self):
        try:
            print "1"
            url = self.uri + self.photo
            print "2"
            html = self.getHTML(url)
            print "3"
            image = self.getPhoto(html)
            print "4"
            image = self.getBigPhotoURL(image)
            print "5"
            #self.downloadPhoto(image)
            self.photo = "?m=photos&func=view_tagged_photo&" + self.getNextPage(html)
            return image
        except:
            print "error"
            max = 0

    def __init__(self):
        print "1"
   
    

