# Include Python's Socket Library
from socket import *

# Specify Server Address
serverName = 'localhost'
serverPort = 12000

# Create TCP Socket for Client
clientSocket = socket(AF_INET, SOCK_STREAM)

# Connect to TCP Server Socket
clientSocket.connect((serverName,serverPort))

# Recieve user input from keyboard
# Recieve user input from keyboard
sentence = input('Input anything:')

# Send! No need to specify Server Name and Server Port!
 
#The below line was commented to  test for Error 408
clientSocket.send(sentence.encode())
#
# # Read reply characters! No need to read address! 
modifiedSentence = clientSocket.recv(1024)

# Print out the received string
# Print out the received string
print ('From Server:', modifiedSentence.decode())
#
# # Close the socket
clientSocket.close()
