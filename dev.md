# Development 

## Extending the concept to include more controllers
To do this you'll need to open multiple serial-ports and keep in mind that there is usually a small possiblity that your COM/tty ports may swap numbers if your Pi reboots. You can use a usb hub that guarantees set port numbers to combat this and look into using /dev/serial/by-id . OR, you could initialize the program by querying the controllers for their ID and setting them up that way. Also be sure to follow along the lab manual SRS provides (search SRS IGC 100) and double-check to ensure you've setup serial-communication instead of just assuming baud-rate etc.

## Extending to include more readings for one controller
This is super simple. In my code I query for GDAT? 1 and GDAT? 3 for IG1 and PG1 respectively. Just look at the documentation in the user manual for GDAT to find the reading code your looking for and adapt my code slightly, perhaps changing my bool igc variable to an enum or integer that you use to keep track of which controller your currently querying/exposing.

## Im having trouble finding the COM Port number, Help!
Use Tests/test_COM.py . its only tested on windows but it may be able to help you.


## Essential cmds to help with dev
    journalctl -e -u prometheus     - This gives you detailed logs about the prometheus server running, helpful when debugging
    lslogins -u                           - TODO update
    sudo systemctl daemon-reload       - reloads services 
    sudo systemctl status prometheus    - check status of prometheus, replace status with "enable" to enable it to start on start-up and replace status with "start" to start.
    nmap -sn 192.168.1.0/24             - finds all users connected to the current router within the range of 192.168.1.0-192.168.1.255 (helpful for locating the pi)
    killall -HUP prometheus            - reloads prometheus so you can update the config file
    service --status-all              - shows current status of all services


## Need help? 
If you've been banging your head on the wall for a few too many hours feel free to email me at asahmed2@ualberta.ca , I may be able to help.