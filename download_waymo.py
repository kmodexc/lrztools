#!/usr/bin/python3
from __future__ import print_function
import glob
import os
import argparse
from subprocess import check_output
import re
import sys

#gsutils_path = "/dss/dsshome1/03/ge95nub3/google-cloud-sdk/bin/gsutil"
gsutils_path = "gsutil"
#download_base_dir = "/dss/dssfs04/lwp-dss-0002/t7441/t7441-dss-0001/waymo/"
download_base_dir = "/dss/dssfs02/lwp-dss-0001/t7441/t7441-dss-0000/waymo"
remote_base = 'gs://waymo_open_dataset_v_1_4_3/individual_files/'
md5_re = re.compile(r".*([0-9a-f]{32})")


def get_remote_ls(path):
    try:
        out = check_output([gsutils_path, "ls", path])
    except:
        assert False, f"Failed to list files from {path}. Make sure gsutils is installed and you logged into your google account (gcloud init) wich has permission to access the waymo dataset."
    lines = out.decode('utf-8').split('\n')
    for p in lines:
        if "tfrecord" in p:
            yield p

def get_remote_hash(file):
    out = check_output([gsutils_path,'hash','-h',file])
    str_out = out.decode('utf-8')
    match_result = md5_re.match(str_out.split('\n')[1])
    assert match_result is not None, f"no md5 hash found {str_out}"
    md5str = match_result.group(1)
    return md5str

def get_local_hash(file):
    out = check_output(['md5sum',file])
    str_out = out.decode('utf-8')
    md5str = str_out.split(' ')[0]
    return md5str

def create_path(path):
    if not os.path.exists(path):
        os.mkdir(path)

def download_file(remote, out_dir):
    flag = os.system(gsutils_path+' cp ' + remote + ' ' + out_dir)
    assert flag == 0, f'Failed to download {remote} to {out_dir}. Make sure gsutils is installed and you logged into your google account (gcloud init) wich has permission to access the waymo dataset.'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--download",action="store_true", help="download the waymo dataset")
    parser.add_argument("-m","--hash",action="store_true", help="check all the downloaded file's hashes against the original file hashes in the cloud")
    parser.add_argument("-l","--list",action="store_true", help="list all the waymo files (from remote)")
    parser.add_argument("-e","--exists",action="store_true", help="check a file is missing which should be downloaded")
    parser.add_argument("-s","--show-paths",action="store_true", help="show all paths that would be processed (for debugging)")
    args = parser.parse_args()

    if not (args.download or args.hash or args.list or args.exists or args.show_paths):
        parser.print_help()
        sys.exit(0)

    create_path(download_base_dir)

    for split in ['training', 'validation']:
        if split == 'training':
            num_segs = 31
        elif split == 'validation':
            num_segs = 8
        remote_dir = remote_base + split + "/"
        download_out_dir = download_base_dir + "raw_data/" 
        create_path(download_out_dir)
       
        file_list = get_remote_ls(remote_dir)

        for f in file_list:
            segment_file = f.split('/')[-1]
            assert "tfrecord" in segment_file
            
            if args.download:
                if not os.path.isfile(download_out_dir + segment_file):
                    download_file(remote_dir + segment_file, download_out_dir)
            elif args.exists:
                if not os.path.isfile(download_out_dir + segment_file):
                    print(f"file missing {download_out_dir + segment_file}")
            elif args.hash:
                h_r = get_remote_hash(remote_dir + segment_file)
                h_l = get_local_hash(download_out_dir + segment_file)
                if h_r != h_l:
                    print(f"{remote_dir + segment_file} and {download_out_dir + segment_file} are not the same (r{h_r} l{h_l} )")
                else:
                    print("hash ok")
            elif args.list:
                for l in file_list:
                    print(l)
                break
            else:
                print("download_dir", download_out_dir)
                print("remote_dir", remote_dir)
                print("segment_file", segment_file)
                print("nothing to do")

            print(f"File {f} processed")



if __name__ == "__main__":
    main()



