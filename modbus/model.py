import pandas as pd


class EngineConstModel():
    def __init__(self, Tlim=40, Tenv=20):
        self.Tenv = Tenv
        self.Tlim = Tlim
        self.K_wind = -0.003
        self.K_body = 0.00195
        self.K_vent = 0
        self.power = []
        self.Q_heat = 0

    def fit(self, df):

        self.power =df['output_power'].mean()

        self.freq = df['actual_turnover'].mean()

        if self.power > 0.001:
            self.Q_heat = 0.02669839889673108 + self.power * 8.391211e-05
        else:
            self.Q_heat = 0

        self.K_vent = -(self.freq * 4.17971024e-05 + 0.0005119055376274992)

        self.Tbody0 = df['body_temperature'][-1]  # t_body[-1]
        self.Twind0 = df['windings_temperature'][-1]  # t_wind[-1]
        print('end')

    def predict(self, time):

        tbody_old = self.Tbody0
        tbody_cur = self.Tbody0

        twind_old = self.Twind0
        twind_cur = self.Twind0

        result = []

        dt = 1
        for t in range(time):
            result.append({
                'time': t,
                'windings_temperature': twind_cur,
                'body_temperature': tbody_cur
            })

            twind_old = twind_cur
            tbody_old = tbody_cur
            twind_cur = twind_old + self.Q_heat * dt + self.K_wind * (twind_old - tbody_old) * dt
            tbody_cur = tbody_old + self.K_body * (twind_old - tbody_old) * dt + self.K_vent * (
                tbody_old - self.Tenv) * dt

        return pd.DataFrame(result)

    def predict_time(self):

        tbody_old = self.Tbody0
        tbody_cur = self.Tbody0

        twind_old = self.Twind0
        twind_cur = self.Twind0

        dt = 0.1
        time = 0
        while twind_cur < self.Tlim and time < 10000:
            twind_old = twind_cur
            tbody_old = tbody_cur
            twind_cur = twind_old + self.Q_heat * dt + self.K_wind * (twind_old - tbody_old) * dt
            tbody_cur = tbody_old + self.K_body * (twind_old - tbody_old) * dt + self.K_vent * (
                tbody_old - self.Tenv) * dt
            time += dt

        return time


class EngineVirtualSensorModel():
    def __init__(self, Tenv=20, Tlim=40):
        self.Tenv = Tenv
        self.Tlim = Tlim
        self.K_wind = -0.003
        self.K_body = 0.00195
        self.K_vent = 0
        self.power = 0.0
        self.Q_heat = 0

    def fit(self, df):

        self.power =df['output_power'].mean()
        self.freq = df['actual_turnover'].mean()

        if self.power > 0.001:
            self.Q_heat = 0.02669839889673108 + self.power * 8.391211e-05
        else:
            self.Q_heat = 0

        self.K_vent = -(self.freq * 4.17971024e-05 + 0.0005119055376274992)

        self.Tbody0 = df['body_temperature'][-1]  # t_body[-1]
        self.Twind0 = df['windings_temperature'][-1]  # t_wind[-1]
        print('end')

    def predict(self, df):

        self.fit(df)
        time = df['time'].values
        t_body = df['body_temperature'].values
        status = df['status'].values
        dt = df['ts'].diff().values
        twind_cur = df['windings_temperature'].iloc[0]

        result = []
        for i in range(1, len(time)):
            twind_old = twind_cur
            twind_cur = twind_old + self.Q_heat * dt[i] + self.K_wind * (twind_old - t_body[i]) * dt[i]
            result.append({
                'time': time[i],
                'windings_temperature': twind_cur,
                'body_temperature': t_body[i],
                'status': status[i]
            })

        return pd.DataFrame(result)
