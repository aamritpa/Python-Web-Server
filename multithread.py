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
            noTimeout=True
            connectionSocket.settimeout(5)
            try:
                sentence = connectionSocket.recv(1024).decode()
                print(sentence)
                serverfile = sentence.split()[1]
                status304=False
                method= sentence.split()[0]
                data= sentence.split() 
                # print("no timeout") 
            except Exception as e:
                print(e)
                # print("timeout has occured")
                noTimeout=False
                header = 'HTTP/1.1 408 Timed out\n\n'
                response = '<html><body><h3>Error 408: You waited too long to request</h3></body></html>'.encode('utf-8')
                # final_response = header.encode('utf-8')
                # final_response += response
                #final_response="timeout error".encode()
                #connectionSocket.send(final_response)
                sentence=''
                serverfile=''
                

            if sentence.find("If-Modified-Since:") != -1 and noTimeout:
                
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

                
            if(serverfile!='/favicon.ico') and noTimeout: #We have to ignore the Favicon Request because we are not going to handle the favicon request

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
                break
                
        except Exception as e:
            print(e) 
    connectionSocket.close()             
    
def Main():
    host = ""
  
    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 12000
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