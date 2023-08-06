pub fn multiply(a: i32, b: i32) -> i32 {
    a * b
}

// test --package cameo_ocean --lib lib_multiply::tests
#[cfg(test)]
mod tests {
    use crate::multiply::multiply;

    #[test]
    fn test_multiply1() {
        assert_eq!(multiply(3, 5), 15);
        println!("pass multiply 3*5=15");
    }

    #[test]
    fn test_multiply2() {
        assert_eq!(multiply(-3, 5), -15);
        println!("pass multiply -3*5=-15");
    }
}
