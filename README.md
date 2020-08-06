# WELCOME TO THE OVERALL DEV GUIDE FOR THIS PROJECT

# REMOVE IP in 1c) and Passwrd in 1d) and 1e) if released publicly

This will be presented in the order of installation. Related code will be in this folder as well and is intentionally written to be simple and easy to modify for your purposes.
For more info or questions, feel free to reach me at asahmed2@ualberta.ca after you've exhausted google. For development tools some tips can be found in the Part 2 of this.

## 1. Setting up Raspberry Pi.
a) This step is perhaps the simplest, we'll start by "flashing" (writing) the Raspberry Pi OS to an SD Card. Navigate to https://www.raspberrypi.org/downloads/ and download the imager for your OS (the os of the machine you're using to write the OS to your SD Card). Download it and run it. In this guide we'll be using the Lite Raspbian OS, feel free to use the full desktop version if you like, it will probably make setting up the Pi easier but you'll need a screen at least until you setup the ssh. 

b) Remove the SD card when the flash is complete and then insert it again. enable ssh by creating a file called "ssh" in the boot directory that was created. Ensure it doesnt have any extension, windows can be misleading about this so double-check the Properties of the file. This is assuming you'll be using a wired connection for the Pi if you choose wireless look that up (TODO: Insert instructions for wireless).

c)Remove the SD card and find your Pi's IP address from your router's control panel. To access your router's control panel type your router's IP address in your browser, youll find this on the router. Currently 172.16.1.69 ##REMOVE THIS BEFORE POSTING##

d)type ssh pi@<ip address> in your cmd prompt and say yes if there's a warning. The default password is "raspberry" Type passwd to change your password and create a new one. Our password for now is "cls4ever"

optional step 1) Setup a static IP (we've gotta talk to ST about this?) to ensure this will always work. follow this (https://www.ionos.ca/digitalguide/server/configuration/provide-raspberry-pi-with-a-static-ip-address/). ** Issues if we're doing ethernet or wifi, for now lets try not to mess with any of this.

e)follow steps on https://grafana.com/tutorials/install-grafana-on-raspberry-pi/#3 to download and install grafana. Our pword is cls4ever again. you should be able to see it at http://172.16.1.69:9090/ (replace the first part with your rPi's ip)

d) Now to download and install Prometheus run the command "cat /proc/cpuinfo" to check the architecture of your pi, I'm currently using a Pi Model 3 B so my architecture is ARMv7. Now check Prometheus' download page and find the github for the appropriate version in this case its "https://github.com/prometheus/prometheus/releases/download/v2.20.0/prometheus-2.20.0.linux-armv7.tar.gz" then on your pi do "wget https://github.com/prometheus/prometheus/releases/download/v2.20.0/prometheus-2.20.0.linux-armv7.tar.gz"

Now that the tar is downloaded do "tar xfz prometheus-2.20.0.linux-armv7.tar.gz" (replace with the version you downloaded) to extract the contetns and then delete the tar file via "rm prometheus-2.20.0.linux-armv7.tar.gz", then change the new directory name to prometheus for simplicity by "mv prometheus-2.20.0.linux-armv7/ prometheus/"

Now to setup prometheus starting up when the Pi starts we create a file in the appropriate directory via "sudo nano /etc/systemd/system/prometheus.service". Paste the following inside this file and save it

~~~
[Unit]
Description=Prometheus Server
Documentation=https://prometheus.io/docs/introduction/overview/
After=network-online.target

[Service]
User=pi
Restart=on-failure

#Change this line if Prometheus is somewhere different
ExecStart=/home/pi/prometheus/prometheus \
--config.file=/home/pi/prometheus/prometheus.yml \
--storage.tsdb.path=/home/pi/prometheus/data

[Install]
WantedBy=multi-user.target
~~~

then run sudo systemctl daemon-reload ,sudo systemctl start prometheus  ,sudo systemctl status prometheus You will have to type Ctrl+C to escape this
then sudo systemctl enable prometheus 
This just makes sure Prometheus is running and will run on system start.

Now on your other computer you should be able to see prometheus running at http://172.16.1.69:9090/ (replace first part with your rPi's IP again)

And just like that the rPi grafana/Prom is all setup. Now we'll deal specifically with our project for montoring the SRS-100. We will modify Prom settings later to ensure we dont overuse our Memory or storage and to ensure we scrape the right thing.


## 2. Finding COM Ports (and development advice)
This is pretty important and can be done on your own PC, which is what I recommend. Once you plug in the USB-serial or even USB hub-serial to your computer and the IGC-100s you can navigate to your Device Manager (on windows) and you should see a list of COM ports. All of those represent the IGCs connected to your computer. 

Dev Advice But Also Useful For Complex Setups: You'll find a test_COM.py file included with this README. This allows you to send queries of your choice accross the COM port of your choice. This is perfect for identifying which IGC was assigned to which COM port. It is important to note that you have no guarantees the IGC's will always show up as the same COM port so it is important to find a way to distinguish between them. (TODO: Find the IGC command that returns their unique identifier). This is important when one script is reading from multiple IGC's via a usb hub. One other key piece of advice is to look at my final script to get a sense of how to read and write to the serial port in Python, it can be extremely easy if you know what youre doing but can lead to a lot of headaches if you dont. THE MOST IMPORTANT THING regardless of your method is the serial attributes must match with the configuration on the IGC100, you can check that in the Menu (read programming manual introduction for more details), however I'll include the configuration I used. Modify the values if you see your IGC is setup differently:

~~~
      port = port_name, #Your COM Port
      baudrate = 115200,
      parity = serial.PARITY_NONE,
      bytesize = serial.EIGHTBITS,
      stopbits = serial.STOPBITS_ONE,
      xonxoff = 0,
      rtscts = 0,
      timeout = 1
~~~

Look at the comments of this file right under this line for some debugging advice if you notice weird RAM usage like i did!
<!-- 
43mb 14:31

reading at 4:11pm

Filesystem      Size  Used Avail Use% Mounted on
/dev/root        14G  1.6G   12G  12% /
devtmpfs        459M     0  459M   0% /dev
tmpfs           464M     0  464M   0% /dev/shm
tmpfs           464M   18M  446M   4% /run
tmpfs           5.0M  4.0K  5.0M   1% /run/lock
tmpfs           464M     0  464M   0% /sys/fs/cgroup
/dev/mmcblk0p1  253M   51M  202M  21% /boot
tmpfs            93M     0   93M   0% /run/user/1000

Should be a memory dump at around 16:32, which is in 15 mins. we'll see if it actually works and the 15 days is for storage retention which should be fine but we can calc to be safe. The question is, if we remove this dashboard will that remove the queries? Probably not, I dont think we can delete Prometheus as a target of itself which means we need to consider this a cost of using Prom, which means less RAM for our project :/

Will update at 16:32. Will leave rPi alone till then and just research other stuff for now so we can get an accurate reading when we read its values after.

Still going up despite some indications that we wrote to the sd card... no idea whats going, will leave running over night to see whats up, in the meantime lets download python and setup the new scraping and whatnot. it is now 17:49 and memory usage is 
             total        used        free      shared  buff/cache   available
Mem:          926Mi       140Mi       162Mi        17Mi       623Mi       757Mi
Swap:          99Mi          0B        99Mi
will download python when i get back from a coffee run to starbucks!

              total        used        free      shared  buff/cache   available
Mem:          926Mi       152Mi       145Mi        17Mi       628Mi       756Mi
Swap:          99Mi          0B        99Mi
^^ at 19:13

Left running over night, creeped up quite a bit more but as reached a plateua 
 -->

## 3. Installing Python and getting our scripts
So now we need to ensure we have python installed, we can do that via "python3 --version", if its not already installed for some reason try "sudo apt update" and check again. Google if that doesn't fix. 

Now we need to get the code (and this Readme!) on our rPi . So let's do that. 

