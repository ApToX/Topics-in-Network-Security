# Topics in Network Security
 Mini Project at BGU in Network Security


# Setup Instructions:

// Run the following commands inorder to run the project &nbsp;

// The following steps were done on Ubunutu Linux Virtual Machine &nbsp;

// First we need to install Python 3 on the Linux machine &nbsp;
sudo apt-get install python3 &nbsp;

// Now we're going to install the necessary python packages &nbsp;
sudo apt-get -y install python3-pip &nbsp;
pip3 install puremagic &nbsp;

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
