#!/usr/bin/python
import sys, os
from subprocess import Popen, PIPE

class Metadata:
    def __init__(self,flac):
        self.metadata = self.get_flac_metadata(flac)

    def to_dict(self):
        return self.metadata

    def to_params(self):
        params = list()
        dict_params = {
                'year':'y',
                'artist':'a',
                'comment':'c',
                'album':'l',
                'genre':'g',
                'tracknum':'n',
                'date':'y',
                'album artist':'a'
                }
        for key, val in dict_params.items():
            if key in self.metadata:
                params.extend(['--t'+val,"'%s'" % (self.metadata[key],)])
        return params

    def get_flac_metadata(self,flac):
        metadata = dict()
        command = 'metaflac --export-tags-to=-'.split(' ')
        output = Popen(command + [flac], stdout=PIPE).communicate()[0]
        metadata_list = output.split('\n')
        for elem in metadata_list:
            if '=' in elem:
                data = elem.split('=')
                key = data[0].lower()
                metadata[key] = data[1].strip()
        return metadata

    
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
        os.makedirs(dir)

def flac2mp3(flac):
    mp3 = target_mp3(flac)
    create_dirs(mp3)
    print Metadata(flac).to_params()    

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

origin = "/media/music/Music/Ahmad Jamal"
os.chdir(origin)
flacs = get_flacs(origin)
for flac in flacs:
    flac2mp3(flac)
