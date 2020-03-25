# Topics in Network Security
 Mini Project at BGU in Network Security


# Setup Instructions:

// Run the following commands inorder to run the project

// The following steps were done on Ubunutu Linux Virtual Machine

// First we need to install Python 3 on the Linux machine
sudo apt-get install python3

// Now we're going to install the necessary python packages
sudo apt-get -y install python3-pip
pip3 install puremagic

// Now we can run the project itself
// Open two shells, One for the server and one for the client

// On the first tab run the following command (Server runs forever so in order to kill when finished, use CTRL-C)
python3 Server.py

// On the second tab run one of the following commands (Depends on whice client you want to test)
python3 Malicious_Client.py
// Or
python3 Suspicious_Client.py
// Or
python3 Normal_Client.py
