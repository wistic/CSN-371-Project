use xml::reader::XmlEvent;
use xml::attribute::OwnedAttribute;
use std::fmt::{Display, Formatter};
use std::fmt;
use std::fs::File;
use std::io::Write;

struct Token {
    tag: String,
    token: Option<String>,
}

impl Display for Token {
    fn fmt(&self, f: &mut Formatter) -> fmt::Result {
        if let Some(token) = &self.token {
            return write!(f, "{}_{}", token, self.tag);
        }
        Ok(())
    }
}

struct MegaToken {
    tag: String,
    token: Vec<String>,
}

impl Display for MegaToken {
    fn fmt(&self, f: &mut Formatter) -> fmt::Result {
        if self.token.len() > 0 {
            for (i, token) in self.token.iter().enumerate() {
                if i == self.token.len() - 1 {
                    write!(f, "{}", token)?;
                } else {
                    write!(f, "{} ", token)?;
                }
            }
            return write!(f, "_{}", self.tag);
        }
        Ok(())
    }
}

pub struct Corpus {
    token: Option<Token>,
    mega_token: Option<MegaToken>,
    file: File,
    lowercase: bool,
}

impl Corpus {
    pub fn new(file: File, lowercase: bool) -> Corpus {
        Corpus {
            file,
            token: None,
            mega_token: None,
            lowercase,
        }
    }

    pub fn feed(&mut self, event: XmlEvent) {
        match event {
            XmlEvent::StartElement { name, attributes, .. } => {
                match name.local_name.as_str() {
                    "w" | "c" => {
                        if let Some(tag) = get_tag(attributes) {
                            self.token = Some(Token {
                                tag,
                                token: None,
                            });
                        }
                    }
                    "mw" => {
                        if let Some(tag) = get_tag(attributes) {
                            self.mega_token = Some(MegaToken {
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
                        if let Some(token) = self.token.take() {
                            if let Err(error) = self.process_token(token) {
                                println!("File writing error: {}", error);
                            }
                        }
                    }
                    "mw" => {
                        if let Some(mega_token) = self.mega_token.take() {
                            if let Err(error) = self.process_mega_token(mega_token) {
                                println!("File writing error: {}", error);
                            }
                        }
                    }
                    _ => ()
                }
            }
            XmlEvent::Characters(token_string) => {
                if let Some(token) = &mut self.token {
                    token.token = Some(token_string.clone());
                }
                if let Some(mega_token) = &mut self.mega_token {
                    mega_token.token.push(token_string);
                }
            }
            _ => ()
        }
    }

    fn format_token(&self, token: String) -> String {
        if self.lowercase {
            token.to_lowercase()
        } else {
            token
        }
    }

    fn process_token(&mut self, token: Token) -> std::io::Result<()> {
        let tag = token.tag;
        if let Some(token) = token.token {
            write!(self.file, "{}_{}\n", self.format_token(token), tag)?;
        }
        Ok(())
    }

    fn process_mega_token(&mut self, mega_token: MegaToken) -> std::io::Result<()> {
        let tag = mega_token.tag;
        if !mega_token.token.is_empty() {
            let mut iter = mega_token.token.into_iter().peekable();
            while let Some(token) = iter.next() {
                write!(self.file, "{}{}", self.format_token(token), if iter.peek().is_some() { '_' } else { ' ' })?;
            }
            write!(self.file, "{}\n", tag)?;
        }
        Ok(())
    }
}

fn get_tag(attributes: Vec<OwnedAttribute>) -> Option<String> {
    for attribute in attributes {
        if attribute.name.local_name == "c5" {
            return Some(attribute.value);
        }
    }
    None
}