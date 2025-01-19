#!/bin/bash
i=0
for(( i=0;i<11;i++)){
	echo $i
        rm tmp/*
	cp exp/conformer/${i}.pt tmp/
        python wenet/bin/average_model.py --dst_model avg_5.pt --src_path tmp/ --num 1
        python wenet/bin/export_jit.py --config exp/conformer/train.yaml --checkpoint avg_5.pt --output_file test.zip  --output_quant_file test.zip
        mv test.zip test_zip/test_${i}.zip
	
}
