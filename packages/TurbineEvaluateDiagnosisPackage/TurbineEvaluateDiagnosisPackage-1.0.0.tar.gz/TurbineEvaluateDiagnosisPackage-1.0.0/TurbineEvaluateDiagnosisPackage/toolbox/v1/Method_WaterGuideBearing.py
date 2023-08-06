import datetime

import pandas as pd
import numpy as np
from scipy import optimize


def linearFunc(x, k, b):
    return k * x + b


def volumeCalculate(waterHeight: float):
    H = waterHeight
    return (6.305e-8)*H**3 + 0.001746 * (H ** 2) + 4.448 * H - 2062


class WaterGuideBearing:
    def __init__(self, **kwargs):
        """
        水导轴承健康评估与故障诊断模块所需特征参数计算

        [1] 参数
        ----------
        WORKING_CONDITION_SECTIONS:
            list[str],运行工况判定条件在实例化该类时指定,需与工况分类参数WORKING_CONDITION中元素对应,默认["(0<=x)and(x<=1)", "((54.6*0.99)<=x)and(x<=(54.6*1.01))", "(x<0)or(x>(54.6*1.01))or((x>1)and(x<54.6*0.99))"]
        DETAIL_CONDITION:
            list[str],针对过渡工况进行细化判断时的细化工况, 判定条件在实例化该类时指定, 默认["启机工况", "停机工况"]
        WORKING_CONDITION:
            list[str],运行工况判定结果在实例化该类时指定,需与工况分类参数WORKING_CONDITION_SECTIONS中元素对应,默认["停机工况", "运行工况", "过渡工况"]
        buffer:
            pd.DataFrame, 最近数期时间(timestamp)、转速(rpm)、轴瓦温度(temper1、temper2、...)的缓存记录, 默认为pd.DataFrame()
        bufferSize:
            int, buffer尺寸, 默认10
        startingConditionKValue:
            float, 针对过渡工况,进一步判定启机工况时,转速的最大允许上升率, 默认0.2
        shuttingConditionKValue:
            float, 针对过渡工况,进一步判定停机工况时,转速的最大允许下降率, 默认-0.2


        [2] 方法
        ----------
        workingConditionJudgement:
            运行工况的判定

        oilDynamicViscosity:
            油品运动黏度指标量计算

        bearingPadTemper:
            轴瓦温度计算值及信号突变判断
                - 最大值
                - 最小值
                - 不均匀度
                - 轴瓦温度信号突变情况
                    - 突变的温度测点名称
                    - 突变的值

        [3] 返回
        -------
        condition:
            当前工况判断结果
        detailCondition:
            当前细节工况判断结果
        bearingPadTemperRiseRatio:
            轴瓦温度上升率
                - 针对所有传入的轴瓦,单独计算温度上升率,并返回其中最大者

        [4] 示例1
        --------
        >>> oilDynamicViscosity = (np.random.rand(3000) + 5).tolist()
        >>> oilStandardViscosity = 5
        >>> temper1 = (np.random.rand(3000) + 54).tolist()
        >>> temper2 = (np.random.rand(3000) + 54).tolist()
        >>> temper3 = (np.random.rand(3000) + 54).tolist()
        >>> temper4 = (np.random.rand(3000) + 54).tolist()
        >>> temper5 = (np.random.rand(3000) + 54).tolist()
        >>> temper6 = (np.random.rand(3000) + 54).tolist()
        >>> rpms = (np.linspace(3000+50, 50, 3000)).tolist()
        >>> times = pd.date_range("2022-06-07 00:00:00", periods=3000, freq="0.68S").values.flatten().tolist()
        >>> dataDF = pd.DataFrame({
        >>>     "oilDymVis": oilDynamicViscosity,
        >>>     "temper1": temper1, "temper2": temper2,
        >>>     "temper3": temper3, "temper4": temper4,
        >>>     "temper5": temper5, "temper6": temper6,
        >>>     "rpms": rpms, "times": [datetime.datetime.fromtimestamp(item/(10e8)) for item in times]
        >>> })
        >>> buffer = pd.DataFrame()
        >>> obj = WaterGuideBearing()
        >>> for i in range(len(dataDF)):
        >>>     obj.workingConditionJudgement(dataDF.loc[i, ["rpms"]].values[0], dataDF.loc[i, "temper1": "temper6"].values.tolist(), dataDF.loc[i, ["times"]].values[0])
        >>>     _oilVisIndex = obj.oilDynamicViscosity(dataDF.loc[i, ["oilDymVis"]].values[0], oilStandardViscosity)
        >>>     _padTemper = obj.bearingPadTemper(dataDF.loc[i, "temper1": "temper6"].values.tolist(), buffer=buffer, timestamp=dataDF.loc[i, ["times"]].values[0])
        >>>     buffer = _padTemper["buffer"]
        >>>     print(f"基础工况: {obj.condition}, 细节工况: {obj.detailCondition}, "
        >>>         f"轴瓦温度上升率: {obj.bearingPadTemperRiseRatio}, 油品运动黏度: {_oilVisIndex}, "
        >>>         f"轴瓦温度最大值: {_padTemper['max']}, 轴瓦温度最小值:{_padTemper['min']}, 轴瓦温度不均匀度:{_padTemper['unevenness']}, "
        >>>         f"温度突变轴瓦名称: {_padTemper['signalMutation']['name']}, 温度突变值: {_padTemper['signalMutation']['value']}, ")
        >>>     print("="*10)
        """

        self.WORKING_CONDITION_SECTIONS = ["(0<=x)and(x<=1)", "((54.6*0.99)<=x)and(x<=(54.6*1.01))",
                                           "(x<0)or(x>(54.6*1.01))or((x>1)and(x<54.6*0.99))"]
        self.WORKING_CONDITION = ["停机工况", "运行工况", "过渡工况"]
        self.DETAIL_CONDITION = ["启机工况", "停机工况"]
        self.sections = kwargs["sections"] if "sections" in kwargs.keys() else self.WORKING_CONDITION_SECTIONS
        self.conditions = kwargs["conditions"] if "conditions" in kwargs.keys() else self.WORKING_CONDITION
        self.buffer = kwargs["buffer"] if "buffer" in kwargs.keys() else pd.DataFrame()
        self.bufferSize = kwargs["bufferSize"] if "bufferSize" in kwargs.keys() else 10
        assert len(self.sections) == len(self.conditions), "sections 与 conditions 应具有相同长度且元素应互相对应"
        self.rpm = None
        self.condition = None
        self.detailCondition = None
        self.startingConditionKValue = kwargs["startingConditionKValue"] if "startingConditionKValue" in kwargs.keys() else 0.2
        self.shuttingConditionKValue = kwargs["shuttingConditionKValue"] if "shuttingConditionKValue" in kwargs.keys() else -0.2
        self.bearingPadTemperRiseRatio = None

    def workingConditionJudgement(self, rpm: float, tempers: list, timestamp: float):
        """
        运行工况的判定

        - 根据轴瓦温升情况计算温升速率
        - 根据速度变化情况判断启机过程/停机过程
        - 运行工况判定条件在实例化该类时使用self.WORKING_CONDITION_SECTIONS指定,并需与工况分类参数self.WORKING_CONDITION中元素对应,
            默认["(0<=x)and(x<=1)", "((54.6*0.99)<=x)and(x<=(54.6*1.01))", "(x<0)or(x>(54.6*1.01))or((x>1)and(x<54.6*0.99))"]
        - 运行工况判定结果在实例化该类时使用self.WORKING_CONDITION指定,并需与工况判定条件参数self.WORKING_CONDITION_SECTIONS中元素对应,
            默认["停机工况", "运行工况", "过渡工况"]
        - 工况判断结果记录在condition属性中

        :param rpm: float, 机组转速(rpm)
        :param tempers: list[float], 所有轴瓦温度(℃)
        :param timestamp: float, Unix时间戳, 可至ns
        """
        self.rpm = rpm
        self.condition = self.__workingConditionJudgement()
        self.__updateBuffer(timestamp, rpm, tempers)
        self.__detailConditionJudgement()
        self.__temperClimbingRatio()

    def __temperClimbingRatio(self):
        _ks = []
        if len(self.buffer)>=3:
            for i in range(len(self.buffer.columns) - 2):
                _tempers = self.buffer[f"temper{i+1}"].values.flatten().tolist()
                _timeLasting = self.buffer["timestamp"].values.flatten().tolist()
                _trans = lambda x: x/(10 ** (len(str(x)) - 10))
                _timeLasting = [_trans(item) for item in _timeLasting]
                _timeLasting = [item - min(_timeLasting) for item in _timeLasting]
                k, b = optimize.curve_fit(linearFunc, _timeLasting, _tempers, bounds=([-100, -5000], [100, 5000]))[0]
                _ks.append(k)
            self.bearingPadTemperRiseRatio = max(_ks)
        else:
            self.bearingPadTemperRiseRatio = None

    def __detailConditionJudgement(self):
        _rpms = self.buffer["rpm"].values.flatten().tolist()
        if len(_rpms) >= 3:
            try:
                k, b = optimize.curve_fit(linearFunc, np.linspace(0, len(_rpms), len(_rpms)), _rpms,
                                          bounds=([-100, -5000], [100, 5000]))[0]
                if k > self.startingConditionKValue:
                    _loc = 0
                elif k < self.shuttingConditionKValue:
                    _loc = 1
                else:
                    _loc = None
                self.detailCondition = self.DETAIL_CONDITION[_loc]
            except Exception as e:
                None

    def __updateBuffer(self, timestamp: float, rpm: float, tempers: list):
        if len(self.buffer) == 0:
            self.buffer = self.buffer.reindex(columns=["timestamp", "rpm"] + [f"temper{i+1}" for i in range(len(tempers))])
        _newDict = {"timestamp": timestamp, "rpm": rpm}
        for i in range(len(tempers)):
            _newDict = {**_newDict, **{f"temper{i+1}": tempers[i]}}
        self.buffer = self.buffer.append(_newDict, ignore_index=True)
        self.buffer = self.buffer.drop_duplicates(subset=["timestamp"])
        while len(self.buffer) > self.bufferSize:
            self.buffer = self.buffer.iloc[1:, :]

    def __workingConditionJudgement(self):
        _determines = []
        [_determines.append(eval(item.replace("x", str(self.rpm)))) for item in self.sections]
        return np.asarray(self.conditions)[_determines][0]

    @staticmethod
    def oilDynamicViscosity(viscosityValue: float, standardViscosityValue: float, EPSILON: float=10e-8) -> float:
        """
        油品运动黏度指标量计算

        :param viscosityValue: float, 油品运动黏度值
        :param standardViscosityValue: float, 油品运动黏度标准值

        返回

        - 油品运动黏度指标量计算

        """
        return viscosityValue / (standardViscosityValue + EPSILON)

    @staticmethod
    def bearingPadTemper(*args, timestamp: float, buffer: pd.DataFrame=pd.DataFrame(), EPSILON:float=10e-8, timeLimit="-3S", threshold=5) -> dict:
        """
        轴瓦温度计算值及信号突变判断

        - 最大值
        - 最小值
        - 不均匀度
        - 轴瓦温度信号突变情况

        返回

        - max: 最大值
        - min: 最小值
        - unevenness: 不均匀度
        - signalMutation: dict
            - name: list 突变的温度测点名称
            - value: list[float] 突变的值
        - buffer: 根据timeLimit参数定义的数据缓存,需要手动显式化地传入

        :param timestamp: float, 当前温度值的唯一时间戳
        :param buffer: pd.DataFrame, 根据timeLimit参数定义的数据缓存,需要手动显式化地传入, 默认 pd.DataFrame()
        :param EPSILON: float, 计算不均匀度时除数偏置, 默认 10e-8
        :param timeLimit: str, 计算不均匀度时除数偏置, 默认 "3S"
        :param threshold: int, 使用timeLimit参数限值的时间范围内,数据的最大允许变化量,默认5

        """
        _buffer = pd.DataFrame(np.asarray([timestamp] + args[0]).reshape(1, -1),
                               columns=["timestamp"] + [f"temper{i+1}" for i in range(np.shape(args)[1])])
        if len(buffer) == 0:
            buffer = _buffer
        else:
            buffer = pd.concat([buffer, _buffer])
        # 选取近3s数据
        _timeRange = pd.date_range(timestamp, freq=timeLimit, periods=2)
        _timeStart, _timeEnd = _timeRange[1], _timeRange[0]
        buffer = buffer.where(buffer["timestamp"]>=_timeStart).dropna(how="any")
        signalMutation = buffer[[f"temper{i+1}" for i in range(np.shape(args)[1])]].apply(lambda x: max(x) - min(x), axis=0)
        signalMutation = signalMutation.where(signalMutation >= threshold).dropna()
        return {"max": np.max(args), "min": np.min(args),
                "unevenness": (np.max(args) - np.min(args)) / (np.average(args) + EPSILON),
                "signalMutation": {"name": signalMutation.index.tolist(), "value": signalMutation.values.tolist()},
                "buffer": buffer}
