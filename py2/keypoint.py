#!/usr/bin/env python
# -*- coding: utf8 -*-

##################################################################
# 2018.8.29
# millions_luo
# 
# 多标签做keypoint定位的调用程序
# 粗定位车牌进来，扩展后检测四个角点
# 然后透视变换出车牌
# 
# 输入：原图，粗定位坐标
# 输出：矫正后的车牌
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

class KeyPoint(object):
    """docstring for KeyPoint"""
    def __init__(self):
        super(KeyPoint, self).__init__()
        self.net_w = 90
        self.net_h = 30
        # mutest 
        self.deploy_net_file = 'models/keypoint_deploy.prototxt'
        self.caffe_model = 'models/keypoint.caffemodel'
        if not os.path.exists(self.caffe_model):
            print "KeyPoint caffemodel does not exist"
            print self.caffe_model
            exit()
        #加载model和deploy
        # self.net = caffe.Net(self.deploy_net_file, self.caffe_model, caffe.TEST)
        self.kp_net = cv2.dnn.readNetFromCaffe(self.deploy_net_file, self.caffe_model)


    def opencv34_test(self,ex_plate):
        ex_plate = cv2.cvtColor(ex_plate, cv2.COLOR_BGR2RGB)
        inputBlob = cv2.dnn.blobFromImage(ex_plate,1,(90, 30),(104, 117, 123))
        self.kp_net.setInput(inputBlob)

        # 取出prob层结果
        result_point = []
        for i in range(1,9,2):
            probx = self.kp_net.forward('prob_'+str(i))
            proby = self.kp_net.forward('prob_'+str(i+1))
            result_point.append([probx.argmax(),proby.argmax()])
        return result_point

    def scale_point(self,img,points):
        dh,dw,ch = img.shape  # (280, 1122, 3)
        scale_y = float(dh)/float(self.net_h)
        scale_x = float(dw)/float(self.net_w)
        result_point = []
        # 4个点变比例
        for x, y in points:
            result_point.append([int(x*scale_x), int(y*scale_y)])
        return result_point


    def draw_point(self,img,points,color):
        # 4个点直接画
        for x, y in points:
            cv2.circle(img, (int(x), int(y)), 5, color, -1)
        return img


    def warp(self,star_points,src_img):

        height = 35
        width = 110 

        pts1 = np.float32([star_points[0],star_points[1],star_points[2],star_points[3]])
        pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])  
        M = cv2.getPerspectiveTransform(pts1,pts2)  
        dst = cv2.warpPerspective(src_img,M,(width,height))  

        return dst


    def get_warp_img(self,src_img,two_point):
        # 先扩展图片
        x_scale = 4  # 扩展宽的1/4
        y_scale = 2  # 扩展高的1/2
        ew = (two_point[1][0]-two_point[0][0])/x_scale
        eh = (two_point[1][1]-two_point[0][1])/y_scale
        ep1 = [two_point[0][0]-ew,two_point[0][1]-eh]
        ep2 = [two_point[1][0]+ew,two_point[1][1]+eh]

        # 防止越界
        if ep1[0]<0:
            ep1[0] = 0
        if ep1[1]<0:
            ep1[1] = 0
        if ep2[0]>src_img.shape[1]:
            ep2[0] = src_img.shape[1]
        if ep2[1]>src_img.shape[0]:
            ep2[1] = src_img.shape[0]
        ex_img = src_img[ep1[1]:ep2[1],ep1[0]:ep2[0]]
        
        result_point = self.opencv34_test(ex_img)
        result_point = self.scale_point(ex_img,result_point)
        self.draw_point(ex_img,result_point,(0,255,0))
        # cv2.imwrite('test_result/crop_plate.jpg',ex_img)

        res_img = self.warp(result_point,ex_img)
        # cv2.imwrite('test_result/warp_plate.jpg',res_img)
        return res_img
# class KeyPoint END 

