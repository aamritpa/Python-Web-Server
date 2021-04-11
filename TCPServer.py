# Include Python's Socket Library
from socket import *
import codecs
import time
from datetime import datetime


date= '04 Apr 2021 16:59:00'
serverDate = datetime.strptime(date, '%d %b %Y %H:%M:%S')


#If-Modified-Since: Tue, 11 Dec 2012 10:10:24 GMT'


# Specified the server port
serverPort = 12000

# Creating TCP socket
serverSocket = socket(AF_INET,SOCK_STREAM)

# Bind the server port to the socket
serverSocket.bind(('',serverPort))

# Server begins listerning foor incoming TCP connections
serverSocket.listen(1)
print ('The server is ready to receive')

while True: # Loop forever
     # Server waits on accept for incoming requests.
     # New socket created on return
     objectModified=False
     badRequest=False
     noTimeout=True
     connectionSocket, addr = serverSocket.accept()
     #Timeout of 5 seconds is set
     connectionSocket.settimeout(5)
     #The try waits for connectionSocket to recieve from client
     try:
          sentence = connectionSocket.recv(1024).decode()
          #print(sentence)
          #file to be accessed form the server
          serverfile = sentence.split()[1]
          status304=False
          method= sentence.split()[0]
          data= sentence.split() 
          # print("no timeout") 
     except Exception as e:
          #print(e)
          # print("timeout has occured")
          noTimeout=False
          #Below is defined header for Error 408 
          #header = 'HTTP/1.1 408 Timed out\n\n'
          #response = '<html><body><h3>Error 408: You waited too long to request</h3></body></html>'.encode('utf-8')
          #final_response = header.encode('utf-8')
          #final_response += response
          sentence=''
          serverfile=''
          #Below is how we tested our error using TCPClient.py and not sending any request form that file
          final_response="timeout error".encode()
          connectionSocket.send(final_response)
          connectionSocket.close()
                    
     
          
     #Checks for 304 Not modified from header
     if sentence.find("If-Modified-Since:") != -1 and noTimeout:
          
          #This makes sure that the format is right and it isn't a bad request
          try:
               index=data.index("If-Modified-Since:")
               index=index+2
               #Compute the date and time sent by the user
               requestDate= data[index]+" "+data[index+1]+" "+data[index+2]+" "+data[index+3]
               requestDate= datetime.strptime(requestDate, '%d %b %Y %H:%M:%S')
               status304=True
               
               #print(requestDate)
               #print(serverDate)
               #Below we check if the file was modified
               if(requestDate<serverDate):
                    print("True")
                    objectModified=True
          
          except Exception as e:
               #Incase the format of the request is wrong -> Error 400
               badRequest=True

     #just go in loop if the socket hasn't timed out    
     if(serverfile!='/favicon.ico') and noTimeout: #We have to ignore the Favicon Request because we are not going to handle the favicon request
          #Check for Error 400
          if (method!='GET' and status304==False) or badRequest:
                header = 'HTTP/1.1 400 Bad Gateway\n\n'
                response = '<html><body><h3>Error 400: Bad Gateway</h3></body></html>'.encode('utf-8')
          
          #Check for 304
          elif status304==True and serverfile[1:]=="test.html":
               if(objectModified==False):
                    #If file is not modified then
                    header = 'HTTP/1.1 304 Not Modified\n\n'
                    response=''.encode('utf-8')

               else:
                    #If the file is modified,the reply is status code -> 200 and the new file is sent
                    with open(serverfile[1:], "r", encoding='utf-8') as f: 
                         response= f.read()

                    response = response.encode('utf-8')    
                    header = 'HTTP/1.1 200 OK\n'
                    header += 'Content-Type: '+str('text/html')+'\n\n'
               
          else:
               try:
                    #This deals with the client request and sends the file
                    with open(serverfile[1:], "r", encoding='utf-8') as f: 
                         response= f.read()

                    response = response.encode('utf-8')
                         
                    header = 'HTTP/1.1 200 OK\n'
                    header += 'Content-Type: '+str('text/html')+'\n\n'
               #If page is not found send -> Error 404 (below exception is sub of .error)
               except (FileNotFoundError, IOError):
                    header = 'HTTP/1.1 404 Page Not Found\n\n'
                    response = '<html><body><h3>Error 404: Page Not Found</h3></body></html>'.encode('utf-8')
               #Otherwise the left over case for .error are cases of Error 400 -> Bad Request
               except connectionSocket.error:
                    header = 'HTTP/1.1 400 Bad Request\n\n'
                    response = '<html><body><h3>Error 400: Bad Request</h3></body></html>'.encode('utf-8') 
          #The final response form all the cases is formed and sent and the socket is closed
          final_response = header.encode('utf-8')
          final_response += response
          connectionSocket.send(final_response)
          connectionSocket.close()
                    
 
