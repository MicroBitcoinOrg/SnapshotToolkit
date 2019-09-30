from core.blockchain import Blockchain
import config
import json
import os

result = []

blockchain = Blockchain(os.path.expanduser('{}/blocks'.format(config.BLOCKCHAIN_DIR)))
for block in blockchain.get_ordered_blocks(os.path.expanduser('{}/blocks/index'.format(config.BLOCKCHAIN_DIR)), start=config.SNAPSHOT_START, end=config.SNAPSHOT_END):
	for tx in block.transactions:
		for pos, output in enumerate(tx.outputs):
			result.append({
					'tx': tx.hash,
					'pos': pos,
					'type': output.type,
					'value': output.value,
					'script': (output.script)[7:-1],
					'height': block.height
				})

with open('{}/raw.json'.format(config.SNAPSHOT_DIR), 'w') as file:
	json.dump(result, file)
