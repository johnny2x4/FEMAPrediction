 # Set the URL string to point to a specific data URL. Some generic examples are:
   #   https://servername/data/path/file
   #   https://servername/opendap/path/file[.format[?subset]]
   #   https://servername/daac-bin/OTF/HTTP_services.cgi?KEYWORD=value[&KEYWORD=value]
IMPORTNAME = 'NASA-DailyPercip.txt'
TIMEDELAY = 1
import time
import requests
f = open(IMPORTNAME, 'r')
for line in f:
    print(line)
    filename = line.split("data/", 1)
    filename =filename[1].replace("/", "_")
    print (filename)
    result = requests.get(line.strip())
    try:
        result.raise_for_status()
        g = open(filename,'wb')
        g.write(result.content)
        g.close()
        print('contents of URL written to '+filename)
    except:
        print('requests.get() returned an error code '+str(result.status_code))
    time.sleep(TIMEDELAY)
