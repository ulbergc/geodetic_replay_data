#!/bin/python
import os
import argparse
from datetime import datetime
import pytz as timezone
import sys

# tanktime comes from the ShakeAlert testsuite repository
from tanktime import get_tank_start_end

##############################################################
# Based on code from Mike Hagerty:
#     https://github.com/mikehagerty/GFAST_playback_data
# and from ShakeAlert STP testsuite repository:
#     https://code.usgs.gov/EEW/testsuite
# Modified by Carl Ulberg, April 2021
##############################################################


tankplayer_bin = '/path/to/tankplayer'
tanksniff_exe = '/path/to/tanksniff'

def get_wave_file(tankplayer_file):
    '''
        Return the tankfile path from a tankplayer.d file
    '''
    ###########################################################
    # code modified from p_automate.py from STP, CWU 20210505 #
    ###########################################################
    try:
        fin = open(tankplayer_file, 'r')
    except IOError:
        print("Configuration file \"" + str(tankplayer_file) + "\" could not be opened.")
        sys.stdout.flush()
        return -1

    tank_file = ''
    for line in fin:
        if(len(line.strip()) == 0):
            continue
        if(line.strip()[0] == '#'):
            continue
        if("WaveFile " in line):
            try:
                tank_file = line.split('#')[0].strip().split()[1]
            except Exception as e:
                print("Exception generating tank_file name: " + str(e))
                sys.stdout.flush()
                continue
            # end try block
        # end if ("Wavefile " in line)
    # end for loop (line in fin)
    fin.close()

    return tank_file

def get_offset_time(seismic_tankplayer_file, geodetic_tankplayer_file):
    '''
        Return the seismic - geodetic tankplayer start times (s)
    '''
    seismic_wave_file = get_wave_file(seismic_tankplayer_file)
    geodetic_wave_file = get_wave_file(geodetic_tankplayer_file)
    seismic_starttime, seismic_endtime = (
        get_tank_start_end(seismic_wave_file, '', tanksniff_exe, "last", dbug=0)
    )
    geodetic_starttime, geodetic_endtime = (
        get_tank_start_end(geodetic_wave_file, '', tanksniff_exe, "last", dbug=0)
    )
    # print("Seismic = {}, {}".format(seismic_starttime, seismic_endtime))
    # print("Geodetic = {}, {}".format(geodetic_starttime, geodetic_endtime))

    return seismic_starttime - geodetic_starttime

def main():
    '''
        Simple script to start seismic and geodetic tankplayer to begin releasing 
        tankplayer packets onto the wave_ring
    '''
    parser = argparse.ArgumentParser(description="Playback tankfiles")
    parser.add_argument('event_name', 
                        help='Name of event')
    parser.add_argument('--offset_time', type=float, default=None, 
                        help=('Seismic - geodetic tankplayer start times (s). Will be'
                              + ' calculated automatically from event cfg by default'))
    options = parser.parse_args()

    event_name = options.event_name
    offset_time = options.offset_time

    os.environ['EW_PARAMS'] = '/path/to/ew/params'
    os.environ['EW_INSTALLATION'] = 'INST_UNKNOWN'
    os.environ['EW_LOG'] = '/path/to/ew/logs'
    log_dir = '/path/to/playback/logs'

    params_dir = os.environ.get('EW_PARAMS')
    cwd = os.getcwd()
    if params_dir is None:
        print("You must source an EW env before running this!")
        exit(2)

    seismic_tankplayer_file  = os.path.join(params_dir, "inp/tankplayer.d.seismic")
    geodetic_tankplayer_file = os.path.join(params_dir, "inp/tankplayer.d.geodetic")

    if offset_time is None:
        offset_time = get_offset_time(seismic_tankplayer_file, geodetic_tankplayer_file)

    print("Doing {} with offset {}s and files {} and {}".format(event_name, 
          offset_time, seismic_tankplayer_file, geodetic_tankplayer_file))

    thread_seismic = myThread(1, "Thread-seismic", 0, seismic_tankplayer_file)
    thread_geodetic = myThread(2, "Thread-geodetic", 0, geodetic_tankplayer_file)

    seismic_start = "0"
    geodetic_start = "0"

    # offset_time is seismic - geodetic start time
    if offset_time > 0:
        '''If positive, geodetic should start first'''
        geodetic_start = "%s" % datetime.now(tz=timezone.utc)
        print("[%s] Start the geodetic tankplayer" % geodetic_start)
        thread_geodetic.start()

        time.sleep(abs(offset_time))

        seismic_start = "%s" % datetime.now(tz=timezone.utc)
        print("[%s] Start the seismic tankplayer" % seismic_start)
        thread_seismic.start()
    else:
        '''Seismic thread should start first'''
        seismic_start = "%s" % datetime.now(tz=timezone.utc)
        print("[%s] Start the seismic tankplayer" % seismic_start)
        thread_seismic.start()

        time.sleep(abs(offset_time))

        geodetic_start = "%s" % datetime.now(tz=timezone.utc)
        print("[%s] Start the geodetic tankplayer" % geodetic_start)
        thread_geodetic.start()

    # Write start times to file
    fid = open(os.path.join(log_dir, "tank_start.log"), "w")
    fid.write("Seismic start: %s\n" % seismic_start)
    fid.write("Geodetic start: %s\n" % geodetic_start)
    fid.close()

    return

import threading
import time

exitFlag = 0

class myThread (threading.Thread):
   def __init__(self, threadID, name, counter, tankfile):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
      self.tankfile = tankfile

   def run(self):
      print("*** Starting Python thread:" + self.name)
      os.system('%s %s' % (tankplayer_bin,self.tankfile))

if __name__ == "__main__":
    main()
