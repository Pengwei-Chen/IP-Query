import os
import sys
import re
import requests

directory = repr(os.path.dirname(os.path.realpath(sys.argv[0]))).strip("'").replace("\\\\", "/") + "/"
table = open(directory + "Table.txt", "w", encoding = "UTF-8")
os.chdir(directory + "/Surfshark_Config")
for file in os.listdir():
    ip = file.split("_")[0]
    content = requests.get("https://www.ipshudi.com/" + ip + ".htm").text
    location = re.findall("<td class=\"th\">归属地</td>\n<td>\n<span>(.*?)</span>", content)[0].rstrip(" ")
    table.write(ip + "\t" + location + "\n")
table.close()