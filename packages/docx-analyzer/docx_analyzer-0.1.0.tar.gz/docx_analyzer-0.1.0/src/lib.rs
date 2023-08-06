use pyo3::prelude::*;
use itertools::Itertools;
use regex::Regex;
use std::collections::VecDeque;
use std::fs;
use std::io;
use std::io::Read;
use std::ops::Not;
use std::path::Path;
use std::path::PathBuf;
use walkdir::WalkDir;

#[pyfunction]
fn analyze(path: String) -> PyResult<Vec<String>> {

    unpack_zip(path);

    let mut tags = Vec::new();
    for file in WalkDir::new("temp/") {
        let path = file.unwrap().path().to_owned();
        if path.is_file() {
            tags = [tags, analyze_doc(&path)].concat();
        };
    }

    let unique_tags: VecDeque<&String> = tags.iter().unique().collect();

    let validated_tags = validate_tags_and_make_fields(unique_tags);

    // clean temp folder
    fs::remove_dir_all("temp/").unwrap();

    validated_tags
}

#[pymodule]
fn docx_analyzer(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(analyze, m)?)?;
    Ok(())
}

fn validate_tags_and_make_fields(tags: VecDeque<&String>) -> PyResult<Vec<String>> {
    // let mut fields = Vec::new();
    let mut fields = Vec::new();
    for i in 0..tags.len() {
        let splitted: VecDeque<&str> = tags[i].split(".").collect();
        if splitted.len() == 2 {
            if splitted[0].is_empty().not() & splitted[1].is_empty().not() {
                fields.push(tags[i].to_owned());
            }
        }
    }
    Ok(fields)
}

fn unpack_zip(path: String) {
    let fname = std::path::Path::new(&path);
    let file = fs::File::open(&fname).unwrap();

    let mut archive = zip::ZipArchive::new(file).unwrap();

    for i in 0..archive.len() {
        let mut file = archive.by_index(i).unwrap();
        let outpath = match file.enclosed_name() {
            Some(path) => path.to_owned(),
            None => continue,
        };

        if (*file.name()).ends_with('/') {
            fs::create_dir_all(&outpath).unwrap();
        } else {
            let outpath_new =
                PathBuf::from("temp/".to_owned() + outpath.file_name().unwrap().to_str().unwrap());
            if let Some(p) = outpath_new.parent() {
                if !p.exists() {
                    fs::create_dir_all(&p).unwrap();
                }
            }
            let mut outfile = fs::File::create(&outpath_new).unwrap();
            io::copy(&mut file, &mut outfile).unwrap();
        }
    }
}

fn analyze_doc(path: &Path) -> Vec<String> {
    let file = fs::File::open(&path).unwrap();

    let mut archive = zip::ZipArchive::new(file).unwrap();

    let mut doc_in_zip = archive.by_name("word/document.xml").unwrap();

    let mut buffer = String::from("");
    doc_in_zip.read_to_string(&mut buffer).unwrap();

    let s_slice: &str = &buffer[..];
    let doc = roxmltree::Document::parse(&s_slice).unwrap();

    let mut doc_xml_nodes = doc.descendants();

    let mut doc_text = String::new();

    loop {
        match doc_xml_nodes.next() {
            Some(x) => {
                if x.has_tag_name("t") {
                    doc_text.push_str(x.text().unwrap());
                }
            }
            None => break,
        }
    }

    let regex = Regex::new(r"(?:(^|[^\{])\{\{)([^\}]*?)(?:\}\}(?:($|[^\}])))").unwrap();
    let mut mat = regex.find_iter(&doc_text);

    let mut regex_res = String::new();

    loop {
        match mat.next() {
            Some(x) => {
                regex_res.push_str(x.as_str());
            }
            None => break,
        }
    }

    regex_res = regex_res
        .replace("{", "")
        .replace("}", "")
        .replace(",", "")
        .replace(")", "")
        .replace("(", "")
        .replace("/", "")
        .replace("_", "");

    let tags = regex_res.split_whitespace().map(str::to_string).collect();

    tags
}
