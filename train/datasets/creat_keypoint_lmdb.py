#!/usr/bin/env python
# -*- coding: utf8 -*-

##################################################################
# 2018.8.16
# millions_luo
# 
# 对于caffe的多标签分类
# 生成图片和标签两个lmdb文件
# 这个是针对关键点定位的
# 图片大小[90,30] 就是分成90类和30类
# 4个点，8个坐标
# 
# 输入：图片的路径和相应的db文件
# 输出：两个lmdb文件
#
#
#更新：
# 2018.8.23
# 随机摆放位置
# 
# 2018.8.30
# git更新
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

import os,sys
import time
import sqlite3
import cv2
import numpy as np
import os
import lmdb
from PIL import Image 
import numpy as np 
import random

# Make sure that caffe is on the python path:
caffe_root = '/data/sdk/caffe-ssd'
sys.path.insert(0, caffe_root + '/python')
import caffe


class MultiLabelLMDB(object):
    """docstring for MultiLabelLMDB"""
    def __init__(self):
        super(MultiLabelLMDB, self).__init__()
        
    def runCommand_creatVec(self):
        # os.system("echo \"Hello World 666\"")
        pass

    # '''获取文件的大小,结果保留两位小数，单位为MB'''
    def get_FileSize(self,filePath):
        # filePath = unicode(filePath,'utf-8')
        fsize = os.path.getsize(filePath)
        fsize = fsize/float(1024*1024)
        return round(fsize,2)

    def read_folder(self,file_dir):   
        for root, dirs, files in os.walk(file_dir):  
            # print(root) #当前目录路径  
            # print(dirs) #当前路径下所有子目录  
            # print(files) #当前路径下所有非目录子文件
            return files

    # 进度条
    def view_bar(self,num, total):
        rate = float(num) / total
        rate_num = int(rate * 100)
        # dis_num = float(rate * 100)
        r = '\r[%s%s]%d%% %s/%s' % ("#"*rate_num, " "*(100-rate_num),rate_num,num,total, )
        sys.stdout.write(r)
        sys.stdout.flush()

    def resize_point(self,line):
        # 你的源图片宽高
        # 可以读取图片来确定shape
        src_w = 748
        src_h = 280

        dst_w = 90
        dst_h = 30

        scale_x = float(dst_w)/float(src_w)
        scale_y = float(dst_h)/float(src_h)

        out_line = []
        for i in range(1,9,2):
            out_line.append(float(line[i]) * scale_x)
            out_line.append(float(line[i+1]) * scale_y)

        return out_line
        

    def writeTXT_from_db(self,db_path,img_path):
        # 读取db数据
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('select * from train')
            # print 'have:',cursor.fetchall()
            print 'db have data'
            datas=cursor.fetchall()
        except: 
            print 'db no label'
        conn.commit()
        conn.close()

        random.shuffle(datas) # 乱序

        # (u'guiiQZPUY5_20180808180523158.jpg', u'353.151346207', u'90.5151475668', 
        # u'844.801574707', u'101.94887352', u'329.807758808', u'221.861862183', 
        # u'829.031341553', u'232.441101074', u'0', u'0')
        
        outfile="keypoint_label.txt"
        file = open(outfile,"wb")
        print 'write label to',outfile
        for line in datas:
            # self.view_bar(datas.index(line),len(datas))
            file_name = line[0]

            if(os.path.exists(img_path+'/'+file_name)==0):
                print 'no file',file_name
                continue
            if(os.path.getsize(img_path+'/'+file_name)<=50):
                print 'file size 0:',file_name
                continue

            label = line[0]
            in_point = [line[0],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10]]
            resize_point = self.resize_point(in_point)
            for point in resize_point:
                label = label + ' ' + str(int(point))  
            # print label
            file.write(label +'\n')  
        file.close() 
        print 'write label done'
        

    # 参考 https://blog.csdn.net/u013010889/article/details/53098346
    def totwolmdb(self,path,pause):
        ####################pre-treatment############################
        #txt with labels eg. (0001.jpg 2 5)
        file_input=open('keypoint_label.txt','r')
        img_list=[]
        label1_list=[]
        label2_list=[]
        label3_list=[]
        label4_list=[]
        label5_list=[]
        label6_list=[]
        label7_list=[]
        label8_list=[]
        for line in file_input:
            content=line.strip() #去除指定字符
            content=content.split(' ') #以某字符来分割
            if(len(content)!=9):
                print 'lmdb:label error',line
                continue
            img_list.append(str(content[0]))
            label1_list.append(int(content[1]))
            label2_list.append(int(content[2]))
            label3_list.append(int(content[3]))
            label4_list.append(int(content[4]))
            label5_list.append(int(content[5]))
            label6_list.append(int(content[6]))
            label7_list.append(int(content[7]))
            label8_list.append(int(content[8]))
            del content
        file_input.close() 


        ####################train data(images)############################
        img_lmdb_path = 'lmdb/lmdb_keypoint_img_'+pause
        print 'creat',img_lmdb_path
        #注意一定要先删除之前生成的lmdb，因为lmdb会在之前的数据基础上新增数据，而不会先清空
        # os.system('rm -rf  ' + img_lmdb_path)
        in_db=lmdb.open(img_lmdb_path,map_size=int(1e12))
        with in_db.begin(write=True) as in_txn:
            for in_idx,in_ in enumerate(img_list):         
                im_file=path+'/'+in_
                im=Image.open(im_file)
                im = im.resize((90,30),Image.BILINEAR)#放缩图片，分类一般用
                # im = im.resize((272,72),Image.BILINEAR)
                #双线性BILINEAR，分割一般用最近邻NEAREST，**注意准备测试数据时一定要一致**
                im=np.array(im) # im: (w,h)RGB->(h,w,3)RGB
                im=im[:,:,::-1]#把im的RGB调整为BGR
                im=im.transpose((2,0,1))#把height*width*channel调整为channel*height*width
                im_dat=caffe.io.array_to_datum(im)
                in_txn.put('{:0>10d}'.format(in_idx),im_dat.SerializeToString())
                # self.view_bar(in_idx,len(img_list))
                print 'data train: [{}/{}] {}'.format(in_idx+1, len(img_list),in_)        
                del im_file, im, im_dat
        in_db.close()
        print 'train data(images) are done!'

        ######train data of label################    
        label_lmdb_path = 'lmdb/lmdb_keypoint_label_'+pause
        print 'creat',label_lmdb_path
        # os.system('rm -rf  ' + label_lmdb_path)
        in_db=lmdb.open(label_lmdb_path,map_size=int(1e12))
        with in_db.begin(write=True) as in_txn:
            for in_idx,in_ in enumerate(img_list):
                target_label=np.zeros((8,1,1))# 7种label
                target_label[0,0,0]=label1_list[in_idx]
                target_label[1,0,0]=label2_list[in_idx]
                target_label[2,0,0]=label3_list[in_idx]
                target_label[3,0,0]=label4_list[in_idx]
                target_label[4,0,0]=label5_list[in_idx]
                target_label[5,0,0]=label6_list[in_idx]
                target_label[6,0,0]=label7_list[in_idx]
                target_label[7,0,0]=label8_list[in_idx]
                label_data=caffe.io.array_to_datum(target_label)
                in_txn.put('{:0>10d}'.format(in_idx),label_data.SerializeToString())
                # self.view_bar(in_idx,len(img_list))
                print 'label train: [{}/{}] {}'.format(in_idx+1, len(img_list),in_)
                del target_label, label_data
        in_db.close()
        print 'train labels are done!'

    def get_lmdb(self,db_path,img_path,pause):
        self.writeTXT_from_db(db_path,img_path)
        self.totwolmdb(img_path,pause)


def main():
    mltwo = MultiLabelLMDB()

    img_path = 'keypoint_train_data/data'
    db_path = 'keypoint_train_data/plate.db'
    mltwo.get_lmdb(db_path,img_path,'train')

    img_path = 'keypoint_test_data/data'
    db_path = 'keypoint_test_data/plate.db'
    mltwo.get_lmdb(db_path,img_path,'test')


if __name__ == '__main__':
    start=time.clock()
    ##################
    main()
    ##################
    end=time.clock()
    print('Runing time %s Seconds'%(end-start)) 
