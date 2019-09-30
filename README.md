# MicroBitcoin UTXO snapshot tool

### Usage

To propery configure snapshot tool you have to set correct path to your MicroBitcoin blockchain directory in `BLOCKCHAIN_DIR` variable in config file. After that you shoul execute following commands:

Parse list of unspent UTXOs which will be saved to `snapshot/unspent.json` file.
```
python3 unspent.py
```

Parse UTXO set starting from `SNAPSHOT_START` to `SNAPSHOT_END` blocks and will be saved to `snapshot/raw.json` file.
```
python3 parser.py
```

Minify repeating UTXO set for each address into 1 record and save it to `snapshot/utxo.json` file.
```
python3 parser.py
```

Keep in mind that depending on UTXO set site this process may take couple hours :)

### Libraries

This toolset is based on following libraries:

- [python-bitcoin-blockchain-parser](https://github.com/alecalve/python-bitcoin-blockchain-parser) by @alecalve (GNU Lesser General Public License v3)
- [utxodump](https://github.com/eklitzke/utxodump) by @eklitzke (GNU General Public License v3)