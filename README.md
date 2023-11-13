## crt.sh

This python script makes it easy to quickly save and parse the output from https://crt.sh website.
 to be sent to tools like httpx!

Usage is pretty simple :

![alt text](https://raw.githubusercontent.com/lun3xcoder/crt.py/main/Screenshot/main.PNG)

Step 1:
```
git clone https://github.com/lun3xcoder/crt.py.git && cd crt.py/ 
```
Step 2:
```
python3 crt.py -h
```
Example :
```
python3 crt.py -d hackerone.com | httpx
```

This will write all of the enumerated subdomains to the specified output file and will be ready to be passed to other tools.


Happy hunting!
