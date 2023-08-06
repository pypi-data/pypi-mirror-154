import pandas as pd
import numpy as np


class GuideVaneServomotor:
  def __init__(self, **kwargs):
    """
    导叶接力器健康评估与故障诊断模块所需特征参数计算

    [1] 参数
    ----------
    WORKING_CONDITION_SECTIONS:
        list[str],运行工况判定条件在实例化该类时指定,需与工况分类参数WORKING_CONDITION中元素对应,默认["(0<=x)and(x<=1)", "(x<0)or(x>1)"]
    WORKING_CONDITION:
        list[str],运行工况判定结果在实例化该类时指定,需与工况分类参数WORKING_CONDITION_SECTIONS中元素对应,默认["停机工况", "运行工况"]

    [2] 方法
    ----------
    workingConditionJudgement:
        运行工况的判定
    distanceIndex:
        接力器行程指标值

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
    >>> obj = GuideVaneServomotor()
    >>> for i in range(len(rpmDF)):
    >>>     obj.workingConditionJudgement(rpm[i])
    >>>     distanceIndex = obj.distanceIndex(list(np.random.rand(10)), 2)
    >>>     print(obj.condition, distanceIndex)
    """

    self.WORKING_CONDITION_SECTIONS = ["(0<=x)and(x<=1)", "(x<0)or(x>1)"]
    self.WORKING_CONDITION = ["停机工况", "运行工况"]
    self.sections = kwargs["sections"] if "sections" in kwargs.keys() else self.WORKING_CONDITION_SECTIONS
    self.conditions = kwargs["conditions"] if "conditions" in kwargs.keys() else self.WORKING_CONDITION
    assert len(self.sections) == len(self.conditions), "sections 与 conditions 应具有相同长度且元素应互相对应"
    self.rpm = None
    self.condition = None

  def workingConditionJudgement(self, rpm: float):
    """
    运行工况的判定

    - 运行工况判定条件在实例化该类时使用self.WORKING_CONDITION_SECTIONS指定,并需与工况分类参数self.WORKING_CONDITION中元素对应,
        默认["(0<=x)and(x<=1)", "(x<0)or(x>1)"]
    - 运行工况判定结果在实例化该类时使用self.WORKING_CONDITION指定,并需与工况判定条件参数self.WORKING_CONDITION_SECTIONS中元素对应,
        默认["停机工况", "运行工况"]
    - 工况判断结果记录在condition属性中

    :param rpm: float, 机组转速(rpm)
    """
    self.rpm = rpm
    self.condition = self.__workingConditionJudgement()

  def __workingConditionJudgement(self):
    _determines = []
    [_determines.append(eval(item.replace("x", str(self.rpm)))) for item in self.sections]
    return np.asarray(self.conditions)[_determines][0]

  def distanceIndex(self, dists: list, maxLimit: float, EPSILON=10e-8) -> float:
    """
    接力器行程指标值

    :param dists: list[float], 接力器行程值列表
    :param maxLimit: float, 最大允许行程
    """
    return max(dists) / (maxLimit + EPSILON)
