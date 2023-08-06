// use std::fs::OpenOptions;
// use std::io::Write;
// use actix_web::http::header::HeaderMap;
//
// use serde_json::Value;
// use substring::Substring;
// use crate::{ok, okn, some, string};
//
// pub fn append_str(result: &mut String, map: &HeaderMap, key: &str) {
//     result.push_str(format!("{}: {}\\n", key, ok!(some!(map.get(key)).to_str())).as_str());
// }
//
//
//
//
//
