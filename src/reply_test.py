from inference import Seq2Seq
import os
import torch
import intel_extension_for_pytorch
app_dir=r"/home/Copy_YourSelf-Project/Copy_YourSelf"
print(Seq2Seq.chat(model_path=os.path.join(app_dir,"model/Learning_test_model"),text="こんにちは",max_length=10,device=torch.device("xpu")))