import json
import config

result = {}
outputs = {}
value = {}

with open('{}/utxo.json'.format(config.SNAPSHOT_DIR)) as unsptent_data:
	data = json.load(unsptent_data)
	for utxo in data:
		if data[utxo]['t'] in ['pubkeyhash', 'p2sh']:
			if data[utxo]['t'] not in result:
				result[data[utxo]['t']] = 1
				outputs[data[utxo]['t']] = data[utxo]['i']
				value[data[utxo]['t']] = data[utxo]['v']

			else:
				result[data[utxo]['t']] += 1
				outputs[data[utxo]['t']] += data[utxo]['i']
				value[data[utxo]['t']] += data[utxo]['v']

print(result)
print(outputs)
print(value)
