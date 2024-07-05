use tokio::fs::File;
use tokio::io::AsyncReadExt;
use tokio::net::TcpListener;
use tokio::time::{sleep, Duration};
use log::info;
use log::error;
use std::env;
use lazy_static::lazy_static;
use std::sync::Mutex;
use tokio::io::AsyncWriteExt;

mod command_line;

lazy_static! {
    static ref Application_DIRECTORY: Mutex<&'static str> = Mutex::new("/home/tagaiza2129/Copy_YourSelf");
}
#[tokio::main]
async fn main() {
    env::set_var("RUST_LOG", "info");
    env_logger::init();
    command_line::option_add("a".to_string(),"server_address".to_string(),"0.0.0.0".to_string(),"HTMLサーバーのアドレスを指定します".to_string(),"ADDRESS".to_string());
    command_line::option_add("p".to_string(),"port".to_string(),"80".to_string(), "webサーバーを立ち上げるポートを指定します".to_string(), "PORT".to_string());
    command_line::option_add("k".to_string(),"open-key".to_string(),"None".to_string(),"秘密鍵を使ってHTTPサーバーを構築します".to_string(),"KEY".to_string());
    command_line::option_add("d".to_string(),"debug_directory".to_string(),"None".to_string(),"デバッグ用のディレクトリを指定します".to_string(),"DIRECTORY".to_string());
    let option_list = command_line::run_command_line(env::args().collect());
    let address = option_list.get("server_address").unwrap();
    let port = option_list.get("port").unwrap();
    let app_directory = if option_list.get("debug_directory").unwrap() == "None" {
        let locked_directory = Application_DIRECTORY.lock().unwrap();
        locked_directory.to_string()
    } else {
        option_list.get("debug_directory").unwrap().clone()
    };
    info!("右記のディレクトリで起動します: {}", app_directory);
    info!("HTTPサーバーを起動します...");
    // 無意味なスリープ関数を隠し味で追加
    sleep(Duration::from_secs(2)).await;
    let listener = match TcpListener::bind(format!("{}:{}", address, port)).await {
        Ok(listener) => {
            let local_addr = if address == "0.0.0.0" || address == "127.0.0.1" { "localhost" } else { address };
            info!("http://{}:{} でWebサービスを起動しました", local_addr, port);
            listener
        },
        Err(e) => {
            if e.kind() == std::io::ErrorKind::PermissionDenied {
                error!("権限エラー: このポートにはアクセスできません");
            } else {
                error!("サーバーを起動できませんでした: {}", e);
            }
            return;
        }
    };
    loop {
        let (stream, addr) = listener.accept().await.unwrap();
        let app_directory_clone = app_directory.clone();
        tokio::spawn(async move {
            handle_connection(stream,addr,&app_directory_clone).await;
        });
    }
}
async fn handle_connection(mut stream: tokio::net::TcpStream,addr: std::net::SocketAddr,html_path:&String) {
    let mut request_buf = [0; 4096];
    let size = stream.read(&mut request_buf).await.unwrap();
    let request = String::from_utf8_lossy(&request_buf);
    let request_lines: Vec<&str> = request.lines().collect();
    info!("{}:{} からリクエストを受信しました", addr.ip(), addr.port());
    info!("通信タイプ: {}", request_lines[0]);
    info!("リクエストサイズ: {}", size);
    let accessed_url = if let Some(first_line) = request_lines.get(0) {
        let first_line = first_line.split_whitespace().collect::<Vec<&str>>();
        if first_line.len() < 1 {
            first_line[1]
        } else {
            "/"
        }
    } else {
        "/"
    };
    info!("アクセスされたURL: {}", accessed_url);
    let file_path = format!("{}static{}{}",html_path,accessed_url, "index.html");
    info!("アクセスされたファイル: {}", file_path);
    let mut file = File::open(file_path).await.unwrap();
    let mut contents = String::new();
    file.read_to_string(&mut contents).await.unwrap();
    stream.write_all(b"HTTP/1.1 200 OK\r\n\r\n").await.unwrap();
    stream.write_all(contents.as_bytes()).await.unwrap();
    stream.flush().await.unwrap();
}