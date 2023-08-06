use actix_web::{get, HttpRequest, HttpResponse, post, Responder};

use crate::{ok_http, string};
use crate::file::{append_file, mkdir, touch};
use crate::string::{append_str, date, date_hour_min};

#[get("/api/hi/")]
pub(crate) async fn hi() -> impl Responder {
    HttpResponse::Ok().body("hi rust")
}

// 2022-05-29 百川海高速錄製所有 http post to msgpack 的程式碼
#[post("/api/log_msgpack/")]

// pub(crate) async fn high_speed_log_all_http_post_to_msgpack(req: HttpRequest, body: String)
//     -> impl Responder {
pub(crate) async fn high_speed_log_all_http_post_to_msgpack
(req: HttpRequest, body: String) -> impl Responder {
    let map_header = req.headers();
    let mut result: String = "{".to_string();
    result.push_str(r#""headers":""#);
    for key in map_header.keys() {
        append_str(&mut result, map_header, key.as_str());
    }
    result.push_str(r#"","body":"#);
    result.push_str(&body);
    result.push('}');
    if let Some(bytes) = string::json_to_bytes(&result) {
        let directory = format!("./data/log_msgpack/{}/", date());
        let filename = format!("{}.msgpack", date_hour_min());
        ok_http!(mkdir(&directory),"err api.rs high_speed_log_all_http_post_to_msgpack mkdir");
        let path = format!("{}{}", &directory, &filename);
        ok_http!(touch(&path),"err api.rs high_speed_log_all_http_post_to_msgpack touch");
        ok_http!(append_file(&path, &bytes),"err api.rs high_speed_log_all_http_post_to_msgpack append_file");
        HttpResponse::Ok().body(path)
    } else {
        HttpResponse::Ok().body("error, api.rs, log_msgpack")
    }
}

#[post("/api/echo/")]
pub(crate) async fn echo(body: String) -> impl Responder {
    HttpResponse::Ok().body(body)
}
