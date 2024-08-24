use log::info;
use pyo3::prelude::*;

// Pythonの関数を呼び出す
pub fn lstm(consultation_json: &str) -> Result<String, PyErr> {
    info!("Start LSTM data{}", consultation_json);
    Python::with_gil(|py| {
        let sys = py.import("sys")?;
        sys.getattr("path")?.call_method1("append", ("/path/to/Python/scripts",))?; // Replace "/path/to/Python/scripts" with the actual path to your Python scripts
        let preproc_module = py.import("Preprocessing.RNN")?;
        Ok::<String, PyErr>("your_value".to_string())
    })?;
    Ok("your_value".to_string())
}