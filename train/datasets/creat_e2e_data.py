#!/usr/bin/python
# -*- coding: utf8 -*-

##################################################################
# 2018.7.25
# millions_luo
# 
# 生成训练数据样本
# 
# 更新
# 2018.8.30
# git上传更新
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
import time
import datetime
import shutil
import cv2
import sqlite3

class Tool(object):
    """docstring for Tool"""
    def __init__(self):
        super(Tool, self).__init__()

    def get_now_time(self):
        time_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
        return time_str
              
    def read_folder(self,file_dir):   
        for root, dirs, files in os.walk(file_dir):  
            # print(root) #当前目录路径  
            # print(dirs) #当前路径下所有子目录  
            # print(files) #当前路径下所有非目录子文件
            return root,files

    # 进度条
    def view_bar(self,num, total):
        rate = float(num) / total
        rate_num = int(rate * 100)
        # dis_num = float(rate * 100)
        r = '\r[%s%s]%d%% %s/%s' % ("#"*rate_num, " "*(100-rate_num),rate_num,num,total, )
        sys.stdout.write(r)
        sys.stdout.flush()

    def mkdir_dir(self,path):
        # 处理：删除之前的
        try:
            os.mkdir(path)
            print 'mkdir',path
        except:
            print 'have dir'
            shutil.rmtree(path)
            os.mkdir(path)
            print 'remove and mkdir',path
            pass

    def loadDB(self,dbname):
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()
        cursor.execute('select * from train')
        datas=cursor.fetchall()
        conn.commit()
        conn.close()
        return datas 
# class Tool END 


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


    def warp(self,star_points,src_img):

        height = 35
        width = 110 

        pts1 = np.float32([star_points[0],star_points[1],star_points[2],star_points[3]])
        pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])  
        M = cv2.getPerspectiveTransform(pts1,pts2)  
        dst = cv2.warpPerspective(src_img,M,(width,height))  

        return dst


    def get_warp_img(self,src_img):

        result_point = self.opencv34_test(src_img)
        result_point = self.scale_point(src_img,result_point)
        res_img = self.warp(result_point,src_img)
        return res_img


def deal(in_img_path,in_db_path,out_img_path):
    kp = KeyPoint()
    tool = Tool()

    datas = tool.loadDB(in_db_path)

    for line in datas:
        tool.view_bar(datas.index(line)+1,len(datas))
        src_img = cv2.imread(in_img_path+'/'+line[0])
        res_img = kp.get_warp_img(src_img)
        cv2.imwrite(out_img_path+'/'+line[0],res_img)
    print ' done'



def main():
    tool = Tool()
    

    # train
    out_img_path = 'e2e_train_data/data'
    in_img_path = 'keypoint_train_data/data'
    in_db_path = 'keypoint_train_data/plate.db'
    tool.mkdir_dir(out_img_path[:-5])
    tool.mkdir_dir(out_img_path)
    deal(in_img_path,in_db_path,out_img_path)

    # test
    out_img_path = 'e2e_test_data/data'
    in_img_path = 'keypoint_test_data/data'
    in_db_path = 'keypoint_test_data/plate.db'
    tool.mkdir_dir(out_img_path[:-5])
    tool.mkdir_dir(out_img_path)
    deal(in_img_path,in_db_path,out_img_path)



if __name__ == '__main__':
    start=time.clock()
    ##################
    main()
    ##################
    end=time.clock()
    print('Runing time %s Seconds'%(end-start)) 
