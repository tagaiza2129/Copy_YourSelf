use tokio::fs::File;
use tokio::io::AsyncReadExt;
use tokio::net::TcpListener;
use tokio::time::{sleep, Duration};
use log::info;
use log::error;
use std::collections::HashMap;
use std::{env, vec};

use std::sync::Mutex;
use lazy_static::lazy_static;
use tokio::io::AsyncWriteExt;

mod command_line;

lazy_static! {static ref Application_DIRECTORY: Mutex<&'static str> = Mutex::new("/home/tagaiza2129/Copy_YourSelf/");}

#[tokio::main]
async fn main() {
    env::set_var("RUST_LOG", "info");
    env_logger::init();
    command_line::option_add("a".to_string(),"server_address".to_string(),"127.0.0.1".to_string(),"HTMLサーバーのアドレスを指定します".to_string(),"ADDRESS".to_string());
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
            }else if  e.kind() ==std::io::ErrorKind::AddrInUse {
                error!("アドレスエラー: このアドレスは既に使用されています"); 
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
    //APIのGET用のリスト
    let _get_api_list: Vec<String> = vec!["/available_device".to_string(),"/make_model".to_string(),"/learning".to_string()];
    info!("{}:{} からリクエストを受信しました", addr.ip(), addr.port());
    //Access_listに使うHTTPのリクエスト形式はPOST通信です
    let accessed_url = if let Some(first_line) = request_lines.get(0) {
        let first_line = first_line.split_whitespace().collect::<Vec<&str>>();
        if first_line.len() > 1 {
            first_line[1]
        } else {
            "/"
        }
    } else {
        "/"
    };
    let url_parts: Vec<&str> = accessed_url.split("/").collect();
    //受診したデータを解析し、GET通信かPOST通信かを判定する
    if request_lines[0].contains("GET") {
        info!("GET通信を受信しました,IPアドレス: {}", addr.ip());
        if _get_api_list.iter().any(|api| api == accessed_url) {
            if accessed_url=="/available_device"{
                let response = "GPU:1, CPU:1";
                let response_body = response.as_bytes();
                let response_header = format!("HTTP/1.1 200 Bad Request\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Length: {}\r\n\r\n",response_body.len());
                let full_response = [response_header.as_bytes(), response_body].concat();
                stream.write_all(&full_response).await.unwrap();
                stream.flush().await.unwrap();
            }else {
                let response = "リクエスト方式が間違っています";
                let response_body = response.as_bytes();
                let response_header = format!("HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Length: {}\r\n\r\n",response_body.len());
                let full_response = [response_header.as_bytes(), response_body].concat();
                stream.write_all(&full_response).await.unwrap();
                stream.flush().await.unwrap();
            }
        }else{
            let file_path = if url_parts.len() > 1 && !url_parts[1].is_empty() {
                format!("{}static/{}", html_path, url_parts.iter().skip(1).map(|s| *s).collect::<Vec<&str>>().join("/"))
            } else {
                format!("{}static/index.html", html_path)
            };
            let mut file = match File::open(&file_path).await {
                Ok(file) => file,
                Err(_) => {
                    let redirect_file_path = format!("{}static/redirect.html", html_path);
                    File::open(&redirect_file_path).await.unwrap()
                }
            };
            let mut contents = String::new();
            file.read_to_string(&mut contents).await.unwrap();
            stream.write_all(b"HTTP/1.1 200 OK\r\n\r\n").await.unwrap();
            stream.write_all(contents.as_bytes()).await.unwrap();
            stream.flush().await.unwrap();
        }
    } else if request_lines[0].contains("POST") {
        let body_str = String::from_utf8_lossy(&request_buf[..size]);
        let body_lines: Vec<&str> = body_str.lines().collect();
        match serde_json::from_str::<HashMap<String, String>>(body_lines[body_lines.len() - 1]) {
            Ok(consultation_json) => {
                info!("受信したJSONデータ: {:?}", consultation_json);
                if _get_api_list.iter().any(|api| api == accessed_url) {
                    if accessed_url == "make_model" {
                        if let (Some(model_name), Some(learning_file), Some(extensions), Some(make_user)) = (
                            consultation_json.get("model_name").map(String::as_str),
                            consultation_json.get("Learning_File").map(String::as_str),
                            consultation_json.get("Extensions").map(String::as_str),
                            consultation_json.get("make_user").map(String::as_str),
                        ) {
                            info!(
                                "情報を取得しました: モデル名: {}, 学習ファイル: {}, 仕様拡張機能: {}, 制作者: {}",
                                model_name, learning_file, extensions, make_user
                            );
                            // ここにモデルの作成処理を追加
                            stream.write_all(return_message("Success", 200, "bad").as_bytes()).await.unwrap();
                            stream.flush().await.unwrap();
                        } else {
                            stream.write_all(return_message("パラメーターが不足しています", 400, "bad").as_bytes()).await.unwrap();
                            stream.flush().await.unwrap();
                        }
                    } else if accessed_url == "learning" {
                        if let (Some(model_name), Some(learning_file), Some(extensions)) = (
                            consultation_json.get("model_name").map(String::as_str),
                            consultation_json.get("Learning_File").map(String::as_str),
                            consultation_json.get("Extensions").map(String::as_str),
                        ) {
                            info!(
                                "情報を取得しました: モデル名: {}, 学習ファイル: {}, 仕様拡張機能: {}",
                                model_name, learning_file, extensions
                            );
                            stream.write_all(return_message("Success", 200, "good").as_bytes()).await.unwrap();
                            stream.flush().await.unwrap();
                        } else {
                            stream.write_all(return_message("パラメーターが不足しています", 400, "bad").as_bytes()).await.unwrap();
                            stream.flush().await.unwrap();
                        }
                    } else {
                        stream.write_all(return_message("リクエスト方式が間違っています", 400, "bad").as_bytes()).await.unwrap();
                        stream.flush().await.unwrap();
                    }
                } else {
                    stream.write_all(return_message("APIが見つかりません", 405, "bad").as_bytes()).await.unwrap();
                    stream.flush().await.unwrap();
                }
            }
            Err(e) => {
                eprintln!("JSONパースエラー: {}", e);
                stream.write_all(return_message("Bad Request", 400, "bad").as_bytes()).await.unwrap();
                stream.flush().await.unwrap();
            }
        }
    }
}
pub fn return_message(response:&str,response_code:u16,bad_good:&str)->String{
    let response_body = response.as_bytes();
    let response_header = format!("HTTP/1.1 {} {} Request\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Length: {}\r\n\r\n",response_code,bad_good,response_body.len());
    let full_response = [response_header.as_bytes(), response_body].concat();
    return std::str::from_utf8(&full_response).unwrap().to_string();   
}