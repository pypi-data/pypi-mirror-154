import pandas as pd
import numpy as np


def linearFunc(x, k, b):
    return k * x + b


def volumeCalculate(waterHeight: float):
    H = waterHeight
    return (6.305e-8)*H**3 + 0.001746 * (H ** 2) + 4.448 * H - 2062


class WaterDistributor:
    def __init__(self, **kwargs):
        """
        导水机构健康评估与故障诊断模块所需特征参数计算

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
        pressurePulsePeak2Peak:
            计算数据列表中的峰-峰值

        [3] 返回
        -------
        condition:
            当前工况判断结果

        [4] 示例1
        --------
        >>> rpm = (np.random.rand(100) + 54).tolist()
        >>> rpmDF = pd.DataFrame({"rpm": rpm, "condition": np.zeros_like(rpm)})
        >>> rpmDF["condition"] = rpmDF["rpm"].mask(pd.DataFrame([rpmDF["rpm"] >= 54.054, rpmDF["rpm"] <= 55.146]).all(),
        >>>                                ["运行工况"])
        >>> obj = WaterDistributor()
        >>> for i in range(len(rpmDF)):
        >>>     obj.workingConditionJudgement(rpm[i])
        >>>     pressurePeak2Peak = obj.pressurePulsePeak2Peak(list(np.random.rand(1000)))
        >>>     print(obj.condition, pressurePeak2Peak)
        >>>
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

    def pressurePulsePeak2Peak(self, wave: list) -> float:
        """
        计算数据列表中的峰-峰值

        :param wave: list, 数据列表
        :return: 峰峰值
        """
        return max(wave) - min(wave)
