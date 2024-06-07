import socket
import argparse
parser = argparse.ArgumentParser(description='TensorFlow等を活用し、人格形成を学習させたChatBotを作成したいです...')
parser.add_argument("IP",type=str,help="学習に利用するデータを指定します。")
parser.add_argument("-p","--port",type=int,help="Socket通信に使うポートを指定します",default=2459)
parser.add_argument("-d","--device",type=str,help="深層学習に使うデバイスを指定します",default="CPU")
def send_data(data):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the server address and port
    server_address = ('localhost', 2459)

    try:
        # Connect to the server
        s.connect(server_address)

        # Send data to the server
        s.sendall(data.encode())

        # Receive response from the server
        response = s.recv(1024)
        print('Received:', response.decode())

    finally:
        # Close the socket
        s.close()

# Example usage
data_to_send = 'Hello, server!'
send_data(data_to_send)