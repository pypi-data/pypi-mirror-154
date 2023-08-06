use std::env;
use actix_cors::Cors;
use actix_web::{App, HttpServer};
use pyo3::prelude::*;
use crate::api;

pub fn concat_host_port(host: &str, int_port: usize) -> String {
    let str_ip_port = format!("{}:{}", host, int_port);
    println!("cameo_ocean actix server at {}", str_ip_port);
    str_ip_port
}

fn print_current_directory() {
    let path = env::current_dir();
    println!("The current directory is {:?}", path);
}

fn print_cli() {
    println!("sh/curl.sh");
}

pub fn multiply(a: i32, b: i32) -> i32 {
    a * b
}

#[actix_rt::main]
#[pyfunction]
async fn actix_server(host: &str, int_port: usize) -> std::io::Result<()> {
    print_current_directory();
    print_cli();
    let http_server = HttpServer::new(|| {
        App::new()
            .wrap(
                Cors::default()
                    .send_wildcard()
                    .allow_any_method()
                    .allow_any_header()
                    .allow_any_origin()
                    .max_age(3600),
            )
            .service(api::high_speed_log_all_http_post_to_msgpack)
            .service(api::hi)
            .service(api::echo)
            .service(actix_files::Files::new("/data/", "./data/").show_files_listing())
    });
    http_server
        .bind(concat_host_port(host, int_port))?
        .run()
        .await
}

#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pyfunction]
pub fn py_multiply(a: i32, b: i32) -> PyResult<i32> {
    Ok(multiply(a, b))
}

#[pymodule]
fn cameo_ocean(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(actix_server, m)?)?;
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(py_multiply, m)?)?;
    Ok(())
}


