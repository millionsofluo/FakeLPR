#!/bin/sh

mkdir -p keypoint_snapshot
# GLOG_logtostderr=0 GLOG_log_dir=log/ \

/data/sdk/caffe-ssd/build/tools/caffe train --solver="keypoint/keypoint_solver.prototxt" \
# 2>&1 | tee log/train_log.log
