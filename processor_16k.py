def shuffle_noise(noise_data,shuffle_size):
    """ Local shuffle the noise
        Args:
            noise_data
            shuffle_size: buffer size for shuffle

        Returns:
            Iterable[noise]
    """
    buf = []
    for sample in noise_data:
        buf.append(sample)
        if len(buf) >= shuffle_size or len(buf)>=len(noise_data):
            random.shuffle(buf)
            for x in buf:
                yield x
            buf = []
    # The sample left over
    random.shuffle(buf)
    for x in buf:
        yield x
def noise_augmentation(data,noiseLst=None,reverb_source=None,max_snr=50,min_snr=10,noise_shuffle_size=10000):
    noiseFiles = read_lists(noiseLst)
    noiseFile=random.choice(noiseFiles)
    print('noiseFile',noiseFile)
    aug_noises=read_noise(noiseFile)
    for sample in data:
        assert 'sample_rate' in sample
        assert 'wav' in sample
        if type(sample['wav']) is np.ndarray:
          yield sample
        else:
          noise_flag = random.randint(0,9)
          waveform = sample['wav']
          if noise_flag<6:
             aug_type = random.randint(0,5)

             if aug_type < 1:
                  # add reverberation
                  audio = sample['wav'].numpy()[0]
                  if np.max(audio)>0.9:
                      audio=audio*0.4

                  audio_len = audio.shape[0]

                  _, rir_data = reverb_source.random_one()
                  #rirId, rir_data = reverb_source.random_one()
                  rir_sr, rir_audio = wavfile.read(io.BytesIO(rir_data))
                  rir_audio = rir_audio.astype(np.float32)
                  rir_audio = rir_audio / np.sqrt(np.sum(rir_audio**2))
                  out_audio = signal.convolve(audio, rir_audio,
                                              mode='full')[:audio_len]
                  sample['wav'] = torch.from_numpy(out_audio).unsqueeze(0)

             else:
                  snr = random.randint(min_snr,max_snr)
                  aug_noise = shuffle_noise(aug_noises,noise_shuffle_size).__next__()
                  aug_noise = aug_noise/(1<<15)
                  if aug_noise.any():
                    while len(aug_noise) <= waveform.shape[1]:
                      aug_noise = np.concatenate((aug_noise, aug_noise), axis=0)
                    diff_len = len(aug_noise) - waveform.shape[1]
                    start = np.random.randint(0, diff_len)
                    end = start + waveform.shape[1]
                    # 计算添加噪音因子
                    P_signal = waveform.pow(2).sum().item()/waveform.shape[1] #信号功率
                    noiseData=torch.unsqueeze(torch.tensor(aug_noise[start:end],dtype=torch.float32),0)
                    P_noise = noiseData.pow(2).sum().item()/waveform.shape[1] #噪音功率
                    if P_noise<=0.0:
                      P_noise=1
                    db=np.sqrt(P_signal/P_noise/(10**(snr/10.0)))
                    # 叠加噪音
                    wav = waveform+db*noiseData
                    sample['wav'] = wav
          yield sample
