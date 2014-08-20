#!/usr/bin/python
# -*- coding: UTF-8 -*-  
# Description: utility to download subtitle and convert it to tradtional chinese
# 
#              step 1. play video with xmp player, which will download subtitle to directory
#                      "C:\Documents and Settings\All Users\Application Data\Thunder Network\XMP4\ProgramData\Subtitle\Online"
#              step 2 transcode the subtitle we download in step 1 into traditional Chinese
# Author: lancebai@gmial.com
#
import  os, sys, subprocess  
from os import listdir
import argparse
import threading
# from thread import start_new_thread
import time
import shutil



#####################
# const vars
#####################
xmp_exe = r'C:\Program Files\Thunder Network\Xmp\Program\XMP.exe'
subtitle_download_folder = r'C:\Documents and Settings\All Users\Application Data\Thunder Network\XMP4\ProgramData\Subtitle\Online'"\\"
#####################

class SubtitleDownloader:
    def __init__(self, video_name, download_timeout):
        print "base class init"
        self.video_name = video_name
        self.complete = False
        self.subtitle_filename = None
        self.download_timeout = download_timeout
    def prepare(self):
        #blow up the subtitle directory
        raise NotImplementedError("Subclass must implement abstract method")
    
    def download_subtitle(self):
        raise NotImplementedError("Subclass must implement abstract method")
    def get_downloaded_subtile(self):
        raise NotImplementedError("Subclass must implement abstract method")
    def finish(self):
        raise NotImplementedError("Subclass must implement abstract method")


# def xmpIsRunning():
#     import win32ui
#     # may need FindWindow("iTunes", None) or FindWindow(None, "iTunes")
#     # or something similar
#     if FindWindow("xmp", "xmp"):
#         print "Found an xmp window"
#         return True
#     return False   

class XmpSubtitleDownloader(SubtitleDownloader):
    def __init__(self, video_name, download_timeout=15):
        self.xmp_binary = xmp_exe
        self.video_name = video_name
        self.original_list = []
        # print self.original_list
        self.complete = False
        self.pooling_interval = 5
        self.subtitle_filename = None
        self.thread_handle = None
        self.download_timeout = download_timeout
 
    def prepare(self):
        from sys import platform as _platform
        if _platform != "win32":
            raise "not supported on non Windows platform" 
        #blow up the subtitle directory 
        if os.path.isdir(subtitle_download_folder):
            for subtitle_dir in os.listdir(subtitle_download_folder):
                shutil.rmtree(subtitle_download_folder+subtitle_dir)
           
    def __wait_till_subtile_downloaded(self):
        subtitle_list = self.original_list

        #compare the list
        time_lapsed = 0
        print "thread:__wait_till_subtile_downloaded"
        while cmp(subtitle_list, self.original_list) == 0 and time_lapsed < self.download_timeout :
            # print "xmp is running", xmpIsRunning()
            print "has been waiting for %d sec\n" %(time_lapsed,),
            time_lapsed += self.pooling_interval 
            time.sleep(self.pooling_interval)
            subtitle_list = os.listdir(subtitle_download_folder)

            # print cmp(subtitle_list, self.original_list)
        # print "subtitle has been downloaded", subtitle_list,  
        # TODO:fill subtitle_filename
        # print subtitle_list
        if subtitle_list:
            self.subtitle_filename = subtitle_download_folder+subtitle_list[0]
            self.subtitle_filename += "\\" 
            self.subtitle_filename += os.listdir(self.subtitle_filename)[0]


    def download_subtitle(self):
        subprocess.Popen([self.xmp_binary, self.video_name])
        print "before create thread"
        self.thread_handle = threading.Thread(target=self.__wait_till_subtile_downloaded)
        self.thread_handle.daemon = True
        self.thread_handle.start()
        print "thread started!"

    def get_downloaded_subtile(self):
        if self.subtitle_filename is None:
            self.thread_handle.join()
        return self.subtitle_filename
            
    #TODO: kill the xmp player
    def finish(self):
        print "killing xmp player proccess"
        subprocess.call([ "taskkill" ,"/IM", "XMP.exe", "/F" ])
        # raise NotImplementedError("not implemented yet")




def check_subtitle_folder():
    ret_list = os.listdir(subtitle_download_folder)
    if ret_list is not None:
        print ret_list



