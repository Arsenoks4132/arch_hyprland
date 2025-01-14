#!/bin/python
from os import listdir
from os.path import isfile, join
from random import choice
from subprocess import run
from datetime import datetime

wp_path = '/home/arsenoks/wallpapers'

wps = [f for f in listdir(wp_path) if isfile(join(wp_path, f))]

wp = join(wp_path, choice(wps))
run(['hyprctl', 'hyprpaper', 'unload', 'all'])
run(['hyprctl', 'hyprpaper', 'preload', wp])
run(['hyprctl', 'hyprpaper', 'wallpaper', f'eDP-1, {wp}'])

# with open('/home/arsenoks/py_logs.txt', 'at') as f:
#     f.write(f'script start at {datetime.now()}\n')
    
