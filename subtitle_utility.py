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
    parser.add_argument("-t", "--timeout", help="waiting timeout",
                        type=int)
    args = parser.parse_args()
    if args.dir[-1] is not os.path.sep:
       args.dir +=  os.path.sep 
    return args.dir, args.timeout



def download_subtitles_in_dir(dir_name, timeout):
    try:
        file_list = os.listdir(dir_name)
        for video_filename in file_list:
            # print "ext:", splitext(video_filename)[1]
            if splitext(video_filename)[1] in [".mkv",".avi"]:
                if os.path.isfile(dir_name+splitext(video_filename)[0]+".ass") or os.path.isfile(dir_name+splitext(video_filename)[0]+".srt") \
                or os.path.isfile(dir_name+splitext(video_filename)[0]+".ssa"):
                    print "subtitle exist already, skip"
                else:
                    print "going to download subtitle:", dir_name+video_filename      
                    download_subtitle(dir_name+video_filename, timeout) 
    except IOError:
        print "failed to open directory", dir_name, 
    
def download_subtitle(video_filename, timeout):
    xmp_downloader = XmpSubtitleDownloader(video_filename, timeout)
    xmp_downloader.prepare()
    xmp_downloader.download_subtitle()
    downloaded_srt = xmp_downloader.get_downloaded_subtile()
    # only carry on when subtitle has been downloaded!
    if downloaded_srt is not None :
        print "subtitle downloaded : ", downloaded_srt 
        # check_subtitle_folder()
        # fileName, fileExtension = os.path.splitext(downloaded_srt)
        tmp_file = splitext(basename(video_filename))[0] + splitext(downloaded_srt)[1]
        tmp_file = os.path.dirname(os.path.realpath(video_filename))+ os.path.sep + tmp_file
        copyfile(xmp_downloader.get_downloaded_subtile(), tmp_file)
        xmp_downloader.finish()
        print "going to conver", tmp_file
        convertFile(tmp_file)
        


def main() :
    print "main function"
    # download_subtitle(test_video)
    # download_subtitles_in_dir("c:\\test_dvd\\")
    args = parse_dir()
    print args
    if args[1] is None:
        timeout = 15
    else:
        timeout = args[1]
    download_subtitles_in_dir(args[0], timeout)
    print "done!"

if __name__ == "__main__":
    main()
    sys.exit(0)    