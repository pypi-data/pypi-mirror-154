import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import platform

from TurbineEvaluateDiagnosisPackage.toolbox.v1.Method_GuideVaneServomotor import GuideVaneServomotor


if 'windows' in platform.system().lower():
  plt.rcParams['font.sans-serif'] = ['SimHei']
else:
  plt.rcParams['font.sans-serif'] = ['STFangsong', 'Songti SC', 'SimHei', 'STFangsong']
plt.rcParams['axes.unicode_minus'] = False


def main():
    rpm = (np.random.rand(100) + 54).tolist()
    rpmDF = pd.DataFrame({"rpm": rpm, "condition": np.zeros_like(rpm)})
    rpmDF["condition"] = rpmDF["rpm"].mask(pd.DataFrame([rpmDF["rpm"] >= 54.054, rpmDF["rpm"] <= 55.146]).all(),
                                           ["运行工况"])
    obj = GuideVaneServomotor()
    for i in range(len(rpmDF)):
        obj.workingConditionJudgement(rpm[i])
        distanceIndex = obj.distanceIndex(list(np.random.rand(10)), 2)
        print(obj.condition, distanceIndex)

if __name__ == '__main__':
    main()