#Created by hectronic
#V. 0.4 alpha
#I don't have decided the license yet. Temporally all rigths reserved

import pygtk
import gtk


class LoginScreen():
    email = ""
    password = ""
    window=object
    def getCredentials(self):
        return self.email, self.password
    
    def enter_callback(self, widget, entry):
        entry_text = entry.get_text()
        
        print "Entry contents: %s\n" % entry_text

    def entry_toggle_editable(self, checkbutton, entry):
        entry.set_editable(checkbutton.get_active())

    def entry_toggle_visibility(self, checkbutton, entry):
        entry.set_visibility(checkbutton.get_active())

    def read(self, button, entry, entry2):
        self.email = entry.get_text()
        self.password = entry2.get_text()
        gtk.main_quit()
        #print "Entry contents: %s %s\n" % (email , password)
        #loggin=Login(email,password)
    def __del__(self):
        self.window.destroy()
    def __init__(self):
        # create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_size_request(200, 100)
        self.window.set_title("GTK Entry")
        self.window.connect("delete_event", lambda w, e: gtk.main_quit())

        vbox = gtk.VBox(False, 0)
        self.window.add(vbox)
        vbox.show()
        hbox = gtk.HBox(False, 0)
        vbox.add(hbox)
        hbox.show()   
        
        email = gtk.Entry()
        email.set_max_length(50)
        #email.connect("activate", self.enter_callback, email)
        email.set_text("")
        #entry.insert_text(" world", len(entry.get_text()))
        email.select_region(0, len(email.get_text()))
        vbox.pack_start(email, True, True, 0)
        email.show()

        password = gtk.Entry()
        password.set_max_length(50)
        password.connect("activate", self.enter_callback, password)
        password.set_text("")
        password.select_region(0, len(password.get_text()))
        vbox.pack_start(password, True, True, 0)
        password.show()
        password.set_visibility(False)
                              
        button = gtk.Button("Aceptar")
        button.connect("clicked", self.read, email, password)
        vbox.pack_start(button, True, True, 0)
        button.set_flags(gtk.CAN_DEFAULT)
        button.grab_default()
        button.show()
        self.window.show()

    def main(self):
        gtk.main()
        return 0

if __name__ == "__main__":
    LoginScreen().main()
   # main()
