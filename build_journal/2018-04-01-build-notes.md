Today I got the kids involved making - and we had some fun getting the motor cables the right way.
However, the stall outs, or lock ups troubled me. 
The piconzero on this (and tankbot) kept stopping - and it could even stop with the motors running.
This was disturbing.

[youtube driving before]

I was researching stuff on motor stall currents, and brushing up my physics - what had I missed? The robot could fail only seonds in, or a while in.

After checking on twitter, and then reading the piconzero docs - it turns out that older pi raspbian images had i2c stability issues.
So I started a dist-upgrade on it. This seemed like a great plan.

Bad news  then - I knocked out the power cable (external wall power) while doing the update!
The image I had was not going to work again. I'd luckily backed up my own code before doing so - so nothing lost but time.
And the @approx_eng came to the rescue with an image he had with BlueZ and sixaxis control on board, along with openCV. Which will save my compiling again.
My old image had python3 - so after using his image, there was some adapting to do.
First - smbus needed to be smbus2 - but this was because I had overlooked I was in a virtual env - once I'd adapted that, the motor test worked.
@biglesp had python3 adaptations of the piconzero code to use now.

I got it to drive again! It was no longer hanging, but I was getting squealing motor stalls.

My next thought was to try taming it from full spin to just braking a tread at a time.
So I make a "tankTest.py" module adapted from "motorTest.py" - using the numeric keypad like tank drive controls:

| Motor   | Left | Right |
| ------- | ---- | ----- |
| Forward |   7  |   9   |
| Stop    |   4  |   6   |
| Reverse |   1  |   3   |

This was then driving brilliantly - few stalls, no piconzero cutouts. Stability seems good.

[youtube driving now]

---
## Controller

This image from @approx_eng comes with BlueZ preinstalled - so lets try getting the controller live.
* First - get the pad to pair/trusted in BlueControl.
    
* Then make a bit of code to read the pad - plan - 2 Sticks for left track/right track. Try to get button reads - start, select, 4 main buttons. Triggers later.
    * This should just print the read values.
* Adapt the tankTest to this.
* Test drive - and video. 
* Publish this on orionrobots blog (filtering out real uuid's)
(Publish all these journal bits, my evernote notes, twitter history on this in an orionrobots piwars tag)

### Pairinig

Powered up the pi - powered from PC via USB to preserve robot battery power.
Started up bluetoothctl as pi user.

Lets plug in the pad to see what happens - according to @approx_eng, this kernel and bluetoothctl has a plugin for registering the sixaxis.
I plug in and see this:

    [NEW] Device 00:19:C1:3A:75:1B Sony PLAYSTATION(R)3 Controller
    [DEL] Device 00:19:C1:3A:75:1B Sony PLAYSTATION(R)3 Controller

Why is it NEW then DEL?

According to Approx_eng I should expect this:

> The guide doesn't assume you've rebuilt BlueZ from source! As I did, 
> you should be able to run bluetoothctl, plug the controller in, 
> say 'yes' to the prompt, then unplug and press the PS button.

Hmm - no prompt. Lets try unplug, then press the PS button.
Flashing lights on the PAD, nothing in bluetoothctl.

DO Need to be root on the pi?
Same - NEW/DEL combo.
Nothing further from BlueToothCtl.

Time to dive into DMesg.


    [  232.228847] usb 1-1.4: USB disconnect, device number 4
    [  268.939861] usb 1-1.4: new full-speed USB device number 5 using dwc_otg
    [  269.097846] usb 1-1.4: New USB device found, idVendor=054c, idProduct=0268
    [  269.097859] usb 1-1.4: New USB device strings: Mfr=1, Product=2, SerialNumber                                                                                                                                   =0
    [  269.097869] usb 1-1.4: Product: PLAYSTATION(R)3 Controller
    [  269.097878] usb 1-1.4: Manufacturer: Sony
    [  269.182343] input: Sony PLAYSTATION(R)3 Controller Motion Sensors as /devices                                                                                                                                   /platform/soc/3f980000.usb/usb1/1-1/1-1.4/1-1.4:1.0/0003:054C:0268.0002/input/in                                                                                                                                   put3
    [  269.250204] input: Sony PLAYSTATION(R)3 Controller as /devices/platform/soc/3                                                                                                                                   f980000.usb/usb1/1-1/1-1.4/1-1.4:1.0/0003:054C:0268.0002/input/input2
    [  269.250997] sony 0003:054C:0268.0002: input,hiddev96,hidraw0: USB HID v81.11                                                                                                                                    Joystick [Sony PLAYSTATION(R)3 Controller] on usb-3f980000.usb-1.4/input0
    [  270.380141] Under-voltage detected! (0x00050005)
    [  276.621037] Voltage normalised (0x00000000)
    [  284.202314] usb 1-1.4: USB disconnect, device number 5

Hmm - We have the device - when plugged in. BUt where is the bluetooth stuff?
Need to probe more into how this image is working. The under voltage has me worried.
BUt first - is there a bluetooth log? Lets check /var/log as root - and see what I have:
    
    -rw-r--r-- 1 root root    7675 Mar 31 23:28 alternatives.log
    drwxr-xr-x 2 root root    4096 Mar 31 23:28 apt
    -rw-r----- 1 root adm   121369 Apr  1 14:03 auth.log
    -rw-r--r-- 1 root root    4925 Apr  1 11:30 boot.log
    -rw-r--r-- 1 root root       0 Mar 13 22:53 bootstrap.log
    -rw------- 1 root utmp     768 Mar 13 23:11 btmp
    -rw-r----- 1 root adm   472905 Apr  1 13:53 daemon.log
    -rw-r----- 1 root adm    26173 Apr  1 11:29 debug
    -rw-r--r-- 1 root root  263885 Mar 31 23:28 dpkg.log
    -rw-r--r-- 1 root root       0 Mar 13 22:53 faillog
    -rw-r--r-- 1 root root     751 Mar 19 18:08 fontconfig.log
    -rw-r----- 1 root adm   710830 Apr  1 13:53 kern.log
    -rw-rw-r-- 1 root utmp  292292 Apr  1 11:30 lastlog
    -rw-r----- 1 root adm   679805 Apr  1 13:53 messages
    drwxr-x--- 2 root adm     4096 Nov 20 22:24 samba
    -rw-r----- 1 root adm  1216548 Apr  1 13:53 syslog
    -rw-r----- 1 root adm    22170 Apr  1 13:53 user.log
    -rw-rw-r-- 1 root utmp   85632 Apr  1 11:30 wtmp

Okay - start with messages and syslog. I'm using less and shift-g to get to the end of a log.

    Apr  1 13:53:44 skittlebot kernel: [  268.939861] usb 1-1.4: new full-speed USB device number 5 using dwc_otg
    Apr  1 13:53:44 skittlebot kernel: [  269.097846] usb 1-1.4: New USB device found, idVendor=054c, idProduct=0268
    Apr  1 13:53:44 skittlebot kernel: [  269.097859] usb 1-1.4: New USB device strings: Mfr=1, Product=2, SerialNumber=0
    Apr  1 13:53:44 skittlebot kernel: [  269.097869] usb 1-1.4: Product: PLAYSTATION(R)3 Controller
    Apr  1 13:53:44 skittlebot kernel: [  269.097878] usb 1-1.4: Manufacturer: Sony
    Apr  1 13:53:44 skittlebot kernel: [  269.182343] input: Sony PLAYSTATION(R)3 Controller Motion Sensors as /devices/platform/soc/3f980000.usb/usb1/1-1/1-1.4/1-1.4:1.0/0003:054C:0268.0002/input/input3
    Apr  1 13:53:44 skittlebot kernel: [  269.250204] input: Sony PLAYSTATION(R)3 Controller as /devices/platform/soc/3f980000.usb/usb1/1-1/1-1.4/1-1.4:1.0/0003:054C:0268.0002/input/input2
    Apr  1 13:53:44 skittlebot kernel: [  269.250997] sony 0003:054C:0268.0002: input,hiddev96,hidraw0: USB HID v81.11 Joystick [Sony PLAYSTATION(R)3 Controller] on usb-3f980000.usb-1.4/input0
    Apr  1 13:53:44 skittlebot mtp-probe: checking bus 1, device 5: "/sys/devices/platform/soc/3f980000.usb/usb1/1-1/1-1.4"
    Apr  1 13:53:44 skittlebot mtp-probe: bus: 1, device: 5 was not an MTP device
    Apr  1 13:53:52 skittlebot kernel: [  276.621037] Voltage normalised (0x00000000)

What is "mtp-probe"? Media-transfer-protocol - okay, that is irrelevant. Try syslog.
    
    Apr  1 13:53:44 skittlebot kernel: [  269.182343] input: Sony PLAYSTATION(R)3 Controller Motion Sensors as /devices/platform/soc/3f980000.usb/usb1/1-1/1-1.4/1-1.4:1.0/0003:054C:0268.0002/input/input3
    Apr  1 13:53:44 skittlebot kernel: [  269.250204] input: Sony PLAYSTATION(R)3 Controller as /devices/platform/soc/3f980000.usb/usb1/1-1/1-1.4/1-1.4:1.0/0003:054C:0268.0002/input/input2
    Apr  1 13:53:44 skittlebot kernel: [  269.250997] sony 0003:054C:0268.0002: input,hiddev96,hidraw0: USB HID v81.11 Joystick [Sony PLAYSTATION(R)3 Controller] on usb-3f980000.usb-1.4/input0
    Apr  1 13:53:44 skittlebot mtp-probe: checking bus 1, device 5: "/sys/devices/platform/soc/3f980000.usb/usb1/1-1/1-1.4"
    Apr  1 13:53:44 skittlebot mtp-probe: bus: 1, device: 5 was not an MTP device
    Apr  1 13:53:44 skittlebot bluetoothd[433]: sixaxis: compatible device connected: Sony PLAYSTATION(R)3 Controller (054C:0268 /sys/devices/platform/soc/3f980000.usb/usb1/1-1/1-1.4/1-1.4:1.0/0003:054C:0268.0002/hidraw/hidraw0)
    Apr  1 13:53:44 skittlebot bluetoothd[433]: sixaxis: setting up new device
    Apr  1 13:53:44 skittlebot bluetoothd[433]: Authentication attempt without agent

Ah-hah "Authentication attempt without agent". Sixaxis is recognising the device. So what is this "authentication attempt without agent" issue?
Lets bring up bluetoothctl again.

    bluetoothctl
    Agent registered
    [bluetooth]# agent on
    Agent is already registered

Hmm. Lets google for that message.
Well the hits suggest I need to trust the device. Lets try that - it didn't work last night. Plug in, then do the trust.

    [NEW] Device 00:19:C1:3A:75:1B Sony PLAYSTATION(R)3 Controller
    [DEL] Device 00:19:C1:3A:75:1B Sony PLAYSTATION(R)3 Controller
    [bluetooth]# trust  00:19:C1:3A:75:1B
    Device 00:19:C1:3A:75:1B not available

Well why is it then not available? Lets try some more with bluetoothctl - maybe it's not properly discoverable by the sixaxis.

    [bluetooth]# default-agent
    Default agent request successful
    [bluetooth]# discoverable on
    Changing discoverable on succeeded
    [CHG] Controller B8:27:EB:68:7E:2B Discoverable: yes
    [bluetooth]# pairable on
    Changing pairable on succeeded
    [bluetooth]# scan on

And now the samsung TV - even *in standby* is flooding my console. How annoying.
Lets unplug and reattach the sixaxis.
    
    [NEW] Device 00:19:C1:3A:75:1B Sony PLAYSTATION(R)3 Controller
    Authorize service
    [blue1m[agent] Authorize service 00001124-0000-1000-8000-00805f9b34fb (yes/no):yes
    [CHG] Device 00:19:C1:3A:75:1B Trusted: yes
    [CHG] Device 00:19:C1:3A:75:1B UUIDs: 00001124-0000-1000-8000-00805f9b34fb

That's it!
Now I may need default scripts to make this happen on startup...
Now unplug - press PS - and it is controller 1! Success.

    root@skittlebot:/var/log# ls /dev/input
    event0  event1  js0  mice

According to [The DualShock PS 3 Input Library Guide](https://approxeng.github.io/approxeng.input/api/dualshock3.html#):

> If a new device has appeared here then congratulations, 
> you have successfully paired your dongle and SixAxis controller. 
> This will persist across reboots, so from now on you can just connect by
pressing the PS button on the controller. Pressing and holding this button will 
> shut the controller down - at the moment there’s no timeout so be sure to turn
> the controller off when you’re not going to be using it for a while.

Now lets get some python code reading it. Starting here: https://approxeng.github.io/approxeng.input/simpleusage.html
I have some old code in my git repo - for doing this in pygame. But no - I think I would like to try it with this stand alone lib. I've heard good
things about the input library.
Lets start off with his sample code - understanding the parts of it.

Nice pertinent bit of information here:

> The connected property on the joystick object indicates whether the underlying device is connected or not - if, for example, you have a controller that goes out of range, runs out of batteries, or is turned off while in use this will be set to False and you can handle the case correctly (if using this code in a robot, this would be an excellent time to turn of all your motors, for instance!)

Ok some code added to read the two sticks Y position and print it.

    print("Left track", joystick.ly, "Right track", joystick.ry)

Lets run this... Ah - no module approxeng - can I pip install it?

    (env3) pi@skittlebot:~/piwars-bot $ pip install approxeng.input
    Collecting approxeng.input
      Downloading https://www.piwheels.org/simple/approxeng-input/approxeng.input-2.0.4-py3-none-any.whl
    ...
    
Oh yes...

Now output - trying the left and right sticks - but not getting what I'd expect here:

    Left track 0 Right track 0
    [W 180401 14:32:35 __init__:295] Unknown axis code 4, value 127
    [W 180401 14:32:35 __init__:295] Unknown axis code 4, value 126

What does this mean? Wait - 2.0.4? 

Now using the controller example from https://approxeng.github.io/approxeng.input/examples/show_controls.html - and the axis are wierd.
Time to talk on twitter.

---

Next stages:
* Fitting camera
* Fitting distance sensors
* Getting my skittlebot code adapted for both the driving style and new opencv.
* Making the distance sensor code.
* Tidying up - cables a mess - my plan is to use PC drive power adaptors.
* Making a cover - not sure how much time, but this is Helena's most wanted task.
   
