use std::error::Error;
use std::fs::File;
use std::io::{BufWriter, Cursor};
use std::result::Result;

use polars::export::arrow::io::parquet::write::CompressionOptions;
use polars::prelude::*;

use crate::file::mkdir_path;
use crate::string::_strs_to_strings;

pub fn bytes_csv_to_df(vu8: &Vec<u8>) -> polars_core::error::Result<DataFrame> {
    let c = Box::new(Cursor::new(vu8));
    CsvReader::new(c).finish()
}

pub fn pl_read_csv(path: &str) -> polars_core::error::Result<DataFrame> {
    let file = File::open(path).expect("err pl.rs, read_csv, could not open file");
    CsvReader::new(file)
        .infer_schema(None)
        .has_header(true)
        .finish()
}

pub fn df_to_parquet(df: &mut DataFrame, path: &str) -> Result<(), Box<dyn Error>> {
    ParquetWriter::new(BufWriter::new(File::create(mkdir_path(path)?)?))
        .with_compression(CompressionOptions::Zstd(None))
        .with_statistics(true)
        .finish(df)?;
    Ok(())
}

pub fn df_to_csv(df: &mut DataFrame, path: String) -> Result<(), Box<dyn Error>> {
    CsvWriter::new(BufWriter::new(File::create(mkdir_path(&path)?)?))
        .has_header(true)
        .finish(df)?;
    Ok(())
}

pub fn df_unique(df: &DataFrame, v_columns: Vec<&str>) -> polars_core::error::Result<DataFrame> {
    df.unique(Some(&_strs_to_strings(v_columns)), UniqueKeepStrategy::First)
}

pub fn padding_zero_hourly(df: &mut DataFrame, col: &str) -> Result<(), Box<dyn Error>> {
    df.try_apply(col, |s: &Series| {
        s.utf8()?.replace(".......... ..", "$0:00:00")
    })?;
    Ok(())
}

pub fn padding_zero_daily(df: &mut DataFrame, col: &str) -> Result<(), Box<dyn Error>> {
    df.try_apply(col, |s: &Series| {
        s.utf8()?.replace("..........", "$0 00:00:00")
    })?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use std::error::Error;
    use std::result::Result;

    use crate::gz::gz_file_to_bytes;
    use crate::pl::{bytes_csv_to_df, df_to_parquet, pl_read_csv};

    #[test]
    fn test_vu8_to_df() -> Result<(), Box<dyn Error>> {
        let vu8 = gz_file_to_bytes("./data/tainan/unzip/673_2022-04-01_all.csv.gz")?;
        bytes_csv_to_df(&vu8)?;
        Ok(())
    }

    #[test]
    fn test_df_to_parquet() -> Result<(), Box<dyn Error>> {
        let mut df = pl_read_csv("./data/tainan/csv/673_2022-04-01_all.csv")?;
        df_to_parquet(&mut df, "./data/parquet/673_2022-04-01_all.parquet")
    }
}