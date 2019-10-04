import serial as comm
import glob
import sys
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class DataLogger():
    def __init__(self, window):
        self.window = window
        self.window.title("Yukee Test")
        self.window.geometry("1024x750")
        self.__baud_rate = IntVar()
        self.__data_bits = IntVar()
        self.__parity_bits = StringVar()
        self.__stop_bits = DoubleVar()
        self.__flow_control_xonxoff = IntVar()
        self.__flow_control_rtscts = IntVar()
        self.__flow_control_dsrdtr = IntVar()
        self.__top_frame = ttk.Frame(self.window).pack()
        self.__bottom_frame = ttk.Frame(self.window).pack(side=BOTTOM)
        self.microcomm = comm.Serial()
        self.simcomm = comm.Serial()

        self.__connect_button = ttk.Button(self.__top_frame, text="Connect", command = self.connect_callback)
        self.__connect_button.place(x=9,y=10)
        self.__disconnect_button= ttk.Button(self.__top_frame, text="Disconnect", command = self.disconnect_callback, state= DISABLED)
        self.__disconnect_button.place(x=9, y=40)
        self.__clear_button = ttk.Button(self.__top_frame, text="Clear Text", command=self.clear_textbox_callback)
        self.__clear_button.place(x=9, y=70)
        MCU_COM = ttk.Label(self.__top_frame, text="MCU COM").place(x=100, y=32)
        self.__micro_port=StringVar()
        self.__simcom_port=StringVar()
        self.comm_ports=[]
        self.__cbox1 = ttk.Combobox(self.__top_frame, text="MCU COM", textvariable=self.__micro_port, height=10, width=10,
                             state='readonly', postcommand=self.check_ports_mcu, values=(self.comm_ports))
        self.__cbox1.place(x=100, y=10)
        self.__cbox2 = ttk.Combobox(self.__top_frame, text="SIM COM", textvariable=self.__simcom_port, height=10, width=10,
                             state='readonly', postcommand=self.check_ports_simcom, values=self.comm_ports)
        self.__cbox2.place(x=100, y=60)
        SIM_COM = ttk.Label(self.__top_frame, text="SIM COM").place(x=100, y=85)
        self.__baud_frame = ttk.LabelFrame(self.__top_frame, text="Baud rate", relief=FLAT, height=150, width=125)
        self.__baud_frame.place(x=200,y=5)
        self.__data_bits_frame = ttk.LabelFrame(self.__top_frame, text="Data Bits", relief=FLAT, height=150, width=100)
        self.__data_bits_frame.place(x=280, y=5)
        self.__parity_frame = ttk.LabelFrame(self.__top_frame, text="Parity", relief=FLAT, height=150, width=100)
        self.__parity_frame.place(x=350, y=5)
        self.__stop_bits_frame = ttk.LabelFrame(self.__top_frame, text="Stop Bits", relief=FLAT, height=150, width=100)
        self.__stop_bits_frame.place(x=415, y=5)
        self.__flow_control_frame = ttk.LabelFrame(self.__top_frame, text="Flow Control", relief=FLAT, height=150, width=100)
        self.__flow_control_frame.place(x=495,y=5)

        ttk.Radiobutton(self.__baud_frame, text="4800", var=self.__baud_rate, value=4800).pack(anchor=W)
        ttk.Radiobutton(self.__baud_frame, text="9600", var=self.__baud_rate, value=9600).pack(anchor=W)
        ttk.Radiobutton(self.__baud_frame, text="19200", var=self.__baud_rate, value=19200).pack(anchor=W)
        ttk.Radiobutton(self.__baud_frame, text="38400", var=self.__baud_rate, value=38400).pack(anchor=W)
        ttk.Radiobutton(self.__baud_frame, text="115200", var=self.__baud_rate, value=115200).pack(anchor=W)
        ttk.Radiobutton(self.__data_bits_frame, text="5", var=self.__data_bits, value=comm.FIVEBITS).pack(anchor=W)
        ttk.Radiobutton(self.__data_bits_frame, text="6", var=self.__data_bits, value=comm.SIXBITS).pack(anchor=W)
        ttk.Radiobutton(self.__data_bits_frame, text="7", var=self.__data_bits, value=comm.SEVENBITS).pack(anchor=W)
        ttk.Radiobutton(self.__data_bits_frame, text="8", var=self.__data_bits, value=comm.EIGHTBITS).pack(anchor=W)
        ttk.Radiobutton(self.__parity_frame, text="None", var=self.__parity_bits, value=comm.PARITY_NONE).pack(anchor=W)
        ttk.Radiobutton(self.__parity_frame, text="Even", var=self.__parity_bits, value=comm.PARITY_EVEN).pack(anchor=W)
        ttk.Radiobutton(self.__parity_frame, text="Odd", var=self.__parity_bits, value=comm.PARITY_ODD).pack(anchor=W)
        ttk.Radiobutton(self.__parity_frame, text="Mark", var=self.__parity_bits, value=comm.PARITY_MARK).pack(anchor=W)
        ttk.Radiobutton(self.__parity_frame, text="Space", var=self.__parity_bits, value=comm.PARITY_SPACE).pack(anchor=W)
        ttk.Radiobutton(self.__stop_bits_frame, text="1", var=self.__stop_bits, value=comm.STOPBITS_ONE).pack(anchor=W)
        ttk.Radiobutton(self.__stop_bits_frame, text="1.5", var=self.__stop_bits, value=comm.STOPBITS_ONE_POINT_FIVE).pack(anchor=W)
        ttk.Radiobutton(self.__stop_bits_frame, text="2", var=self.__stop_bits, value=comm.STOPBITS_TWO).pack(anchor=W)
        ttk.Checkbutton(self.__flow_control_frame, text="XON/XOFF", var=self.__flow_control_xonxoff).pack(anchor=W)
        ttk.Checkbutton(self.__flow_control_frame, text="RTS/CTS", var=self.__flow_control_rtscts).pack(anchor=W)
        ttk.Checkbutton(self.__flow_control_frame, text="DSR/DTR", var=self.__flow_control_dsrdtr).pack(anchor=W)
        self.__mcu_response_frame = ttk.LabelFrame(self.__bottom_frame, text="MCU RESPONSE", width=150, height=25)
        self.__mcu_response_frame.place(x=10, y=150)
        self.__sim_response_frame = ttk.LabelFrame(self.__bottom_frame, text="SIM RESPONSE", width=150, height=25)
        self.__sim_response_frame.place(x =450, y=150)
        self.mcu_textbox = Text(self.__mcu_response_frame, width=50, height=25, state='normal',wrap='word')
        self.mcu_textbox.pack(padx=(3,20), pady=(20,3))
        self.sim_textbox= Text(self.__sim_response_frame, width=50, height=25, state='normal', wrap='word')
        self.sim_textbox.pack(padx=(3,20), pady=(20,3))

        scrollbar = ttk.Scrollbar(self.__bottom_frame, orient=VERTICAL, command=self.move_text_box)
        scrollbar.pack(side=RIGHT,fill=Y)

        self.mcu_textbox.config(yscrollcommand=scrollbar.set)
        self.sim_textbox.config(yscrollcommand=scrollbar.set)

    def __serial_port(self):
        """
        Lists Serial port Names
        : raises EnvironmentError
         on unsupported or Unkonwn Platforms
            :return:
        A list of Serial ports available on the System
            """
        if sys.platform.startswith('win'):
            self.ports = ['COM%s' % (i + 0) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            self.ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            self.ports = glob.glob('dev/tty/.*')
        else:
            raise EnvironmentError("Unsupported Platform!")

        result = []
        for port in self.ports:
            try:
                s = comm.Serial(port)
                s.close()
                result.append(port)
            except comm.SerialException:
                pass
        return (result)

    def connect_callback(self):
        mcuport =self.__micro_port.get()
        simport =self.__simcom_port.get()
        print(mcuport)
        print(simport)
        try:
            if (mcuport == simport)or((mcuport==None)and(simport==None)):
                print("The value of com ports are the same i.e. {} and {}".format(mcuport, simport))
                raise comm.SerialException
            if mcuport:
                self.microcomm = comm.Serial(mcuport,baudrate=self.__baud_rate.get(), bytesize=self.__data_bits.get(),
                                         parity=self.__parity_bits.get(), stopbits=self.__stop_bits.get(), xonxoff=self.__flow_control_xonxoff.get(),
                                         rtscts=self.__flow_control_rtscts.get(),dsrdtr=self.__flow_control_dsrdtr.get())
                print("MCU PORT is OPENED")


            if simport:
                self.simcomm = comm.Serial(simport, baudrate=self.__baud_rate.get(), bytesize=self.__data_bits.get(),
                                       parity=self.__parity_bits.get(), stopbits=self.__stop_bits.get(), xonxoff=self.__flow_control_xonxoff.get(),
                                       rtscts=self.__flow_control_rtscts.get(), dsrdtr=self.__flow_control_dsrdtr.get())
                print("SIMCOM PORT IS OPENED")


            if(self.microcomm.is_open) or (self.simcomm.is_open):
                self.__connect_button['state']= DISABLED
                self.__disconnect_button['state'] = NORMAL
                self.__cbox1['state'] = DISABLED
                self.__cbox2['state'] = DISABLED
                for child in  self.__baud_frame.winfo_children():
                    child['state'] = DISABLED
                for child in self.__data_bits_frame.winfo_children():
                    child['state'] = DISABLED
                for child in self.__parity_frame.winfo_children():
                    child['state'] = DISABLED
                for child in self.__flow_control_frame.winfo_children():
                    child['state'] = DISABLED
                for child in self.__stop_bits_frame.winfo_children():
                    child['state'] = DISABLED
        except (comm.SerialException):
            messagebox.showinfo(title="Serial Port Error", message="The COM ports need to be selected properly!,"
                                                                "They cannot be the same or NoValue!!")
        except ValueError:
            messagebox.showinfo(title="Value Error", message="Please check if the Settings of COM port are selected")

    def disconnect_callback(self):
        if self.microcomm.is_open:
            self.microcomm.close()
            print("MCU PORT IS CLOSED")
        if self.simcomm.is_open:
            self.simcomm.close()
            print("SIMCOM PORT IS CLOSED")
        self.__disconnect_button.config(state=DISABLED)
        self.__connect_button.config(state=NORMAL)
        self.__cbox1['state'] = NORMAL
        self.__cbox2['state'] = NORMAL
        for child in self.__baud_frame.winfo_children():
            child['state'] = NORMAL
        for child in self.__data_bits_frame.winfo_children():
            child['state'] = NORMAL
        for child in self.__parity_frame.winfo_children():
            child['state'] = NORMAL
        for child in self.__flow_control_frame.winfo_children():
            child['state'] = NORMAL
        for child in self.__stop_bits_frame.winfo_children():
            child['state'] = NORMAL


    def check_ports_mcu(self):
        self.__cbox1['values']=()
        comm_ports = (self.__serial_port())
        for ports in comm_ports:
            self.__cbox1['values'] +=(ports,)
        ##self.__cbox1.set(comm_ports)
        print(self.comm_ports)

    def check_ports_simcom(self):
        self.__cbox2['values']=()
        comm_ports = self.__serial_port()
        for ports in comm_ports:
            self.__cbox2['values'] +=(ports,)
        print((self.comm_ports))

    def clear_textbox_callback(self):
        self.mcu_textbox.delete("1.0",END)
        self.sim_textbox.delete("1.0",END)

    def move_text_box(self,*args):
        self.sim_textbox.yview(*args)
        self.mcu_textbox.yview(*args)




