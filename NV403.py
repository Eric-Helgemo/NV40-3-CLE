# This software is provided 'as-is', without any express or implied warranty. 
# In no event will the author be held liable for any damages arising from the 
# use of this software.
#
# Permission is granted to anyone to use this software for any purpose, 
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
# claim that you wrote the original software. If you use this software in a
# product or paper, an acknowledgement in the product documentation or citation of the github page would be appreciated
# but is not required.
# 2. Altered source versions should be plainly marked as such so we can avoid confusion

#Note that I, the author of this driver, am not at all affiliated with this company nor was I commisioned to write this by the company.
#A document explaining how to use the program and a demonstration of it is included in the github page.

import pyvisa as visa
import sys
import time

class NV40_3():
    #First entry is the resource name you assigned when initializing the device. This is here so you can run multiple NV40/3 systems if needed for a given application without
    #issue. An explaination of how to connect to the system is given above.
    #Device type should be either NV40/3 or NV40/3CLE. This will track the types of allowed commands by model.
    #is_remote will default set all channels to remote. If you want only specific ones, pass them as 0 for off and 1 for on as [z, y, x]
    #is_closed_loop will set the channels to closed loop depending on if it is 0 for open loop or 1 for closed loop. If it is a NV40/3 model, this is skipped.
    #By default it assumes that you are using closed loop, because why wouldn't you want to use closed loop if you payed extra for it?
    def __init__(self, resource_name, model, is_remote = [1, 1, 1], is_closed_loop = [1, 1, 1]):
        if model == "NV40/3" or model == "NV40/3CLE":
            self.model = model
        else:
            sys.exit("Your model must be either NV40/3 or NV40/3CLE.")
        #You can determine your visa address in a number of ways. Some are listed in the github documentation.
        self.Jena = resource_name
        #Sets all channels to remote on startup.
        self.Remote(0, is_remote[0])
        self.Remote(1, is_remote[1])
        self.Remote(2, is_remote[2])
        #Note that only NV40/3CLE can change out of open loop. For this reason, we don't have to worry about it for NV40/3. This is why the default is this way.
        if model == "NV40/3CLE":
            self.is_closed = is_closed_loop
            self.Closed(0, is_closed_loop[0])
            self.Closed(0, is_closed_loop[1])
            self.Closed(0, is_closed_loop[2])
        else:
            self.is_closed = [0, 0, 0]

    #Currently not working! Doesn't want to display the right string. Feel free to end me a fix if you find one!
    #Check for Error. If there is no error, returns "OK. No error." Else, returns the string that's associated with the error.
    def Error(self):
        self.Jena.write("Err?")
        #Can't handle imediately takeing the information.
        time.sleep(0.15)
        return str(self.Jena.read())
    #Version fails similarly to Error. Should return the version the device is.
    def Version(self):
        self.Jena.write(f"ver")
        return self.Jena.read()
    
    #Sets the channel to remote or not remote. By default, sets to remote. 0 = off, 1 = on. Channels are z = 0, y = 1, x = 2.
    def Remote(self, channel, is_on = 1):
        self.Jena.write(f'setk,{channel},{is_on}')

    #Switches the channel to closed if is_closed = 1 and open if is_closed = 0
    def Closed(self, channel, is_closed):
        if  self.model == "NV40/3":
            sys.exit("NV40/3 does not have closed loop capabilities.")
        self.Jena.write(f"cloop, {channel}, {is_closed}")
        self.is_closed[channel] = is_closed

    #Returns if a channel is currently open(0) or closed(1). 
    def is_Closed(self, channel):
        return self.is_closed[channel]

    #Returns channel value. In closed loop, this is in um and in open loop it's in volts.
    def Set(self, channel, setting):
        return self.Jena.write(f"set, {channel}, {setting}")

    #Sets all values at once.
    def Setall(self, ch0, ch1, ch2):
        self.Jena.write(f"setall, {ch0}, {ch1}, {ch2}")

    #Returns a given channel's current setting to 3 decimal places. In closed loop, this is in um and in open it is in V. Returns it as a float.
    def Measure(self, channel):
        self.Jena.write(f"rk, {channel}")
        self.Jena.write(f"measure")
        time.sleep(0.15)
        out = str(self.Jena.read()).split(",")
        #On rare occasions, this will output something in a not workable form.
        #This will loop it until it comes in a form workable by this line, which is the majority of the time.
        try:
            return float(out[-1].split("\r")[0])
        except:
            self.Measure(channel)

    #Returns all position measurements of the 3 channels as a list of [ch0, ch1, ch2] as floats where of voltage or um depending on loop setting 
    #and organized as [ch0, ch1, ch2]
    def Measure_All(self):
        self.Jena.write(f"measure")
        time.sleep(0.15)
        out = self.Jena.read().split(",")
        #On rare occasions, this will output something in a not workable form.
        #This will loop it until it comes in a form workable by this line, which is the majority of the time.
        try:
            return [float(out[-3]), float(out[-2]), float(out[-1].split("\r")[0])]
        except:
            self.Measure_All()

    #Sets the channel to either softstart when the system is booted up, setting = 1, or disable softstart when the system starts, setting = 0.
    def Soft_Start_Enable(self, channel, setting):
            self.Jena.write(f"fenable, {channel}, {setting}")

    #Sets soft start for all channels to either off, 0, or on, 1.
    def Soft_Start_Enable_All(self, setting):
        self.Jena.write(f"fready, {setting}")
