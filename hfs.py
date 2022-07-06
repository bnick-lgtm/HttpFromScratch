import socket

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)

while True:    
    client_connection, client_address = server_socket.accept()

    request = client_connection.recv(1024).decode()
    headers = request.split('\n')
    
    request_method = headers[0].split(' ')[0]
    request_route = headers[0].split(' ')[1]
    request_page = None
    response = None
    content = None
    
    if (request_route != '/'):
        request_page = request_route.replace('/', '')
    else:
        request_page = 'index'
    
    try:
        page = open(f'./routes/{request_page}.html')
        content = page.read()
        page.close()
        response = 'HTTP/1.0 200 OK\n\n' + content
    except:
        content = '<h1>The requested file was not found!</h1>'
        response = 'HTTP/1.0 200 OK\n\n' + content

    client_connection.sendall(response.encode())
        
    client_connection.close()

# Close socket
server_socket.close()