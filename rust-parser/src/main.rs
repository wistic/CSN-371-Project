use std::fs::File;
use std::io::BufReader;
use xml::{EventReader, ParserConfig};
use xml::reader::XmlEvent;
use corpus::Corpus;
use clap::Clap;

mod corpus;

#[derive(Clap)]
#[derive(Debug)]
#[clap(version = "1.0", author = "Simpu <id.simpu@gmail.com>")]
struct Opts {
    read: String,
    write: String,
    #[clap(short, long, parse(from_occurrences))]
    lowercase: i32,
}

fn read_file(path: &str) -> Option<File> {
    match File::open(path) {
        Ok(file) => Some(file),
        Err(error) => {
            println!("File: {} Error: {}", path, error);
            None
        }
    }
}

fn write_file(path: &str) -> Option<File> {
    match File::create(path) {
        Ok(file) => Some(file),
        Err(error) => {
            println!("File: {} Error: {}", path, error);
            None
        }
    }
}

fn to_bool(value: i32) -> bool {
    if value == 0 {
        false
    } else {
        true
    }
}

fn main() {
    let opts: Opts = Opts::parse();
    if let (Some(read), Some(write)) = (read_file(opts.read.as_str()), write_file(opts.write.as_str())) {
        let buff = BufReader::new(read);
        let config = ParserConfig::default().trim_whitespace(true);
        let reader = EventReader::new_with_config(buff, config);
        let mut corpus = Corpus::new(write, to_bool(opts.lowercase));
        for event in reader {
            match event {
                Ok(event) => {
                    match event {
                        XmlEvent::EndDocument => return,
                        event => corpus.feed(event)
                    }
                }
                Err(error) => {
                    println!("xml parsing failed. {}", error.msg());
                    break;
                }
            }
        }
    }
}
