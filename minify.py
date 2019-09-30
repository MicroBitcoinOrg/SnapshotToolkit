import json
import tqdm
import config

unspent = []
result = {}

with open('{}/unspent.json'.format(config.SNAPSHOT_DIR)) as unsptent_data:
	data = json.load(unsptent_data)
	unspent = data

with open('{}/raw.json'.format(config.SNAPSHOT_DIR)) as raw_data:
	data = json.load(raw_data)
	for utxo in tqdm.tqdm(data):
		if utxo['tx'] in unspent:
			if utxo['script'] not in result:
				result[utxo['script']] = {
					't': utxo['type'],
					'v': utxo['value'],
					'i': 1
				}
			else:
				result[utxo['script']]['v'] += utxo['value']
				result[utxo['script']]['i'] += 1

with open('{}/utxo.json'.format(config.SNAPSHOT_DIR), 'w') as file:
	json.dump(dict(result), file)
