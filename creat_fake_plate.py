import numpy as np
import os
import sys
import time
import datetime
import shutil
import cv2
from PIL import Image, ImageDraw, ImageFont

import traceback
import random
from math import *

province_change = [
    ["京", "jing"],
    ["沪", "hu"],
    ["津", "jin"],
    ["渝", "yu"],
    ["冀", "jii"],
    ["晋", "jinn"],
    ["蒙", "meng"],
    ["辽", "liao"],
    ["吉", "ji"],
    ["黑", "hei"],
    ["苏", "su"],
    ["浙", "zhe"],
    ["皖", "wan"],
    ["闽", "min"],
    ["赣", "gann"],
    ["鲁", "lu"],
    ["豫", "yuu"],
    ["鄂", "e"],
    ["湘", "xiang"],
    ["粤", "yue"],
    ["桂", "gui"],
    ["琼", "qiong"],
    ["川", "chuan"],
    ["贵", "guii"],
    ["云", "yun"],
    ["藏", "zang"],
    ["陕", "shan"],
    ["甘", "gan"],
    ["青", "qing"],
    ["宁", "ning"],
    ["新", "xin"],
]


def mkdir_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def get_now_time():
    time_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    return time_str


class NoramlPlate:
    """docstring for NoramlPlate"""

    def __init__(self):
        super(NoramlPlate, self).__init__()
        # 字体我根据兰亭雅黑改过，主要改的是英文和数字，比较像
        self.font_path = "Font/plate_lantinghei_0_change2.ttf"

    def standard_line(self, img):
        # ssss = [(15,25),(60,115),
        #         (72,25),(117,115),
        #         (151,25),(196,115),
        #         (208,25),(253,115),
        #         (265,25),(310,115),
        #         (322,25),(367,115),
        #         (379,25),(424,115),]
        # heng line
        cv2.line(img, (0, 25), (440, 25), (0, 0, 255), 1)
        cv2.line(img, (0, 115), (440, 115), (0, 0, 255), 1)

        # shu line
        cv2.line(img, (15, 0), (15, 140), (0, 0, 255), 1)
        # char yun  15 25
        cv2.line(img, (60, 0), (60, 140), (0, 0, 255), 1)
        cv2.line(img, (72, 0), (72, 140), (0, 0, 255), 1)
        # A   72 25
        cv2.line(img, (117, 0), (117, 140), (0, 0, 255), 1)
        cv2.line(img, (129, 0), (129, 140), (0, 0, 255), 1)
        # .  129 25
        cv2.line(img, (139, 0), (139, 140), (0, 0, 255), 1)
        cv2.line(img, (151, 0), (151, 140), (0, 0, 255), 1)
        # 1   151 25
        cv2.line(img, (196, 0), (196, 140), (0, 0, 255), 1)
        cv2.line(img, (208, 0), (208, 140), (0, 0, 255), 1)
        # 2   208 25
        cv2.line(img, (253, 0), (253, 140), (0, 0, 255), 1)
        cv2.line(img, (265, 0), (265, 140), (0, 0, 255), 1)
        # 3   265 25
        cv2.line(img, (310, 0), (310, 140), (0, 0, 255), 1)
        cv2.line(img, (322, 0), (322, 140), (0, 0, 255), 1)
        # 4   322 25
        cv2.line(img, (367, 0), (367, 140), (0, 0, 255), 1)
        cv2.line(img, (379, 0), (379, 140), (0, 0, 255), 1)
        # 5   379 25
        cv2.line(img, (424, 0), (424, 140), (0, 0, 255), 1)

        # temp
        cv2.line(img, (0, 70), (440, 70), (0, 0, 255), 1)

        return img

    def num_char(self, plate):

        width = 440
        height = 140
        channels = 3

        imgShape = (height, width, channels)
        img = np.zeros(imgShape, np.uint8)

        # change color
        for i in range(height):
            for j in range(width):
                # b,g,r
                img[i, j] = (255, 0, 0)

        # text
        cv2_im = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(cv2_im)

        draw = ImageDraw.Draw(pil_im)
        numfont = ImageFont.truetype(self.font_path, 130, encoding="utf-8")

        color = (255, 255, 255)
        # num
        temp_scale = -18
        draw.text((72, temp_scale), plate[1], color, font=numfont)
        draw.text((151, temp_scale), plate[2], color, font=numfont)
        draw.text((208, temp_scale), plate[3], color, font=numfont)
        draw.text((265, temp_scale), plate[4], color, font=numfont)
        draw.text((322, temp_scale), plate[5], color, font=numfont)
        draw.text((379, temp_scale), plate[6], color, font=numfont)

        # point
        pofont = ImageFont.truetype(self.font_path, 35, encoding="utf-8")
        draw.text((124, 38), ".", color, font=pofont)

        cimg = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)

        return cimg

    def province_char(self, plate):

        if plate[0] == "云":
            width = 100
            height = 89
            imgShape = (height, width, 3)
            image = np.zeros(imgShape, np.uint8)
            # change color
            for i in range(height):
                for j in range(width):
                    # b,g,r
                    image[i, j] = (255, 0, 0)
            cv2_im = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_im = Image.fromarray(cv2_im)

            draw = ImageDraw.Draw(pil_im)
            pfont = ImageFont.truetype(self.font_path, 105, encoding="utf-8")

            # province
            draw.text((-2, -26), plate[0], (255, 255, 255), font=pfont)

            cimg = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)

            # cv2.imshow('province',cimg)
            # cv2.waitKey(0)
            return cimg

        height = 98
        width = 100
        channels = 3

        imgShape = (height, width, channels)
        image = np.zeros(imgShape, np.uint8)
        # change color
        for i in range(height):
            for j in range(width):
                # b,g,r
                image[i, j] = (255, 0, 0)
        cv2_im = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(cv2_im)

        draw = ImageDraw.Draw(pil_im)
        pfont = ImageFont.truetype(self.font_path, 105, encoding="utf-8")

        # province
        draw.text((-2, -20), plate[0], (255, 255, 255), font=pfont)

        cimg = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)

        # cv2.imshow('province',cimg)
        # cv2.waitKey(0)
        return cimg

    def merge_img(self, src, roi):
        roi_resize = cv2.resize(roi, (45, 90), interpolation=cv2.INTER_AREA)
        src[25:115, 15:60] = roi_resize
        return src

    def out_widge(self, img):
        b_thinckness = random.randint(2, 9)  # default = 6
        cv2.rectangle(
            img,
            (b_thinckness, b_thinckness),
            (440 - b_thinckness, 140 - b_thinckness),
            (225, 255, 225),
            thickness=random.randint(2, 6),
        )  # thickness default = 3

        # cv2.circle(img, (200, 300), 75, (0, 0, 255), 5)
        # cv2.rectangle(img, (100, 10), (115, 15), (0, 255, 0), thickness=1)
        # cv2.rectangle(img, (325, 10), (340, 15), (0, 255, 0), thickness=1)
        # cv2.rectangle(img, (100, 125), (115, 130), (0, 255, 0), thickness=1)
        # cv2.rectangle(img, (325, 125), (340, 130), (0, 255, 0), thickness=1)

        cv2_im = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(cv2_im)

        draw = ImageDraw.Draw(pil_im)
        pfont = ImageFont.truetype(self.font_path, 50, encoding="utf-8")

        # maoding
        color = (233, 233, 216)
        # color = (220,220,220)
        # color = (220,223,227)
        # color = (220,192,192)
        draw.text((100, -20), "-", color, font=pfont)
        draw.text((325, -20), "-", color, font=pfont)
        draw.text((100, 95), "-", color, font=pfont)
        draw.text((325, 95), "-", color, font=pfont)

        cimg = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)

        return cimg

    def get_noramal_plate(self, plate_chs):
        # (u'\u4e91AS6251',u'yunAS6251')
        numImg = self.num_char(plate_chs)
        charImg = self.province_char(plate_chs)

        putImg = self.merge_img(numImg, charImg)

        com = self.out_widge(putImg)
        return com


# class NoramlPlate END


# 参考: https://github.com/LCorleone/hyperlpr-train_e2e/blob/master/PlateCommon.py
class ExtendPlate:
    """docstring for Extendplate"""

    def __init__(self):
        super(ExtendPlate, self).__init__()
        self.NoPlates = "NoPlates"

    def r(self, val):
        return int(np.random.random() * val)

    def rot(self, img, angel, shape, max_angel, line):
        """使图像轻微的畸变
        img 输入图像
        factor 畸变的参数
        size 为图片的目标尺寸
        """
        size_o = [shape[1], shape[0]]

        size = (
            shape[1] + int(shape[0] * cos((float(max_angel) / 180) * 3.14)),
            shape[0],
        )
        # print ''
        # print size_o
        # print size

        interval = abs(int(sin((float(angel) / 180) * 3.14) * shape[0]))
        # print 'interval:',interval

        pts1 = np.float32(
            [[0, 0], [0, size_o[1]], [size_o[0], 0], [size_o[0], size_o[1]]]
        )
        if angel > 0:
            pts2 = np.float32(
                [
                    [interval, 0],
                    [0, size[1]],
                    [size[0], 0],
                    [size[0] - interval, size_o[1]],
                ]
            )
        else:
            pts2 = np.float32(
                [
                    [0, 0],
                    [interval, size[1]],
                    [size[0] - interval, 0],
                    [size[0], size_o[1]],
                ]
            )

        M = cv2.getPerspectiveTransform(pts1, pts2)
        dst = cv2.warpPerspective(img, M, size)

        # 点变化部分
        change = []
        for item in line:
            # print item
            change.append(np.float32(item))
        # 变点
        result = []
        for item in change:
            result.append(cv2.perspectiveTransform(item[None, :, :], M))

        # print result
        line2 = []
        for ee in result:
            for item in ee:
                zifu = []
                for point in item:
                    zifu.append([point[0], point[1]])
                line2.append(zifu)

        # print len(change)
        # print len(result)

        # for item in line2:
        #     print item
        return dst, line2

    def rot_add_bak(self, img, line):
        # print 'img.shape',img.shape
        # cv2.imwrite('test_result/add_img_shape.jpg',img)
        # 要放在多大的上
        width = img.shape[1] + (img.shape[1] / 3)
        height = img.shape[0] * 2
        channels = 3
        bak_shape = (height, width, channels)
        bak_img = np.zeros(bak_shape, np.uint8)
        # print 'bak_img.shape',bak_img.shape

        x_start = (width - img.shape[1]) / 2
        y_start = (height - img.shape[0]) / 2

        bak_img[y_start : y_start + img.shape[0], x_start : x_start + img.shape[1]] = (
            img
        )

        # 变点
        # print line
        for boxpoint in line:
            for point in boxpoint:
                point[0] += x_start
                point[1] += y_start

        ##########################################
        # 随机把图放在一个地方
        new_bak_img = np.zeros(bak_shape, np.uint8)
        # 1.先随机缩小
        scale = float(random.randint(60, 99)) / float(100)
        resize_w = bak_img.shape[1] * scale
        resize_h = bak_img.shape[0] * scale
        resize_img = cv2.resize(bak_img, (int(resize_w), int(resize_h)))
        for boxpoint in line:
            for point in boxpoint:
                point[0] = scale * point[0]
                point[1] = scale * point[1]

        # 2.随机放在背景中
        h_pad = new_bak_img.shape[0] - resize_img.shape[0]
        w_pad = new_bak_img.shape[1] - resize_img.shape[1]
        new_x_start = random.randint(1, w_pad)
        new_y_start = random.randint(1, h_pad)
        new_bak_img[
            new_y_start : new_y_start + resize_img.shape[0],
            new_x_start : new_x_start + resize_img.shape[1],
        ] = resize_img
        for boxpoint in line:
            for point in boxpoint:
                point[0] += new_x_start
                point[1] += new_y_start

        return new_bak_img, line

    def rotRandrom(self, img, factor, size, line):
        # 仿射变换
        shape = size
        pts1 = np.float32([[0, 0], [0, shape[0]], [shape[1], 0], [shape[1], shape[0]]])
        pts2 = np.float32(
            [
                [self.r(factor), self.r(factor)],
                [self.r(factor), shape[0] - self.r(factor)],
                [shape[1] - self.r(factor), self.r(factor)],
                [shape[1] - self.r(factor), shape[0] - self.r(factor)],
            ]
        )

        M = cv2.getPerspectiveTransform(pts1, pts2)
        dst = cv2.warpPerspective(img, M, size)

        # 点变化部分
        # 变成np.float
        change = []
        for item in line:
            change.append(np.float32(item))
        # 变点
        result = []
        for item in change:
            result.append(cv2.perspectiveTransform(item[None, :, :], M))

        line2 = []
        for ee in result:
            for item in ee:
                zifu = []
                for point in item:
                    zifu.append([point[0], point[1]])
                line2.append(zifu)

        # print len(change)
        # print len(result)

        # for item in line2:
        #     print item

        return dst, line2

    def tfactor(self, img):
        # 变色
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        hsv[:, :, 0] = hsv[:, :, 0] * (0.8 + np.random.random() * 0.2)
        hsv[:, :, 1] = hsv[:, :, 1] * (0.3 + np.random.random() * 0.7)
        hsv[:, :, 2] = hsv[:, :, 2] * (0.2 + np.random.random() * 0.8)

        img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return img

    def random_envirment(self, img, data_set, index):
        env = cv2.imread(data_set[index])
        env = cv2.resize(env, (img.shape[1], img.shape[0]))
        bak = img == 0
        bak = bak.astype(np.uint8) * 255
        inv = cv2.bitwise_and(bak, env)
        img = cv2.bitwise_or(inv, img)
        return img

    def extend_background(self, img, data_set, line, index):
        bak = cv2.imread(data_set[index])
        bak_resize = (img.shape[1] * 2, img.shape[0] * 2)
        bak = cv2.resize(bak, bak_resize)
        # print 'img.shape',img.shape
        # print 'bak.shape',bak.shape
        # (140, 561, 3)
        # (36, 136, 3)
        # src[25:115,15:60] = roi_resize
        # src[y1:y2,x1:x2]

        # x_start = self.r(bak.shape[1]/3)
        # y_start = self.r(bak.shape[0]/3)
        x_start = random.randint(bak.shape[1] / 10, bak.shape[1] / 3)
        y_start = random.randint(bak.shape[0] / 10, bak.shape[0] / 3)
        # print x_start,y_start

        # 放上去
        bak[y_start : y_start + img.shape[0], x_start : x_start + img.shape[1]] = img

        # 变点
        # print line
        for boxpoint in line:
            for point in boxpoint:
                point[0] += x_start
                point[1] += y_start
        # print line
        # self.temp_draw_point(bak,line)

        return bak, line

    def AddNoiseSingleChannel(self, single):
        diff = 255 - single.max()
        noise = np.random.normal(0, 1 + self.r(6), single.shape)
        noise = (noise - noise.min()) / (noise.max() - noise.min())
        noise = diff * noise
        noise = noise.astype(np.uint8)
        dst = single + noise
        return dst

    def addNoise(self, img, sdev=0.5, avg=10):
        img[:, :, 0] = self.AddNoiseSingleChannel(img[:, :, 0])
        img[:, :, 1] = self.AddNoiseSingleChannel(img[:, :, 1])
        img[:, :, 2] = self.AddNoiseSingleChannel(img[:, :, 2])
        return img

    def AddGauss(self, img, level):
        return cv2.blur(img, (level * 2 + 1, level * 2 + 1))

    def temp_draw_point(self, img, line):
        for boxpoint in line:
            for x, y in boxpoint:
                cv2.circle(img, (int(x), int(y)), 10, (0, 255, 0), -1)
        # cv2.imwrite('test_result/fin.jpg',img)

    def get_extend_plate(self, npe_img):
        ##############################
        # 变换处理
        line = [
            [
                [0, 0],
                [npe_img.shape[1], 0],
                [0, npe_img.shape[0]],
                [npe_img.shape[1], npe_img.shape[0]],
            ]
        ]
        # print npe_img.shape  # (140, 440, 3)
        try:
            # 变换处理
            # 水平畸变
            # com,line = self.rot(npe_img,self.r(60)-30,npe_img.shape,30,line)  # 原本的
            com, line = self.rot(npe_img, self.r(90) - 45, npe_img.shape, 30, line)
            # cv2.imwrite("creat_plate/dst1.jpg", com)

            # 加一点背景，扩展图片大小
            # com, line = self.rot_add_bak(com, line)

            # 仿射变换，随机值10
            com, line = self.rotRandrom(
                com, 10, (com.shape[1], com.shape[0]), line
            )  # 原本的
            # com, line = self.rotRandrom(com, 30, (com.shape[1], com.shape[0]), line)
            # cv2.imwrite("creat_plate/dst2.jpg", com)
            # print line
            # self.temp_draw_point(com,line)

            # 随机变色
            com = self.tfactor(com)

            # # 放在假背景中
            # noplates_path = []
            # for parent, parent_folder, filenames in os.walk(self.NoPlates):
            #     for filename in filenames:
            #         path = parent + "/" + filename
            #         noplates_path.append(path)
            # index = self.r(len(noplates_path))
            # com = self.random_envirment(com, noplates_path, index)  # 他原版的
            # com,line = self.extend_background(com,noplates_path,line,index)  # 我贴的,再加一圈

            # 加噪声
            com = self.AddGauss(com, 1 + self.r(4))  # 原本的
            # com = self.AddGauss(com, 1+self.r(10))
            com = self.addNoise(com)
            # cv2.imwrite("creat_plate/dst3.jpg", com)

            # 画点看看
            # self.temp_draw_point(com,line)

        except Exception as e:
            # print 'repr(e):\t', repr(e)
            print("e.message:", e)
            print(traceback.format_exc())

            return npe_img, line, False

        ##############################
        return com, line, True


# 随机生成字符
def random_7char(num=10, if_yun=False):
    chars = [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "J",
        "K",
        "L",
        "M",
        "N",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]

    plate_list = (
        []
    )  # [[中文车牌，拼音车牌],[u'gannKGPPHP',u'\u8d63KGPPHP'], [u'\u85cfMMCFYH',u'zangMMCFYH']]

    t_count = 0
    while t_count != num:

        per_random_num = np.random.randint(0, len(province_change))
        temp_plate_chs = province_change[per_random_num][0]
        temp_plate_py = province_change[per_random_num][1]

        if if_yun:
            temp_plate_chs = "云"
            temp_plate_py = "yun"

        for i in range(0, 6):
            random_num6 = chars[np.random.randint(0, len(chars))]
            temp_plate_chs += random_num6
            temp_plate_py += random_num6

            if len(temp_plate_chs) == 7:

                if temp_plate_chs[1] not in [
                    "0",
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                ]:
                    two = [temp_plate_chs, temp_plate_py]
                    plate_list.append(two)
                    t_count += 1

                temp_plate_chs = ""
                temp_plate_py = ""

    # print plates
    return plate_list


def only_creat(out_img_path, creat_img_num):
    # 生成主要程序
    npl = NoramlPlate()
    expl = ExtendPlate()
    plate_list = random_7char(creat_img_num, if_yun=False)

    db_list = []
    print("creat plate total is", len(plate_list))
    for i, plate_line in enumerate(plate_list):
        # npl.view_bar(i+1,len(plate_list))
        print(i, "/", len(plate_list), plate_line)

        # print plate_chs,plate_py
        plate_chs, plate_py = plate_line

        npl_img = npl.get_noramal_plate(plate_chs)
        expl_img, f_point, flag = expl.get_extend_plate(npl_img)

        save_path = os.path.join(out_img_path, plate_chs + ".jpg")

        # cv2.imwrite(save_path, expl_img)
        cv2.imencode(".jpg", expl_img)[1].tofile(save_path)

    print(" creat plate done")
    return db_list


def main():

    # 生成图片数
    creat_num = 2000

    out_img_path = "creat_plate"

    mkdir_dir(out_img_path)
    only_creat(out_img_path, creat_num)


if __name__ == "__main__":
    main()
