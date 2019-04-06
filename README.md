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
3. Install python-firebase:
```
sudo pip3 install requests
sudo pip3 install python-firebase
```
4. We install the required packages for WS281x:
```
sudo apt-get install gcc make build-essential python-dev git scons swig
```
5. Now we can download the library
```
git clone https://github.com/jgarff/rpi_ws281x
```
In this directory are on the one hand some C files included, which can be easily compiled. The example code for this is easy to understand. In order to use them in Python, we need to compile them:
```
cd rpi_ws281x/
sudo scons
```
6. Switch to the Python folder and carry out the installation:
```
cd python
sudo python setup.py build
sudo python setup.py install
```

Download ZIP files above and extract it to python/examples

Run: 
```
sudo python3 Read.py
```

