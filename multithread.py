# import socket programming library
from socket import *
from datetime import datetime
  
# import thread module
from _thread import *
import threading

date= '04 Apr 2021 16:59:00'
serverDate = datetime.strptime(date, '%d %b %Y %H:%M:%S')
print_lock = threading.Lock()
# thread function
def threaded(connectionSocket):
    while True: 
        try:
            objectModified=False
            badRequest=False
            timeout=False
            status304=False
            
            try:
                sentence = connectionSocket.recv(1024).decode()
                serverfile = sentence.split()[1]
                
                method= sentence.split()[0]
                data= sentence.split()  
                print(serverfile)
            except Exception as e:
                header = 'HTTP/1.1 408 Time Out\n\n'
                response = '<html><body><h3>Error 408: Time Out</h3></body></html>'.encode('utf-8')
                final_response = header.encode('utf-8')
                final_response += response
                connectionSocket.send(final_response)
                break
                
            if sentence.find("If-Modified-Since:") != -1:
                
                try:
                    index=data.index("If-Modified-Since:")
                    index=index+2
                    requestDate= data[index]+" "+data[index+1]+" "+data[index+2]+" "+data[index+3]
                    requestDate= datetime.strptime(requestDate, '%d %b %Y %H:%M:%S')
                    status304=True

                    if(requestDate<serverDate):
                            objectModified=True
                except Exception as e:
                    badRequest=True
                
            if(serverfile!='/favicon.ico'): #We have to ignore the Favicon Request because we are not going to handle the favicon request

                if (method!='GET' and status304==False) or badRequest:
                        header = 'HTTP/1.1 400 Bad Gateway\n\n'
                        response = '<html><body><h3>Error 400: Bad Gateway</h3></body></html>'.encode('utf-8')

                elif status304==True and serverfile[1:]=="test.html":
                    if(objectModified==False):
                        header = 'HTTP/1.1 304 Not Modified\n\n'
                        response=''.encode('utf-8')
                    else:
                        print_lock.acquire()
                        with open(serverfile[1:], "r", encoding='utf-8') as f: 
                            response= f.read()
                            print_lock.release()

                        response = response.encode('utf-8')
                        header = 'HTTP/1.1 200 OK\n'
                        header += 'Content-Type: '+str('text/html')+'\n\n'
                    
                else:
                    try:
                        print("I am here Positive")
                        with open(serverfile[1:], "r", encoding='utf-8') as f: 
                            response= f.read()
                        response = response.encode('utf-8')
                                
                        header = 'HTTP/1.1 200 OK\n'
                        header += 'Content-Type: '+str('text/html')+'\n\n'

                    except IOError as e:
                        print(e)
                        header = 'HTTP/1.1 404 Page Not Found\n\n'
                        response = '<html><body><h3>Error 404: Page Not Found</h3></body></html>'.encode('utf-8')

                    except connectionSocket.error:
                        header = 'HTTP/1.1 400 Bad Gateway\n\n'
                        response = '<html><body><h3>Error 400: Bad Gateway Request</h3></body></html>'.encode('utf-8') 
                
                final_response = header.encode('utf-8')
                final_response += response
                connectionSocket.send(final_response)
                break
                
        except Exception as e:
            print(e) 
    connectionSocket.close()             
    
def Main():
    host = ""
  
    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 8888
    serverSocket = socket(AF_INET,SOCK_STREAM)

    # Bind the server port to the socket
    serverSocket.bind((host,port))
    serverSocket.listen(1)
    
    while True:
  
        # establish connection with client
        connectionSocket, addr = serverSocket.accept()
        # lock acquired by client
        print('Connected to :', addr[0], ':', addr[1])
  
        # Start a new thread and return its identifier
        start_new_thread(threaded, (connectionSocket,))

    serverSocket.close()
  
  
if __name__ == '__main__':
    Main()