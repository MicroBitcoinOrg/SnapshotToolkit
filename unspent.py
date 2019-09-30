# Based on https://github.com/eklitzke/utxodump
from typing import Tuple
import binascii
import leveldb
import config
import json
import os

def decode_varint(val: bytearray) -> Tuple[int, int]:
	n = 0
	for i, c in enumerate(val):
		n = (n << 7) | (c & 0x7f)
		if c & 0x80:
			n += 1
		else:
			return n, i + 1
	assert False  # not reached

def decode_height(val: bytearray) -> int:
	code, consumed = decode_varint(val)
	return code >> 1

def decode_txid(key: bytearray) -> str:
	assert key[0] == 67
	txid = binascii.hexlify(key[1:33][::-1]).decode('utf8')
	return txid

def locate_db(path: str) -> str:
	datadir = os.path.expanduser(path)
	return os.path.join(datadir, 'chainstate')

def get_obfuscate_key(conn: leveldb.LevelDB) -> bytearray:
	secret = conn.Get(bytearray(b'\x0e\x00obfuscate_key'))
	assert secret[0] == 8 and len(secret) == 9
	return secret[1:]

def decrypt(ciphertext: bytearray, key: bytearray):
	for i, c in enumerate(ciphertext):
		ciphertext[i] = c ^ key[i % len(key)]

def get_unspent(path: str, snapshot_start: str, snapshot_end: str):
	conn = leveldb.LevelDB(locate_db(path))
	secret = get_obfuscate_key(conn)
	result = []

	for k, v in conn.RangeIter(b'C', b'D', include_value=True):
		decrypt(v, secret)
		txid = decode_txid(k)
		height = decode_height(v)
		if height > snapshot_start and height < snapshot_end:
			result.append(txid)

	return list(set(result))

data = get_unspent(config.BLOCKCHAIN_DIR, config.SNAPSHOT_START, config.SNAPSHOT_END)
with open('{}/unspent.json'.format(config.SNAPSHOT_DIR), 'w') as file:
	json.dump(data, file)
