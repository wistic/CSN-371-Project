## CSN-371-Project


### To run this project locally:
- Clone this repository.
- Download train and test data hosted on:
```md
  https://drive.google.com/drive/folders/1hRSOfKaRUU6w2OwMWeTJUANCxvRzUVCm?usp=sharing
```
- Edit [cfg_default.py](https://github.com/wistic/CSN-371-Project/blob/main/cfg_default.py) according to the location of train and test data or create a local version named **cfg_modified.py** using the same structure as cfg_default.py. And set an output folder path.
- __(Optional)__ Create a [virtualenv](https://pypi.org/project/virtualenv/) and activate it.
- Install requirements:
```shell
 $ pip install -r requirements.txt
```
- Install cargo:
```shell
 $ curl https://sh.rustup.rs -sSf | sh -s -- --default-toolchain nightly -y
```
- Install *corpus_processor* implemented in Rust.
```shell
 $ cd rust_preprocessor/ && maturin develop --release && cd ..
```
- Change the main program as per your needs and run:
```shell
 $ python main.py
```
