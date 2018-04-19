# Inverted Encryption Index 

**Authors:**  
Matthew Hartshorn  
Alex Sammons

This project illustrates a basic implementation of an inverted index of encrypted data. The index can be used to searh for words in encrypted files and provide the content that encrypted data. The index works by utilizing SHA256 hashing to generate searchable tokens for the contents of an indexed file. The files themselves are encrypted using AES-256 encryption and CBC mode with randomly generated Initialization Vectors. 

The encrypted files also maintain their former filenames as to provide users with meaningful filenames after decryption. These filenames are also part of the encrypted data in order to keep user data secure. To avoid filename collision when generating the encrypted files, we utilized UUIDs as randomly generated file names to ensure files could safely be created.



# Environment

The following information denotes the environment setup in which the code was written and tested.

**Language:** Python 3.5+

**Operating System:** Windows 10


# Prerequisites

The Python 3.5+ command line interface must be installed on the device. The download for Python can be found [here](https://www.python.org/downloads/).

**Cryptography** - Python encryption library
```bash
> pip install cryptography
```


# Usage

Run Python followed by the script `se.py` then specify which command you want to run and any required arguments.

```
> python se.py

usage: se.py [-h] {keygen,add,token,search} ...

positional arguments:
  {keygen,add,token,search}
                        Commands
    keygen              Generates a psuedorandom encryption key used for AES
                        file encryption
    add                 Adds a file to the searchable encryption index
    token               Generates an encryption token used to search the index
    search              Searches the index for files that satisfy the provided
                        query

optional arguments:
  -h, --help            show this help message and exit
```

# Commands

## Keygen

**Command:** `keygen`

**Description:**  
Generates a pseudorandom encryption key used by the AES-256 algorithm. Encryption is used on any indexed files.

**Options:**

| Char | Verbose     | Arg       | Description
| ---- | ----------- | --------- | -------------------------------------------- |
| `-s` | `--size`    | `SIZE`    | The size of the key in bits, with valid key sizes of 128, 192, or 256
| `-o` | `--output`  | `FILE`    | The output path in which the key is written

**Usage:**  
```
keygen [-h] [-s {128,192,256}] [-o FILE]
```

**Examples:**  
```
> python se.py keygen
c5a271455b9ccdf680e541c3304aeadceb62795bc5d4f63297a3cfc957590e41

> python se.py keygen -s 128
75f29d61f44d4ba42c5059e4667cf6dd

> python se.py keygen -o ./data/key.txt
```


## Add

**Command:** `add`

**Description:**  
Adds one or more files to the searchable encryption index. Will generate a new index if one does not already exist. If a directory is provided, all files within that directory will be indexed.

**Note:** By default, if no directory or index location is provided the current working directory will be utilized as output directory.

**Options:**

| Char | Verbose     | Arg       | Description                                  | Default        |
| ---- | ----------- | --------- | -------------------------------------------- | -------------- |
| `-k` | `--keyFile` | `FILE`    | The path of the encryption key file          | `./skaes.txt`  |
| `-i` | `--index`   | `FILE`    | The path of the index file                   | `./.index`     |
| `-d` | `--dir`     | `DIR`     | The output directory of the encrypted files  | `./`           |

**Arguments:**

| Argument | Required | Description
| -------- | -------- | ---------------------------------------- |
| `path`   | Yes      | The file or directory path of the files to be added to the index

**Usage:**  
```
se.py add [-h] [-k FILE] [-i FILE] [-d DIR] path
```

**Examples:**  
```
> python se.py ./some-file.txt

> python se.py -k ./data/key.txt ./some-file.txt

> python se.py -k ./data/key.txt -i ./out/index.json -d ./out ./some-file.txt

> python se.py -k ./data/key.txt -i ./out/index.json -d ./out ./data
```


## Token

**Command:** `token`

**Description:**  
Generates one or more encryption tokens used to search the index. When multiple keywords are 
provided each word becomes its own token.

**Options:**

| Char | Verbose     | Arg       | Description
| ---- | ----------- | --------- | -------------------------------------------- |
| `-o` | `--output`  | `FILE`    | The output path in which the token is written

**Arguments:**

| Argument | Required | Description
| -------- | -------- | ---------------------------------------- |
| `query`  | Yes      | One or more keywords required in all matching files

**Usage:**  
```
se.py token [-h] [-o FILE] query [query ...]
```

**Examples:**  
```
> python se.py token word
98c1eb4ee93476743763878fcb96a25fbc9a175074d64004779ecb5242f645e6

> python se.py token more than one word
187897ce0afcf20b50ba2b37dca84a951b7046f29ed5ab94f010619f69d6e189
7383711c1b05e72a1eddda46d34365edf3736a7c23806ab39b9e6f403c9dd625
7692c3ad3540bb803c020b3aee66cd8887123234ea0c6e7143c0add73ff431ed
98c1eb4ee93476743763878fcb96a25fbc9a175074d64004779ecb5242f645e6

> python se.py token -o ./out/token.txt more than one word
```


## Search

**Command:** `search`

**Description:**  
Searches the index for files that satisfy the provided query. The query can either be a list of plaintext keywords or a set of pre-generated tokens. For a file to match it must contain all parts of the provided query (keywords/tokens). The result is the list of files, and their content, that matched the given query.

**Options:**
 
| Char | Verbose       | Arg        | Required  | Description
| ---- | ------------- | ---------- | --------- | -------------------------------------------- |
| `-k` | `--keyFile`   | `FILE`     | No        | The path of the encryption key file
| `-i` | `--index`     | `FILE`     | No        | The path of the index file
| `-d` | `--dir`       | `DIR`      | No        | The directory of the encrypted files
| `-t` | `--tokenFile` | `FILE`     | Yes       | The file that contains the search token(s)
| `-q` | `--query`     | `WORDS`    | Yes       | One or more keywords required in all matching files


**Usage:**  
```
se.py search [-h] [-k FILE] [-i FILE] [-d DIR] (-t FILE | -q WORDS [WORDS ...])
```

**Examples:**  
```
> python se.py search -q word

> python se.py search -q more than one word

> python se.py search -t ./out/token.txt

> python se.py search -i ./out/index.json -d ./out -k ./out/key.txt -t ./out/token.txt
```


# Example Environment

### Starting Directory Structure
```
./
  data/
    f1.txt
    f2.txt
    f3.txt
    f4.txt
    f5.txt
    f6.txt
  src/
    ...
  se.py
```

### Command Prompt
```
> python se.py keygen -o ./out/key

> python se.py token -o ./out/token bengals steelers

> python se.py add -i ./out/index -d ./out -k ./out/key ./data

> python se.py search -i ./out/index -d ./out -k ./out/key -t ./out/token
```
### Results
```
c4876a426f4445329feec901775ebf4b: {
    "filename: "f1.txt"
    "content: "bengals steelers packers"
}

c7ff3b0957bb487da1c46c15da0ced62: {
    "filename: "f4.txt"
    "content: "steelers bengals"
}
```


### Resulting Directory Structure
```
./
  data/
    ...
  out/
    0eb5016e029b4b65af4ceb214c588a2c
    06c70a27e31f4669befeed98d3407091
    8bb2186225c64750aca2092cb3e31908
    395a251393fd4d398187b37d03680834
    c7ff3b0957bb487da1c46c15da0ced62
    c4876a426f4445329feec901775ebf4b
    index
    key
    token
  src/
    ...
  se.py
```