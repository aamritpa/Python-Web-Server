# Include Python's Socket Library
from socket import *
import codecs
import time


# Specify Server Port
serverPort = 12000

# Create TCP welcoming socket
serverSocket = socket(AF_INET,SOCK_STREAM)

# Bind the server port to the socket
serverSocket.bind(('',serverPort))

# Server begins listerning foor incoming TCP connections
serverSocket.listen(1)
print ('The server is ready to receive')

while True: # Loop forever
     # Server waits on accept for incoming requests.
     # New socket created on return
     connectionSocket, addr = serverSocket.accept()
     
     
     # Read from socket (but not address as in UDP)
     sentence = connectionSocket.recv(1024).decode()
     serverfile = sentence.split()[1]
     print(serverfile)
     method = sentence.split()[0]
     print("hello1")
     
     if(serverfile!='/favicon.ico'): #We have to ignore the Favicon Request because we are not going to handle the favicon request

          if (method!='GET'):
               print("hello2")
               header = 'HTTP/1.1 400 Bad Gateway\n\n'
               response = '<html><body><h3>Error 400: Bad Gateway</h3></body></html>'.encode('utf-8')

               final_response = header.encode('utf-8')
               final_response += response
               connectionSocket.send(final_response)
          
               connectionSocket.close()
          else:
               try:
                    print("hello3")
                    with open(serverfile[1:], "r", encoding='utf-8') as f: 
                         response= f.read()

                    print("hello5")
                    response = response.encode('utf-8')
                    header = 'HTTP/1.1 200 OK\n'
                    header += 'Content-Type: '+str('text/html')+'\n\n'

               except Exception as e:
                    print("hello4")
                    print(e)
                    header = 'HTTP/1.1 408 Conection Time Out\n\n'
                    response = '<html><body><h3>Error 408: Connection Timeout</h3></body></html>'.encode('utf-8')
               '''
               except :
                    print(e)
                    header = 'HTTP/1.1 400 Conection Time Out\n\n'
                    response = '<html><body><h3>Error 400: Connection Timeout</h3></body></html>'.encode('utf-8')
               '''
               
               final_response = header.encode('utf-8')
               final_response += response
               connectionSocket.send(final_response)
               connectionSocket.close()
                    
     #connectionSocket.send('HTTP/1.1 200 OK\nContent-Type: text/html\n\n')

     # Send the reply
     
     
     # Close connectiion too client (but not welcoming socket)
     #connectionSocket.close()
