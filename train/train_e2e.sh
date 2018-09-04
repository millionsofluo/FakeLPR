#!/bin/sh

mkdir -p e2e_snapshot
# GLOG_logtostderr=0 GLOG_log_dir=log/ \

/data/sdk/caffe-ssd/build/tools/caffe train --solver="e2e/e2e_solver.prototxt" \

