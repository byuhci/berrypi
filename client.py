"""
Client script.
"""
import sys
from uuid import getnode

from berry.client import BerryClient
from berry.berries import BerryButton
from berry.utilities import CLIENT_PORT


if __name__ == '__main__':
    # Get the port number to run this client on
    try:
        port = int(sys.argv[1])
    except:
        # Default port
        port = CLIENT_PORT

    # Test berry
    berry = BerryButton(
        berry_type='button',
        name='left_button',
        guid=getnode().__str__() + str(port),
    )

    client = BerryClient(berry=berry, port=port)

    # Listen for a reply on the same port. TCP for replies.
    response = client.find_a_server()

    # TODO: Import handlers? Or does this happen somewhere else?

    # Client loop (waiting for events or incoming messages)
    while True:
        # TODO: Figure out how to trigger a code edit message, etc.

        # Wait for incoming TCP messages
        message = client.wait_for_message()

        # And process the message
        client.process_message(message=message)
