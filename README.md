# Monitoring SRS100 Remotely (Instructions on how to setup and use)

For dev advice and in-depth discussion on how to install see dev.md

This guide is assuming you've ssh'd into a Raspberry Pi.

1. Download python, grafana, and prometheus via sudo apt-get, follow Grafana's advice on setting up the service here: https://grafana.com/tutorials/install-grafana-on-raspberry-pi/#1

2. Modify /etc/prometheus/prometheus.yml to include the job srs_igc from the prometheus.yml file in this repo

3. Get monitor_srs.py onto your pi either by cloning this repo or curl/wget.

4. Ensure the code reflects your USB-serial port, then run monitor_srs.py via the command:
    
        python3 monitor_srs.py

to verify the code works. You may or may not have the dependecies already installed, if not, use sudo apt-get to install pip3 then use pip3 to get all the depndencies.
 TODO: SIMPLIFY THIS

5. do "sudo nano /etc/rc.local" and before the exit 0 line insert:
        python3 /home/pi/PATH_TO_YOUR_FILE/monitor_srs.py &

This ensures the code will run on startup everytime and suppresses outputs. 

6. Congratulations, Your SRS IGC 100 will now be remotely monitorable using Grafana! usually at port 30000 of your Pi.

7. Need to extend the project ? For example add another controller or perhaps more readings from the same controller? See dev.md