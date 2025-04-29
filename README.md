# SCP_Display
A Raspberry Pi Zero W-based keychain displaying random SCP pages from https://scp-wiki.wikidot.com

**How does it work??**
Without going into too much detail, it will generate a random number between 2-100 
(keeping out SCP-001 intentionally because I'm too lazy to code the different proposals)
and will insert that number into this into a link kinda like this: https://scp-wiki.wikidot.com/scp-___

It will then scrape that link for the SCP classification, name, containment procedures, and description
Then it will format it onto the Waveshare e-ink screen, all pretty looking

There's a bunch of other goobletygoop that controls and makes sure that it doesn't overflow the screen,
making sure that the classification doesn't mash into the other stuff, etc., that I won't be explaining unless someone specifically asks





**INSTRUCTIONS**
*This is an intermediate-level project, and some Windows and Linux knowledge is expected.*


*parts*
Costs of parts are ~$80 on Amazon 
- Raspberry Pi Zero WH https://a.co/d/21jY7oC
- Waveshare V4 (although if you're smart, you can adjust my code) https://a.co/d/08nji3Y
- PiSugar Batter (I used the S because it's cheap, but any work) https://a.co/d/hyGs7Vb
- I'm assuming you have an SD card and a reader
- Not technically needed, but see if you can 3d print a case for it. 
- https://www.thingiverse.com/thing:5450141 i'm like 80% sure this one will work

*flashing and setting up*

1. Follow the instructions in this article for basic flashing and installation: https://www.instructables.com/How-to-Install-RASPBERRY-PI-OS-on-MicroSD-Card-Usi/

2. Make sure that you enable these settings:
     - Use the Raspberry Pi OS Lite (uses fewer resources, and we don't need a GUI)
     - Set the wifi to whatever your wifi stuff is (yes, it's caps sensitive)
     - Set your username to whatever, just make sure you change it in the code.
     - ENABLE SSH!!!!! You won't be able to do jackshit if you don't. Just have it on password verification for the            sake of simplicity. It will use whatever password you set for your username.
     - Flash it and wait until it says done
     - Put the SSD into your Zero WH
     - Plug it in (the plug furthest from the center)

3. SSH into your Pi
     - This is a relatively simple process, assuming you have all your settings correct in your flashing setup
     - Give your Pi Zero a bit to boot up and get all its stuff set up
     - open your command terminal in whatever OS you're using (I **think** it works the same on everything, but idk im          just a Windows fella)
     - Type "**ssh YOURUSERNAM@raspberrypi.local**" and see if it lets you in. If it doesn't let you in, wait like ~1         minute and try again. If that also doesnt work, you probably fucked up the wifi setup and you need to 
       reflash and re-enter everything
      - If it worked, you should have a wall of text pop up about fingerprints, just type yes and enter the password           you set.
      - If shit hits the fan and it's not working:
      - Ensure you're using the right password. If you forgot it, you need to reflash your stuff and start over
        (sidenote: when you SSH again after restarting your password, it'll pop up a bunch of scary text. This is              normal; just follow this tutorial:
        https://www.outdoortechnologist.com/2024/01/31/remove-ssh-known-hosts-on-windows/

4. Update your shit and install packages
     - update and upgrade your OS with this command: "sudo apt update && sudo apt upgrade -y"
     - Install the Python tools we need using this: "sudo apt install -y python3-pip git python3-pil python3-numpy"
     - enable SPI for the e-ink screen: "sudo raspi-config" then go to Interface Options → SPI → Enable
     - get Waveshare's e-paper library: "git clone https://github.com/waveshare/e-Paper"
     - install requests and bs4: "sudo apt install python3-requests python3-bs4"
     - install my script and the SCP logo
     - git clone https://github.com/TyGy08baka/SCP_Display.git
     - cd SCP_Display


3. Test your Waveshare screen works
     Go to Waveshare's test directories: "cd ~/e-Paper/RaspberryPi_JetsonNano/python/examples"
     - assuming you're running the V4 I am, run: "python3 epd_2in13_V4_test.py" and if you have seated correctly, you           should be ballin
     - If you don't have the Waveshare and Pisugar seated, it's easy asf, so I don't feel the need to explain.
       google it if you're confused


4. Add your phone's hotspot
     - For the most part, the process is simple (although I will admit I don't know the in-depth of how to connect to          an Android hotspot. First, just set it up (I'm not explaining this if you're confused, Google it)
     - ssh into your pi and connect to your phone hotspot. this will get it in it's known networks.
     - **sudo nmcli device wifi connect "HOTSPOT NAME" password "HOTSPOT PASSWORD"**
     - when it connects, just restart it and turn off your phone hotspot. it should automatically connect back to your        wifi you originally connected it to.
     - SSH into it and use **nmcli connection show** to see all your known connections. It might have the wifi you set        up in flashing as "preconfigured" or something like that.
     - Set your home wifi as low priority using this:
     - **sudo nmcli connection modify "WIFI_SET_UP_IN_FLASHING" connection.autoconnect-priority 10**
     - Then set your phone hotspot priority as high
     - **sudo nmcli connection modify "PHONE_HOTSPOT_NAME" connection.autoconnect-priority 100**
     - Give it a quick reboot and see if it connects to your hotspot.
     - If it doesn't, make sure you entered everything right and you have your phone hotspot actually on when rebooting
     - **NOTE. IF YOU ARE ON IPHONE, YOU MUST TURN ON MAXIMIZE CAPABILITY**

5. test it 
     - inside your SSH session, run the following code:
     - cd ~
     - mkdir scp_terminal
     - cd scp_terminal
     - python3 scp_display.py
     - You SHOULD have a fully functioning mobile SCP-displayer.


I have zero doubt that i fucked up something in this tutorial. if I did, please feel free to make an issue in github or bully me on the reddit post i probably put this on.

