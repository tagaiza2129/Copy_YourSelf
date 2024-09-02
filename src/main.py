from flask import Flask, render_template, request
import os
import yaml
import ssl
import random
import string
os.chdir("../")
app_dir=os.getcwd()
app = Flask(__name__)
@app.route("/")
def main():
    return render_template(os.path.join(app_dir,"src","index.html"))
@app.route("/model_upload",methods=["POST"])
def upload():
    file_pass=[random.choice(string.ascii_letters + string.digits) for i in range(n)]
    file_pass="".join(file_pass)
    file=request.files["file"]
    file_name=file.filename
    file.save(os.path.join(app_dir,"model",file.filename))
    os.rename(os.path.join(app_dir,"model",file.filename),os.path.join(app_dir,"model",file_name))
    return file_pass
@app.route("</file_pass>")
async def file(file_pass):
    return send_from_directory(os.path.join(app_dir,file_pass))
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