from datetime import datetime

from typing import Iterable


class Message_INNER:
    FMT_BEGIN = ">"
    TS_FIELD = "ts"
    FIELDS = [{"name": "status", "fmt": "H", "ru": "Статус"},
              {f"name": "EMPTY", "fmt": "H", "ru": "EMPTY"},
              {"name": "actual_turnover", "fmt": "f", "ru": "Фактические обороты"},
              {"name": "generator_voltage", "fmt": "f", "ru": "Упр. Напряжением. На генераторе"},
              {"name": "brake_degree", "fmt": "f", "ru": "Степень торможения"},
              {"name": "body_temperature", "fmt": "f", "ru": "Температура на корпусе"},
              {"name": "windings_temperature", "fmt": "f", "ru": "Температура на обмотках"},
              {"name": "vibration_speed", "fmt": "f", "ru": "Виброскорость"},
              {"name": "specified_frequency", "fmt": "f", "ru": "Заданная частота"},
              {"name": "acceleration_frequency", "fmt": "f", "ru": "Частота разгона"},
              {"name": "current_consumption", "fmt": "f", "ru": "Ток потребления"},
              {"name": "output_voltage", "fmt": "f", "ru": "Выходное напряжение"},
              {"name": "output_power", "fmt": "f", "ru": "Выходная мощность"},
              {"name": "power_coefficient", "fmt": "f", "ru": "Коэффициент мощности"},
              {"name": "IGBT_temperature", "fmt": "H", "ru": "Температура IGBT модуля"},
              {"name": "start_stop", "fmt": "H", "ru": "Пуск/Стоп"}, ]

    def __init__(self, state: Iterable):
        self.ts = datetime.now().timestamp()
        self.state = [v for i, v in enumerate(state) if i not in self._empty_indexes()]
        self.FIELDS = [v for i, v in enumerate(self.FIELDS) if i not in self._empty_indexes()]

    @classmethod
    def _empty_indexes(cls):
        return [i for i, v in enumerate(cls.FIELDS) if v["name"] == "EMPTY"]

    @classmethod
    def build_fmt(cls):
        fmt = [cls.FMT_BEGIN]
        for field in cls.FIELDS:
            fmt.append(field["fmt"])
        return "".join(fmt)

    @classmethod
    def get_cols(cls):
        cols = [cls.TS_FIELD]
        cols.extend([val['name'] for i, val in enumerate(cls.FIELDS) if i not in cls._empty_indexes()])
        return cols

    @classmethod
    def dict_from_csv_row(cls, row: str):
        values = row.strip().split(',')
        cols = cls.get_cols()
        return {cols[i]: float(val) for i, val in enumerate(values)}

    def get_csv_row(self):
        """
        Format message as csv row
        :return: 'message.ts,val1,...valN'
        """
        return f"{self.ts}, {','.join([str(v) for v in self.state])}"

    def pretty_print(self):
        for i, v in enumerate(self.FIELDS):
            print(v["ru"], self.state[i])
