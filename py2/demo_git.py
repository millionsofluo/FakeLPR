#!/usr/bin/env python
# -*- coding: utf8 -*-

##################################################################
# 2018.8.29
# millions_luo
# 
# 车牌检测的主程序
# 检测车牌，扩大车牌，校正车牌，识别车牌
# 
# 输入：测试图片路径
# 输出：车牌字符
# 
# 不要caffe，只用opencv来提取结果
# 还是分开一个一个的文件，要不然太乱了
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


import tools
import hyper_plate
import keypoint
import e2e_char


tool = tools.Tool()
h_plate = hyper_plate.HyperDetectPlate()
kp_warp = keypoint.KeyPoint()
e2e_mutest = e2e_char.MutestModel()


def get_all_result(src_img):
    # hyper的cascade方法定位车牌
    h_plate_list = h_plate.get_detect_plate(src_img)

    result_list = []
    for crop_plate_img,two_point in h_plate_list:
        start_time = time.clock()

        # 扩展然后关键点矫正
        warp_plate = kp_warp.get_warp_img(src_img,two_point)
        # 端到端的结果
        label_py,label_chs = e2e_mutest.get_plate_char(warp_plate)
        # print label_py,label_chs
        
        end_time = time.clock()
        fps = tool.cal_FPS(0,start_time,end_time)    

        result = [crop_plate_img,two_point,warp_plate,label_py,label_chs,fps]
        result_list.append(result)
    return result_list
            


# def main():
#     test_result_dir = 'test_result'
#     tool.mkdir_dir(test_result_dir)

#     #################### 测试图片路径 ########################
#     test_img_path = '/home/ljgw/code/pr/car_plate_image/min'
#     ##########################################################
    
#     root,files = tool.read_folder(test_img_path)
#     for name in files:
#         if name[-4:] != '.jpg':
#             continue
#         img_path = root+'/'+name
#         print img_path
#         src_img = cv2.imread(img_path)
#         # hyper的cascade方法定位车牌
#         h_plate_list = h_plate.get_detect_plate(src_img)
#         draw = src_img.copy()
#         for crop_plate_img,two_point in h_plate_list:
#             plate_p1 = (two_point[0][0],two_point[0][1])
#             plate_p2 = (two_point[1][0],two_point[1][1])
#             cv2.rectangle(draw,plate_p1,plate_p2,(0,255,0),2) # 画粗定位的框

#             # 扩展然后关键点矫正
#             warp_plate = kp_warp.get_warp_img(src_img,two_point)

#             # 端到端的结果
#             label_py,label_chs = e2e_mutest.get_plate_char(warp_plate)
#             print label_py,label_chs
            
#             # 画结果
#             try:
#                 cv2.putText(draw,'m:'+label_py,(plate_p1[0],plate_p1[1]-20),
#                         cv2.FONT_HERSHEY_COMPLEX,1,(0, 255, 0),2)
#             except Exception as e:
#                 print e
#                 pass

#             cv2.imwrite(test_result_dir+'/'+name[:-4]+'_plate.jpg',draw)

#     pass


# if __name__ == '__main__':
#     start=time.clock()
#     ##################
#     main()
#     ##################
#     end=time.clock()
#     print('Runing time %s Seconds'%(end-start)) 

#define COLOR_GREEN cv::Scalar(0, 255, 0)
#define COLOR_RED cv::Scalar(0, 0, 255)
#define COLOR_YELLOW cv::Scalar(0,255,255)
#define COLOR_BLUE cv::Scalar(255,0,0)
#define COLOR_WHITE cv::Scalar(255,255,255)
#define COLOR_PURPLE cvScalar(160, 32, 240)
#define COLOR_BLACK cvScalar(0, 0, 0)