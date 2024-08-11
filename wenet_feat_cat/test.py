import onnx
from onnxruntime.quantization import quantize_dynamic, QuantType
 
model_encoder = 'encoder.onnx'
model_quant_encoder = 'encoder.onnx.int8'
quantized_model = quantize_dynamic(model_encoder, model_quant_encoder, weight_type=QuantType.QUInt8)
model_decoder = 'decoder.onnx'
model_quant_decoder = 'decoder.onnx.int8'
quantized_model = quantize_dynamic(model_decoder, model_quant_decoder, weight_type=QuantType.QUInt8)
model_ctc = 'ctc.onnx'
model_quant_ctc = 'ctc.onnx.int8'
quantized_model = quantize_dynamic(model_ctc, model_quant_ctc, weight_type=QuantType.QUInt8)
