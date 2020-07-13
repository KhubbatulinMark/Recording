import pika


class Producer:

    _conn = None

    def __init__(self, host, exchange):
        self.HOST = host
        self.EXCHANGE = exchange
        self.conn = self._rabbit_connection(host)
        self.channel = self.channel_declare(self.conn)

    @classmethod
    def _rabbit_connection(cls, host):
        connection_params = pika.ConnectionParameters(heartbeat=0, host=host)
        if not cls._conn:
            cls._conn = pika.BlockingConnection(connection_params)
        return cls._conn

    def channel_declare(self, connection):
        channel = connection.channel()
        channel.exchange_declare(exchange=self.EXCHANGE, exchange_type='fanout')
        return channel

    def send(self, msg: str):
        self.channel.basic_publish(exchange=self.EXCHANGE,
                                   routing_key='',
                                   body=msg)


class Consumer:

    def __init__(self, host, exchange):
        self.HOST = host
        self.EXCHANGE = exchange
        self.conn = self.rabbit_connection()
        self.queue_name, self.channel = self.channel_declare(self.conn)

    def rabbit_connection(self):
        connection_params = pika.ConnectionParameters(heartbeat=0, host=self.HOST)
        return pika.BlockingConnection(connection_params)

    def channel_declare(self, connection):
        channel = connection.channel()
        channel.exchange_declare(exchange=self.EXCHANGE, exchange_type='fanout')
        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=self.EXCHANGE, queue=queue_name)
        return queue_name, channel

    def messages(self):
        return self.channel.consume(queue=self.queue_name)
