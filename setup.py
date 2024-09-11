from setuptools import setup, find_packages
import os
dir=os.path.dirname(__file__)
#これはあくまでコマンドとして実行する為のファイルです
#必要なライブラリが全てインストールされわけではないので
#詳しくはinstallのHowToInstallを参照してください

#インストールする為には以下のコマンドを実行してください
#python3 setup.py develop
setup(
    name="Copy_YourSelf",
    version="0.1",
    description="AIツール、CopyYourSelfのサーバー側のツール",
    author="tagaiza2129",
    packages=find_packages(where=os.path.join(dir,"src")),
    package_dir={"": "src"},
    install_requires=["torch==2.4.0", "transformers", "pydantic", "requests", "pyyaml", "torchtext==0.6.0","dill","scikit-learn","pandas","janome","flask[async]"],
    entry_points={
        "console_scripts": [
            "Copy_YourSelf=main:start",
            "YourSelf-Client=client:start",
            "YourSelf-model=model:start"
        ]
    }
)