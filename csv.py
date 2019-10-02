import json
import config
import base58

def get_address(script, script_type):
	if script_type == 'p2sh':
		data = '33' + script[11:-9]
	else:
		data = '1a' + script[18:-27]

	return base58.b58encode_check(bytes.fromhex(data)).decode("utf-8")

with open('{}/utxo.json'.format(config.SNAPSHOT_DIR)) as unsptent_data:
	data = json.load(unsptent_data)
	print('Address,Balance')

	for utxo in data:
		if data[utxo]['t'] in ['pubkeyhash', 'p2sh']:
			address = get_address(utxo, data[utxo]['t'])
			amount = float((data[utxo]['v'] / pow(10, 4)))
			print('{},{}'.format(address, amount))
