import torch
import sys
inFile = sys.argv[1]
model = torch.load(inFile)
for name,para in model.items():
  #print(name)
  # new_model
  #if name in ["encoder.encoders.1.self_attn.pos_bias_u","encoder.encoders.5.self_attn.pos_bias_u"]:
  # old model
  if name in ["encoder.encoders.2.self_attn.pos_bias_u","encoder.encoders.6.self_attn.pos_bias_u"]:
      print(name,para)
