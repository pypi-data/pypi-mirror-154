from TurbineEvaluateDiagnosisPackage.toolbox.v1.Method_MainShaftSealing import MainShaftSealing


def main():
    # 润滑水膜厚度计算
    for i in range(10):
        b = MainShaftSealing.lubricateWaterMembraneThickness()
        print(b)