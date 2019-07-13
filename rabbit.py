#!/usr/bin/env python3.7
import pika
import traceback

class Publisher:
    def init(self, config):
        self.config = config
        
    def publish(self, message):
        connection = None
        
        try:
            connection = self._create_connection()
            channel = connection.channel()
            
            # channel.exchange_declare(exchange=self.config['exchangeName'], passive=True)

            channel.queue_declare(queue='hello')
            channel.basic_publish('', routing_key=self.config['routingKey'], body=message)
            
            print(" [x] Sent message %r" % message)
        except Exception as e:
            print(repr(e))
            traceback.print_exc()
            raise e
        finally:
            if connection:
                connection.close()
        
    def _create_connection(self):
        credentials = pika.PlainCredentials(self.config['userName'], self.config['password'])
        parameters = pika.ConnectionParameters(
            host="localhost",
            port="5672",
            heartbeat=200,
            credentials=credentials,
        )
        
        return pika.BlockingConnection(parameters)


rabbit = Publisher()

rabbit.init({
    'host' : "localhost", 
    'userName' : "guestx", 
    'password' : 'guest', 
    'virtualHost' : "localhost", 
    "port" : 5672, 
    "exchangeName" : 'testing',
    "routingKey" : "hello"
    })

rabbit.publish('test rabbitmq');