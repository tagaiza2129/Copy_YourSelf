extern crate getopts;
mod command_line;
use std::env;
fn main() {
    command_line::option_add("d".to_string(), "device".to_string(), "CPU".to_string(), "デバイスを指定します".to_string(),"DEVICE".to_string());
    command_line::option_add("e".to_string(),"epoch".to_string(),"10".to_string(),"学習回数を指定します".to_string(),"EPOCH".to_string());
    command_line::option_add("b".to_string(),"batch".to_string(),"100".to_string(),"バッチサイズを指定します".to_string(),"BATCH".to_string());
    command_line::option_add("l".to_string(),"Lerning_mode".to_string(), "RNN".to_string(),"学習モードを指定します".to_string(),"MODE".to_string());
    command_line::option_add("s".to_string(),"server_multi_processing".to_string(),"False".to_string(),"複数PCで学習するかをしています".to_string(),"True/False".to_string());
    let args: Vec<String> = env::args().collect();
    let _command_line_options=command_line::run_command_line(args);
    println!("{:?}",_command_line_options);
    // GUIが使えるかどうかの判定
    if cfg!(feature = "gui")&& "GUI_ENABLED"== "True" {
        println!("GUI は有効です");
    } else {
        println!("GUI is disabled");
    }
}