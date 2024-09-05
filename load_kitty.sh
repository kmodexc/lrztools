#!/bin/bash

set -e

mkdir -p /dss/dssfs02/lwp-dss-0001/t7441/t7441-dss-0000/kitti
cd /dss/dssfs02/lwp-dss-0001/t7441/t7441-dss-0000/kitti

echo "Downloading compressed KITTI dataset now"

wget -nc https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_image_2.zip
wget -nc https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_velodyne.zip
wget -nc https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_calib.zip
wget -nc https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_label_2.zip
wget -nc --http-user=tufast --http-password=tufast https://kmode.dev/public/data/datasets/kitty/train_planes.zip

echo "Extracting KITTI dataset now"

find . -name "data_*" -exec unzip {} \;
unzip -d training train_planes.zip

echo "Finished loading the KITTI dataset successfully"
