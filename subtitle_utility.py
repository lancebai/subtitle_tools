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

def main() :
    print "main function"
    # play_video_with_xmp(test_video)
    xmp_downloader = XmpSubtitleDownloader(test_video)
    xmp_downloader.prepare()
    xmp_downloader.download_subtitle()
    downloaded_srt = xmp_downloader.get_downloaded_subtile()
    print "subtitle downloaded : ", downloaded_srt 
    # check_subtitle_folder()
    # fileName, fileExtension = os.path.splitext(downloaded_srt)
    tmp_file = splitext(basename(test_video))[0] + splitext(downloaded_srt)[1]
    copyfile(xmp_downloader.get_downloaded_subtile(), tmp_file)
    convertFile(tmp_file)
    print "done!"

if __name__ == "__main__":
    main()
    sys.exit(0)    