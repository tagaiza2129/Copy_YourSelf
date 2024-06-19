extern crate getopts;
use std::env;
use getopts::Options;
//参考資料集
//Rustでコマンドライン引数をパースする方法
//https://ubnt-intrepid.hatenablog.com/entry/rust_commandline_parsers
fn do_work(inp: &str, out: Option<String>) {
    println!("{}", inp);
    match out {
        Some(x) => println!("{}", x),
        None => println!("No Output"),
    }
}

fn print_usage(program: &str, opts: Options) {
    let brief = format!("Usage: {} FILE [options]", program);
    print!("{}", opts.usage(&brief));
}
fn command_line() {
    // コマンドライン引数の処理
    let args: Vec<String> = env::args().collect();
    let program = args[0].clone();

    let mut opts = Options::new();
    opts.optopt("o", "output", "set output file name", "NAME");
    opts.optflag("h", "help", "print this help menu");
    let matches = match opts.parse(&args[1..]) {
        Ok(m) => { m }
        Err(f) => {
            eprintln!("Failed to parse command line options: {}", f);
            return;
        }
    };
    if matches.opt_present("h") {
        print_usage(&program, opts);
        return;
    }
    let output = matches.opt_str("o");
    let input = if !matches.free.is_empty() {
        matches.free[0].clone()
    } else {
        print_usage(&program, opts);
        return;
    };
    do_work(&input, output);
}
fn main() {
    let _command_line_options=command_line();
    // GUIが使えるかどうかの判定
    if cfg!(feature = "gui")&& "GUI_ENABLED"== "True" {
        println!("GUI は有効です");
    } else {
        println!("GUI is disabled");
    }
}
