use std::process::Command;
use log::info;

pub fn check_app_installed(app_name: &str) -> bool {
    let output = Command::new(app_name)
        .arg("--version")
        .output();
    info!("{}がインストールされているか確認します",app_name);
    info!("{:?}",output);
    match output {
        Ok(output) => output.status.success(),
        Err(_) => false,
    }
}