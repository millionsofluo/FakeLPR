#!/usr/bin/python
# -*- coding: utf8 -*-

##################################################################
# 2018.8.29
# millions_luo
# 
# 工具
#
##################################################################

# ************** 葱官赐福，百无禁忌 *************
# ***********************************************
#  _______________#########_______________________
# ______________############_____________________
# ______________#############____________________
# _____________##__###########___________________
# ____________###__######_#####__________________
# ____________###_#######___####_________________
# ___________###__##########_####________________
# __________####__###########_####_______________
# ________#####___###########__#####_____________
# _______######___###_########___#####___________
# _______#####___###___########___######_________
# ______######___###__###########___######_______
# _____######___####_##############__######______
# ____#######__#####################_#######_____
# ____#######__##############################____
# ___#######__######_#################_#######___
# ___#######__######_######_#########___######___
# ___#######____##__######___######_____######___
# ___#######________######____#####_____#####____
# ____######________#####_____#####_____####_____
# _____#####________####______#####_____###______
# ______#####______;###________###______#________
# ________##_______####________####______________ 
# ***********************************************
# ***********************************************

import numpy as np  
import sys,os  
# import time
# import datetime
import shutil
import cv2
# import sqlite3
# import Image, ImageDraw, ImageFont
# from math import *
# import scipy.signal as signal
# import traceback

province_change = [
        [u"京",'jing'], [u"沪",'hu'], [u"津",'jin'], [u"渝",'yu'], [u"冀",'jii'], [u"晋",'jinn'], 
        [u"蒙",'meng'], [u"辽",'liao'], [u"吉",'ji'], [u"黑",'hei'], [u"苏",'su'], [u"浙",'zhe'], 
        [u"皖",'wan'],  [u"闽",'min'], [u"赣",'gann'], [u"鲁",'lu'], [u"豫",'yuu'], [u"鄂",'e'], 
        [u"湘",'xiang'], [u"粤",'yue'], [u"桂",'gui'], [u"琼",'qiong'], [u"川",'chuan'], [u"贵",'guii'], 
        [u"云",'yun'], [u"藏",'zang'],[u"陕",'shan'], [u"甘",'gan'], [u"青",'qing'], [u"宁",'ning'], 
        [u"新",'xin'] ]

class Tool(object):
    """docstring for Tool"""
    def __init__(self):
        super(Tool, self).__init__()
        self.all_fps = [0]

    def hpel_self(self):
        # for index,item in enumerate(('a','b','c')):
        #     print i,j
        #     0,a
        #     1,b
        #     2,c
        
        # ex_img = src_img[y1:y2,x1:x2]
        pass

    def get_now_time(self):
        time_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
        return time_str
              
    def read_folder(self,file_dir):   
        for root, dirs, files in os.walk(file_dir):  
            # print(root) #当前目录路径  
            # print(dirs) #当前路径下所有子目录  
            # print(files) #当前路径下所有非目录子文件
            return root,files

    # 计算fps的
    
    def cal_FPS(self,flag,start_time=0,end_time=0):
        # time_start=time.time()
        # out = net.forward()  
        # time_end=time.time()
    
        # 0 单个图片fps
        if flag == 0 and start_time != 0 and end_time != 0:
            time = end_time-start_time
            fps = float(1)/float(time)
            # print 'FPS:',fps
            self.all_fps.append(fps)
            return fps

        # 1  所有的平均fps
        if flag == 1:
            count = 0.0
            for fps in self.all_fps:
                count+=fps
            mean_fps = count/float(len(self.all_fps))
            return mean_fps

        return float(0)


    # 进度条
    def view_bar(self,num, total):
        # 因为需要计算，总数太多容易拖慢速度，10w以上
        rate = float(num) / total
        rate_num = int(rate * 100)
        r = '\r[%s%s]%d%% %s/%s' % ("#"*rate_num, " "*(100-rate_num),rate_num,num,total, )
        sys.stdout.write(r)
        sys.stdout.flush()

    # def read_text(self):
    #     text_file = 'img_list.txt'
    #     f = open(text_file, 'r')
    #     img_list = []
    #     for imgpath in f.readlines():
    #         imgpath = imgpath.split('\n')[0]
    #         img_list.append(imgpath)

    def mkdir_dir(self,path):
        # 处理：删除之前的
        try:
            os.mkdir(path)
            print 'mkdir',path
        except:
            print 'have',path,'dir'
            shutil.rmtree(path)
            os.mkdir(path)
            print 'remove and mkdir',path
            pass

    # 读中文路径图片
    def cv_imread_chs(self,file_path):
        cv_img = cv2.imdecode(np.fromfile(file_path,dtype=np.uint8),-1)
        return cv_img

    def py2chs_pre(self,py):
        for change in province_change:
            if py == change[1]:
                return change[0]
        return 'None'

    def chs2py_pre(self,py):
        for change in province_change:
            if py == change[0]:
                return change[1]
        return 'None'

    def chs2pingyin_plate(self,chs_label):
        try:
            for change in province_change:
                if(chs_label[0] == change[0]):
                    return change[1]+chs_label[1:]
        except:
            return 'None'

    def pingyin2chs_plate(self,py_label):
        try:
            for change in province_change:
                if(py_label[:-6] == change[1]):
                    return change[0]+py_label[-6:]
        except:
            return 'None'
# class Tool END 