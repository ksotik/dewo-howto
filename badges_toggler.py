import subprocess
import os
import pathlib
import time
import sys

path = pathlib.Path(__file__).parent.absolute()

f = open('%s/appslist.txt' % path, 'r')
apps = f.readlines()

def toggle_badge(appid, state):
#    print('/usr/local/bin/python3 %s/ncprefs.py --set-badge-icon %s %s' % (path, state, appid))
    os.system('/usr/local/bin/python3 %s/ncprefs.py --set-badge-icon %s %s' % (path, state, appid))

res = subprocess.check_output('defaults read ~/Library/Preferences/ByHost/com.apple.notificationcenterui.plist', shell=True, text=True)
#print(res)
dnd = False
if 'dndEnd' in res or 'doNotDisturb = 1' in res:
#    print('dnd enabled, hide badges')
    dnd = True
else:
#    print('dnd disabled, show badges')
    dnd = False

statefile = '%s/%s.last' % (path, 'disable' if dnd else 'enable')
if os.path.isfile(statefile):
    sys.exit()
else:
    os.system('touch %s' % statefile)
statefile = '%s/%s.last' % (path, 'disable' if not dnd else 'enable')
try:
    os.remove(statefile)
except:
    pass

for app in apps:
    app = app.strip()
    if app:
        toggle_badge(app, 'disable' if dnd else 'enable')
        time.sleep(3)
os.system('killall NotificationCenter')
