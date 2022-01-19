# yetToBeNamed

## Description
A "honeypot" webpage that is used to display a fake organisation that fingerprints the actor's device and browser information upon visit. Once an actor visits the page for login, fingerprint.js will be executed. This data will be logged for SIEM monitoring like Splunk and creating signatures. To lure attackers, credentials can be released on the net whereupon successful logon using those credentials would reveal bad actors and fingerprinting is done. Failed login attempts can also be monitored for fingerprinting when brute force takes place. Splunk rules for those scenarios can be created and once alerted it will execute main.py which is responsible for extracting the right fingerprints from the logs for generating 3 main types of signatures for each actor/unique fingerprint. These 3 signatures are designed for 3 different stages of defence - Rate Limiting, Challenge, Blocks which can be released to the cyber community to deal will the bad actors with continuously updating signatures.

## Websever Setup
Install the package & and run `install`
> Take note - if you have apache installed and happen to have any files in `/var/www/html`, you will have to tranfer them somewhere safe since this directory will be overwritten
```shell
git clone https://github.com/DJShankyShoe/yetToBeNamed.git
tar -xvzf yetToBeNamed.git && cd yetToBeNamed
sudo ./install
```

## Splunk Installation
<details>
<summary>Click for details</summary>
  
For this part, users must do it manually, due to the Splunk license. User can use their 60days free trial to download
https://www.splunk.com/en_us/download/splunk-enterprise.html


Download .tgz format

![image](https://user-images.githubusercontent.com/83162708/149708677-d4c5ccd7-a07f-48b3-9c59-b3349786e70f.png)


Extract the splunk tar package at `/opt` </br>
```shell
sudo tar -xvzf splunk-8.2.4-87e2dda940d1-Linux-x86_64.tgz -C /opt
```

For the first time setup, users would have to create admin username and password </br>
```shell
sudo /opt/splunk/bin/splunk start --accept-license
```

![image](https://user-images.githubusercontent.com/83162708/149709048-d36afa98-97da-4b3c-9e3e-589db68b28c3.png) </br>


## Splunk Setup
Please place
[main.py](https://github.com/DJShankyShoe/yetToBeNamed/blob/master/splunk/main.py) at ```/opt/splunk/bin/scripts```


### Data Input:
Click Settings > Data inputs

![image](https://user-images.githubusercontent.com/83162708/149710610-9ecfce6c-6a0a-4404-a2e7-bfa42dab5f86.png) </br>


Add new to Files & Directories

![image](https://user-images.githubusercontent.com/83162708/149709105-2cdb5ac9-0af9-40b5-b8fc-be2c3548e8e6.png) </br>


File or Directories: `/var/log/apache2` <br>
Do the same for: `/var/log/fingerprint`

![image](https://user-images.githubusercontent.com/83162708/149709127-2b4464d5-c2c7-4b20-bdd5-6f54c182437b.png) </br>


### Alert:
Search: `source="/var/log/apache2/access.log*" user=zebrapal123`

![image](https://user-images.githubusercontent.com/83162708/149709248-a1c43b4f-c8e8-4a52-b688-eefdd9aec189.png)


Click Save as alert: </br>
> Tile: Actor Login </br>
> Alert type: Real-time </br>
> Expires: 60 days </br>
> When triggered: Run a script, File name:main.py

![image](https://user-images.githubusercontent.com/62169971/150076852-c6c5ff6e-a49d-430e-a2a8-4f1873c4f549.png)
</details>

## Flow
![image](https://user-images.githubusercontent.com/62169971/150096967-4a1bfe06-89b0-47d4-b588-8575fccaaada.png)

- Upon successful/failed login, the page will load fingerprint.php
- Fingerprint.php creates a randomly generated PHP file name for retrieving POST data
- Fingerprint.php collects fingerprint from the actor and POSTS it to the generated PHP file
- The generated PHP file logs the fingerprint & deletes itself
- The logs from apache & fingerprint is logged by SIEM Splunk
- Upon alert (customizable by the user), it executes main.py which then extracts the appropriate fingerprint for that event
- Main.py will then generate 3 main types of Yara signatures where used for **Rate Limiting**, **Challenge**, **Block** 

## Fingerprints Details
- General
  - Screen Resolution
  - Broswer Type
  - Broswer Version
  - Mobile (True/False)
  - OS Type
  - OS Version
  - Cookies (True/False)
  - Flash Version
  - Agent
- Hardware
  - CPU Cores
  - GPU
- Network
  - API Status
  - Country
  - Region
  - Region Name
  - City
  - Zip
  - Latitude
  - Longitude
  - ISP
  - ORG
  - As
  - Asname
  - Reverse DNS
  - Mobile - Cellular Data (True/False)
  - Proxy (True/False)
  - Hosting (True/False)
  - IP Address
- Browser
  - Broswer Permissions
    - Geolocation
    - Notification
    - Push
    - Midi
    - Camera
    - Microphone
    - Speaker
    - Device-info
    - Background-fetch
    - Background-sync
    - Bluetooth
    - Persistent-storage
    - Ambient-light-sensor
    - Accelerometer
    - Gyroscope
    - Magnetometer
    - Clipboard
    - Screen-wake-lock
    - NFC
    - Display-capture
    - Accessibility-events
    - Clipboard-read
    - Clipboard-write
    - Payment-handle
    - Idle-detection
    - Periodic-background-sync
    - System-wake-lock
    - Storage-access
    - Window-placement
    - Font-access
    - Tabs
    - Bookmarks
    - UnlimitedStorage
  - Language
    - Browser Language
    - System Language
    - User Language
  - Plugins
  - Fonts
  - Timezone
  - Canvas Hash
- Unqiue Visitor ID - FingerprintJS

## After alert being triggered
The main.py located at ```/opt/splunk/bin/scripts``` will be executed</br>
The script will hash the JSON formated fingerprints and verifies for any duplicates in hash.txt

**If Duplicate Exist:**
- Do nothing

<br>**If NO Duplicates Exist:**
- Update the myhash.txt
- Create a new folder named: yara-(Hash values of the JSON fingerprints）, in the folder it will consist:
  1. yara_ratelimit
  2. yara_challenge
  3. yara_block

## Splunk Dashboard
This is sample dashboard that user can use:
![image](![image](https://user-images.githubusercontent.com/83162708/150101566-30d4f84d-5821-4443-add9-d5e24e536be1.png)

Funtions of this dashboard
- Every hash is represented by a unique avatar
- The user able to select the hash to check the 3 Yara signatures
- The user able to input ip to check if there is realated hash to the IP
- Check the locations

Click [HERE](https://github.com/DJShankyShoe/yetToBeNamed/blob/master/splunk/dashboard.xml) to get dashboard source code




## Use Cases

Attackers have been using multiple methods to exploit sites, services, steal credentials & much more. When successful, attackers can use that to gain access to restricted sites, information or permissions. At this stage, defenders would be 1 step behind thus it is important to gain hold of attacker footprints in advance to improve defensive detection by introducing more specific signatures directed to those attackers/bad actors. 

### Scenario: Exposed Credentials
> Thus, releasing fake credentials on such places will lure attackers to our site,  giving us information about their fingerprints.

Release of our website crednetials on pastebins. Hopefully atatcker's crawler would pick it up
![image](https://user-images.githubusercontent.com/62169971/150104029-e7cfb3ad-775f-4a50-9ad3-4c2ea24f1e40.png)

When the crawler picks it up, the attacker would attempt to log in using our credentials on our site
![image](https://user-images.githubusercontent.com/62169971/150104616-2ac73027-093a-4c6b-8464-efa16cf1a070.png)

Upon logon, fingerprinting of attacker's device is collected
![image](https://user-images.githubusercontent.com/62169971/150104677-32082f31-387f-4e42-b611-e2def69ed436.png)

A rule written to detect login will be triggered and execute a python script to create signatures
![image](https://user-images.githubusercontent.com/62169971/150110059-de2ba7b0-1a66-48a3-ace3-40fa6260b7ec.png)

3 main types of signatures are created (Block, Challenge, Rate Limit)
![image](https://user-images.githubusercontent.com/62169971/150109026-53261c6d-7b8d-4c07-ac04-5a5498e026be.png)

For this scenarios, the Block signature can be integrated with a firewall to block the atatcker usage to organisation sites. Do note that, from the picture below, the attacker is blocked from accessing the honeypot site which is only an example. Organisation can use those signatures on their actual network to deal with attackers
![image](https://user-images.githubusercontent.com/62169971/150109302-15b66f23-ee26-4d33-96ab-c327a0380b4d.png)


![image](https://user-images.githubusercontent.com/62169971/150117223-8ada9e1c-25ba-4154-8849-51174fc80229.png)

![image](https://user-images.githubusercontent.com/62169971/150117272-71b0b165-ace3-44f0-9760-1c5799904d11.png)

![image](https://user-images.githubusercontent.com/62169971/150120676-cb36a1d7-5147-466a-b7a3-a8ac749590fe.png)

![image](https://user-images.githubusercontent.com/62169971/150121180-0525666e-2928-49fc-aa56-6f1646edcdaa.png)




 
## Moving Forward
- Using the created signature yara_block to create auto block
- Integration of more SIEM tools
- Fingeprint more information
- Customize your own signatures easily


