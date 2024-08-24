use pyo3::prelude::*;
use pyo3::types::IntoPyDict;

pub fn lstm(consultation_json: &str) -> String {
    Python::with_gil(|py| {
        let sys = py.import("sys").unwrap();
        let sys_path: &str = sys.get("path").unwrap().extract().unwrap();
        let sys_path = sys_path.to_string();
        let sys_path = sys_path + "/src";
        sys.setattr("path", sys_path).unwrap();
        let lstm = py.import("lstm").unwrap();
        let args = IntoPyDict::new(py);
        args.set_item("consultation_json", consultation_json).unwrap();
        let response = lstm.call_method("main", (args,), None).unwrap();
        response.extract().unwrap()
    })
}