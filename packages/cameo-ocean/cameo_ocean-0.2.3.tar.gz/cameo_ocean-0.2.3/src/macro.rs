#[macro_export]
macro_rules! some {
    ($e:expr) => {
        match $e {
            Some(s) => s,
            None => return,
        }
    };
}

#[macro_export]
macro_rules! some_none {
    ($e:expr) => {
        match $e {
            Some(s) => s,
            None => return None,
        }
    };
}

#[macro_export]
macro_rules! some_continue {
    ($e:expr) => {
        match $e {
            Some(s) => s,
            None => continue,
        }
    };
}

#[macro_export]
macro_rules! ok {
    ($e:expr) => {
        match $e {
            Ok(o) => o,
            Err(_e) => return,
        }
    };
}

#[macro_export]
macro_rules! ok_http{
    ($e:expr,$error_message:expr) => {
        match $e {
            Ok(o) => o,
            Err(_) => return HttpResponse::Ok().body($error_message),
        }
    };
}

#[macro_export]
macro_rules! ok_none {
    ($e:expr) => {
        match $e {
            Ok(o) => o,
            Err(_e) => return None,
        }
    };
}

#[macro_export]
macro_rules! ok_continue {
    ($e:expr) => {
        match $e {
            Ok(o) => o,
            Err(_e) => continue,
        }
    };
}