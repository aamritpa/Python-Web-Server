# Include Python's Socket Library
from socket import *
import codecs
import time
from datetime import datetime

monthDict = {
'01' : 'Jan',
'02' : 'Feb',
'03' : 'Mar',
'04' : 'Apr',
'05' : 'Ma',
'06' : 'Jun',
'07' : 'Jul',
'08' : 'Aug',
'09' : 'Sep',
'10' : 'Oct',
'11' : 'Nov',
'12' : 'Dec'
}

date= '04 Apr 2021 16:59:00'
serverDate = datetime.strptime(date, '%d %b %Y %H:%M:%S')


#If-Modified-Since: Tue, 11 Dec 2012 10:10:24 GMT'


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
     objectModified=False
     badRequest=False
     timeout=False
     connectionSocket, addr = serverSocket.accept()
     connectionSocket.settimeout(5)
     # elapsed=0.0
     # minutes=0
     # for i in range(10,00000000000):
     #      i=i+1
     # # Read from socket (but not address as in UDP)
     try:
          sentence = connectionSocket.recv(1024).decode()
          serverfile = sentence.split()[1]
          status304=False
          method= sentence.split()[0]
          data= sentence.split() 
          #print("no timeout") 
     except Exception as e:
          timeout=True
          print("timeout has occured")
          connectionSocket.close()
          
  
     if sentence.find("If-Modified-Since:") != -1:
          
          try:
               index=data.index("If-Modified-Since:")
               index=index+2
               requestDate= data[index]+" "+data[index+1]+" "+data[index+2]+" "+data[index+3]
               requestDate= datetime.strptime(requestDate, '%d %b %Y %H:%M:%S')
               status304=True
               
               print(requestDate)
               print(serverDate)
               if(requestDate<serverDate):
                    print("True")
                    objectModified=True
          
          except Exception as e:
               badRequest=True

         
     if(serverfile!='/favicon.ico'): #We have to ignore the Favicon Request because we are not going to handle the favicon request

          if (method!='GET' and status304==False) or badRequest:
                header = 'HTTP/1.1 400 Bad Gateway\n\n'
                response = '<html><body><h3>Error 400: Bad Gateway</h3></body></html>'.encode('utf-8')

          elif status304==True and serverfile[1:]=="test.html":
               print("Hello1")
               print("Hello1")
               if(objectModified==False):
                    print("Hello2")
                    header = 'HTTP/1.1 304 Not Modified\n\n'
                    response=''.encode('utf-8')
               else:
                    with open(serverfile[1:], "r", encoding='utf-8') as f: 
                         response= f.read()

                    response = response.encode('utf-8')
                         
                    header = 'HTTP/1.1 200 OK\n'
                    header += 'Content-Type: '+str('text/html')+'\n\n'
               
          else:
               try:
                    with open(serverfile[1:], "r", encoding='utf-8') as f: 
                         response= f.read()

                    response = response.encode('utf-8')
                         
                    header = 'HTTP/1.1 200 OK\n'
                    header += 'Content-Type: '+str('text/html')+'\n\n'

               except (FileNotFoundError, IOError):
                    header = 'HTTP/1.1 404 Page Not Found\n\n'
                    response = '<html><body><h3>Error 404: Page Not Found</h3></body></html>'.encode('utf-8')

               except connectionSocket.error:
                    header = 'HTTP/1.1 400 Bad Gateway\n\n'
                    response = '<html><body><h3>Error 400: Bad Gateway Request</h3></body></html>'.encode('utf-8') 
          
          final_response = header.encode('utf-8')
          final_response += response
          connectionSocket.send(final_response)
          connectionSocket.close()
                    
 
