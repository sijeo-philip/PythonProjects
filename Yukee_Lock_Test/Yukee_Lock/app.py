
from commport import *
import datetime

def refresh_text_widget():
    ##print("{} am hit".format(refresh_text_widget.__name__))
    if application.microcomm.isOpen() and application.microcomm.in_waiting:
        application.mcu_textbox.config(fg='red', font=('Verdana',8,'bold'))
        data = application.microcomm.read(application.microcomm.inWaiting())
        application.mcu_textbox.insert(END, data)
        application.mcu_textbox.see(END)
        application.microcomm.flushInput()
    if application.simcomm.isOpen() and application.simcomm.in_waiting:
        data = application.simcomm.read(application.simcomm.inWaiting())
        application.sim_textbox.config(fg='blue', font=('Times',8,'bold'))
        application.sim_textbox.insert(END, data)
        application.sim_textbox.see(END)
        application.simcomm.flushInput()
    root.after(250, refresh_text_widget)



if __name__ == '__main__':
    root = Tk()
    application = DataLogger(root)
    root.after(250,refresh_text_widget)

    root.mainloop()




