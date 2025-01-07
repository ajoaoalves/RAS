import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='image_processing', durable=True)

# Declare an exchange
channel.exchange_declare(exchange='image_exchange', exchange_type='direct')

# Bind queue to exchange
channel.queue_bind(exchange='image_exchange', queue='image_processing', routing_key='process_image')

print("Queue and exchange set up successfully.")
connection.close()
