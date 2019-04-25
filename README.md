# RFIDTapPoint

# Preparation & Installation:

1. Update our Raspberry Pi:
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-dev python3-pip
sudo pip3 install spidev
```
2. Install the MFRC522 library to your Raspberry Pi using pip:
```
sudo pip3 install mfrc522
```
3. Install Pyrebase:
```
sudo pip3 install pyrebase
sudo pip3 install --upgrade google-auth-oauthlib
```
4. We install the required packages for WS281x:
```
sudo apt-get install gcc make build-essential python-dev git scons swig
```
Notes: if you run into problem spi package could not be uninstalled, please find and remove it from the script so the installation will go through.

5. Now we can download the library
```
git clone https://github.com/jgarff/rpi_ws281x
```
In this directory are on the one hand some C files included, which can be easily compiled. In order to use them in Python, we need to compile them:
```
cd rpi_ws281x/
sudo scons
```
6. Switch to the Python folder and carry out the installation:
```
cd python
sudo python3 setup.py build
sudo python3 setup.py install
```


Done! Now we should be able to clone or download RFIDTapPoint repo above to the desired location and run:
```
cd RFIDTapPoint/
sudo python3 Read.py
```

# Run on startup:
1. Edit the file /etc/rc.local:
```
sudo nano /etc/rc.local
```
Add commands to execute the python program at the bottom, replace the path to /home/pi/<your-path>/Read.py
```
sudo python3 /home/pi/RFIDTapPoint-master/Read.py &
exit 0
```
Press Ctrl-O to save then Ctrl-X to exit nano
