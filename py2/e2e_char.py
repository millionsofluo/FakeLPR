#!/usr/bin/env python
# -*- coding: utf8 -*-

##################################################################
# 2018.8.29
# millions_luo
# 
# 端到端识别车牌
# mutest识别模型调用
# 
# 输入：车牌区域图片
# 输出：车牌list
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
import cv2

import tools
tool = tools.Tool()

province_change = [
        [u"京",'jing'], [u"沪",'hu'], [u"津",'jin'], [u"渝",'yu'], [u"冀",'jii'], [u"晋",'jinn'], 
        [u"蒙",'meng'], [u"辽",'liao'], [u"吉",'ji'], [u"黑",'hei'], [u"苏",'su'], [u"浙",'zhe'], 
        [u"皖",'wan'],  [u"闽",'min'], [u"赣",'gann'], [u"鲁",'lu'], [u"豫",'yuu'], [u"鄂",'e'], 
        [u"湘",'xiang'], [u"粤",'yue'], [u"桂",'gui'], [u"琼",'qiong'], [u"川",'chuan'], [u"贵",'guii'], 
        [u"云",'yun'], [u"藏",'zang'],[u"陕",'shan'], [u"甘",'gan'], [u"青",'qing'], [u"宁",'ning'], 
        [u"新",'xin'] ]

province_char = ['jing', 'hu','jin','yu','jii','jinn','meng','liao','ji','hei','su','zhe','wan','min','gann','lu','yuu','e',
        'xiang','yue','gui','qiong','chuan','guii','yun','zang','shan','gan','qing','ning','xin']

city_char = [u"A", u"B", u"C", u"D", u"E", u"F", u"G", u"H", u"J", u"K", u"L", u"M", u"N", u"P", u"Q", u"R", u"S",
        u"T", u"U", u"V", u"W", u"X", u"Y", u"Z"]

label_char = [u"A", u"B", u"C", u"D", u"E", u"F", u"G", u"H", u"J", u"K", u"L", u"M", u"N", u"P", u"Q", u"R", u"S",
        u"T", u"U", u"V", u"W", u"X", u"Y", u"Z", u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9"]


class MutestModel(object):
    """docstring for MutestModel"""
    def __init__(self):
        super(MutestModel, self).__init__()
        # mutest 
        self.deploy_net_file= 'models/mutest_deploy.prototxt'  
        # self.caffe_model = 'models/mutest.caffemodel'  # 混了一些真实样本的模型
        self.caffe_model = 'models/e2e.caffemodel'

        if not os.path.exists(self.caffe_model):
            print("caffemodel does not exist")
            exit()

        self.mutest_net = cv2.dnn.readNetFromCaffe(self.deploy_net_file, self.caffe_model)
        # self.net = caffe.Net(self.deploy_net_file, self.caffe_model, caffe.TEST) #加载model和deploy

    def opencv34_test(self,plate_img):
        plate_img = cv2.cvtColor(plate_img, cv2.COLOR_BGR2RGB)
        inputBlob = cv2.dnn.blobFromImage(plate_img,1,(110, 35),(104, 117, 123))
        self.mutest_net.setInput(inputBlob)

        # 取出prob层结果
        result = []
        for i in range(1,8):
            prob = self.mutest_net.forward('prob_'+str(i))
            result.append(prob.argmax())
        return result


    def num2label(self,num):
        label_list = []
        label = ''
        label_list.append(province_char[num[0]])
        label_list.append(city_char[num[1]])
        label_list.append(label_char[num[2]])
        label_list.append(label_char[num[3]])
        label_list.append(label_char[num[4]])
        label_list.append(label_char[num[5]])
        label_list.append(label_char[num[6]])
        
        for item in label_list:
            label+=item
        label_py = label
        label_chs = tool.py2chs_pre(label[:-6])+label[-6:]
        return label_py,label_chs

    def get_plate_char(self,plate_img):
        prob_index_result = self.opencv34_test(plate_img)
        label_py,label_chs = self.num2label(prob_index_result)
        return label_py,label_chs

        # print prob_index_result
        # print label_list,label    
# class MutestModel END 