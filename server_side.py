# This is code for Question 1
# Fouzan Abdullah, 6840797
# Basim Ahmad, 7022494

import random
import socket
import os
from concurrent.futures import ThreadPoolExecutor
from opentelemetry import trace
from opentelemetry.exporter.prometheus import PrometheusSpanExporter
from opentelemetry.sdk.trace import TracerProvider

probability_sampling = 0.4

# initializing open-telemetry
# help with OpenTelemetry was taken from ChatGPT as I was very confused on how to make this work
# the documentation for OpenTelemetry is also very basic and does not outline any components that were of use

trace.set_tracer_provider(TracerProvider())
prometheus_exporter = PrometheusSpanExporter()
trace.get_tracer_provider().add_span_processor(prometheus_exporter)
tracer = trace.get_tracer(__name__)

# configuring the server
server_host = 'localhost'
server_port = 12345
buffer_size = 1500
output_folder = '/Users/fouzanabdullah/Desktop/COSC_3P95/fa19vm_Assign2/Server/received_files'


# function that receives the files and takes in the data
def receive_file(client_socket, filename, file_size):
    received_data = 0

    # opening the file for writing
    output_file_path = os.path.join(output_folder, filename)
    with open(output_file_path, 'wb') as output_file:
        while received_data < file_size:
            chunk = client_socket.recv(min(buffer_size, file_size - received_data))

            if not chunk:
                break

            output_file.write(chunk)

            received_data += len(chunk)

    print(f"File {filename} received and saved as {output_file_path}")


# function that handles the client
def handle_client(client_socket, address):
    print(f"Accepted connection from {address[0]}:{address[1]}")

    try:
        with tracer.start_as_current_span("file_transfer_server"):
            # receiving file info from the client
            filename = client_socket.recv(buffer_size).decode()
            file_size = int(client_socket.recv(buffer_size).decode())

            print(f"Receiving {filename} with ({file_size} bytes) from {address[0]}:{address[1]}")

            # receiving a file form the client
            receive_file(client_socket, filename, file_size)

            print(f"File {filename} received successfully from {address[0]}:{address[1]}")
    except Exception as e:
        with tracer.start_as_current_span("file_transfer_error"):
            print(f"Error handling client {address[0]}:{address[1]}:{str(e)}")
    finally:
        client_socket.close()  # closing the client socket
        print(f"Connection from {address[0]}:{address[1]} is closed")


def fork_parallel_pattern(server_socket = None):
    with ThreadPoolExecutor(max_workers = 10) as executor:
        while True:
            client_socket, address = server_socket.accept()
            executor.submit(handle_client, client_socket, address)


os.makedirs(output_folder, exist_ok = True)


# function that generates random content within the files that we will create further
def generate_random_file_content(file_path, size):
    with open(file_path, 'wb') as file:
        # generating random content
        content = os.urandom(size)
        file.write(content)


# function that generates the random files
def generate_random_files(num_files):
    for i in range(num_files):
        # set the random file size between 5kb and 100mb
        file_size = random.randint(5 * 1024, 100 * 1024 * 1024)

        # file name is set based on the index of each file
        file_name = f'file {i+1}.txt'
        file_path = os.path.join(output_folder, file_name)

        # generating the random files and writing them
        generate_random_file_content(file_path, file_size)
        print(f"Generate {file_name} with the size of {file_size} bytes.")


# set the number of files to generate
generate_random_files(20)


def main():
    # setting up server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(5)
    print(f"Listening on {server_host}:{server_port}")

    # if output folder does not exist, create it
    os.makedirs(output_folder, exist_ok=True)

    try:
        with ThreadPoolExecutor(max_workers=10) as executor:
            while True:
                client_socket, address = server_socket.accept()
                executor.submit(handle_client, client_socket, address)
    except KeyboardInterrupt:
        print("Server is shitting down.")


if __name__ == "__main__":
    main()
