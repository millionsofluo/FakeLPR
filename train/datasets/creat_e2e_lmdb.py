#!/usr/bin/env python
# -*- coding: utf8 -*-

##################################################################
# 2018.7.25
# millions_luo
# 
# 对于车牌端到端识别的caffe的多标签分类
# 生成图片和标签两个lmdb文件
# 
# 输入：图片的路径和相应的db文件
# 输出：两个lmdb文件
#
# 更新
# 2018.7.25  
# class打包
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


province_change = [
        [u"京",'jing'], [u"沪",'hu'], [u"津",'jin'], [u"渝",'yu'], [u"冀",'jii'], [u"晋",'jinn'], 
        [u"蒙",'meng'], [u"辽",'liao'], [u"吉",'ji'], [u"黑",'hei'], [u"苏",'su'], [u"浙",'zhe'], 
        [u"皖",'wan'],  [u"闽",'min'], [u"赣",'gann'], [u"鲁",'lu'], [u"豫",'yuu'], [u"鄂",'e'], 
        [u"湘",'xiang'], [u"粤",'yue'], [u"桂",'gui'], [u"琼",'qiong'], [u"川",'chuan'], [u"贵",'guii'], 
        [u"云",'yun'], [u"藏",'zang'],[u"陕",'shan'], [u"甘",'gan'], [u"青",'qing'], [u"宁",'ning'], 
        [u"新",'xin'] ]
        
all_label = ['jing', 'hu','jin','yu','jii','jinn','meng','liao','ji','hei','su','zhe','wan','min','gann','lu','yuu','e',
        'xiang','yue','gui','qiong','chuan','guii','yun','zang','shan','gan','qing','ning','xin',
        u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9",
        u"A", u"B", u"C", u"D", u"E", u"F", u"G", u"H", u"J", u"K", u"L", u"M", u"N", u"P", u"Q", u"R", u"S",
        u"T", u"U", u"V", u"W", u"X", u"Y", u"Z"]


province_char = ['jing', 'hu','jin','yu','jii','jinn','meng','liao','ji','hei','su','zhe','wan','min','gann','lu','yuu','e',
        'xiang','yue','gui','qiong','chuan','guii','yun','zang','shan','gan','qing','ning','xin']

city_char = [u"A", u"B", u"C", u"D", u"E", u"F", u"G", u"H", u"J", u"K", u"L", u"M", u"N", u"P", u"Q", u"R", u"S",
        u"T", u"U", u"V", u"W", u"X", u"Y", u"Z"]

label_char = [u"A", u"B", u"C", u"D", u"E", u"F", u"G", u"H", u"J", u"K", u"L", u"M", u"N", u"P", u"Q", u"R", u"S",
        u"T", u"U", u"V", u"W", u"X", u"Y", u"Z", u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9"]


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

    def label2num(self,label):
        # eg: label = 'shanERT1SJ'
        pre_city = label[:-5]
        pre = pre_city[:-1]
        city = pre_city[-1:]
        nums = label[-5:]
        # print label
        # print pre,city,nums
        return_label = []
        if(pre in province_char):
            return_label.append(str(province_char.index(pre)))
        if(city in city_char):
            return_label.append(str(city_char.index(city))) 
        for char in nums:
            if(char in label_char):
                return_label.append(str(label_char.index(char)))
        return return_label


    def writeTXT_from_db(self,db_path,img_path):
        # 读取db数据
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('select * from train')
            # print 'have:',cursor.fetchall()
            print 'have data'
            datas=cursor.fetchall()
        except: 
            print 'no label'
        conn.commit()
        conn.close()

        random.shuffle(datas) # 乱序

        # 写入label
        # [u'dc92b6945992949e_yunA565KW.jpg', u'yunA565KW', u'\u4e91A565KW', 'None', 'None']
        outfile="e2e_label.txt"
        file = open(outfile,"wb")
        for item in datas:
            file_name = item[0]
            if(os.path.exists(img_path+'/'+file_name)==0):
                print 'no file',file_name
                continue
            if(os.path.getsize(img_path+'/'+file_name)<=50):
                print 'file size 0:',file_name
                continue
            label_list = self.label2num(item[1])
            for l in label_list:
                l = ' '+l
                file_name += l
            file.write(file_name +'\n')  
        file.close() 
        print 'write label done'

    def totwolmdb(self,path,pause):
        ####################pre-treatment############################
        #txt with labels eg. (0001.jpg 2 5)
        file_input=open('e2e_label.txt','r')
        img_list=[]
        label1_list=[]
        label2_list=[]
        label3_list=[]
        label4_list=[]
        label5_list=[]
        label6_list=[]
        label7_list=[]
        for line in file_input:
            content=line.strip() #去除指定字符
            content=content.split(' ') #以某字符来分割
            if(len(content)!=8):
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
            del content
        file_input.close() 


        ####################train data(images)############################
        img_lmdb_path = 'lmdb/lmdb_e2e_img_'+pause
        #注意一定要先删除之前生成的lmdb，因为lmdb会在之前的数据基础上新增数据，而不会先清空
        # os.system('rm -rf  ' + img_lmdb_path)
        in_db=lmdb.open(img_lmdb_path,map_size=int(1e12))
        with in_db.begin(write=True) as in_txn:
            for in_idx,in_ in enumerate(img_list):         
                im_file=path+'/'+in_
                im=Image.open(im_file)
                im = im.resize((110,35),Image.BILINEAR)#放缩图片，分类一般用
                # im = im.resize((272,72),Image.BILINEAR)
                #双线性BILINEAR，分割一般用最近邻NEAREST，**注意准备测试数据时一定要一致**
                im=np.array(im) # im: (w,h)RGB->(h,w,3)RGB
                im=im[:,:,::-1]#把im的RGB调整为BGR
                im=im.transpose((2,0,1))#把height*width*channel调整为channel*height*width
                im_dat=caffe.io.array_to_datum(im)
                in_txn.put('{:0>10d}'.format(in_idx),im_dat.SerializeToString())   
                print 'data train: [{}/{}] {}'.format(in_idx+1, len(img_list),in_)        
                del im_file, im, im_dat
        in_db.close()
        print 'train data(images) are done!'

        ######train data of label################    
        label_lmdb_path = 'lmdb/lmdb_e2e_label_'+pause
        # os.system('rm -rf  ' + label_lmdb_path)
        in_db=lmdb.open(label_lmdb_path,map_size=int(1e12))
        with in_db.begin(write=True) as in_txn:
            for in_idx,in_ in enumerate(img_list):
                target_label=np.zeros((7,1,1))# 7种label
                target_label[0,0,0]=label1_list[in_idx]
                target_label[1,0,0]=label2_list[in_idx]
                target_label[2,0,0]=label3_list[in_idx]
                target_label[3,0,0]=label4_list[in_idx]
                target_label[4,0,0]=label5_list[in_idx]
                target_label[5,0,0]=label6_list[in_idx]
                target_label[6,0,0]=label7_list[in_idx]
                label_data=caffe.io.array_to_datum(target_label)
                in_txn.put('{:0>10d}'.format(in_idx),label_data.SerializeToString())
                print 'label train: [{}/{}] {}'.format(in_idx+1, len(img_list),in_)
                del target_label, label_data    
        in_db.close()
        print 'train labels are done!'

    def get_lmdb(self,db_path,img_path,pause):
        self.writeTXT_from_db(db_path,img_path)
        self.totwolmdb(img_path,pause)


def main():
    mltwo = MultiLabelLMDB()

    img_path = 'e2e_train_data/data'
    db_path = 'keypoint_train_data/plate.db'
    mltwo.get_lmdb(db_path,img_path,'train')

    img_path = 'e2e_test_data/data'
    db_path = 'keypoint_test_data/plate.db'
    mltwo.get_lmdb(db_path,img_path,'test')


if __name__ == '__main__':
    start=time.clock()
    ##################
    main()
    ##################
    end=time.clock()
    print('Runing time %s Seconds'%(end-start)) 
