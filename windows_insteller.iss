[Setup]
AppId={{68D60AC9-17C3-4A14-8C2D-CDBE5BFD2D27}}
AppName=Copy_YourSelf
AppVerName=Copy_YourSelf 0.0.1
AppCopyright=tagaiza2129
AppendDefaultDirName=yes
VersionInfoDescription=Copy_YourSelfの初期バージョンインストーラー
VersionInfoVersion=0.0.1
OutputBaseFilename = Copy_YourSelf_installer
DefaultDirName={userappdata}\Copy_YourSelf
DisableWelcomePage=no
DefaultGroupName=Copy_YourSelf
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
;以下のファイルパスは絶対パスで入力する
;インストーラーのアイコンファイル
SetupIconFile=C:\Users\tagai\Copy_YourSelf\static\img\icon.ico
;インストーラーの初期画面の背景画像
;WizardImageFile=C:\Users\user\Documents\app\image.bmp
;インストーラーの完了画面の背景画像
;WizardSmallImageFile=C:\Users\user\Documents\app\image.bmp
;必要なアプリケーションがインストールされていればインストールを続行する

;途中でインストールされるドライバーの選択肢を表示する
[Tasks]
Name: "NVIDIA"; Description: "NVIDIA"; GroupDescription: "追加インストールするドライバーを選択してください:"; Flags: unchecked
Name: "IntelGPU"; Description: "Intel Arc"; GroupDescription: "追加インストールするドライバーを選択してください:"; Flags: unchecked
Name: "DirectX"; Description: "DirectX"; GroupDescription: "追加インストールするドライバーを選択してください:"; Flags: unchecked
Name: "OpenVINO"; Description: "OpenVINO"; GroupDescription: "追加インストールするドライバーを選択してください:"; Flags: unchecked
[Languages]
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"