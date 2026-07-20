# Import required modules
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

# Set up PubNub configuration
pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'demo'  # Replace with your subscribe key
pnconfig.publish_key = 'demo'    # Replace with your publish key
pnconfig.user_id = 'python-user'
pnconfig.enable_subscribe = True

# Create a PubNub instance
pubnub = PubNub(pnconfig)


import os
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.exceptions import PubNubException

def send_file(pubnub: PubNub, file_path: str, channel: str):
    try:
        with open(file_path, 'rb') as sample_file:
            response = pubnub.send_file() \
                .channel(channel) \
                .file_name("sample.gif") \
                .message({"test_message": "test"}) \
                .file_object(sample_file) \
                .sync()
            print("File sent successfully. File ID:", response.result.file_id)

    except PubNubException as e:
        print(f"Error: {e}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")


def main():
    # Configuration for PubNub instance
    pn_config = PNConfiguration()
    pn_config.subscribe_key = os.getenv('SUBSCRIBE_KEY', 'demo')
    pn_config.publish_key = os.getenv('PUBLISH_KEY', 'demo')
    pn_config.user_id = os.getenv('USER_ID', 'my_custom_user_id')

    # Initialize PubNub client
    pubnub = PubNub(pn_config)

    # Send file
    send_file(pubnub, 'path/to/sample.gif', 'my_channel')


if __name__ == "__main__":
    main()
