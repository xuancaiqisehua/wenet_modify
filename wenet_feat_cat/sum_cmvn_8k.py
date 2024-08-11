import json
import glob
import torch
import numpy as np
import sys
def readjsonfile(filename):
    with open(filename,'r') as load_f:
        new_dict = json.load(load_f) 
    return new_dict
def getAllCMVN(path,out_cmvn):
  feat_dim=40
  filelist=glob.glob(path)
  all_mean_stat=np.zeros(feat_dim)
  all_var_stat = np.zeros(feat_dim)
  all_number=0
  #num=0
  #num1=0
  for file in filelist:
    info=readjsonfile(file)
    print(len(info['mean_stat']))
    all_mean_stat += np.array(info['mean_stat'])
    all_var_stat += np.array(info['var_stat'])
    all_number += info['frame_num']
  all_mean_stat=torch.Tensor(all_mean_stat)
  all_var_stat=torch.Tensor(all_var_stat)
  cmvn_info = {
        'mean_stat': list(all_mean_stat.tolist()),
        'var_stat': list(all_var_stat.tolist()),
        'frame_num': all_number
    }
  #print('first_num',num)
  with open(out_cmvn, 'w') as fout:
        fout.write(json.dumps(cmvn_info))
dir=sys.argv[1]
path=dir+'/'+'global_cmvn/*cmvn'
out_cmvn=dir+'/'+'global_cmvn_final'
getAllCMVN(path,out_cmvn)
