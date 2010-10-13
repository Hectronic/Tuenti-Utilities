#Created by hectronic
#V. 0.4 alpha
#I don't have decided the license yet. Temporally all rigths reserved


import pygtk
import gtk


class changeStatusScreen():
    statusmsg = ""
    mainObject = object
    def getCredentials(self):
        return self.status
    
    def enter_callback(self, widget, entry):
        entry_text = entry.get_text()
        
        print "Entry contents: %s\n" % entry_text

    def entry_toggle_editable(self, checkbutton, entry):
        entry.set_editable(checkbutton.get_active())

    def entry_toggle_visibility(self, checkbutton, entry):
        entry.set_visibility(checkbutton.get_active())

    def read(self, button, status):
        self.statusmsg = status.get_text()
        print self.statusmsg
        self.mainObject.changeStatus(self.statusmsg)
        #print "Entry contents: %s %s\n" % (email , password)
        #loggin=Login(email,password)
        
    def __init__(self, mainObject):
        # create a new window
        self.mainObject = mainObject
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_size_request(200, 100)
        window.set_title("GTK Entry")
        window.connect("delete_event", lambda w, e: gtk.main_quit())

        vbox = gtk.VBox(False, 0)
        window.add(vbox)
        vbox.show()
        hbox = gtk.HBox(False, 0)
        vbox.add(hbox)
        hbox.show()   
        
        status = gtk.Entry()
        status.set_max_length(50)
        #email.connect("activate", self.enter_callback, email)
        status.set_text("Estado")
        #entry.insert_text(" world", len(entry.get_text()))
        status.select_region(0, len(status.get_text()))
        vbox.pack_start(status, True, True, 0)
        status.show()

                              
        button = gtk.Button("Aceptar")
        button.connect("clicked", self.read, status)
        vbox.pack_start(button, True, True, 0)
        button.set_flags(gtk.CAN_DEFAULT)
        button.grab_default()
        button.show()
        window.show()

    def main(self):
        gtk.main()
        return 0

#if __name__ == "__main__":
    #LoginScreen().main()
   # main()
