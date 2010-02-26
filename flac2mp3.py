#!/usr/bin/python

import os, subprocess

import os

    
def append_list(arg, directory, files):
    for file in files:
        if file[-4:] == 'flac':
            arg.append(os.path.join(directory, file))

def get_flacs(origin):
    flacs=list()
    os.path.walk('.', append_list, flacs)
    return flacs

def target_mp3(flac):
    return 'mp3'+flac[1:-4]+'mp3'
    
def create_dirs(file):
    dir = os.path.dirname(file)
    if not os.path.isdir(dir):
        print "creating dir " + os.path.abspath(dir)
        os.makedirs(dir)

def flac2mp3(flac):
    mp3 = target_mp3(flac)
    create_dirs(mp3)

    #flac_command = "flac -d "
    #lame_command = 'lame --ta "Mozart" --tl "Requiem" --tg "Classical" ' # change these settings to suit your needs
    #count =+ 1
    #
    #filename_wav = file_name[:-4] + "wav"
    #filename_mp3 = file_name[:-4] + "mp3"
    #
    #flac_command = flac_command + '"' + file_name + '"'
    #lame_command = lame_command + ' "' + filename_wav + '" "' + filename_mp3 + '"'
    #
    #print "[X] " + flac_command
    #print "[X] " + lame_command
    #
    #print "[X] Flac Deflating: " + file_name + "..."
    #os.popen(flac_command)
    #print "[X] Converting to Mp3: " + filename_wav + "..."
    #os.popen(lame_command)
    #os.remove(filename_wav)
    #print "[X] Finished: " + filename_mp3

origin = "/Users/jmelis/borrar/music"
os.chdir(origin)
flacs = get_flacs(origin)
for flac in flacs:
    flac2mp3(flac)
