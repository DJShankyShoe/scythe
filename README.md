# yetToBeNamed

# Description
A honeypot webpage running using an apache server and will take in the visitor/attacker fingerprint. We have Splunk to monitor the logs for the apache. Once the visitor/attacker has used the given username and password to log in this will trigger the alert and a python script, the script will use the visitor ID to identify the user if is unique if the user does not exist in the signature. It will automatically update the YARA signatures into 3 different parts.


# Splunk Installation
For this part, users must do it manually, due to the Splunk license. User can use their 60days free trial to download
https://www.splunk.com/en_us/download/splunk-enterprise.html

Download .tgz format

![image](https://user-images.githubusercontent.com/83162708/149708677-d4c5ccd7-a07f-48b3-9c59-b3349786e70f.png)

```sudo mkdir /opt/splunk``` </br>


Based on the version of download </br>
```sudo mv splunk-8.2.4-87e2dda940d1-Linux-x86_64.tgz /opt/splunk``` </br>


```sudo tar xvzf splunk-8.2.4-87e2dda940d1-Linux-x86_64.tgz```

For the first time using splunk, user have to create admin username and password.</br>
```sudo splunk/bin/splunk start --accept-license  (at /opt/splunk)```

![image](https://user-images.githubusercontent.com/83162708/149709048-d36afa98-97da-4b3c-9e3e-589db68b28c3.png)

# Splunk Setup
### Data Input:
Click Settings > Data inputs

![image](https://user-images.githubusercontent.com/83162708/149710610-9ecfce6c-6a0a-4404-a2e7-bfa42dab5f86.png)


Add new to Files & Directories

![image](https://user-images.githubusercontent.com/83162708/149709105-2cdb5ac9-0af9-40b5-b8fc-be2c3548e8e6.png)


File or Directories: /var/log/apache2

![image](https://user-images.githubusercontent.com/83162708/149709127-2b4464d5-c2c7-4b20-bdd5-6f54c182437b.png)


### Alert:
Search: "/var/log/apache2/*" user=zebrapal123 

![image](https://user-images.githubusercontent.com/83162708/149709248-a1c43b4f-c8e8-4a52-b688-eefdd9aec189.png)

Save as alert:
Tile: zebrapal </br>
Alert type: Real-time </br>
Expires: 60 days </br>
When triggered: Run a script, File name:main.py

![image](https://user-images.githubusercontent.com/83162708/149710721-b11d2b42-55a0-4b5a-8f38-648dcb9210f4.png)

