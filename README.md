## CSN-371-Project


### To run this project locally:
- Clone this repository.
- Download train and test data hosted on:
```
    https://drive.google.com/drive/folders/1hRSOfKaRUU6w2OwMWeTJUANCxvRzUVCm?usp=sharing
```
- Edit [cfg.py](https://github.com/wistic/CSN-371-Project/blob/main/cfg.py) according to the location of train and test data. And set an output folder path.
- __(Optional)__ Create a [virtualenv](https://pypi.org/project/virtualenv/) and activate it.
- Install requirements:
```
 $ pip install -r requirements.txt
```
- Install *corpus_processor* implemented in Rust.
```
 $ cd rust_preprocessor/ && maturin develop --release && cd ..
```
- Change the main program as per your needs and run:
```
 $ python main.py
```
