#!/usr/bin/python
# -*- coding: UTF-8 -*-  
# Description: utility to download subtitle and convert it to tradtional chinese
# 
#              step 1. play video with xmp player, which will download subtitle to directory
#                      "C:\Documents and Settings\All Users\Application Data\Thunder Network\XMP4\ProgramData\Subtitle\Online"
#              step 2 transcode the subtitle we download in step 1 into traditional Chinese
# Author: lancebai@gmial.com
#

import os
from os.path import basename, splitext 
from subtitle_downloader import *
from shutil import copyfile 
from g2butf8 import convertFile

test_video = r'c:\dvd\Da.Vincis.Demons.S01E08.720p.HDTV.x264-EVOLVE.mkv'

def parse_dir():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", help="file containing video clips",
                        type=str)
    args = parser.parse_args()
    return args.dir



def download_subtitle_in_dir(dir_name):
    try:
        file_list = os.listdir(dir_name)
        for video_filename in file_list:
            download_subtitle(dir_name+video_filename) 
    except IOError:
        print "failed to open directory", dir_name, 
    
def download_subtitle(video_filename):
    xmp_downloader = XmpSubtitleDownloader(video_filename)
    xmp_downloader.prepare()
    xmp_downloader.download_subtitle()
    downloaded_srt = xmp_downloader.get_downloaded_subtile()
    print "subtitle downloaded : ", downloaded_srt 
    # check_subtitle_folder()
    # fileName, fileExtension = os.path.splitext(downloaded_srt)
    tmp_file = splitext(basename(video_filename))[0] + splitext(downloaded_srt)[1]
    copyfile(xmp_downloader.get_downloaded_subtile(), os.path.dirname(os.path.realpath(video_filename))+ "//" +tmp_file)
    xmp_downloader.kill_xmp_player()
    convertFile(tmp_file)


def main() :
    print "main function"
    # download_subtitle(test_video)
    # download_subtitle_in_dir("c:\\test_dvd\\")
    download_subtitle_in_dir(parse_dir())
    print "done!"

if __name__ == "__main__":
    main()
    sys.exit(0)    