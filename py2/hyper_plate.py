#!/usr/bin/env python
# -*- coding: utf8 -*-

##################################################################
# 2018.8.29
# millions_luo
# 
# hyper的车牌粗定位
# cascade检测调用
# 
# 输入：原图
# 输出：车牌区域的list
#
##################################################################

# ************** 葱官赐福，百无禁忌 *************
# ***********************************************
#  _______________#########______________________
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

import cv2


class HyperDetectPlate(object):
    """docstring for HyperDetectPlate"""
    def __init__(self):
        super(HyperDetectPlate, self).__init__()
        self.cascade_model_path = 'models/hyper_plate_cascade.xml'
        self.watch_cascade = cv2.CascadeClassifier(self.cascade_model_path)    

    # 防止截取图像越界，会报错
    def computeSafeRegion(self,shape,bounding_rect):
        top = bounding_rect[1] # y
        bottom  = bounding_rect[1] + bounding_rect[3] # y +  h
        left = bounding_rect[0] # x
        right =   bounding_rect[0] + bounding_rect[2] # x +  w
        min_top = 0
        max_bottom = shape[0]
        min_left = 0
        max_right = shape[1]
        if top < min_top:
            top = min_top
        if left < min_left:
            left = min_left
        if bottom > max_bottom:
            bottom = max_bottom
        if right > max_right:
            right = max_right
        return [left,top,right-left,bottom-top]

    # 截取image的rect部分
    def cropImage(self,image,rect):
        x, y, w, h = self.computeSafeRegion(image.shape,rect)
        return image[y:y+h,x:x+w]

    # 车牌粗定位，用的watch_cascade级联分类器，返回粗定位的车牌部分，list返回[crop_img,rect]
    def detectPlateRough(self,image_gray,resize_h = 720,en_scale =1.08 ,top_bottom_padding_rate = 0.05):
        if top_bottom_padding_rate>0.2:
            print("error:top_bottom_padding_rate > 0.2:",top_bottom_padding_rate)
            exit(1)
        height = image_gray.shape[0]
        padding =    int(height*top_bottom_padding_rate)
        scale = image_gray.shape[1]/float(image_gray.shape[0])
        image = cv2.resize(image_gray, (int(scale*resize_h), resize_h))
        image_color_cropped = image[padding:resize_h-padding,0:image_gray.shape[1]]
        image_gray = cv2.cvtColor(image_color_cropped,cv2.COLOR_RGB2GRAY)
        watches = self.watch_cascade.detectMultiScale(image_gray, en_scale, 2, minSize=(36, 9),maxSize=(36*40, 9*40))
        cropped_images = []
        for (x, y, w, h) in watches:
            x -= w * 0.14
            w += w * 0.28
            y -= h * 0.15
            h += h * 0.3
            cropped = self.cropImage(image_color_cropped, (int(x), int(y), int(w), int(h)))
            cropped_images.append([cropped,[x, y+padding, w, h]])
        return cropped_images

    # 总执行的是这个函数
    def get_detect_plate(self,all_img):
        # 车牌粗定位
        images = self.detectPlateRough(all_img,all_img.shape[0],top_bottom_padding_rate=0.1)
        
        all_plate_list = []
        for j,plate in enumerate(images):
            plate, rect  = plate
            p1 = [int(rect[0]),int(rect[1])]
            p2 = [int(rect[0])+int(rect[2]),int(rect[1])+int(rect[3])]
            all_plate_list.append([plate, [p1,p2]])

        return all_plate_list
# class HyperDetectPlate END 
   
