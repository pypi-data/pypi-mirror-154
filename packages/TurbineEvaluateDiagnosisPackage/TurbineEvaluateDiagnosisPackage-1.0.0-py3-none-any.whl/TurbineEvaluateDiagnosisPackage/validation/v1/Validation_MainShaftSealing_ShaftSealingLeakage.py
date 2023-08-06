import pandas as pd
import numpy as np
from TurbineEvaluateDiagnosisPackage.toolbox.v1.Method_MainShaftSealing import MainShaftSealing


def main():
    waterHeight = np.arange(300, 1200)
    waterHeight[200:300] = 500
    waterHeightDF = pd.DataFrame({"waterHeight": waterHeight, "timestamp": np.zeros_like(waterHeight)})
    waterHeightDF["timestamp"] = pd.date_range("2022-06-03 00:00:00", periods=900, freq="0.98S")

    obj = MainShaftSealing()
    buffer_leakageVolume = pd.DataFrame()
    for i in range(len(waterHeightDF)):
        res_leakageVolume = obj.sealingLeakageVolume(waterHeight=waterHeightDF.iloc[i, 0],
                                                     timestamp=waterHeightDF.iloc[i, 1],
                                                     buffer=buffer_leakageVolume,
                                                     drainPumpStatus=[False, False, False, False, False])
        buffer_leakageVolume = res_leakageVolume["buffer"]
        print("泄露量", waterHeightDF.iloc[i, 0], res_leakageVolume["sealingLeakageVolumePerMinutes"])
