# Fouzan Abdullah, 6840797
# Basim Ahmad,

import socket
import os
from opentelemetry import trace
from opentelemetry.exporter.prometheus import PrometheusSpanExporter
from opentelemetry.sdk.trace import TracerProvider

# initializing OpenTelemetry
trace.set_tracer_provider(TracerProvider())
prometheus_exporter = PrometheusSpanExporter()
trace.get_tracer_provider().add_span_processor(prometheus_exporter)

# configuring the client
server_host = 'localhost'
server_port = 12345
buffer_size = 1500
input_folder = '/Users/fouzanabdullah/Desktop/COSC_3P95/fa19vm_Assign2/Client'


# function that sends the client file
def send_file(filename, server_socket):
    server_socket.send(filename.encode())  # send filename to server

    file_size = os.path.getsize(filename)  # getting the file size
    server_socket.send(str(file_size).encode())

    # opening file for reading
    with open(filename, 'rb') as file:
        while True:
            data = file.read(buffer_size)
            if not data:
                break  # end of file

            server_socket.send(data)

    print(f"File {filename} sent successfully.")


# main function
def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    # iterating over files in input folder
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            file_path = os.path.join(root, file)
            send_file(file_path, client_socket)

    # closing the client socket
    client_socket.close()


if __name__ == "__main__":
    main()
