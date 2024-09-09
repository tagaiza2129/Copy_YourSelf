import time
print("テストモードなので計測を開始します")
start = time.time()
import os
from inference.Seq2Seq import Learning  
#Intel GPUを使用するために消さないでって言ったじゃん！少し過去の俺！
import intel_extension_for_pytorch
#Batch_sizeは2のn乗でないといけない
batch_size = 16
APP_dir = os.path.dirname(os.path.dirname(__file__))
device="xpu"
os.chdir(os.path.join(APP_dir, "model/Learning_test_model/Lerarning"))

with open("input.txt", "r", encoding="utf-8") as f:
    inputs = f.readlines()
with open("output.txt", "r", encoding="utf-8") as f:
    outputs = f.readlines()

model=Learning(path=os.path.join(APP_dir,"model/Learning_test_model"), inputs=inputs, outputs=outputs, device=device, batch_size=batch_size, lr=0.01, epochs=10)
end=time.time()
time_diff = end - start
print(time_diff)
