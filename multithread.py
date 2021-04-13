# import socket programming library
from socket import *
from datetime import datetime
  
# import thread module
from _thread import *
import threading

#RFC 822 Date Format(Considering only one Pattern)
#The below date is the date when the file was updated last
date= '04 Apr 2021 16:59:00'
serverDate = datetime.strptime(date, '%d %b %Y %H:%M:%S')

def threaded(connectionSocket):
    while True: 
        try:
            objectModified=False  #To keep state of object? Wheather modified or not
            badRequest=False     #To keep track if any bad request occur
            noTimeout=True       #To keep track of if timout occur or not
            status304=False      #To keep track of the status code 304
            connectionSocket.settimeout(5)   #Setting up timeout for that connection
            try:
                sentence = connectionSocket.recv(1024).decode()
                #Below commented code was for testing multithreading using TCPClient
                # print("I have made a connection")
                # sentence=sentence+" "+"I am happy that you work."
                # connectionSocket.send(sentence.encode())
                # #print(sentence)  #To check the request data 
                serverfile = sentence.split()[1] #Get the File name in the request
                method= sentence.split()[0]  #Taking out the method 'GET'/'POST'....or anything else
                data= sentence.split() #Split the data to keep track of informtions seperately
                # print("no timeout") 
            except Exception as e: #Occurs when timeout happen
                print(e)
                # print("timeout has occured")
                noTimeout=False 
                header = 'HTTP/1.1 408 Timed out\n\n'
                response = '<html><body><h3>Error 408: You waited too long to request</h3></body></html>'.encode('utf-8')
                final_response = header.encode('utf-8')
                final_response += response
                #below line was for testing error 408 with TCPClient
                #final_response="timeout error".encode()
                connectionSocket.send(final_response)
                sentence=''   #Sentence will be empty
                serverfile='' #Serverfile will be empty
                break

            if sentence.find("If-Modified-Since:") != -1 and noTimeout:  #Enter if request contain 'If-Modified-Since' and no timout occur
                
                #The Request will contain value in this format "If-Modified-Since: Tue, 11 Dec 2012 10:10:24 GMT"
                try:
                    index=data.index("If-Modified-Since:") #Getting the index of the "If-Modified-Since:" from the array of data
                    index=index+2 #Getting the index where date information start
                    requestDate= data[index]+" "+data[index+1]+" "+data[index+2]+" "+data[index+3]
                    requestDate= datetime.strptime(requestDate, '%d %b %Y %H:%M:%S')
                    status304=True  
                    
                    if(requestDate<serverDate ): #Comparing the the date of if-modified-since date with the server file modified date 
                        print("The Object has been Modified")
                        objectModified=True
                
                except Exception as e: #Exception for bad request
                    badRequest=True

                
            if(serverfile!='/favicon.ico') and noTimeout: #We have to ignore the Favicon Request because we are not interested in handling the favicon request in this particular project

                if (method!='GET' and status304==False) or badRequest: #Bad Request Handling for status code 400
                    header = 'HTTP/1.1 400 Bad Request\n\n'
                    response = '<html><body><h3>Error 400: Bad Request</h3></body></html>'.encode('utf-8')

                elif status304==True and serverfile[1:]=="test.html": 
                    print("Hello1")
                    print("Hello1")
                    if(objectModified==False):   #Object Modified is false then 304 Not Modified
                        print("Hello2")
                        header = 'HTTP/1.1 304 Not Modified\n\n'
                        response=''.encode('utf-8')
                    else:#Object Modified is True then send 200 OK with new file.
                        with open(serverfile[1:], "r", encoding='utf-8') as f: 
                                response= f.read()

                        response = response.encode('utf-8')
                                
                        header = 'HTTP/1.1 200 OK\n'
                        header += 'Content-Type: '+str('text/html')+'\n\n'
                    
                else:
                    try:
                        with open(serverfile[1:], "r", encoding='utf-8') as f:  #Reading server file
                                response= f.read()

                        response = response.encode('utf-8') #Handling 200 OK 
                                
                        header = 'HTTP/1.1 200 OK\n'
                        header += 'Content-Type: '+str('text/html')+'\n\n'

                    except (FileNotFoundError, IOError): #File not found in server than 404 Page Not Found
                        header = 'HTTP/1.1 404 Page Not Found\n\n'
                        response = '<html><body><h3>Error 404: Page Not Found</h3></body></html>'.encode('utf-8')

                    except connectionSocket.error: #Handling Conncetion error for bad request
                        header = 'HTTP/1.1 400 Bad Request\n\n'
                        response = '<html><body><h3>Error 400: Bad Request</h3></body></html>'.encode('utf-8') 
                
                final_response = header.encode('utf-8')
                final_response += response          # adding header and response
                connectionSocket.send(final_response)#Send the response to the client
                break 
                
        except Exception as e: #General Exception to cover bad scenarios
            print(e) 
    connectionSocket.close() #Closing particluar connection             
    
def main():
    host = ""  #Initial host is empty

    port = 12000  #Setting the port number
    serverSocket = socket(AF_INET,SOCK_STREAM) #creating the socket

    serverSocket.bind((host,port)) #Binding the socket
    serverSocket.listen(1) #Started Listening 
    print ('The server is ready to receive')
    while True:
  
        # establish connection with client
        connectionSocket, addr = serverSocket.accept()
        #Creating New Threads for each connection
        print("Client Connected  "+str(addr[0])+" : "+str(addr[1]))
        start_new_thread(threaded, (connectionSocket,))

    serverSocket.close() #Closing the socket when sever finish
  
if __name__ == '__main__':
    main()