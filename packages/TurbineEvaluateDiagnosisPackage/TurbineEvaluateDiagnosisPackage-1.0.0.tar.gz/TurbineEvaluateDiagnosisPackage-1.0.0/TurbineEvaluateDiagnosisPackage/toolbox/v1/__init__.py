"""
Classes
-------
1.Method_MainShaftSealing: 主轴密封健康评估与故障诊断模块所需特征参数计算
    - workingConditionJudgement: 运行工况的判定
    - sealingBlockWearingValue: 密封块磨损速率计算
    - sealingLeakageVolume: 密封泄漏量计算
    - lubricateWaterMembraneThickness: 润滑水膜厚度计算(待补充)

2.Method_GuideVaneServomotor: 导叶接力器健康评估与故障诊断模块所需特征参数计算
    - workingConditionJudgement: 运行工况的判定
    - distanceIndex: 接力器行程指标值

3.Method_WaterGuideBearing: 水导轴承健康评估与故障诊断模块所需特征参数计算
    - workingConditionJudgement: 运行工况的判定
    - oilDynamicViscosity: 油品运动黏度指标量计算
    - bearingPadTemper: 轴瓦温度计算值及信号突变判断
        - 最大值
        - 最小值
        - 不均匀度
        - 轴瓦温度信号突变情况
            - 突变的温度测点名称
            - 突变的值

4.Method_Turbine:转轮健康评估与故障诊断模块所需特征参数计算
    - workingConditionJudgement: 运行工况的判定
    - pressurePulsePeak2Peak: 计算数据列表中的峰-峰值

5.Method_TailTube: 尾水管健康评估与故障诊断模块所需特征参数计算
    - TailWaterDoorKarmanVortex: 带通滤波并计算频带峰峰幅值
        - filtered: 滤波后的波形
        - peak2peak: 滤波后波形的峰峰值

    - TailTubeWorkCondition: 尾水管健康评估与故障诊断模块所需特征参数计算
        - workingConditionJudgement: 运行工况的判定
        - pressurePulsePeak2Peak: 计算数据列表中的峰-峰值

6.Method_WaterDistributor: 导水机构健康评估与故障诊断模块所需特征参数计算
    - workingConditionJudgement: 运行工况的判定
    - pressurePulsePeak2Peak: 计算数据列表中的峰-峰值
"""

from . import *
