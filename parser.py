from core import blockchain
import config
import json
import os

result = []

print('Loading unspent list...')
with open('{}/unspent.json'.format(config.SNAPSHOT_DIR)) as unsptent_data:
	unspent = json.load(unsptent_data)

print('Reading blocks...')
blockchain = blockchain.Blockchain(os.path.expanduser('{}/blocks'.format(config.BLOCKCHAIN_DIR)))
for block in blockchain.get_ordered_blocks(os.path.expanduser('{}/blocks/index'.format(config.BLOCKCHAIN_DIR)), start=config.SNAPSHOT_START, end=config.SNAPSHOT_END):
	print('Parsing block: #{}'.format(block.height))
	for tx in block.transactions:
		if tx.hash in unspent:
			for pos, output in enumerate(tx.outputs):
				if pos in unspent[tx.hash]:
					result.append({
							'tx': tx.hash,
							'pos': pos,
							'type': output.type,
							'value': output.value,
							'script': str(output.script)[7:-1],
							'height': block.height
						})

with open('{}/raw.json'.format(config.SNAPSHOT_DIR), 'w') as file:
	json.dump(result, file)
