import numpy as np
import pandas as pd

from TurbineEvaluateDiagnosisPackage.toolbox.v1.Method_WaterDistributor import WaterDistributor


def main():
    rpm = (np.random.rand(100) + 54).tolist()
    rpmDF = pd.DataFrame({"rpm": rpm, "condition": np.zeros_like(rpm)})
    rpmDF["condition"] = rpmDF["rpm"].mask(pd.DataFrame([rpmDF["rpm"] >= 54.054, rpmDF["rpm"] <= 55.146]).all(),
                              ["运行工况"])
    obj = WaterDistributor()
    for i in range(len(rpmDF)):
        obj.workingConditionJudgement(rpm[i])
    pressurePeak2Peak = obj.pressurePulsePeak2Peak(list(np.random.rand(1000)))
    print(obj.condition, pressurePeak2Peak)
