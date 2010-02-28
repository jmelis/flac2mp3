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
                params.extend(['--t'+val,self.metadata[key]])
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
    lame_opts = '-m s -q 2 -V 2 -b 128 -B 320'.split(' ')
    mp3 = target_mp3(flac)
    create_dirs(mp3)
    metadata = Metadata(flac).to_params()
    
    flac_process = Popen(['flac','-dc',flac],stdout=PIPE)
    lame_process = Popen(['lame'] + lame_opts + metadata + ['--add-id3v2','-',mp3],stdin=flac_process.stdout,stdout = PIPE)
    output = lame_process.communicate()[0]
        

origin = "/media/music/Music/Ahmad Jamal"
os.chdir(origin)
flacs = get_flacs(origin)
for flac in flacs:
    flac2mp3(flac)
