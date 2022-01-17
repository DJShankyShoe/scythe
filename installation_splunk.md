For this part, users must do it manually, due to the Splunk license. User can use their 60days free trial to download.

[Download Splunk](https://www.splunk.com/en_us/download/splunk-enterprise.html)

Download .tgz format
![image](https://user-images.githubusercontent.com/83162708/149708677-d4c5ccd7-a07f-48b3-9c59-b3349786e70f.png)

```sudo mkdir /opt/splunk``` </br>
![image](https://user-images.githubusercontent.com/83162708/149708763-cfb7420b-d671-494d-8028-3096a9a0d861.png)

```sudo mv splunk-8.2.4-87e2dda940d1-Linux-x86_64.tgz /opt/splunk``` #Base on the version you download
![image](https://user-images.githubusercontent.com/83162708/149708775-03914b42-a7e4-49ba-8e6f-a6fd7eb2855c.png)

```sudo tar xvzf splunk-8.2.4-87e2dda940d1-Linux-x86_64.tgz```

For the first time using splunk, user have to create admin username and password.</br>
```sudo splunk/bin/splunk start --accept-license  (at /opt/splunk)```
![image](https://user-images.githubusercontent.com/83162708/149709048-d36afa98-97da-4b3c-9e3e-589db68b28c3.png)

# In splunk
### Data Input:
Click Settings > Data inputs
![image](https://user-images.githubusercontent.com/83162708/149709150-e569fb39-8884-47cf-a2cf-408ef46cce9b.png)

Add new to Files & Directories
![image](https://user-images.githubusercontent.com/83162708/149709105-2cdb5ac9-0af9-40b5-b8fc-be2c3548e8e6.png)

File or Directories: /var/log/apache2
![image](https://user-images.githubusercontent.com/83162708/149709127-2b4464d5-c2c7-4b20-bdd5-6f54c182437b.png)

### Alert:
Search: "/var/log/apache2/*" user=zebrapal123 
![image](https://user-images.githubusercontent.com/83162708/149709248-a1c43b4f-c8e8-4a52-b688-eefdd9aec189.png)

Save as alert:
Tile: zebrapal
Alert type: Real-time
Expires: 60 days
When triggered: Run a script, File name:main.py
![image](https://user-images.githubusercontent.com/83162708/149709342-db6b20e8-0b4c-4f0b-becb-389e07567a9c.png)

