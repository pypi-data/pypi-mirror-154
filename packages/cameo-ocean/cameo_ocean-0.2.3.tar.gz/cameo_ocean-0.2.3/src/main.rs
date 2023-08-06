use std::error::Error;
use std::result::Result;
use crate::tainan::main_tainan;

mod file;
mod pl;
mod zip;
mod threads;
mod gz;
mod string;
mod r#macro;
mod api;
mod py;
mod tainan;

fn main() -> Result<(), Box<dyn Error>> {
    println!("hi rust main()");
    main_tainan()?;
    Ok(())
}
