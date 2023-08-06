use std::error::Error;
use std::result::Result;
use polars_core::prelude::*;
use polars_lazy::prelude::*;
use rayon::prelude::*;
use crate::file::*;
use crate::gz::*;
use crate::{ok};
use crate::pl::*;
use crate::zip::*;

pub fn mean_count_reuse(df: &mut DataFrame, col_time: &str, str_slice_n: u64, expr: Expr) -> polars_core::error::Result<DataFrame> {
    df.try_apply("TIME", |s: &Series| {
        Ok(s.utf8()?.str_slice(0, Some(str_slice_n)).unwrap())
    })?;
    df.clone().lazy().groupby(
        [col("DEVICE_ID"), col("SENSOR_ID"), col(col_time)])
        .agg([
            col("LAT").first(),
            col("LON").first(),
            expr
        ])
        .sort("DEVICE_ID", Default::default())
        .sort("SENSOR_ID", Default::default())
        .sort(col_time, Default::default())
        .collect()
}

pub fn df_mean(df: &mut DataFrame, col_time: &str, str_slice_n: u64) -> polars_core::error::Result<DataFrame> {
    let expr = col("VALUE").mean().alias("VALUE_mean");
    mean_count_reuse(df, col_time, str_slice_n, expr)
}

pub fn df_count(df: &mut DataFrame, col_time: &str, str_slice_n: u64) -> polars_core::error::Result<DataFrame> {
    let expr = col("DEVICE_ID").count().alias("DEVICE_ID_count");
    mean_count_reuse(df, col_time, str_slice_n, expr)
}

#[allow(dead_code)]
pub fn gz_to_parquet(filename: String, bytes: Vec<u8>) -> Result<(), Box<dyn Error>> {
    if !filename.contains("_all.csv.gz") { return Ok(()); }
    println!("csv_gz {:?}", filename);
    let bytes_csv = decompress_gz_bytes(&bytes)?;
    let df = bytes_csv_to_df(&bytes_csv)?;
    // 4.zip 2.15s 也是需要一點時間，但為了正確性可能很難省
    let df_unique = df_unique(&df, vec!["DEVICE_ID", "SENSOR_ID", "TIME", "VALUE"])?;
    // hourly
    let mut df = df_unique.clone();
    let mut df = df_mean(&mut df, "TIME", 13)?;
    df_to_parquet(&mut df, format!("./data/parquet/{}_hourly.parquet", filename).as_str())?;
    println!("hourly df {:?}", df);
    // daily
    let mut df = df_unique.clone();
    let mut df = df_mean(&mut df, "TIME", 10)?;
    df_to_parquet(&mut df, format!("./data/parquet/{}_daily.parquet", filename).as_str())?;
    // count
    let mut df = df_unique;
    let mut df = df_count(&mut df, "TIME", 10)?;
    df_to_parquet(&mut df, format!("./data/parquet/{}_count.parquet", filename).as_str())?;
    Ok(())
}

#[allow(dead_code)]
pub fn gz_to_csv(filename: String, bytes_gz: Vec<u8>, target_directory: &str) -> Result<(), Box<dyn Error>> {
    if !filename.contains("_all.csv.gz") { return Ok(()); }
    println!("csv_gz {:?}", filename);
    let bytes_csv = decompress_gz_bytes(&bytes_gz)?;
    let df = bytes_csv_to_df(&bytes_csv)?;
    // 4.zip 2.15s 也是需要一點時間，但為了正確性可能很難省
    let mut df_unique = df_unique(&df, vec!["DEVICE_ID", "SENSOR_ID", "TIME", "VALUE"])?;
    // hourly
    // let mut df = ;
    let mut df = df_mean(&mut df_unique.clone(), "TIME", 13)?;
    padding_zero_hourly(&mut df, "TIME")?;
    df_to_csv(&mut df, format!("{}{}_table_hourly-mean.csv", target_directory, filename))?;
    // daily
    let mut df = df_mean(&mut df_unique.clone(), "TIME", 10)?;
    padding_zero_daily(&mut df, "TIME")?;
    df_to_csv(&mut df, format!("{}{}_table_daily-mean.csv", target_directory, filename))?;
    // count
    let mut df = df_count(&mut df_unique, "TIME", 10)?;
    padding_zero_daily(&mut df, "TIME")?;
    df_to_csv(&mut df, format!("{}{}_table_daily-count.csv", target_directory, filename))?;
    Ok(())
}

#[allow(dead_code)]
pub fn zip_decompress_callback(filename: &str, bytes: &Vec<u8>) -> Result<(), Box<dyn Error>> {
    let mut df = bytes_csv_to_df(&decompress_gz_bytes(bytes)?)?;
    df_to_parquet(&mut df, format!("{}.parquet", filename).as_str())?;
    Ok(())
}

pub fn main_tainan() -> Result<(), Box<dyn Error>> {
    let v_all_zip = ls("./data/tainan/zip_few/*.zip")?;
    v_all_zip.par_iter().for_each(|zip_path| {
        println!("\n== process .zip file {} ==\n", zip_path);
        let z = ok!(zip_stream(zip_path));
        z.into_iter().for_each(|tup_filename_bytes| {
            ok!(gz_to_csv(tup_filename_bytes.0, tup_filename_bytes.1,"./data/csv_daily/"));
        });
    });
    // aggregate_csv("./data/csv_daily/*2022-04*_count.csv", "./data/csv_monthly/table_daily-count_month_2022-04_sensor_all.csv", "DEVICE_ID,SENSOR_ID,TIME,LAT,LON,DEVICE_ID_count\n")?;
    // aggregate_csv("./data/csv_daily/*2022-04*_hourly.csv", "./data/csv_monthly/table_hourly-mean_month_2022-04_sensor_all.csv", "DEVICE_ID,SENSOR_ID,TIME,LAT,LON,VALUE_hourly_mean\n")?;
    // aggregate_csv("./data/csv_daily/*2022-04*_daily.csv", "./data/csv_monthly/table_daily-mean_month_2022-04_sensor_all.csv", "DEVICE_ID,SENSOR_ID,TIME,LAT,LON,VALUE_daily_mean\n")?;

    loop_filter_to_csv("./data/csv_daily/*2022-04*_hourly-mean*.csv", "./data/table_agg_ext_csv/")?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use std::error::Error;
    use crate::main_tainan;

    #[test]
    fn test_main_tainan() -> Result<(), Box<dyn Error>> {
        main_tainan()
    }
}
