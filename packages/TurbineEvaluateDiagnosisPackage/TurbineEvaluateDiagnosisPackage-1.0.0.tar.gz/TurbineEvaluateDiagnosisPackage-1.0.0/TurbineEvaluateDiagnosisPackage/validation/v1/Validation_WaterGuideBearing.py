import datetime

import pandas as pd
import numpy as np
from TurbineEvaluateDiagnosisPackage.toolbox.v1.Method_WaterGuideBearing import WaterGuideBearing


def main():
    oilDynamicViscosity = (np.random.rand(3000) + 5).tolist()
    oilStandardViscosity = 5

    temper1 = (np.random.rand(3000) + 54).tolist()
    temper2 = (np.random.rand(3000) + 54).tolist()
    temper3 = (np.random.rand(3000) + 54).tolist()
    temper4 = (np.random.rand(3000) + 54).tolist()
    temper5 = (np.random.rand(3000) + 54).tolist()
    temper6 = (np.random.rand(3000) + 54).tolist()
    rpms = (np.linspace(3000 + 50, 50, 3000)).tolist()
    times = pd.date_range("2022-06-07 00:00:00", periods=3000, freq="0.68S").values.flatten().tolist()

    dataDF = pd.DataFrame({
        "oilDymVis": oilDynamicViscosity,
        "temper1": temper1, "temper2": temper2,
        "temper3": temper3, "temper4": temper4,
        "temper5": temper5, "temper6": temper6,
        "rpms": rpms, "times": [datetime.datetime.fromtimestamp(item / (10e8)) for item in times]
    })

    buffer = pd.DataFrame()
    obj = WaterGuideBearing()
    for i in range(len(dataDF)):
        obj.workingConditionJudgement(dataDF.loc[i, ["rpms"]].values[0],
                                      dataDF.loc[i, "temper1": "temper6"].values.tolist(),
                                      dataDF.loc[i, ["times"]].values[0])
        _oilVisIndex = obj.oilDynamicViscosity(dataDF.loc[i, ["oilDymVis"]].values[0], oilStandardViscosity)
        _padTemper = obj.bearingPadTemper(dataDF.loc[i, "temper1": "temper6"].values.tolist(), buffer=buffer,
                                          timestamp=dataDF.loc[i, ["times"]].values[0])
        buffer = _padTemper["buffer"]
        print(f"基础工况: {obj.condition}, 细节工况: {obj.detailCondition}, "
              f"轴瓦温度上升率: {obj.bearingPadTemperRiseRatio}, 油品运动黏度: {_oilVisIndex}, "
              f"轴瓦温度最大值: {_padTemper['max']}, 轴瓦温度最小值:{_padTemper['min']}, 轴瓦温度不均匀度:{_padTemper['unevenness']}, "
              f"温度突变轴瓦名称: {_padTemper['signalMutation']['name']}, 温度突变值: {_padTemper['signalMutation']['value']}, ")
        print("=" * 10)
