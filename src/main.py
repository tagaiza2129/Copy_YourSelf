from flask import Flask, render_template,send_from_directory
from flask import request as req
import os
import yaml
import ssl
import random
import string
os.chdir(os.path.dirname(__file__))
os.chdir("../")
app_dir=os.getcwd()
print(f"アプリディレクトリを{app_dir}に設定しました")
app = Flask(__name__)
@app.route("/")
async def main():
    return send_from_directory(os.path.join(app_dir,"static"),"index.html")
@app.route("/model_upload",methods=["POST"])
async def upload():
    file_pass=[random.choice(string.ascii_letters + string.digits) for i in range(20)]
    file_pass="".join(file_pass)
    file=req.files["file"]
    file_name=file.filename
    file.save(os.path.join(app_dir,"model",file.filename))
    os.rename(os.path.join(app_dir,"model",file.filename),os.path.join(app_dir,"model",file_name))
    return file_pass
@app.route("/<string:file_pass>")
async def file(file_pass):
    file_name=os.path.dirname(file_pass)
    return send_from_directory(os.path.join(app_dir,"static",os.path.dirname(file_pass)),os.path.basename(file_pass))
#中身を後で実装する所一覧
@app.route("/available_device",methods=["GET"])
async def available_device():
    return "Available"
@app.route("/learning",methods=["POST"])
async def learning():
    return "Learning"
if __name__ == "__main__":
    with open("config.yaml",mode="r",encoding="UTF-8")as f:
        config = yaml.safe_load(f)
    import argparse
    parser = argparse.ArgumentParser(prog="Copy_YourSelf-Client",description='AIツール、CopyYourSelfのクライアント側のツール',usage="python3 main.py <file_Path> <options>",add_help=True)
    parser.add_argument("-a","--address",type=str,help="学習、又は推論に利用するデータを指定します。",default=config["server_ip"])
    parser.add_argument("-p","--port",type=int,help="分散学習に利用するサーバーのポートを指定します",default=config["server_port"])
    parser.add_argument("-k","--public_key",type=str,help="公開鍵を指定します",default=config["public_key_path"])
    parser.add_argument("-c","--cert",type=str,help="証明書を指定します",default=config["cert_path"])
    args = parser.parse_args()
    if args.public_key =="No" or args.cert=="No":
        app.run(host=args.address,port=args.port,debug=False)    
    else:
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(args.cert, args.public_key)
        app.run(host=args.address,port=args.port,ssl_context=context,debug=False)