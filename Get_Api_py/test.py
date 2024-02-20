import rabbitmq

message = 'test class'
print("CCCC")
connection,channel = rabbitmq.open_connection()
print("BBBBB")

rabbitmq.publisher(channel,message)

rabbitmq.close_connection(connection)