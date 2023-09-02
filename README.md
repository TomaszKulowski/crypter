# General info
Crypter.py is encrypting files application.

Supported files extensions: ```.cr``` ```.csv``` ```.json``` ```.txt```

## Technologies 
Python 3.10

### Setup

1. Clone repo

    ```bash
    git clone https://github.com/TomaszKulowski/crypter.git
    ```
    
2. Install requirements packages

    ```bash
    pip install -r requirements.txt
    ```

### Usage

   ```bash
    usage: crypter.py [-h] -m  -p PASSWORD [-v] (--file FILE [FILE ...] | --folder FOLDER) [-e {.csv,.json,.txt,.cr} [{.csv,.json,.txt,.cr} ...]] [-r {True,False}]
    
    Encypting files application
    
    options:
      -h, --help            show this help message and exit
      -m , --mode           Available modes: encrypt, decrypt, append; encrypt given file or files; decrypt encrypted file or files; append -> decrypt file, append text and encrypt the file again
      -p PASSWORD, --password PASSWORD
                            Password to encrypt or decrypt
      -v, --verbose         Verbose mode
      --file FILE [FILE ...]
                            The path to the name of the file/files with data to be processed
      --folder FOLDER       The path to the folder with files to be processed
      -e {.csv,.json,.txt,.cr} [{.csv,.json,.txt,.cr} ...], --extension {.csv,.json,.txt,.cr} [{.csv,.json,.txt,.cr} ...]
                            The extensions of files to be processed. All supported extensions are processed by default
      -r {True,False}, --remove {True,False}
                            Remove parent file. Default is False

  ```
