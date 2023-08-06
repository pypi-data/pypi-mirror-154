use std::str;
use actix_web::http::header::HeaderMap;
use serde_json::Value;
use substring::Substring;
use crate::{ok, ok_none,some};

pub fn _bytes_to_string(bytes: &[u8]) -> String {
    println!("v_u8_to_string");
    return match str::from_utf8(bytes) {
        Ok(s) => s.to_string(),
        Err(e) => {
            println!("v_u8_to_string, err, {:?}", e);
            "".to_string()
        }
    };
}

pub fn _strs_to_strings(v: Vec<&str>) -> Vec<String> {
    v.iter().map(|s| s.to_string()).collect()
}

pub fn json_to_bytes(result: &str) -> Option<Vec<u8>> {
    let v: Value = ok_none!(serde_json::from_str(result));
    let bytes = ok_none!(rmp_serde::to_vec(&v));
    Some(bytes)
}

pub fn time_slice(i: usize) -> String {
    format!("{:?}", chrono::offset::Local::now())
        .substring(0, i)
        .replace(':', "_")
        .replace('T', "_")
}

pub fn date() -> String {
    time_slice(10)
}

pub fn date_hour_min() -> String {
    time_slice(16)
}

pub fn append_str(result: &mut String, map: &HeaderMap, key: &str) {
    result.push_str(format!("{}: {}\\n", key, ok!(some!(map.get(key)).to_str())).as_str());
}
