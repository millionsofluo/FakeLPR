#!/usr/bin/env python
# -*- coding: utf8 -*-

##################################################################
# 2018.8.30
# millions_luo
# 
# 车牌检测的主程序
# 
# 步骤：检测车牌，扩大车牌，校正车牌，识别车牌
# 
# 输入：测试图片路径
# 输出：车牌字符
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

import time
import cv2


from py2 import tools
from py2 import demo_git


tool = tools.Tool()


def main():
    test_result_dir = 'test_result'
    tool.mkdir_dir(test_result_dir)

    #################### 测试图片路径 ########################
    test_img_path = 'test_images/real_all_image'
    # test_img_path = 'test_images/real_crop_image'
    # test_img_path = 'test_images/creat_image'
    # test_img_path = '你的图片文件夹'
    ##########################################################
    
    root,files = tool.read_folder(test_img_path)
    for name in files:
        # 读jpg图片
        if name[-4:] != '.jpg':
            continue
        img_path = root+'/'+name
        print img_path
        src_img = cv2.imread(img_path)
        result_list = demo_git.get_all_result(src_img)
        draw = src_img.copy()
        for index,line in enumerate(result_list):
            crop_plate_img,two_point,warp_plate,label_py,label_chs,fps = line
            # [粗定位车牌图片,粗定位的两个点(左上右下),校正后车牌图片,拼音车牌结果,中文车牌结果,fps]
            # print 'FPS:',fps
            
            # 分离出两点坐标
            plate_p1 = (two_point[0][0],two_point[0][1]) 
            plate_p2 = (two_point[1][0],two_point[1][1]) 

            # 存中间结果看看
            cv2.imwrite(test_result_dir+'/'+name[:-4]+'_b_'+str(index)+'_crop.jpg',crop_plate_img)  # 存粗定位结果
            cv2.imwrite(test_result_dir+'/'+name[:-4]+'_c_'+str(index)+'_warp_result_'+label_py+'.jpg',warp_plate)  # 存校正结果
            
            # 画结果
            try:
                cv2.rectangle(draw,plate_p1,plate_p2,(0,255,0),2) # 画粗定位的框
                cv2.putText(draw,label_py,(plate_p1[0],plate_p1[1]-20),
                        cv2.FONT_HERSHEY_COMPLEX,1,(0, 255, 0),2)
            except Exception as e:
                print e
                pass
        cv2.imwrite(test_result_dir+'/'+name[:-4]+'_a_result.jpg',draw)


if __name__ == '__main__':
    start=time.clock()
    ##################
    main()
    ##################
    end=time.clock()
    print('Runing time %s Seconds'%(end-start)) 

#define COLOR_GREEN cv::Scalar(0, 255, 0)
#define COLOR_RED cv::Scalar(0, 0, 255)
#define COLOR_YELLOW cv::Scalar(0,255,255)
#define COLOR_BLUE cv::Scalar(255,0,0)
#define COLOR_WHITE cv::Scalar(255,255,255)
#define COLOR_PURPLE cvScalar(160, 32, 240)
#define COLOR_BLACK cvScalar(0, 0, 0)