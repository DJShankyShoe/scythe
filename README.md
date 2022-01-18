# yetToBeNamed

## Description
A "honeypot" webpage that is used to display a fake organisation that fingerprints the actor's device and broswer information upon visit. Once an actor visits the page for login in, fingerprint.js will be executed. This data will logged for SIEM monitoring like Splunk and creating signatures. To lure attacker, credentials can be released on the net where upon successeful logon using those credential would reveal bad actors and fingerprinting is done. Failed logon attempts can also be monitored for fingerprinting when a bruteforce takes place. Splunk rules for those scenarios can be created and once alerted it will exeute main.py which is responsibile for extracting the right fingerprints from the logs for generrting 3 main types of signatures for each actor/unique fingerprint. These 3 singatures are designed for 3 different stages of defense - Rate Limiting, Challenge, Blocks which can be released to the cyber community to deal will the bad actors with continously updateing signatures.

## Websever Setup
Install the package & and run `install`
> Take note - if you have apache installed and happen to have any files in `/var/www/html`, you will have to move them somehwere safe since this directory will be overwritten
```shell
git clone https://github.com/DJShankyShoe/yetToBeNamed.git
tar -xvzf yetToBeNamed.git && cd yetToBeNamed
sudo ./install
```

When Installed


## Splunk Installation
<details>
<summary>Click for details</summary>
  
For this part, users must do it manually, due to the Splunk license. User can use their 60days free trial to download
https://www.splunk.com/en_us/download/splunk-enterprise.html


Download .tgz format

![image](https://user-images.githubusercontent.com/83162708/149708677-d4c5ccd7-a07f-48b3-9c59-b3349786e70f.png)


Create a directory at `/opt/splunk` for your splunk installation and move splunk tar package there for extarction </br>
```shell
sudo mv splunk-8.2.4-87e2dda940d1-Linux-x86_64.tgz /opt/splunk
sudo tar -xvzf /opt/splunk/splunk-8.2.4-87e2dda940d1-Linux-x86_64.tgz
```
Create a myhash.txt at `/opt/splunk` to store the hashes of the JSON fingerprints </br>
```shell
sudo touch myhash.txt
```

For the first time setup, users would have to create admin username and password </br>
```shell
sudo /opt/splunk/splunk/bin/splunk start --accept-license
```

![image](https://user-images.githubusercontent.com/83162708/149709048-d36afa98-97da-4b3c-9e3e-589db68b28c3.png) </br>


## Splunk Setup
Please place
[main.py](https://github.com/DJShankyShoe/yetToBeNamed/blob/master/splunk/main.py) at ```/opt/splunk/splunk/bin/scripts```


### Data Input:
Click Settings > Data inputs

![image](https://user-images.githubusercontent.com/83162708/149710610-9ecfce6c-6a0a-4404-a2e7-bfa42dab5f86.png) </br>


Add new to Files & Directories

![image](https://user-images.githubusercontent.com/83162708/149709105-2cdb5ac9-0af9-40b5-b8fc-be2c3548e8e6.png) </br>


File or Directories: /var/log/apache2

![image](https://user-images.githubusercontent.com/83162708/149709127-2b4464d5-c2c7-4b20-bdd5-6f54c182437b.png) </br>


### Alert:
Search: `"/var/log/apache2/*" user=zebrapal123`

![image](https://user-images.githubusercontent.com/83162708/149709248-a1c43b4f-c8e8-4a52-b688-eefdd9aec189.png)


Click Save as alert: </br>
> Tile: zebrapal </br>
> Alert type: Real-time </br>
> Expires: 60 days </br>
> When triggered: Run a script, File name:main.py

![image](https://user-images.githubusercontent.com/83162708/149710721-b11d2b42-55a0-4b5a-8f38-648dcb9210f4.png)
</details>

## How it Works

## After alert being triggered
The main.py located at ```/opt/splunk/splunk/bin/scripts``` will run.</br>
The script will hash the JSON format fingerprints and check if the hash is exist in myhash.txt

If Exist:</br>
Do nothing.

If NOT Exist:</br>
- Update the myhash.txt
- Create a new folder named: yara-(Hash values of the JSON fingerprints）, in the folder it will consist:
  1. yara_ratelimit
  2. yara_challenge
  3. yara_block

## Use Cases
 
## Moving Forward
- Using the created signature yara_block to create auto block
- Integration of more SIEM tools
- Fingeprint more information
- Customize your own signatures easily


