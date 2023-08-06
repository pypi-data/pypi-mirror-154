use std::error::Error;
use std::fs;
use std::fs::File;
use std::fs::OpenOptions;
use std::io::{BufReader, Write};
use std::io::{BufRead};
use std::io::Read;
use std::path::Path;
use std::result::Result;

use glob::glob;
use polars_core::frame::DataFrame;
use polars_lazy::dsl::{col, IntoLazy};
use polars_lazy::prelude::{lit};

use crate::{ok, ok_continue};
use crate::pl::{df_to_csv, pl_read_csv};

#[allow(dead_code)]
pub fn rmdir(dir: &str) -> std::io::Result<()> {
    fs::remove_dir_all(dir)
}

pub fn mkdir(directory: &str) -> std::io::Result<()> {
    fs::create_dir_all(directory)
}

pub fn path_to_str(path: &Path) -> Result<&str, Box<dyn Error>> {
    Ok(path.as_os_str().to_str().ok_or("err path_to_str")?)
}

pub fn mkdir_path(path: &str) -> Result<&str, Box<dyn Error>> {
    let dir = Path::new(path).parent().ok_or("err mkdir_path parent")?;
    mkdir(path_to_str(dir)?)?;
    Ok(path)
}

pub fn extract_filename_from_path(path: &str) -> Result<String, Box<dyn Error>> {
    Ok(Path::new(&path).file_name().ok_or("")?.to_str().ok_or("")?.to_string())
}

pub fn ls(dir_wildcards: &str) -> Result<Vec<String>, Box<dyn Error>> {
    let mut v: Vec<String> = Vec::new();
    for entry in glob(dir_wildcards)? {
        match entry {
            Ok(path) => v.push(path.display().to_string()),
            Err(e) => println!("{:?}", e),
        }
    }
    Ok(v)
}

pub fn touch(path: &str) -> Result<(), Box<dyn Error>> {
    OpenOptions::new().create(true).write(true).open(Path::new(path))?;
    Ok(())
}

pub fn read_file(path: &str) -> Result<Vec<u8>, Box<dyn Error>> {
    let f = File::open(path)?;
    let mut reader = BufReader::new(f);
    let mut v_u8 = Vec::new();
    reader.read_to_end(&mut v_u8)?;
    Ok(v_u8)
}

pub fn _exists(path: &str) -> bool {
    Path::new(path).exists()
}

pub fn bytes_to_file(bytes: &[u8], target_path: &str) -> std::io::Result<()> {
    let mut f = File::create(target_path)?;
    f.write_all(bytes)
}

pub fn _open_file_append_mode(path: &str) -> Result<File, Box<dyn Error>> {
    mkdir_path(path)?;
    touch(path)?;
    Ok(OpenOptions::new().write(true).append(true).open(path)?)
}

pub fn append_file(path: &String, bytes: &[u8]) -> std::io::Result<()> {
    let mut file = OpenOptions::new()
        .write(true)
        .append(true)
        .open(path)
        .expect(&*format!("err reuse.rs append_file, path:{}", path));
    file.write_all(bytes)
}

// pub fn f_println_df(df:DataFrame){
//     println!("f_println_df {:?}",df);
// }

pub fn loop_filter_to_csv(source_wildcard: &str, target_directory: &str) -> Result<(), Box<dyn Error>> {
    let v_csv = ls(source_wildcard)?;
    for path in v_csv {
        ok_continue!(once_filter_to_csv(target_directory, path));
    };
    Ok(())
}

fn once_filter_to_csv(t_directory: &str, path: String) -> Result<(), Box<dyn Error>> {
    let df_all = pl_read_csv(path.as_str())?;
    let filename = extract_filename_from_path(path.as_str())?;
    let v_select_columns = vec!["DEVICE_ID", "SENSOR_ID", "TIME", "LAT", "LON", "VALUE_mean"];
    // todo 還要向外再抽兩層出去，抽出 filter_col, eq, postfix 要消滅(轉小寫即可組合出來)
    filter_to_csv(t_directory, &df_all, &filename, &v_select_columns, "SENSOR_ID", "voc", "_sensor_id_voc.csv")?;
    filter_to_csv(t_directory, &df_all, &filename, &v_select_columns, "SENSOR_ID", "pm2_5", "_sensor_id_pm2_5.csv")?;
    Ok(())
}

fn filter_to_csv(t_directory: &str, df_all: &DataFrame, filename: &String, v_sel_columns: &[&str], filter_col: &str, eq: &str, postfix: &str) -> Result<(), Box<dyn Error>> {
    let mut df = df_filter_eq(df_all, v_sel_columns, filter_col, eq)?;
    df_to_csv(&mut df, format!("{}{}{}", t_directory, filename, postfix))?;
    Ok(())
}

fn df_filter_eq(df: &DataFrame, v_sel_col: &[&str], filter_col: &str, eq: &str) -> polars_core::error::Result<DataFrame> {
    df.clone().lazy()
        .select(v_sel_col.iter().map(|s| { col(s) }).collect::<Vec<_>>())
        .filter(col(filter_col).eq(lit(eq)))
        .collect()
}

pub fn _aggregate_csv(source_wildcard: &str, target_path: &str, header: &str) -> Result<(), Box<dyn Error>> {
    let v_csv = ls(source_wildcard)?;
    fs::remove_file(target_path)?;
    let mut f = _open_file_append_mode(target_path)?;
    f.write_all(header.as_bytes())?;
    v_csv.into_iter().for_each(|csv_filename| {
        let lines = BufReader::new(ok!(File::open(csv_filename))).lines();
        for line in lines.skip(1) {
            ok!(f.write_all(line.unwrap().as_bytes()));
            ok!(f.write_all(b"\n"));
        }

        // println!("lines:{:?}",lines.count());
    });
    Ok(())
    // if let Ok(lines) = read_lines("./hosts") {
    //     // Consumes the iterator, returns an (Optional) String
    //     for line in lines {
    //         if let Ok(ip) = line {
    //             println!("{}", ip);
    //         }
    //     }
    // }
}

#[cfg(test)]
mod tests {
    use std::error::Error;
    use std::result::Result;

    use crate::file::{ls, mkdir, read_file, rmdir, touch};

    #[test]
    fn test_mkdir_same_dir_twice() -> Result<(), Box<dyn Error>> {
        mkdir("./data/test_mkdir_same_dir_twice/")?;
        mkdir("./data/test_mkdir_same_dir_twice/")?;
        rmdir("./data/test_mkdir_same_dir_twice/")?;
        Ok(())
    }

    #[test]
    fn test_ls() -> Result<(), Box<dyn Error>> {
        mkdir("./data/test_ls/")?;
        touch("./data/test_ls/001.txt")?;
        touch("./data/test_ls/002.txt")?;
        touch("./data/test_ls/003.txt")?;
        println!("test_ls, {:?}", ls("./data/test_ls/*"));
        rmdir("./data/test_ls/")?;
        Ok(())
    }

    #[test]
    fn test_read_file() -> Result<(), Box<dyn Error>> {
        read_file("data/tainan/unzip/673_2022-04-01_all.csv.gz")?;
        Ok(())
    }
}