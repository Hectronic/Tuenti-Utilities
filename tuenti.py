#Created by hectronic
#V. 0.4 alpha
#I don't have decided the license yet. Temporally all rigths reserved

import ClientForm
import urllib2
import sys
import os

uri = "http://m.tuenti.com/"
profile = "?m=profile&func=my_profile"
messages = "?m=messaging"
friends = "?m=friends"
sitios = "?m=local"
photo = ""
url = ""
images = "http://imagenes2.tuenti.net"
imagesDir = "photos"
photonumber=0

def getData():
    name = raw_input("Type your email: ");
    password = raw_input("Type your password: ");
    return name, password
def getMsg():
    msg = raw_input("Status message: ")
    return msg
def doRequest(request):
    request.add_header('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Ubuntu/10.04 Chromium/6.0.472.53')
    page = urllib2.urlopen(request)
    return page
def getHTML(url):
    request = urllib2.Request(url)
    page = doRequest(request)
    html = page.read()
    page.close
    return html
def getPhotosPage(page):
    ini = page.find('collection_key=')
    fin = page.find('">Fotos en las que salgo<')
    photo = page[ini:fin]
    return photo
def login(datos):
    url = uri
    request = urllib2.Request(url)
    page = doRequest(request)
    forms = ClientForm.ParseResponse(page, backwards_compat=False)
    form = forms[0]
    form.find_control("remember").items[0].selected = False#Desactivamos el recordar, por lo que pueda pasar
    form["tuentiemail"] = datos[0]
    form["password"] = datos[1]
    request = form.click()
    page.close()
    page = doRequest(request)
    return page

#Maneja las cookies de forma mas o menos automatica
def handleCookies():
    cookie_h = urllib2.HTTPCookieProcessor()  
    opener = urllib2.build_opener(cookie_h)  
    urllib2.install_opener(opener) 
def getBigPhotoURL(photo):
    ini = photo.find('/i/')
    fin = photo.find('.jpg')
    photo = photo[ini - 4:fin + 4]
    ini = photo.find('/i')
    fin = photo.find('br.75.75')
    photo1 = photo[ini:fin]
    photo2 = photo[fin + 8:]
    photo = images + photo1 + "600" + photo2
    return photo
    
def getNextPage(html):
    ini = html.find('>Siguiente')
    fin = html.find('"><img src="http://thumbs')
    if (fin == -1):
        fin = html.find('"><img src="http://cd')
    photo = html[ini:fin]
    ini = photo.find('collection_key')
    photo = photo[ini:fin]
    return photo

def getPhoto(html):
    ini = html.find('http://thumbs')
    if (ini != -1): 
        fin = html.find('.jpg')
        image = html[ini:fin + 4]
        image = getBigPhotoURL(image)
    else:
        ini = html.find('http://cd')
        fin = html.find('.jpg')
        image = html[ini:fin + 4]
    return image

def createDir(name):
    if not os.path.isdir(name):
        os.mkdir(name)
    os.chdir(name)    

def save(entrada, formato, link):
    try:
        fp = open (entrada + formato, "wb+")
    except:
        print  "File couldn't be write"
        sys.exit(0)
        
    data = urllib2.urlopen(link)
    fp.write(data.read())
    fp.close()
        
def downloadPhoto(image):
    ini=image.rfind("/") + 1
    fin=len(image)-6
    name=image[ini:fin]
    save(name, ".jpg", image)
    
    
def getPhotos(max):
    url = uri + profile
    html = getHTML(url)
    photo = "?m=photos&func=view_tagged_photo&" + getPhotosPage(html)

    print "Downlading photos "
    while(max):
        try:
            max -= 1
            url = uri + photo
            html = getHTML(url)
            image = getPhoto(html)
            downloadPhoto(image)
            photo = "?m=photos&func=view_tagged_photo&" + getNextPage(html)
        except:
            print "error"
            max = 0
           
def changeStatus(msg):
    url = uri
    request = urllib2.Request(url)
    page = doRequest(request)
    forms = ClientForm.ParseResponse(page, backwards_compat=False)
    form = forms[0]
    form["status"] = msg
    request = form.click()
    page.close()
    doRequest(request)
def menu():  
    print "What dou you want to do:\n1)Download photos\n2)Change status\n0)Salir"  
    option = input("Type your option: ")      
    if (option == 1):
        originalDir=os.getcwd()
        createDir(imagesDir)
        getPhotos(input("type the number of photos do you want to download (-1 for all)"))
        os.chdir(originalDir)
        menu()
        
    elif (option == 2):
        changeStatus(getMsg())
        menu()

def main():
    handleCookies()
    if(len(sys.argv) == 1):
        datos = getData()
        login(datos)
        menu()
    else:
        datos = sys.argv[1], sys.argv[2]
        option = sys.argv[3]
        login(datos)
        if(option == "status"):
            msg = sys.argv[4]
            changeStatus(msg)
        elif(option == "photos"):
            createDir(imagesDir)
            max = int(sys.argv[4])
            getPhotos(max)
        

if __name__ == "__main__":
    main()

