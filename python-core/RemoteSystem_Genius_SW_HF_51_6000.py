from ControlInterfaceBase import *
from time import sleep

class PowerButton(ButtonsOnOff):
    def __init__(self, name, default_value, connection, command_on, command_off, interface):
        self.name = name
        self.default_value = default_value
        self.value = default_value
        self.connection = connection
        self.command_on = command_on
        self.command_off = command_off
        self.interface = interface

    def SetValue(self, value):
        was_off = 0
        if self.value == 0 and value == 1:
            self.value = 1
            was_off = 1
            self.ClickOn()
        elif self.value == 1 and value == 0:
            self.value = 0
	    self.interface.GetButton("mute").SetValue(1)
	    sleep(0.5)
	    self.ClickOff()

        if was_off:
            sleep(3)
            for button in self.interface.GetButtons():
                if button.GetName() != "power" and button.GetName() != "reset" and button.GetName() != "mute":
                    button.RestoreValue()
		if button.GetName() == "mute":
		    button.Reset()

class ResetButton(SingleButton):
    def __init__(self, name, default_value, connection, command, interface):
        self.name = name
        self.default_value = default_value
        self.value = default_value
        self.connection = connection
        self.command = command
        self.interface = interface

    def SetValue(self):
        self.Click()
        for button in self.interface.GetButtons():
            if button.GetName() != "mute":
                button.Reset()

class RemoteSystem_Genius_SW_HF_51_6000:
    def SetButtons(self):
        interface = self.interface

        ir_connection = "ir"
        radio_connection = "radio"

        button_power = PowerButton("power", 1, radio_connection, "python /home/pi/python-core/RFSendAudio.py audio_on", "python /home/pi/python-core/RFSendAudio.py audio_off", interface)
        interface.SetButton(button_power)

        button_reset = ResetButton("reset", 0, ir_connection, "KEY_RESET", interface)
        interface.SetButton(button_reset)

        button_mute = SingleButton("mute", 0, ir_connection, "KEY_MUTE")
        interface.SetButton(button_mute)

        button_volume = ButtonPair("volume", 0, 63, 45, ir_connection, "KEY_VOLUME_UP", "KEY_VOLUME_DOWN")
        interface.SetButton(button_volume)

        button_volume_woofer = ButtonPair("volume_woofer", -8, 8, 0, ir_connection, "KEY_WOOFER_UP", "KEY_WOOFER_DOWN")
        interface.SetButton(button_volume_woofer)

        button_volume_center = ButtonPair("volume_center", -8, 8, 0, ir_connection, "KEY_CENTER_UP", "KEY_CENTER_DOWN")
        interface.SetButton(button_volume_center)

        button_volume_front = ButtonPair("volume_front", -8, 8, 0, ir_connection, "KEY_FRONT_UP", "KEY_FRONT_DOWN")
        interface.SetButton(button_volume_front)

        button_volume_rear = ButtonPair("volume_rear", -8, 8, 0, ir_connection, "KEY_REAR_UP", "KEY_REAR_DOWN")
        interface.SetButton(button_volume_rear)

    def __init__(self):
        self.device_name = "GENIUS_SW_HT_5.1_6000"
        self.interface = ControlInterfaceBase(self.device_name)
        self.SetButtons()

        #initial synchronization algorithm
        self.interface.GetButton("power").SetValue(0)
        sleep(1)
        self.interface.GetButton("power").SetValue(1)
        sleep(1)
        for button in self.interface.GetButtons():
            button.Reset()
	self.interface.GetButton("volume").SetValue(10)

    def GetInterface(self):
        return self.interface

    def GetName(self):
        return self.device_name

    def GetStatus(self):
        message = []
        for button in self.interface.GetButtons():
            message.append("%s=%d" % (button.GetName(), button.GetValue()))
        return message
