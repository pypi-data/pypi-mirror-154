import pandas as pd
import numpy as np
from TurbineEvaluateDiagnosisPackage.toolbox.v1.Method_MainShaftSealing import MainShaftSealing


def main():
    rpm = (np.random.rand(100) + 54).tolist()
    rpmDF = pd.DataFrame({"rpm": rpm, "condition": np.zeros_like(rpm)})
    rpmDF["condition"] = rpmDF["rpm"].mask(pd.DataFrame([rpmDF["rpm"] >= 54.054, rpmDF["rpm"] <= 55.146]).all(),
                                           ["运行工况"])

    wearingDF = rpmDF.copy()
    wearingDF.columns = ["wearingValue", "timestamp"]
    wearingDF["timestamp"] = pd.date_range("2022-06-03 00:00:00", periods=100, freq="0.98S", )

    obj = MainShaftSealing()
    buffer_sealingBlock = pd.DataFrame()
    for i in range(len(wearingDF)):
        res_sealingBlock = obj.sealingBlockWearingValue(wearingDF.iloc[i, 0], wearingDF.iloc[i, 1], buffer_sealingBlock)
        buffer_sealingBlock = res_sealingBlock["buffer"]
        print("磨损率", res_sealingBlock["sealingBlockWearingValuePerMinutes"])
