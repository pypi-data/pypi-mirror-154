import datetime
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize


def linearFunc(x, k, b):
    return k * x + b


def volumeCalculate(waterHeight: float):
    H = waterHeight
    return (6.305e-8)*H**3 + 0.001746 * (H ** 2) + 4.448 * H - 2062


class MainShaftSealing:
    def __init__(self, **kwargs):
        """
        主轴密封健康评估与故障诊断模块所需特征参数计算

        [1] 参数
        ----------
        WORKING_CONDITION_SECTIONS:
            list[str],运行工况判定条件在实例化该类时指定,需与工况分类参数WORKING_CONDITION中元素对应,默认["(0<=x)and(x<=1)", "((54.6*0.99)<=x)and(x<=(54.6*1.01))", "(x<0)or(x>(54.6*1.01))or((x>1)and(x<54.6*0.99))"]
        WORKING_CONDITION:
            list[str],运行工况判定结果在实例化该类时指定,需与工况分类参数WORKING_CONDITION_SECTIONS中元素对应,默认["停机工况", "运行工况", "过渡工况"]

        [2] 方法
        ----------
        workingConditionJudgement:
            运行工况的判定

        sealingBlockWearingValue:
            密封块磨损速率计算

        sealingLeakageVolume:
            密封泄漏量计算

        lubricateWaterMembraneThickness:
            润滑水膜厚度计算(待补充)

        [3] 返回
        -------
        condition:
            当前工况判断结果

        [4] 示例1
        --------
        >>> # 工况的判断
        >>> rpm = (np.random.rand(100)+54).tolist()
        >>> rpmDF = pd.DataFrame({"rpm": rpm, "condition": np.zeros_like(rpm)})
        >>> rpmDF["condition"] = rpmDF["rpm"].mask(pd.DataFrame([rpmDF["rpm"]>=54.054, rpmDF["rpm"]<=55.146]).all(), ["运行工况"])
        >>> obj = MainShaftSealing()
        >>> for i in range(len(rpmDF)):
        >>>     obj.workingConditionJudgement(rpm[i])
        >>>     print(obj.condition)
        >>>
        >>> # 密封块磨损速率计算
        >>> wearingDF = rpmDF.copy()
        >>> wearingDF.columns = ["wearingValue", "timestamp"]
        >>> wearingDF["timestamp"] = pd.date_range("2022-06-03 00:00:00", periods=100, freq="0.98S", )
        >>> obj = MainShaftSealing()
        >>> buffer_sealingBlock = pd.DataFrame()
        >>> for i in range(len(wearingDF)):
        >>>     res_sealingBlock = obj.sealingBlockWearingValue(wearingDF.iloc[i, 0], wearingDF.iloc[i, 1], buffer_sealingBlock)
        >>>     buffer_sealingBlock = res_sealingBlock["buffer"]
        >>>     print("磨损率", res_sealingBlock["sealingBlockWearingValuePerMinutes"])
        >>>
        >>> # 密封泄漏量计算
        >>> waterHeight = np.arange(300, 1200)
        >>> waterHeight[200:300] = 500
        >>> waterHeightDF = pd.DataFrame({"waterHeight": waterHeight, "timestamp": np.zeros_like(waterHeight)})
        >>> waterHeightDF["timestamp"] = pd.date_range("2022-06-03 00:00:00", periods=900, freq="0.98S")
        >>> obj = MainShaftSealing()
        >>> buffer_leakageVolume = pd.DataFrame()
        >>> for i in range(len(waterHeightDF)):
        >>>     res_leakageVolume = obj.sealingLeakageVolume(waterHeight=waterHeightDF.iloc[i, 0], timestamp=waterHeightDF.iloc[i, 1],
        >>>                         buffer=buffer_leakageVolume, drainPumpStatus=[False, False, False, False, False])
        >>>     buffer_leakageVolume = res_leakageVolume["buffer"]
        >>>     print("泄露量", waterHeightDF.iloc[i, 0], res_leakageVolume["sealingLeakageVolumePerMinutes"])
        >>>
        >>> # 润滑水膜厚度计算
        >>> for i in range(10):
        >>>     b = MainShaftSealing.lubricateWaterMembraneThickness()
        >>>     print(b)
        """

        self.WORKING_CONDITION_SECTIONS = ["(0<=x)and(x<=1)", "((54.6*0.99)<=x)and(x<=(54.6*1.01))",
                                      "(x<0)or(x>(54.6*1.01))or((x>1)and(x<54.6*0.99))"]
        self.WORKING_CONDITION = ["停机工况", "运行工况", "过渡工况"]
        self.sections = kwargs["sections"] if "sections" in kwargs.keys() else self.WORKING_CONDITION_SECTIONS
        self.conditions = kwargs["conditions"] if "conditions" in kwargs.keys() else self.WORKING_CONDITION
        assert len(self.sections) == len(self.conditions), "sections 与 conditions 应具有相同长度且元素应互相对应"
        self.rpm = None
        self.condition = None

    def workingConditionJudgement(self, rpm: float):
        """
        运行工况的判定

        - 运行工况判定条件在实例化该类时使用self.WORKING_CONDITION_SECTIONS指定,并需与工况分类参数self.WORKING_CONDITION中元素对应,
            默认["(0<=x)and(x<=1)", "((54.6*0.99)<=x)and(x<=(54.6*1.01))", "(x<0)or(x>(54.6*1.01))or((x>1)and(x<54.6*0.99))"]
        - 运行工况判定结果在实例化该类时使用self.WORKING_CONDITION指定,并需与工况判定条件参数self.WORKING_CONDITION_SECTIONS中元素对应,
            默认["停机工况", "运行工况", "过渡工况"]
        - 工况判断结果记录在condition属性中

        :param rpm: float, 机组转速(rpm)
        """
        self.rpm = rpm
        self.condition = self.__workingConditionJudgement()

    def __workingConditionJudgement(self):
        _determines = []
        [_determines.append(eval(item.replace("x", str(self.rpm)))) for item in self.sections]
        return np.asarray(self.conditions)[_determines][0]

    @staticmethod
    def sealingBlockWearingValue(wearingValue: float, timestamp: float,
                                 buffer=pd.DataFrame(), bufferSize: int=100, EPSILON=10e-5) -> dict:
        """
        密封块磨损速率计算

        :param wearingValue: float, 当前磨损量
        :param timestamp: float, 当前Unix时间
        :param buffer: pd.DataFrame, 磨损量缓存
        :param bufferSize: int, buffer尺寸限值,默认100
        :param EPSILON: float, 当近1分钟的磨损速率小于此值时,返回0,默认10e-5

        返回

        - sealingBlockWearingValuePerMinutes: 近1分钟磨损量(mm/min),当该值过小(<=10e-5或为负数时),输出0
        - buffer: 缓存,需要在下一次迭代时显性化地输入

        """
        # buffer拼接
        _cache = pd.DataFrame({"timestamp": [timestamp], "wearingValue": [wearingValue]})
        buffer = pd.concat([buffer, _cache]).reset_index(drop=True)
        # buffer尺寸控制
        while len(buffer) > bufferSize:
            buffer = buffer.iloc[-bufferSize:, :]
        # buffer时间选择
        _latestTime = buffer.loc[len(buffer)-1, ["timestamp"]].values.flatten().tolist()[0]
        _latestTimeMinus1Min = _latestTime - datetime.timedelta(minutes=1)
        # 近1分钟时间序列选择
        _bufferSelected = buffer.copy()
        _bufferSelected = _bufferSelected[_bufferSelected["timestamp"]>=_latestTimeMinus1Min]
        # 密封块磨损速率
        _timeEnd, _timeStart = _bufferSelected["timestamp"].iloc[-1], _bufferSelected["timestamp"].iloc[0]
        _timeDelta = _timeEnd - _timeStart
        _valueEnd, _valueStart = _bufferSelected["wearingValue"].iloc[-1], _bufferSelected["wearingValue"].iloc[0]
        _res = (_valueEnd - _valueStart) / _timeDelta.seconds * 60 if _timeDelta.seconds>=EPSILON else 0
        return {"sealingBlockWearingValuePerMinutes": _res if _res>0 else 0, "buffer": buffer}


    @staticmethod
    def sealingLeakageVolume(waterHeight: float, timestamp: float, drainPumpStatus: list,
                             waterHeightLimit: str="(x>=400)and(x<=1000)", waterHeightIncreaseRatio: float=0.3,
                             buffer=pd.DataFrame(), bufferSize: int=100, EPSILON: float=10e-5) -> dict:
        """
        密封泄漏量计算,在满足下述条件时

        - 当水位在限值范围内时(限值范围使用参数 `waterHeightLimit` 指定,默认str="(x>=400)and(x<=1000)")
        - 当水位在1分钟内呈持续上升状态时(持续上升幅度使用参数 `waterHeightIncreaseRatio` 指定,默认float=0.3)
        - 当排水泵全停([False, False, ...])时(泵运行状态使用参数 `drainPumpStatus` 指定, list[bool])
            - `drainPumpStatus` 参数表示排水泵是否为全停状态,即 `[False, False, False]` 表示全停

        返回

        - sealingLeakageVolumePerMinutes: 近1分钟泄漏量(L/min),不满足计算条件时,输出np.nan
        - buffer: 缓存,需要在下一次迭代时显性化地输入

        :param waterHeight: float, 当前水位值(mm)
        :param timestamp: float, 当前Unix时间
        :param drainPumpStatus: list[bool], 当前排水泵状态(泵是否在运行)
        :param waterHeightLimit: str, 当水位在该限值范围内时,可以计算泄漏量
        :param waterHeightIncreaseRatio: str, 当水位在1分钟内呈按此参数持续上升时,计算泄漏量
        :param buffer: pd.DataFrame, 当水位在1分钟内呈按此参数持续上升时,计算泄漏量
        :param bufferSize: int, buffer尺寸限值,默认100
        :param EPSILON: float, 当近1分钟的水位变化率小于此值时,返回0,默认10e-5
        """
        # buffer拼接
        _cache = pd.DataFrame({"timestamp": [timestamp], "waterHeight": [waterHeight]})
        buffer = pd.concat([buffer, _cache]).reset_index(drop=True)
        # buffer尺寸控制
        while len(buffer) > bufferSize:
            buffer = buffer.iloc[-bufferSize:, :]
        # buffer时间选择
        _latestTime = buffer.loc[len(buffer) - 1, ["timestamp"]].values.flatten().tolist()[0]
        _latestTimeMinus1Min = _latestTime - datetime.timedelta(minutes=1)
        # 近1分钟时间序列选择
        _bufferSelected = buffer.copy()
        _bufferSelected = _bufferSelected[_bufferSelected["timestamp"] >= _latestTimeMinus1Min]
        # 水位近1分钟数据范围与时间戳
        _timeEnd, _timeStart = _bufferSelected["timestamp"].iloc[-1], _bufferSelected["timestamp"].iloc[0]
        _timeDelta = _timeEnd - _timeStart
        _valueEnd, _valueStart = _bufferSelected["waterHeight"].iloc[-1], _bufferSelected["waterHeight"].iloc[0]
        # 水位近1分钟变化率
        _res = (volumeCalculate(_valueEnd) - volumeCalculate(_valueStart)) / _timeDelta.seconds * 60 if _timeDelta.seconds >= EPSILON else 0
        # 水位近1分钟是否持续上升
        bufferValues = _bufferSelected["waterHeight"].values.flatten().tolist()
        _bufferSelected_cache = _bufferSelected.copy()
        _bufferSelected_cache.dropna(how="any", inplace=True)
        _bufferSelected_cache.drop_duplicates(inplace=True)
        if len(_bufferSelected_cache) >= 5:
            try:
                k, b = optimize.curve_fit(linearFunc, np.linspace(0, len(bufferValues), len(bufferValues)), bufferValues,
                                          bounds=([-100, -5000], [100, 5000]))[0]
                waterHeightKeepIncrease = True if k >= waterHeightIncreaseRatio else False
            except Exception as e:
                waterHeightKeepIncrease = False
        else:
            waterHeightKeepIncrease = False
        # 当前水位是否在限值区域
        waterHeightFit = eval(waterHeightLimit.replace("x", "waterHeight"))
        # 当前排水泵是否全停
        drainPumpsAllStop = all([not item for item in drainPumpStatus])
        # 输出
        _res = np.nan if not (waterHeightFit and waterHeightKeepIncrease and drainPumpsAllStop) else _res if _res > 0 else 0
        return {"sealingLeakageVolumePerMinutes": _res, "buffer": buffer}

    @staticmethod
    def lubricateWaterMembraneThickness(**kwargs) -> float:
        """
        润滑水膜厚度计算(待补充)

        :key supplyWaterPressure: float, 供水压力, 默认 0
        :key muddySideWaterPressure: float, 浑水侧压力, 默认 0
        :key sealingBlockLiftingDistance: float, 密封块抬起量, 默认 0
        :key func: function, 润滑水膜厚度计算函数,默认 lambda Xs, Coefs: np.average(np.multiply(Xs, Coefs))
        :key coefs: list[float], 润滑水膜厚度计算函数系数,默认 [0, 0, 0]

        :return: 润滑水膜厚度
        """
        supplyWaterPressure = kwargs["supplyWaterPressure"] if "supplyWaterPressure" in kwargs.keys() else 0
        muddySideWaterPressure = kwargs["supplyWaterPressure"] if "supplyWaterPressure" in kwargs.keys() else 0
        sealingBlockLiftingDistance = kwargs["supplyWaterPressure"] if "supplyWaterPressure" in kwargs.keys() else 0
        func = kwargs["func"] if "func" in kwargs.keys() else lambda Xs, Coefs: np.average(np.multiply(Xs, Coefs))
        coefs = kwargs["coefs"] if "coefs" in kwargs.keys() else [0, 0, 0]
        return func([supplyWaterPressure, muddySideWaterPressure, sealingBlockLiftingDistance], coefs)
