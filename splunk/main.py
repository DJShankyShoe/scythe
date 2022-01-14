#!/usr/bin/python3
import json
import hashlib
import os
import os.path
fingerprint_log_file = "log.txt"
hash_file = "myhash.txt"

# get latest json data
with open(fingerprint_log_file, 'r') as f:
    json_data = f.readlines()[-1]

# hash the json_data
json_hash = hashlib.md5(json_data.encode("utf-8")).hexdigest()
json_dict = json.loads(json_data)

# get the visitor id
visitorId = json_dict['visitorId']

# browser permissions hash
browser_permissions = json.dumps(json_dict['browser']['permissions'])
browser_permissions_hash = hashlib.md5(browser_permissions.encode("utf-8")).hexdigest()

# broswer font hash
browser_font = json.dumps(json_dict['browser']['fonts'])
browser_font_hash = hashlib.md5(browser_font.encode("utf-8")).hexdigest()


def getfingerprint(value1, value2):
    fingerprint = json_dict[value1][value2]
    return fingerprint


if json_hash not in open('myhash.txt').read():
    with open('myhash.txt', 'a+') as hash:
        hash.write(json_hash)
        hash.write("\n")

    path = "C:/Users/zengy/PycharmProjects/blackhat/" + "yara-" + visitorId
    os.mkdir(path)

    with open(path + '/yara_ratelimit', 'a+') as yara1:
        yara1.write("rule yara_ratelimit\n"
                    "{\n"
                    ""
                    "strings:\n"
                    "   $browser = " + '"' + getfingerprint('jscd','browser') + '"\n' +
                    "   $browserMajorVersion = " + '"' + str(getfingerprint('jscd','browserMajorVersion')) + '"\n' +
                    "   $mobile = " + '"' + str(getfingerprint('jscd','mobile')) + '"\n' +
                    "   $os = " + '"' + getfingerprint('jscd','os') + '"\n' +
                    "   $agent = " + '"' + getfingerprint('jscd','agent') + '"\n' +
                    "   $ip = " + '"' + getfingerprint('network','query') + '"\n' +
                    "\n"
                    "condition:\n"
                    "    $browser and $browserMajorVersion and $mobile and $os and $agent and $ip"
                    "\n"
                    "}")

    with open(path + '/yara_challenge', 'a+') as yara2:
        yara2.write("rule yara_challenge\n"
                    "{\n"
                    ""
                    "strings:\n"
                    "   $browser_permissions_hash = " + '"' + browser_permissions_hash + '"\n' +
                    "   $browser_font_hash = " + '"' + browser_font_hash + '"\n' +
                    "   $city = " + '"' + getfingerprint('network','city') + '"\n' +
                    "   $cavas = " + '"' + getfingerprint('browser','canvas') + '"\n' +
                    "\n"
                    "condition:\n"
                    "    $browser_permissions_hash and $browser_font_hash and $city and $cavas"
                    ""
                    "\n"
                    "}")

    with open(path + '/yara_block', 'a+') as yara3:
        yara3.write("rule yara_block\n"
                    "{\n"
                    ""
                    "strings:\n"
                    "   $browser_permissions_hash = " + '"' + browser_permissions_hash + '"\n' +
                    "   $browser_font_hash = " + '"' + browser_font_hash + '"\n' +
                    "   $ip = " + '"' + getfingerprint('network','query') + '"\n' +
                    "   $visitor_id = " + '"' + visitorId + '"\n' +
                    "   $cavas = " + '"' + getfingerprint('browser','canvas') + '"\n' +
                    "   $agent = " + '"' + getfingerprint('jscd', 'agent') + '"\n' +
                    "\n"
                    "condition:\n"
                    "    $browser_permissions_hash and $browser_font_hash and $ip and $visitor_id and $cavas and $agent"
                    ""
                    "\n"
                    "}")
