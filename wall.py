#!/usr/bin/python
import os, commands, httplib, urllib, sys, string, random, md5, time

#  **************************
#  **************************
#  ***                    ***
#  ***  BBSlink.net Wall  ***
#  ***                    ***
#  **************************
#  **************************
#  
#  PLEASE DO NOT DISTRIBUTE THIS FILE
#  ==================================
#  
#  Version 0.1.beta  13th December 2015
#  (C)2015 Christopher Taylor. All Rights Reserved.
#
#  Insert your system's BBSlink.net log in credentials between the "" below:

#  Mystic BBS Configuration:
#  Command: (D-) Exec door (no dropfile)
#     Data: /mystic/scripts/wall.py %# %U
#

host = "games.bbslink.net" # Server address, usually 'games.bbslink.net'
syscode = "" # Your system code
authcode = "" # Your system's authorisation code
schemecode = "" # Scheme code

if len(sys.argv) < 3:
    sys.exit(1)

userno = sys.argv[1]
username = sys.argv[2]

dg = "[0;40;30m"
red = "[0;40;31m"
gray = "[0;40;0m"
white = "[0;40;37m"

os.system("stty echo")
clear = lambda: os.system('clear')

def ShowWall():
    # Show splash
    clear()
    print red + "Reading the wall..."

    # Get ANSI text from BBSlink server
    conn = httplib.HTTPConnection(host, 80, timeout=5)
    conn.request("GET", "/wall.php?action=show")
    response = conn.getresponse()
    wall = response.read()
    conn.close

    # Display the wall
    clear()
    print wall

    return

def SendToServer(action, data):
    xkey = "".join([str(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)) for i in xrange(0,6)])
    scripttype = "PY"
    scriptver = "0.1.beta"

    conn = httplib.HTTPConnection(host, 80, timeout=5)
    conn.request("GET", "/token.php?key=" + xkey)
    response = conn.getresponse()
    token = response.read()
    conn.close

    m = md5.new()
    m.update(authcode + token)
    xauth = m.hexdigest()

    m = md5.new()
    m.update(schemecode+ token)
    xcode = m.hexdigest()

    headers = {"X-User": userno,
               "X-System": syscode,
               "X-Auth": xauth,
               "X-Code": xcode,
               "X-Key": xkey,
               "X-Token": token,
               "X-Type": scripttype,
               "X-Version": scriptver,
               "X-Data": data
    }
    conn = httplib.HTTPConnection(host, 80, timeout=5)
    conn.request("GET", "/wall.php?action=" + action + "&key=" + xkey, "", headers)
    response = conn.getresponse()
    out = response.read()
    conn.close

    return out

# Show the wall!
ShowWall()

# Ask user if they want to write to the wall themselves
yes = set(['yes','y', 'ye'])
no = set(['no','n'])
choice = raw_input(white + "Write on the wall [Y/n]? ").lower()

if choice in no:
    sys.exit(0)
elif choice in yes:
    clear()
else:
    sys.exit(0)

print red + "What's on your mind, " + username + "? (max 64 characters)"
wallmsg = raw_input()

if len(wallmsg) > 5:
    f = SendToServer("newuser", username);
    postresult = SendToServer("post", wallmsg)
    
    # Check result of post attempt
    if postresult == "*post":
        # Successful
        print "Post successful!"
    elif postresult == "*int":
        # Last post < 10 minutes ago
        print "Sorry, you have to wait 10 minutes between posts."
        time.sleep(3)
        sys.exit()
    elif postresult == "*inval":
        # Post contained > 64 characters
        print "Your post contained too many characters (max length 64 chars)."
        time.sleep(3)
        sys.exit()
    else:
        # Post failed, unknown reason
        print "\nPost failed :-("
        time.sleep(3)
        sys.exit()
else:
    print "Your post was too short!"
    time.sleep(3)
    sys.exit()

time.sleep(0.70)
clear()
ShowWall()

raw_input("[0;40;37mPress [1;30m[[37mEnter[30m][0m to continue.")
