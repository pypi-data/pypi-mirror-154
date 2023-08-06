import pandas as pd
import numpy as np

from TurbineEvaluateDiagnosisPackage.toolbox.v1.Method_Turbine import Turbine


def main():
    # 工况的判断
    rpm = (np.random.rand(100) + 54).tolist()
    rpmDF = pd.DataFrame({"rpm": rpm, "condition": np.zeros_like(rpm)})
    rpmDF["condition"] = rpmDF["rpm"].mask(pd.DataFrame([rpmDF["rpm"] >= 54.054, rpmDF["rpm"] <= 55.146]).all(),
                                           ["运行工况"])
    obj = Turbine()
    for i in range(len(rpmDF)):
        obj.workingConditionJudgement(rpm[i])
        print(obj.condition)

    wave = np.sin(np.linspace(0, 5, 1000))
    peak2Peak = obj.pressurePulsePeak2Peak(wave)
    print(peak2Peak)
