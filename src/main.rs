#![warn(clippy::all, rust_2018_idioms)]
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")] // no console window on windows

use std::env;
mod command_line;
fn main() -> eframe::Result<()> {
    // ビルドする際に以下のオプションを利用しないと23行目のif文が反応しない
    //--features "gui"
    command_line::option_add("d".to_string(), "device".to_string(), "CPU".to_string(), "デバイスを指定します".to_string(),"DEVICE".to_string());
    command_line::option_add("e".to_string(),"epoch".to_string(),"10".to_string(),"学習回数を指定します".to_string(),"EPOCH".to_string());
    command_line::option_add("b".to_string(),"batch".to_string(),"100".to_string(),"バッチサイズを指定します".to_string(),"BATCH".to_string());
    command_line::option_add("l".to_string(),"Lerning_mode".to_string(), "RNN".to_string(),"学習モードを指定します".to_string(),"MODE".to_string());
    command_line::option_add("s".to_string(),"server_multi_processing".to_string(),"False".to_string(),"複数PCで学習するかをしています".to_string(),"True/False".to_string());
    command_line::option_add("g".to_string(), "GUI_ENABLED".to_string(), "True".to_string(),"GUIかCUIで起動するかを選びます(SSH等のCUIしかない場合は無効)".to_string(),"GUI/CUI".to_string());
    let args: Vec<String> = env::args().collect();
    let _command_line_options=command_line::run_command_line(args);
    let _device = _command_line_options.get("device").unwrap();
    let _epoch = _command_line_options.get("epoch").unwrap();
    let _batch = _command_line_options.get("batch").unwrap();
    let _mode = _command_line_options.get("Lerning_mode").unwrap();
    let _server_multi_processing = _command_line_options.get("server_multi_processing").unwrap();
    let _gui = _command_line_options.get("GUI_ENABLED").unwrap();
    println!("{:?}",_command_line_options);
    // GUIが使えるかどうかの判定
    if cfg!(feature = "gui") && _gui == "True" {
        println!("GUI は有効です");
        println!("GUIアプリケーションを起動します");
        let native_options = eframe::NativeOptions {
            viewport: egui::ViewportBuilder::default()
                .with_inner_size([400.0, 300.0])
                .with_min_inner_size([300.0, 220.0])
                .with_icon(
                    eframe::icon_data::from_png_bytes(&include_bytes!("../assets/icon-256.png")[..])
                        .expect("Failed to load icon"),
                ),
            ..Default::default()
        };
        eframe::run_native("Copy Your Self", native_options, Box::new(|cc| Box::new(copy_your_self::TemplateApp::new(cc))))
    } else {
        println!("GUI は無効です");
        Ok(())
    }
}