#!/bin/python
from os import listdir
from os.path import isfile, join
from random import choice

wp_path = '/home/arsenoks/wallpapers'

wps = [f for f in listdir(wp_path) if isfile(join(wp_path, f))]

wp = join(wp_path, choice(wps))

with open('/home/arsenoks/.config/hypr/hyprpaper.conf', 'wt') as f:
    f.writelines((
                     'splash = false\n',
                     f'preload = {wp}\n',
                     f'wallpaper = eDP-1, {wp}\n'
                 ))
