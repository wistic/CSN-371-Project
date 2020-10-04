use xml::reader::XmlEvent;
use xml::attribute::OwnedAttribute;
use std::fs::File;
use std::io::{Write, BufWriter, BufReader};
use xml::{ParserConfig, EventReader};
use std::error::Error;

struct Token {
    tag: String,
    token: Option<String>,
}

struct MegaToken {
    tag: String,
    token: Vec<String>,
}

pub fn corpus_convert(reader: BufReader<File>, mut writer: BufWriter<File>, lowercase: bool) -> Result<(), Box<dyn Error>> {
    let config = ParserConfig::default().trim_whitespace(true);
    let reader = EventReader::new_with_config(reader, config);
    let mut token = None;
    let mut mega_token = None;
    for event in reader {
        let event = event?;
        match event {
            XmlEvent::StartElement { name, attributes, .. } => {
                match name.local_name.as_str() {
                    "w" | "c" => {
                        if let Some(tag) = get_tag(attributes) {
                            token = Some(Token {
                                tag,
                                token: None,
                            });
                        }
                    }
                    "mw" => {
                        if let Some(tag) = get_tag(attributes) {
                            mega_token = Some(MegaToken {
                                tag,
                                token: Vec::new(),
                            });
                        }
                    }
                    _ => ()
                }
            }
            XmlEvent::EndElement { name, .. } => {
                match name.local_name.as_str() {
                    "w" | "c" => {
                        if let Some(token) = token.take() {
                            if let Err(error) = process_token(&mut writer, token) {
                                println!("File writing error: {}", error);
                            }
                        }
                    }
                    "mw" => {
                        if let Some(mega_token) = mega_token.take() {
                            if let Err(error) = process_mega_token(&mut writer, mega_token) {
                                println!("File writing error: {}", error);
                            }
                        }
                    }
                    _ => ()
                }
            }
            XmlEvent::Characters(token_string) => {
                match (&mut token, &mut mega_token) {
                    (Some(token), Some(mega_token)) => {
                        let token_string = format_token(token_string, lowercase);
                        token.token = Some(token_string.clone());
                        mega_token.token.push(token_string);
                    }
                    (Some(token), None) => {
                        token.token = Some(format_token(token_string, lowercase));
                    }
                    (None, Some(mega_token)) => {
                        mega_token.token.push(format_token(token_string, lowercase));
                    }
                    _ => ()
                }
            }
            XmlEvent::EndDocument => {
                writer.flush()?;
                return Ok(());
            }
            _ => ()
        }
    }
    Ok(())
}

fn get_tag(attributes: Vec<OwnedAttribute>) -> Option<String> {
    for attribute in attributes {
        if attribute.name.local_name == "c5" {
            return Some(attribute.value);
        }
    }
    None
}

fn format_token(token: String, lowercase: bool) -> String {
    if lowercase {
        token.to_lowercase()
    } else {
        token
    }
}

fn process_token(writer: &mut BufWriter<File>, token: Token) -> std::io::Result<()> {
    let tag = token.tag;
    if let Some(token) = token.token {
        writer.write_all(token.as_ref())?;
        writer.write_all(b"_")?;
        writer.write_all(tag.as_ref())?;
        writer.write_all(b"\n")?;
    }
    Ok(())
}

fn process_mega_token(writer: &mut BufWriter<File>, mega_token: MegaToken) -> std::io::Result<()> {
    let tag = mega_token.tag;
    if !mega_token.token.is_empty() {
        let mut iter = mega_token.token.into_iter().peekable();
        while let Some(token) = iter.next() {
            writer.write_all(token.as_ref())?;
            if iter.peek().is_some() {
                writer.write_all(b" ")?;
            } else {
                writer.write_all(b"_")?;
            }
        }
        writer.write_all(tag.as_ref())?;
        writer.write_all(b"\n")?;
    }
    Ok(())
}