use rayon::ThreadPoolBuildError;

#[allow(dead_code)]
pub fn set_max_threads(n: usize) -> Result<(), ThreadPoolBuildError> {
    rayon::ThreadPoolBuilder::new().num_threads(n).build_global()
}

#[cfg(test)]
mod tests {
    use std::error::Error;
    use crate::threads::set_max_threads;

    #[test]
    fn test_set_max_threads() -> Result<(), Box<dyn Error>> {
        set_max_threads(0)?;
        Ok(())
    }
}