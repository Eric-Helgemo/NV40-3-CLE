# NV40-3-CLE
This is python instrument interface code I wrote for controlling Piezosystem Jena's NV40/3 and NV40/3CLE piezo amplifier. This code was written independently by me without affiliation with the Piezosystem Jena company.

# Files Included
- NV403.py is the driver file for this device.
- Driver Introduction.ipynb gives an introduction to the driver and how it is used.

# Getting Started
The driver takes 2 to 4 inputs:
The 1st is an initialization of your device. This means that you will need to initialize your device through pyvisa as shown in the driver introduction document. There are many methods to find your visa ID, such as:
- through National Instrument's VISA driver system: shttps://www.ni.com/en/support/downloads/drivers/download.ni-visa.html#521671
- Through pyvisa itself, you can sometimes recognize visa ID's through it's resource list.
- the python package Serial can sometimes be used to find these ID's.
The 2nd entry is simply a string indicating the model, either "NV40/3" or "NV40/3CLE".
The 3rd is the list of channels you want to use remotely. By default, this is all of them on: [1, 1, 1]
The 4th is the list of channels you want to use in closed vs open loop. Note that this is only applicable to NV40/3CLE systems, as NV40/3 can only use open loop. Be careful that you don't change from open to closed or visa-versa in the wrong moment, as changing modes will cause the piezo to extend up to 20% of it's range of motion. See device documentation for more details.

# Caviots/Notes
This program has been tested on the NV40/3 system and not the NV40/3CLE system. The only differences are commands for closed loop actions, so the commands designed for the NV40/3CLE should work with the given structure, allowing this device to be usable. Another note is that I was able to get everything to work within this class with the exception of the "version" command and "error" command, because they wouldn't properly send back words. If you get this working, feel free to let me know and I'll add that to the driver code. All other components seem to work consistently.

# Fair Use
You are free to use this as you wish. While an acknowledgement of this code being used in any product or citation to the github page in any research project would be appreciated, it is not at all required or expected. The only thing I ask is that you don't claim this code is written as your own and if you use it as a base for your own code, that you acknowledge this somewhere in the documentation.

# Contacting me
Feel free to reach out if you run into issues. Keep in mind that I don't personally own this device, so at the time you message me I might not have access to a device to test your issues on. At the moment, you can reach me at erichelgemo@g.ucla.edu.

Good luck with your experiments and I hope this is helpful!

