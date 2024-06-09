import time
import os

from backend.blockchain.block import Block

from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from pubnub.pubnub import PubNub

from os.path import join, dirname

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

pnconfig = PNConfiguration()
pnconfig.subscribe_key = os.environ.get('SUBSCRIBE_KEY')
pnconfig.publish_key = os.environ.get('PUBLISH_KEY')
# pnconfig.user_id = 'vietnguyen_kma'

CHANNELS = {
    'TEST': 'TEST',
    'BLOCK': 'BLOCK'
}

class Listener(SubscribeCallback):
    def __init__(self, blockchain):
        self.blockchain = blockchain
    
    def message(self, pubnub, message_object):
        print(f'\n-- Channel: {message_object.channel} | Message: {message_object.message}')
        
        if message_object.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message_object.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)
            
            try:
                self.blockchain.replace_chain(potential_chain)
                print(f'\n-- Successfully replaced the local chain')
            except Exception as e:
                print(f'\n-- Did not replace chain: {e}')
        
class PubSub():
    def __init__(self, blockchain) -> None:
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain))
        
    def publish(self, channel, message):
        self.pubnub.unsubscribe().channels([channel]).execute()
        self.pubnub.publish().channel(channel).message(message).sync()
        self.pubnub.subscribe().channels([channel]).execute()
        
    def broadcast_block(self, block):
        self.publish(CHANNELS['BLOCK'], block.to_json())

def main():
    pubsub = PubSub()
    
    time.sleep(1)

    pubsub.publish(CHANNELS['TEST'], {'foo': 'bar'})

if __name__ == '__main__':
    main()