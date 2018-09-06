# FakeLPR

`caffe 多标签分类`
`人造车牌`

## 调用
需要 **opencv3.4**
```
cd FakeLPR
python py_demo.py
```

## 训练
需要 **caffe**

生成数据
```shell
cd FakeLPR/train/datasets
# 1.生成keypoint数据
python creat_keypoint_data.py
# 2.生成训练keypoint的lmdb
python creat_keypoint_lmdb.py
# 3.生成e2e数据
python creat_e2e_data.py
# 4.生成训练e2e的lmdb
python creat_e2e_lmdb.py
```
caffe训练模型
```shell
# 返回 FakeLPR/train
cd ..
# 5.训练keypoint模型
sh ./train_keypoint.sh
# 6.训练e2e模型
sh ./train_e2e.sh
```

## 具体的看blog

[FakeLPR车牌识别(1) ----- 概述](https://blog.csdn.net/luoyanjunhehehe/article/details/82256483)

[FakeLPR车牌识别(2) ----- 车牌角点定位](https://blog.csdn.net/luoyanjunhehehe/article/details/82347489)

[FakeLPR车牌识别(3) ----- 车牌端到端识别](https://blog.csdn.net/luoyanjunhehehe/article/details/82349990)
