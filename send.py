import pika
import json
from datetime import datetime

connection=pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel=connection.channel()
channel.queue_declare(queue='Medium')

body = dict(key='youtube',min_date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

body = json.dumps(body)

channel.basic_publish( exchange='',
                       routing_key='youtube',
                       body=body)

print("[x] 'Hello World!' Gönderildi")
connection.close()
