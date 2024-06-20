use std::collections::HashMap;
use getopts::Options;
//参考資料集
//Rustでコマンドライン引数をパースする方法
//https://ubnt-intrepid.hatenablog.com/entry/rust_commandline_parsers
use once_cell::sync::Lazy;
static OPTION_LIST: Lazy<std::sync::Mutex<Vec<HashMap<String, String>>>> = Lazy::new(|| std::sync::Mutex::new(Vec::new()));
pub fn option_add(short_name: String, long_name: String, default_value: String, description: String,hint: String){
    let mut map: HashMap<String, String> = HashMap::new();
    map.insert("short_name".to_string(), short_name);
    map.insert("full_name".to_string(), long_name);
    map.insert("description".to_string(), description);
    map.insert("default_value".to_string(), default_value);
    map.insert("hint".to_string(), hint);
    OPTION_LIST.lock().unwrap().push(map);
}

fn print_usage(program: &str, opts: Options) {
    let brief = format!("Usage: {} FILE [options]", program);
    print!("{}", opts.usage(&brief));
}
pub fn run_command_line(args:Vec<String>) -> HashMap<String, String> {
    // コマンドライン引数の処理
    let program = args[0].clone();
    let mut return_options: HashMap<String, String> = HashMap::new();

    let mut opts = Options::new();
    for option in OPTION_LIST.lock().unwrap().iter() {
        opts.optopt(&option["short_name"], &option["full_name"], &option["description"], &option["hint"]);
    }
    opts.optflag("h", "help", "このメニューを表示します");
    let matches = match opts.parse(&args[1..]) {
        Ok(m) => { m }
        Err(f) => {
            eprintln!("Failed to parse command line options: {}", f);
            std::process::exit(1);
        }
    };
    if matches.opt_present("h") {
        print_usage(&program, opts);
        std::process::exit(1);
    }
    //for文でオプションが入れられてたらそのままに、入れられていなかったらデフォルト値を入れる
    for option in OPTION_LIST.lock().unwrap().iter(){
        let option_short_name = &option["short_name"];
        let option_full_name = &option["full_name"];
        let option_value = matches.opt_str(&option_short_name);
        if let Some(value) = option_value {
            return_options.insert(option_full_name.to_string(), value);
        }else {
            let default_value = &option["default_value"];
            return_options.insert(option_full_name.to_string(),default_value.to_string());
        }
    }
    //返すためのリスト、mut_return_optionsをメイン関数に返す
    return return_options;
}