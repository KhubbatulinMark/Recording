# from clickhouse_adapter import Adapter as AdapterCH


from rabbit import Producer
from model_facade import ModelFacade
from threading import Thread

import settings

logger = settings.logging.getLogger(__name__)

URL = settings.CH_MATH_URL
DATABASE = settings.CH_MATH_DATABASE
TABLE_NAME = settings.CH_MATH_TABLE_NAME
USER = settings.CH_MATH_USER
PASSWORD = settings.CH_MATH_PASSWORD

from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def process_chunk(self, chunk: list):
        pass

    @abstractmethod
    def process_message(self, msg: str):
        pass

    @property
    @abstractmethod
    def is_producing(self) -> bool:
        return False


class MathObserver(Observer):
    CHUNK_SIZE = settings.MATH_CHUNK_SIZE
    query_template = (f"INSERT INTO {DATABASE}.{TABLE_NAME} "
                      "({cols}) FORMAT CSV {data}")

    def __init__(self):

        self.producer = Producer(host=settings.HOST, exchange=settings.EXCHANGE_EVENTS)
        logger.info(f"Run events producer:{Producer}")

    def process_chunk(self, data: list):
        model = ModelFacade(data)
        predict = model.run()
        logger.info(f"Send data, count {len(data)}, table {TABLE_NAME}")
        for index, row in predict.iterrows():
            self.producer.send(str({key: row[key] for key in ("ts", "windings_temperature", "status")}))
        predict.drop(['status'], axis=1, inplace=True)
        query = self.query_template.format(cols=','.join(predict.columns),
                                           data=predict.to_csv(index=False, header=None))
        t = Thread(target=self.ch.raw, args=[query])
        t.start()

    def process_message(self, msg: str):
        pass

    def is_producing(self):
        return True

