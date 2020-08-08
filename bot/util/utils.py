import re
import os
MAGNET_REGEX = r"magnet:\?xt=urn:btih:[a-zA-Z0-9]*"

URL_REGEX = r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+"


def is_url(url: str):
    url = re.findall(URL_REGEX, url)
    if url:
        return True
    return False


def is_magnet(url: str):
    magnet = re.findall(MAGNET_REGEX, url)
    if magnet:
        return True
    return False


def Human_size(num, suffix='B'):
    num = int(num)
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)




# For folder upload
def listdir(mypath):
    files = []
    directory = []
    for (dirpath, dirnames, filenames) in os.walk(mypath):
        files.extend(mapPath(filenames))
        directory.extend(mapPath(dirnames))
        break
    return files ,directory

def mapPath(filenames):
  lists = []
  for file in filenames :
    dir = os.path.join("./",file)
    lists.append(dir)
  return lists

# print(f)
# print(d)


