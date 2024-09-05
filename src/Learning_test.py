import os
from inference.Seq2Seq import Learning
#Intel GPUを使用するために消さないでって言ったじゃん！少し過去の俺！
import torch_directml
batch_size = 32
APP_dir = os.path.dirname(os.path.dirname(__file__))
device=torch_directml.device()
os.chdir(os.path.join(APP_dir, "model/Learning_test_model/Lerarning"))

with open("input.txt", "r", encoding="utf-8") as f:
    inputs = f.readlines()
with open("output.txt", "r", encoding="utf-8") as f:
    outputs = f.readlines()

model=Learning(inputs,outputs,device=device,batch_size=batch_size,lr=0.001)