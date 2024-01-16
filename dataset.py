noise_aug = conf.get('noise_aug', False)
if noise_aug:
       noise_conf = conf.get('noise_conf', {})
       reverb_lmdb_file = conf.get('reverb_source', {})
       reverb_data = LmdbData(reverb_lmdb_file)
       print('reverb_lmdb_file',reverb_lmdb_file)
       dataset = Processor(dataset,processor.noise_augmentation,noiseLst=noise_conf['noiseLst'],reverb_source=reverb_data,max_snr=noise_conf['max_snr'],min_snr=noise_conf['min_snr'],noise_shuffle_size=noise_conf['noise_shuffle_size'])
