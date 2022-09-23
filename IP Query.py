import os
import sys
import shutil
import re
import requests
from googletrans import Translator

directory = repr(os.path.dirname(os.path.realpath(sys.argv[0]))).strip("'").replace("\\\\", "/") + "/"
table = open(directory + "Table.txt", "w", encoding = "UTF-8")
os.chdir(directory + "Surfshark_Config")
shutil.rmtree(directory + "OpenVPN Config")
os.mkdir(directory + "OpenVPN Config")
for file in os.listdir():
    if file.find("tcp") != -1:
        continue
    ip = file.split("_")[0]
    content = requests.get("https://www.ipshudi.com/" + ip + ".htm").text
    try:
        location = re.findall("<td class=\"th\">归属地</td>\n<td>\n<span>(.*?)</span>", content)[0].rstrip(" ")
        if location.find(" ") != -1:
            location = location.split(" ")[0]
    except:
        print(ip)
        continue
    translator = Translator()
    translate = translator.translate(location, dest = "en").text
    translate = translate[0].upper() + translate[1:]
    table.write(ip + "\t" + translate + "\n")
    name = translate + " - " + ip
    os.mkdir(directory + "OpenVPN Config/" + name)
    config_file = open(file, "r")
    config = "".join(config_file.readlines()).replace("auth-user-pass", "auth-user-pass auth-user-pass.txt") + '''
route douyu.com 255.255.255.255 net_gateway
route zju.edu.cn 255.255.255.255 net_gateway
route youdao.com 255.255.255.255 net_gateway
route 10.109.92.4 255.255.255.255 net_gateway
route 10.105.100.224 255.255.255.255 net_gateway
route 10.109.92.5 255.255.255.255 net_gateway
route 47.52.206.109 255.255.255.255 net_gateway
route hoffman2.idre.ucla.edu 255.255.255.255 net_gateway
'''
    config_file.close()
    config_file = open(directory + "OpenVPN Config/" + name + "/" + name + ".ovpn", "w")
    config_file.write(config)
    config_file.close()
    shutil.copy(directory + "auth-user-pass.txt", directory + "OpenVPN Config/" + name + "/")
table.close()