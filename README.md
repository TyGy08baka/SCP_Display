# SCP_Display
A Raspberry Pi Zero W-based keychain displaying random SCP pages from https://scp-wiki.wikidot.com

**How does it work??**
without going into too much detail, it will generate a random number between 2-100 
(keeping out SCP-001 intentionally because im too lazy to code the different proposals)
and will insert that number into this into a link kinda like this: https://scp-wiki.wikidot.com/scp-___

it will then scrap that link for the SCP classification, name, containment procedures, and description
then it will format it onto the waveshare e-ink screen all pretty looking

theres a bunch of other goobletygoop that controls and makes sure that it doesnt overflow the screen,
making sure that the classification doesnt mash into the other stuff, etc. that i wont be explaining unless someone specifically asks





**INSTRUCTIONS**
*this is a intermediate level project, and some windows and linux knowledge is expected*


*parts*
Costs of parts are ~$80 on amazon 
- Raspberry Pi Zero WH https://a.co/d/21jY7oC
- Waveshare V4 (although if youre smart you can adjust my code) https://a.co/d/08nji3Y
- PiSugar Batter (I used the S bcus its cheap but any work) https://a.co/d/hyGs7Vb
- I'm assuming you have an SD card and reader


*flashing and setting up*

1. follow the instructions in this article for basic flashing and installation: https://www.instructables.com/How-to-Install-RASPBERRY-PI-OS-on-MicroSD-Card-Usi/
   **HOWEVER**
   make sure you follow these VERY important steps.

2. Make sure that you enable these settings:
     - Use the Raspberry Pi OS Lite (uses less resources and we dont need a GUI)
     - Set the wifi to whatever your wifi stuff is (yes its caps sensitive)
     - set your username to veritium (not **techincally** required, but unless you want to dig into my dumpster fire          of code to change the username in all of it, it's best to keep it as it is in the code)
     - ENABLE SSH!!!!! You won't be able to do jackshit if you dont. just have it on password verification for the            sake of simplicity. it will use whatever password you set for your veritium username.
     - flash it and wait until it says done
     - put the SSD into your Zero WH
     - plug it in (the plug furthest from the center)

3. SSH into your pi
     - this is a relatively simple process, assuming your have all your settings correct in your flashing setup
     - give your Pi Zero a bit to boot up and get all its stuff set up
     - open your command terminal in whatever OS youre using (i **think** it works the same on everything but idk im          just a windows fella)
     - type "ssh veritium@raspberrypi.local" and see if it lets you in.
           - If it doesnt let you in, wait like ~1 minute and try again
           - If that also doesnt work, you probably fucked up the wifi setup and you need to reflash and re-enter                    everything
      - if it worked, you should have a wall of text pop up about fingerprints, just type yes and enter the password           you set
            - if you keep getting the password wrong check two things.
            - first check if you changed the username from something thats not veritium in the settings. if so do
              "ssh (YOUR USERNAME HERE)@raspberrypi.local"
            - Ensure your using the right password. if you forgot it, you need to reflash your stuff and start over
              (sidenote when you ssh again after restarting your password itll pop up a bunch of scary text, this is                 normal, just follow this tutorial: https://www.outdoortechnologist.com/2024/01/31/remove-ssh-known-                    hosts-on-windows/

4. Update your shit and install packages
     - update and upgrade your OS with this command: "sudo apt update && sudo apt upgrade -y"
     - install the python tools we need using this: "sudo apt install -y python3-pip git python3-pil python3-numpy"
     - enable SPI for the e-ink screen: "sudo raspi-config" then go to Interface Options → SPI → Enable
     - get Waveshare's e-paper library: "git clone https://github.com/waveshare/e-Paper"
     - install requests and bs4: "sudo apt install python3-requests python3-bs4"

3. test your waveshare screen works
     - go to waveshare's test directories: "cd ~/e-Paper/RaspberryPi_JetsonNano/python/examples"
     - assuming your running the V4 i am, run: "python3 epd_2in13_V4_test.py" and if you have seated correctly, you           should be ballin
           - if you dont have the waveshare and pisugar seated, its easy asf so i dont really feel the need to explain.
             google it if your confused
4. start the fun part
     - inside your ssh session, run the following code:
       cd ~
       mkdir scp_terminal
       cd scp_terminal
       nano scp_display.py
     - BEFORE you start copying and pasting, we need to import the scp logo.
           - you can techincally use any one you want (although the one i provide is the easiest), just keep in mind                it'll be shrunk to 30x30
           - once youve downloaded it, make sure it's named "scp_logo" and convert it to a .bmp file. the easiest way               to do this is to just open microsoft paint, import whatever file you chose and export it as a .bmp
           - download gitbash using this link: https://git-scm.com/downloads
                 - it's pretty intuitive, just click the bitbash button in the installer and click recommeded for                         everything else, but heres a video if you getconfused: https://www.youtube.com/watch?v=USZqL4QDXjU
       
