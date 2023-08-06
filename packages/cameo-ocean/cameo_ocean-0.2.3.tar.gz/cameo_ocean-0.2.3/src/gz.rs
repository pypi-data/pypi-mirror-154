use std::error::Error;
use std::io::Read;
use std::result::Result;

use flate2::read::GzDecoder;

use crate::file::bytes_to_file;
use crate::file::read_file;

pub fn gz_file_to_bytes(path: &str) -> Result<Vec<u8>, Box<dyn Error>> {
    let vu8 = read_file(path)?;
    let mut gz_decoder = GzDecoder::new(&*vu8);
    let mut bytes: Vec<u8> = Vec::new();
    gz_decoder.read_to_end(&mut bytes)?;
    Ok(bytes)
}

pub fn decompress_gz_bytes(bytes: &Vec<u8>) -> Result<Vec<u8>, Box<dyn Error>> {
    let mut gz_decoder = GzDecoder::new(bytes.as_slice());
    let mut bytes: Vec<u8> = Vec::new();
    gz_decoder.read_to_end(&mut bytes)?;
    Ok(bytes)
}

#[allow(dead_code)]
pub fn decompress_gz_file(s: &str, t: &str) -> Result<(), Box<dyn Error>> {
    bytes_to_file(&gz_file_to_bytes(s)?, t)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use std::error::Error;
    use std::result::Result;

    use crate::file::mkdir;
    use crate::gz::decompress_gz_file;

    #[test]
    fn test_decompress_gz() -> Result<(), Box<dyn Error>> {
        mkdir("./data/tainan/csv/")?;
        decompress_gz_file("./data/tainan/unzip/673_2022-04-01_all.csv.gz",
                           "./data/tainan/csv/673_2022-04-01_all.csv")?;
        Ok(())
    }
}
