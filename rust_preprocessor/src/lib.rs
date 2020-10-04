use pyo3::{Python, PyResult};
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use std::fs::File;
use std::error::Error;
use std::io::{BufReader, BufWriter, Write};
use pyo3::types::{PyList, PyString};

mod corpus;

#[pymodule]
fn corpus_processor(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(process))?;
    Ok(())
}

#[pyfunction]
fn process(src_list: &PyList, des: String, low: bool) -> PyResult<bool> {
    let mut srcs = Vec::new();
    for src in src_list.iter() {
        if let Ok(string) = src.extract::<&PyString>() {
            srcs.push(string.to_string());
        }
    }
    match process_rs(srcs, des, low) {
        Ok(_) => Ok(true),
        Err(_) => Ok(false),
    }
}

fn process_rs(src: Vec<String>, des: String, low: bool) -> Result<(), Box<dyn Error>> {
    let mut writer = BufWriter::new(File::create(des)?);
    for src in src {
        let src = File::open(src)?;
        corpus::corpus_preprocess(BufReader::new(src), &mut writer, low)?;
    }
    writer.flush()?;
    Ok(())
}
