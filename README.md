# SCYTHE: `The Yara Signature Crafter` that fingerprints honeypot traffic

```                                                                               
                                         =.                      =-            
                                         .+:.==:            :=-:==             
                                          :%#=               .*%#..:.          
                                      =#%%==#*:             .+#+.+%%%#:        
                                    -%%%%%. .#%-           .*%=  -%%%%%=       
                                   *%%%%#%:   +%+         :##:    :+%%%%*.     
 @@@@@@    @@@@@@@  @@@ @@@      .#%%%=.:*.    =%*.      =%*.       .=%%%#.    @@@@@@@  @@@  @@@  @@@@@@@@  
@@@@@@@   @@@@@@@@  @@@ @@@      *%%=.   -      :%#:    *%+           .+%%*    @@@@@@@  @@@  @@@  @@@@@@@@  
!@@       !@@       @@! !@@     =%#.             .#%- .*%-              .#%=     @@!    @@!  @@@  @@!       
!@!       !@!       !@! @!!     %#.                *%*%#.                .#%.    !@!    !@!  @!@  !@!       
!!@@!!    !@!        !@!@!     -%:                  #%#.                  :%-    @!!    @!@!@!@!  @!!!:!    
 !!@!!!   !!!         @!!!     +#                 .*%#%*.                  %+    !!!    !!!@!!!!  !!!!!:    
     !:!  :!!         !!:      -%.               .#%+ .#%:                 %=    !!:    !!:  !!!  !!:       
    !:!   :!:         :!:      .%.              -%%-    +%=               .%.    :!:    :!:  !:!  :!:       
:::: ::    ::: :::     ::       ==             =%#:      -%*              =#.     ::    ::   :::   :: ::::  
:: : :     :: :: :     :         +.           *%*.        :##:           .*:      :      :   : :  : :: ::     
                                 .-         .#%=           .*%-          :.    
                                           :%#:              =%+               
                                          :*+.                ##+              
                                         :#:                  =.+*.            
                                         .                    +  .:            
                                                              =.               
                                                                               
```

## TOC 

- [SCYTHE: `The Yara Signature Crafter`](#scythe---the-yara-signature-crafter--that-fingerprints-honeypot-traffic)
  * [TOC](#toc)
  * [Description](#description)
    + [Mechanism](#mechanism)
  * [Webserver Setup](#webserver-setup)
  * [Splunk Installation](#splunk-installation)
  * [Splunk Setup](#splunk-setup)
  * [Flow](#flow)
  * [Aftermath of Alert Triggers](#aftermath-of-alert-triggers)
  * [Fingerprint Details](#fingerprint-details)
    + [Extended Fingerprint Collection](#extended-fingerprint-collection)
  * [Splunk Dashboard](#splunk-dashboard)
  * [Use Cases](#use-cases)
    + [Scenario 1: Login Abuses](#scenario-1-login-abuses-such-as-brute-forcing-incl-password-spraying-credentials-dumping-via-ip-rotate)
    + [Scenario 2: Honeypot Credentials](#scenario-2-honeypot-credentials-for-attribution-of-threat-actors-triggering-the-tripwires)
    + [Scenario 3: Honeypot Website](#scenario-3-honeypot-website-for-threat-intelligence)
  * [Why create signatures from browser fingerprints](#why-create-signatures-from-browser-fingerprints)
    + [Reduce False Positives](#reduce-false-positives)
    + [Simplicity](#simplicity)
    + [High Redundancy](#high-redundancy)
  * [Moving Forward](#moving-forward)
  * [Credits - Fingerprint Collection](#credits---fingerprint-collection)


---

## Description
A fingerprinting engine that creates value from abusive traffic by generating attacker YARA signatures of various strictness levels to apply differing levels of mitigating friction. The tool further deploys honeypot entities to proactively perform threat actor attribution to identify and action against malicious actors rotating IP addresses.

### Mechanism
A honeypot webpage fingerprints a malicious actor's device and browser information. Upon visit the login page, `fingerprint.js` will be executed. The captured fingerprint gets forwarded to SIEM and the YARA signature is created. 
To lure attackers, credentials can be released via `scythe` on public sites whereupon successful logon using those credentials would reveal malicious actors and fingerprinting is completed. Failed login attempts are also fingerprinted once rate-limiting thresholds are exceeded or when brute-forcing is detected. Upon such a detection, `main.py` will be executed and **3 levels of YARA signatures of varying strictness will be created**:

| Levels            | 1                                                                                                                            | 2                                                                 | 3                                                                                                                                                        |
|-------------------|------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| Filename          | yara_ratelimit                                                                                                               | yara_challenge                                                    | yara_block                                                                                                                                               |
| Strictness        | least                                                                                                                        | mid                                                               | high                                                                                                                                                     |
| Description       | signature bears least amount of specificity                                                                                  | signature bears broad definitions that are likely to be malicious | signature bears precise details, such as fingerprint + IP, such that layer 7 blocks are only applied to actor and not other users on shared IP addresses |
| Suggested Control | apply rate-limiting policies based on this signature, ie. block the 20th requests coming in within 10 minutes for 15 minutes | throw Google re-captcha on new visits that matches this signature | block requests matching this signature at layer 7                                                                                                        |
<br />

## Webserver Setup
Install the package & and run `install`
> Take note - if you have apache installed and have files in `/var/www/html`, you will have to tranfer them somewhere safe since this directory will be overwritten
```shell
git clone https://github.com/DJShankyShoe/scythe.git
tar -xvzf scythe.git && cd scythe
sudo ./install
```

## Splunk Installation
<details>
<summary>Click for details</summary>
  
You may download a free trial here:
https://www.splunk.com/en_us/download/splunk-enterprise.html


Download .tgz format

![image](https://user-images.githubusercontent.com/83162708/149708677-d4c5ccd7-a07f-48b3-9c59-b3349786e70f.png)


Extract the splunk tar package at `/opt` </br>
```shell
sudo tar -xvzf splunk-8.2.4-87e2dda940d1-Linux-x86_64.tgz -C /opt
```

A set of admin credentials need to be created </br>
```shell
sudo /opt/splunk/bin/splunk start --accept-license
```

![image](https://user-images.githubusercontent.com/83162708/149709048-d36afa98-97da-4b3c-9e3e-589db68b28c3.png) </br>
</details>

## Splunk Setup
<details>
<summary>Click for details</summary>

  Please place [main.py](https://github.com/DJShankyShoe/scythe/blob/master/splunk/main.py)  at ```/opt/splunk/bin/scripts```
  
  
### Data Input:
Click Settings > Data inputs

![image](https://user-images.githubusercontent.com/83162708/149710610-9ecfce6c-6a0a-4404-a2e7-bfa42dab5f86.png) </br>


Add new to Files & Directories

![image](https://user-images.githubusercontent.com/83162708/149709105-2cdb5ac9-0af9-40b5-b8fc-be2c3548e8e6.png) </br>


File or Directories: `/var/log/apache2` <br>
Do the same for: `/var/log/fingerprint`

![image](https://user-images.githubusercontent.com/83162708/149709127-2b4464d5-c2c7-4b20-bdd5-6f54c182437b.png) </br>


### Splunk Alert:
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

1. Upon successful/failed login, the page will load fingerprint.php
2. Login status gets logged and monitored by splunk
3. Fingerprint.php collects fingerprint from the actor's device and broswer
4. Fingerprint.php creates a randomly generated PHP file name for retrieving POST data
5. Fingerprint Data is POSTED to the generated PHP file
6. The generated PHP file, logs the fingerprint whoch would be monitored by splunk
7. The generated PHP file deletes itself after PHP is fully executed
8. Upon alert from SIEM Splunk (customizable by the user), it executes main.py 
9. Main.py extracts the appropriate fingerprint for that event
10. Main.py will finally generate 3 main types of Yara signatures where used for **Rate Limiting**, **Challenge**, **Block** 


## Aftermath of Alert Triggers
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


## Fingerprint Details


| **General**               | **Hardware**    | **Network**                              | **Browser**         | **Unqiue Visitor ID**   |
|     :---                  |    :---         |                :---                      |         :---        |        :---             |
| Screen Resolution         | CPU Cores       | API Status                               | Broswer Permissions | FingerprintJS           |
| Broswer Type              | GPU             | Country                                  | Language            |                         |
| Broswer Version           |                 | Region                                   | Plugins             |                         |
| Mobile `(True/False)`     |                 | Region Name                              | Fonts               |                         |
| OS Type                   |                 | City                                     | Timezone            |                         |
| OS Version                |                 | Zip                                      | Canvas Hash         |                         |
| Cookies `(True/False)`    |                 | Latitude                                 |                     |                         |
| Flash Version             |                 | Longitude                                |                     |                         |
| AGent                     |                 | ISP                                      |                     |                         |
|                           |                 | ORG                                      |                     |                         |
|                           |                 | As                                       |                     |                         |
|                           |                 | Asname                                   |                     |                         |
|                           |                 | Reverse DNS                              |                     |                         |
|                           |                 | Mobile - Cellular Data `(True/False)`    |                     |                         |
|                           |                 | Proxy  `(True/False)`                    |                     |                         |
|                           |                 | Hosting `(True/False)`                   |                     |                         |
|                           |                 | IP Address                               |                     |                         |

### Extended Fingerprint Collection
<details>
<summary>Browser Permissions</summary>
  
`Geolocation` `Notification` `Push` `Midi` `Camera` `Microphone` `Speaker` `Device-info` `Background-fetch` `Background-sync` `Bluetooth` `Persistent-storage` `Ambient-light-sensor` `Accelerometer` `Gyroscope` `Magnetometer` `Clipboard` `Screen-wake-lock` `NFC` `Display-capture` `Accessibility-events` `Clipboard-read` `Clipboard-write` `Payment-handle` `Idle-detection` `Periodic-background-sync` `System-wake-lock` `Storage-access` `Window-placement` `Font-access` `Tabs` `Bookmarks` `UnlimitedStorage` 

</details>

<details>
<summary>Language</summary>

`Browser Language` `System Language` `User Language`
  
</details>

## Splunk Dashboard
This is sample dashboard that users can use:

![image](https://user-images.githubusercontent.com/83162708/150303178-5ed2278b-c9ee-4683-bf45-b5143927219d.png)

**Funtions of this dashboard**
- Every hash is represented by a dynamically generated unique avatar <img src="https://user-images.githubusercontent.com/83162708/150305684-edb2db2b-85b6-4c8a-a253-efba65209836.gif" width="25">
- The user can select the hash to check the 3 Yara signatures
- The user can input IP to check for associated hashes
- Check IP locations

Click [HERE](https://github.com/DJShankyShoe/scythe/blob/master/splunk/dashboard.xml) to get dashboard source code




## Use Cases

Attackers have been using multiple methods to exploit sites, services, steal credentials and more. When successful, attackers can use that to gain access to restricted sites, information or  permissions. We provide proactive approaches to engage the attackers early on.

<br /><br />

### Scenario 1: Login Abuses such as Brute-forcing (incl. Password Spraying, Credentials Dumping) via IP Rotate
> Attackers may bypass rate-limiting controls by employing IP-rotate techniques, thus we fingerprint the attackers device and browser for attribution

`Attackers may attempt to perform bruteforce (when unsuccesful login occurs, fingerprinting of attacker's device is collected)`

![image](https://user-images.githubusercontent.com/62169971/150117223-8ada9e1c-25ba-4154-8849-51174fc80229.png)
---
`A rule written to detect bruteforce attempts will be triggered and executes a python script to create signatures`

![image](https://user-images.githubusercontent.com/62169971/150117272-71b0b165-ace3-44f0-9760-1c5799904d11.png)
---
`3 main types of signatures are created (Block, Challenge, Rate Limit)`

![image](https://user-images.githubusercontent.com/62169971/150120676-cb36a1d7-5147-466a-b7a3-a8ac749590fe.png)
---
`For this scenarios, the Challenge signature can be used for creating recaptcha to prevent/slow down bruteforce attempts by attackers`<br />
**The image below presents a non-exhausive illustration of an attacker being challenged with recaptcha**

![image](https://user-images.githubusercontent.com/62169971/150121180-0525666e-2928-49fc-aa56-6f1646edcdaa.png)

<br /><br /><br />

### Scenario 2: Honeypot Credentials for Attribution of Threat Actors Triggering the Tripwires
> Releasing fake credentials on such places will lure attackers to our site, giving us information about their fingerprints.

`Release of our website credentials on pastebins`

![image](https://user-images.githubusercontent.com/62169971/150104029-e7cfb3ad-775f-4a50-9ad3-4c2ea24f1e40.png)
---
`When attacker's crawler picks it up, the attacker would attempt to log in using our credentials on our honeypot site`

![image](https://user-images.githubusercontent.com/62169971/150104616-2ac73027-093a-4c6b-8464-efa16cf1a070.png)
---
`Upon logon, fingerprinting of attacker's device is collected`

![image](https://user-images.githubusercontent.com/62169971/150104677-32082f31-387f-4e42-b611-e2def69ed436.png)
---
`A rule written to detect login will be triggered and execute a python script to create signatures`

![image](https://user-images.githubusercontent.com/62169971/150110059-de2ba7b0-1a66-48a3-ace3-40fa6260b7ec.png)
---
`3 main types of signatures are created (Block, Challenge, Rate Limit)`

![image](https://user-images.githubusercontent.com/62169971/150109026-53261c6d-7b8d-4c07-ac04-5a5498e026be.png)
---
`For this scenarios, the Block signature can be integrated with a firewall to block the attacker usage to organisation network` <br>
**Do note that, from the picture below, the attacker is blocked from accessing the honeypot site which is only an example. Organisation can use those signatures on their actual network to deal with attackers**

![image](https://user-images.githubusercontent.com/62169971/150109302-15b66f23-ee26-4d33-96ab-c327a0380b4d.png)

<br /><br /><br />

### Scenario 3: Honeypot Website for Threat Intelligence
> Launching scythe with a honeypot / fake site (of a similar industry) to fingerprint malicious traffic for signature creation. The honeypot could be placed under a dummy subdomain of an organization. This feed of signatures can then be shared with the open-source threat intelligence community or consumed internally.

`The attacker used the unkowing Paypal honeypot released credentials to sign into a honeypot account`

![image](https://user-images.githubusercontent.com/62169971/150458414-941acfdf-3a40-4414-91f2-be31bf8c3574.png)
---
`Upon successful sign in, the attacker's fingeprint get logged and signature is generated`

![image](https://user-images.githubusercontent.com/62169971/150458537-13a9056d-b1ae-41a8-bc10-3236046690b8.png)
---
`The user gets blocked from accessing the the organisation's domain network using the yara block generated signature`

![image](https://user-images.githubusercontent.com/62169971/150459546-10becd09-4d9b-4358-9f48-3960078bb2a1.png)

<br /><br /><br />

## Integration

When you want the user fingerprints to be collected & logged, include the following code `require "../fingerprint.php";`. This can be placed on the home page, or when the user has performed a **successful**/**failed** login.

The fingerprint will be logged at `/var/log/fingerprint/log.txt` path. So create one if doesn't exist. Make sure it is given appropriate permissions for web-service to write into the log file

`main.py` is responsible for extracting fingerprint logs and converting them into signatures. Signatures can be found on the following path `/opt/signatures`. **Do make sure to create an empty file `myhash.txt` before executing `main.py`.**


## Why create signatures from browser fingerprints

### Reduce False Positives
Organisation has been mostly using only IP Addresses to deal with bad actors. Sometimes these information are not enough as these IP's could come from organisations, merchants, or any shared groups. These can largly affect customers when using single information like IP for blocks, challenges or rate-limiting. Thus to limit false positives, we can use broswer fingerprints to uniquely identify bad actors among actors for defensive measures without affecting customers and merchants. 

### Simplicity
It is very easy to obtain broswer fingerprints using javascript or logs. It can be done in the background without affecting cusotmer's experience. This makes it simple for organisation to deploy tools for broswer fingerprinting. 

### High Redundancy
Browser fingerprints can be broken down to other multiple information such as header, ip, hardware, canvas hash, etc. So even if 1 or more information is missing, a proper signature can still be crafted for various use cases and confidence levels.

## Moving Forward
- Using the created signature yara_block to create auto block
- Integration of more SIEM tools
- Fingeprint more information
- Customize your own signatures easily

## Credits - Fingerprint Collection

> Network:        http://ip-api.com <br>
> Canvas:         https://codepen.io/jon/pen/rwBbgQ <br>
> Font:           https://codepen.io/run-time/pen/XJNXWV <br>
> Language:       https://codepen.io/run-time/pen/XJNXWV <br>
> Timezone:       https://codepen.io/run-time/pen/XJNXWV <br>
> Fingerprintjs:  https://github.com/fingerprintjs/fingerprintjs <br>
> Permissions:    https://stackoverflow.com/questions/62706697/how-to-enumerate-supported-permission-names-in-navigator-permissions <br>


