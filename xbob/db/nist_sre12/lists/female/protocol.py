#!/usr/bin/env python

import xbob.db.verification.filelist

# 0/ The database to use
name = 'nist_sre_2012'
db = xbob.db.verification.filelist.Database('protocol_nist/')
protocol = 'female'

# 1/ Path and extension of wave files 
wav_input_dir = "/idiap/temp/ekhoury/NIST_DATA/WAV/"
wav_input_ext = ".sph"

