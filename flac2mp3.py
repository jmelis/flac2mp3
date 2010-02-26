#!/usr/bin/python
from sys import exit, argv
import os

def parseDirectory(dir_name):
    if os.path.isdir(dir_name):
        os.chdir(dir_name) # cd into the directory
        files = os.listdir(dir_name)
        for f in files:
            if os.path.isfile(f): parseFile(f) # pass the file to the corresponding function
        print "Completed: " + dir_name

def parseFile(file_name):
    if file_name[-4:] == "flac":
        flac_command = "flac -d "
        lame_command = 'lame --ta "Mozart" --tl "Requiem" --tg "Classical" ' # change these settings to suit your needs
        count =+ 1
        
        filename_wav = file_name[:-4] + "wav"
        filename_mp3 = file_name[:-4] + "mp3"
        
        flac_command = flac_command + '"' + file_name + '"'
        lame_command = lame_command + ' "' + filename_wav + '" "' + filename_mp3 + '"'
        
        print "[X] " + flac_command
        print "[X] " + lame_command
        
        print "[X] Flac Deflating: " + file_name + "..."
        os.popen(flac_command)
        print "[X] Converting to Mp3: " + filename_wav + "..."
        os.popen(lame_command)
        os.remove(filename_wav)
        print "[X] Finished: " + filename_mp3

print "Dir: " + str(argv[1])
if os.path.isdir(argv[1]): parseDirectory(argv[1])
