import os
from time import sleep

class Controls:
    def __init__(self,name):
        self.name = name
        self.default_value = 0
        self.value = 0
        self.last_value = 0
        self.device_name = ""
    def GetName(self):
        return self.name
    def GetValue(self):
        return self.value
    def Reset(self):
        self.last_value = self.value
        self.value = self.default_value
    def RestoreValue(self):
        self.Reset()
        self.SetValue(self.last_value)
    def SetDeviceName(self,device_name):
        self.device_name = device_name
    def SendCommand(self, connection_type, command_code):
        command_string = ""

        if connection_type == "ir":
            command_string += "irsend SEND_ONCE "
            command_string += self.device_name
            command_string += " "
            command_string += command_code
        elif connection_type == "radio":
            command_string += command_code
        else:
            print("Error: Unknown Connection Type")
            exit(1)

        os.system(command_string)
        #sleep(0.5)


class SingleButton(Controls):
    def __init__(self, name, connection,command):
        self.name = name
        self.default_value = 0
        self.value = 0
        self.connection = connection
        self.command = command
    def __init__(self, name, default_value, connection, command):
        self.name = name
        self.default_value = default_value
        self.value = default_value
        self.connection = connection
        self.command = command

    # click method has to be re-implemented in daugther
    def Click(self):
        #print self.GetName(), " Toogle: ", self.value
        self.SendCommand(self.connection, self.command)

    def Toogle(self):
        if self.value == 0:
            self.value = 1
        else:
            self.value = 0
        self.Click()

    def SetValue(self, value):
        if value != self.value:
            self.Toogle()

class ButtonPair(Controls):
    def __init__(self, name, connection, command_up, command_down):
        self.value = 0
        self.default_value = 0
        self.name = name
        self.min = 0
        self.max = 1
        self.connection = connection
        self.command_up = command_up
        self.command_down = command_down
    def __init__(self, name, min, max, default_value, connection, command_up, command_down):
        self.name = name
        self.default_value = default_value
        self.value = default_value
        self.min = min
        self.max = max
        self.connection = connection
        self.command_up = command_up
        self.command_down = command_down

    # Click Up and Down have to be re-implemented
    def ClickUp(self):
        #print self.GetName(), " Up: ", self.value
        self.SendCommand(self.connection, self.command_up)
    def ClickDown(self):
        #print self.GetName(), " Down: ", self.value
        self.SendCommand(self.connection, self.command_down)

    def Up(self):
        if self.value < self.max:
            self.value = self.value + 1
            self.ClickUp()
    def Down(self):
        if self.value > self.min:
            self.value = self.value - 1
            self.ClickDown()

    def SetValue(self, value):
        if value != self.value:
            number_of_clicks = value - self.value
            if number_of_clicks > 0:
                for i in range(0, number_of_clicks):
                    self.Up()
            else:
                for i in range(0, -number_of_clicks):
                    self.Down()

class ButtonsOnOff(Controls):
    def __init__(self, name, connection, command_on, command_off):
        self.value = 0
        self.default_value = 0
        self.name = name
        self.connection = connection
        self.command_on = command_on
        self.command_off = command_off
    def __init__(self, name, default_value, connection, command_on, command_off):
        self.name = name
        self.default_value = default_value
        self.value = default_value
        self.connection = connection
        self.command_on = command_on
        self.command_off = command_off

    # Click Up and Down have to be re-implemented
    def ClickOn(self):
        #print self.GetName(), " On: ", self.value
        self.SendCommand(self.connection, self.command_on)
    def ClickOff(self):
        #print self.GetName(), " Off: ", self.value
        self.SendCommand(self.connection, self.command_off)

    def On(self):
        self.value = 1
        self.ClickOn()
    def Off(self):
        self.value = 0
        self.ClickOff()

    def SetValue(self, value):
        if value != self.value:
            if value == 1:
                self.On()
            else:
                self.Off()

class ControlInterfaceBase:
        def __init__(self, device_name):
            self.buttons = []
            self.device_name = device_name
        def SetButton(self, button):
            name = button.GetName()
            for entry in self.buttons:
                if name == entry.GetName():
                    print("Error. Button with name ", name, " already exists")
                    exit(1)
            button.SetDeviceName(self.device_name)
            self.buttons.append(button)
        def GetButtons(self):
            return self.buttons
        def GetButton(self, name):
            for button in self.buttons:
                if button.GetName() == name:
                    return button
            print("Error. Button ", name, " does not exist!")
            exit(1)
