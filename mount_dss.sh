#!/bin/bash
sudo mkdir -p /dss/dssfs02/lwp-dss-0001/t7441/t7441-dss-0000
sudo mount -t nfs -o rsize=1048576,wsize=1048576,hard,tcp,bg,timeo=600,vers=3 dss01nfs14.dss.lrz.de:/dss/dssfs02/lwp-dss-0001/t7441/t7441-dss-0000 /dss/dssfs02/lwp-dss-0001/t7441/t7441-dss-0000 
