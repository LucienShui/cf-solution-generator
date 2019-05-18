# cf-solution-generator

Help myself write solution in markdown of cf faster

## Usage

### gen.py

Assume that there is a file `a.cpp` stay with the script, just like that:

```plain
cf-solution-generator
├── gen.py
└── a.cpp
```

Run `python3 gen.py <contest id> a <blog id>` to get a `.md` file with code of `a.cpp` and urls of pasteme and Lucien's Blog

### pull.sh

This script require [cf-tool](https://github.com/xalanq/cf-tool)

After cf-tool login, run `bash pull.sh <contest id> <blog id>` to get all `.md` with the code you have passed
