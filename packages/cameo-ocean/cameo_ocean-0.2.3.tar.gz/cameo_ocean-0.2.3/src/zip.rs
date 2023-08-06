use std::error::Error;
use std::fs;
use std::fs::File;
use std::io;
use std::io::{BufReader, Read};
use std::result::Result;

use zip::read::read_zipfile_from_stream;

use crate::{ok_continue, ok_none, some_continue, some_none};
use crate::file::mkdir;

#[allow(dead_code)]
fn unzip_to_directory(zip_path: &str, unzip_dir: &str) -> Result<(), Box<dyn Error>> {
    mkdir(unzip_dir)?;
    let file = File::open(&zip_path)?;
    let mut archive = zip::ZipArchive::new(file)?;
    for i in 0..archive.len() {
        let mut extract = ok_continue!(archive.by_index(i));
        let t_filename = some_continue!(extract.enclosed_name());
        let t_path = format!("{}{}", &unzip_dir, t_filename.display());
        if (*extract.name()).ends_with('/') {
            println!("File {} extracted to {}", i, t_path);
            ok_continue!(fs::create_dir_all(&t_path));
        } else {
            println!("File {} extracted to {} ({} bytes)", i, t_path, extract.size());
            let mut f = ok_continue!(fs::File::create(&t_path));
            ok_continue!(io::copy(&mut extract, &mut f));
        }
        #[cfg(unix)]
        {
            use std::os::unix::fs::PermissionsExt;
            let mode = some_continue!(extract.unix_mode());
            ok_continue!(fs::set_permissions(&t_path, fs::Permissions::from_mode(mode)));
        }
    }
    Ok(())
}

#[allow(dead_code)]
fn stream_unzip(zip_path: &str, f_consume: fn(&str, &Vec<u8>)) -> Result<(), Box<dyn Error>> {
    let f = File::open(&zip_path)?;
    let mut buf_reader = BufReader::new(f);
    while let Ok(Some(mut zipfile)) = read_zipfile_from_stream(&mut buf_reader) {
        let mut bytes: Vec<u8> = Vec::new();
        ok_continue!(zipfile.read_to_end(&mut bytes));
        f_consume(zipfile.name(), &bytes);
    }
    Ok(())
}

pub struct ZipStream {
    buf_reader: BufReader<File>,
}

impl ZipStream {
    pub fn new(breader: BufReader<File>) -> Self {
        ZipStream {
            buf_reader: breader,
        }
    }
}

impl Iterator for ZipStream {
    type Item = (String, Vec<u8>);
    fn next(&mut self) -> Option<Self::Item> {
        let mut zipfile = some_none!(ok_none!(read_zipfile_from_stream(&mut self.buf_reader)));
        let mut bytes: Vec<u8> = Vec::new();
        match zipfile.read_to_end(&mut bytes) {
            Ok(_) => Some((zipfile.name().to_string(), bytes)),
            Err(_) => None,
        }
    }
}

pub fn zip_stream(s_path: &str) -> Result<ZipStream, Box<dyn Error>> {
    Ok(ZipStream::new(BufReader::new(File::open(s_path)?)))
}

#[cfg(test)]
mod tests {
    use std::error::Error;
    use std::fs::File;
    use std::io::{BufReader};
    use std::result::Result;

    use crate::zip::{unzip_to_directory, ZipStream};

    #[test]
    fn test_unzip() -> Result<(), Box<dyn Error>> {
        unzip_to_directory("./data/tainan/zip/0.zip", "./data/tainan/unzip/0/")
    }

    // #[test]
    // fn test_unzip_dir() -> Result<(), ThreadPoolBuildError> {
    //     set_max_threads(10)
    // }

    // #[test]
    // fn test_串流解zip() -> Result<(), Box<dyn Error>> {
    //     // set_max_threads(0)?;
    //     stream_unzip("./data/tainan/zip/0.zip", tainan::zip_decompress_callback)
    // }

    #[test]
    fn test_zip_stream() -> Result<(), Box<dyn Error>> {
        let s_path = "./data/tainan/zip/0.zip";
        for (filename, bytes) in ZipStream::new(
            BufReader::new(File::open(s_path)?)) {
            println!("test_zip_stream: {:?},{:?}", filename, bytes.len());
        }
        Ok(())
    }
}