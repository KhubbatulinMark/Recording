from modbus.model import EngineConstModel, EngineVirtualSensorModel

import pandas as pd
from modbus.message import Message_INNER
from typing import Iterable

from datetime import datetime

from modbus import settings


class ModelFacade:
    df = None
    cols = Message_INNER.get_cols()
    ts_col = Message_INNER.TS_FIELD

    def __init__(self, data):
        self._prepare_data(data)
        self.engine_model = EngineConstModel(Tenv=settings.ROOM_TEMP)
        self.virtual_sensor = EngineVirtualSensorModel(Tenv=20)

    def _prepare_data(self, data: Iterable):

        self.df = pd.DataFrame.from_dict(data)
        self.df.set_index(self.df[self.ts_col].apply(lambda x: datetime.fromtimestamp(x)), inplace=True)
    def return_data(self):
        return self.df

    def run(self):

        df = self.df
        print(type(df))
        # print( df['ts'])
        # print('NNNN', df['ts'] - df['ts'].values[0])
        df['time'] = df['ts'] - df['ts'].values[0]
        self.engine_model.fit(df)
        time_to_heat = self.engine_model.predict_time()
        self.virtual_sensor.fit(df)
        predict = self.virtual_sensor.predict(df)
        predict['ts'] = predict['time'] + df['ts'].values[0]
        predict['time_to_heat'] = time_to_heat
        predict.drop(['time', 'body_temperature'], inplace=True, axis=1)
        return predict
