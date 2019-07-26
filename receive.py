import pika
import json
from mediumcrawler import MediumCrawler

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='Medium')


def callback(ch, method, properties, body):
    data = json.loads(body.decode('utf8'))
    MediumCrawler(data['key'])
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='Medium',consumer_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()