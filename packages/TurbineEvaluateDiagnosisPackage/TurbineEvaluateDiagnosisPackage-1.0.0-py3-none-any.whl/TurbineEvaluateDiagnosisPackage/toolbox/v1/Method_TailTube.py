"""
Classes
-------
1.TailWaterDoorKarmanVortex: 带通滤波并计算频带峰峰幅值
    - filtered: 滤波后的波形
    - peak2peak: 滤波后波形的峰峰值

2.TailTubeWorkCondition: 尾水管健康评估与故障诊断模块所需特征参数计算
    - workingConditionJudgement: 运行工况的判定
    - pressurePulsePeak2Peak: 计算数据列表中的峰-峰值
"""

import numpy as np
import matplotlib.pyplot as plt
import platform

from scipy.signal import firwin
from scipy.fft import fft


if 'windows' in platform.system().lower():
  plt.rcParams['font.sans-serif'] = ['SimHei']
else:
  plt.rcParams['font.sans-serif'] = ['STFangsong', 'Songti SC', 'SimHei', 'STFangsong']
plt.rcParams['axes.unicode_minus'] = False


class BandPassFilter:
    def __init__(self, order, samplingFreq, lowFreq, highFreq, window="hamming"):
        """
        带通滤波并计算频带峰峰幅值

        [1] 参数
        ----------
        order:
            int,阶数, 可设置为采样频率
        samplingFreq:
            int,采样频率
        lowFreq:
            int,带通低频值
        highFreq:
            int,带通高频值
        window:
            str, 加窗
            barthann、bartlett、blackman、blackmanharris、bohman、boxcar、chebwin、cosine、dpss、exponential、flattop、
            gaussian、general_cosine、general_gaussian、general_hamming、hamming、hann、hanning、kaiser、nuttall、parzen、
            taylor、triang、tukey

        [2] 方法
        ----------
        filter:
            根据定义的FIR滤波器对输入的波形进行带通滤波

        [3] 返回
        -------
        filtered:
            滤波后的波形

        peak2peak:
            滤波后波形的峰峰值

        [4] 示例1
        --------
        >>> # 带通滤波
        >>> samplingFreq = 1000
        >>> x = np.linspace(0, 3, samplingFreq * 3)
        >>> signal = 20 * np.sin(2 * np.pi * 50 * x)
        >>> signal_noise = signal + np.sin(2 * np.pi * 335 * x) + np.sin(2 * np.pi * 485 * x)
        >>> obj = TailWaterDoorKarmanVortex(999, 1000, 48, 52, window="bohman")
        >>> obj.filter(signal_noise)
        >>> print(obj.peak2peak)
        >>>
        >>> freq_list = np.arange(samplingFreq*3)
        >>> yy = fft(obj.filtered)  # 快速傅里叶变换
        >>> yf = abs(yy)  # 取模
        >>>
        >>> plt.figure()
        >>> plt.subplot(411)
        >>> plt.plot(signal[500:1000], 'r', label="信号")
        >>> plt.plot(signal_noise[500:1000], 'b', label="噪声信号")
        >>> plt.legend()
        >>> plt.subplot(412)
        >>> plt.plot(obj.filtered[500:1000], 'r', label="滤波后信号")
        >>> plt.plot(signal[500:1000], 'b', label="信号")
        >>> plt.legend()
        >>> plt.subplot(413)
        >>> plt.plot(obj.firFilter, 'y', label="滤波器")
        >>> plt.legend()
        >>> plt.subplot(414)
        >>> freqs = np.linspace(0, 1, len(yf)) * samplingFreq
        >>> amps = yf / (samplingFreq * 3 / 2)
        >>> plt.plot(freqs[:int(len(freqs)/2)], amps[:int(len(amps)/2)])
        >>> plt.show()
        """
        self.order = order
        self.firFilter = self.__bandpass_firwin(samplingFreq, lowFreq, highFreq, samplingFreq, window)
        self.filtered = None
        self.peak2peak = None

    def filter(self, originSignal):
        output = []
        for i in range(len(originSignal)):
            sum = 0
            if i < self.order:
                for j in range(i):
                    sum = sum + self.firFilter[j] * originSignal[i - j]
            else:
                for j in range(self.order):
                    sum = sum + self.firFilter[j] * originSignal[i - j]
            output.append(sum)
        self.filtered = output
        self.peak2peak = max(output) - min(output)

    @staticmethod
    def __bandpass_firwin(ntaps, lowcut, highcut, fs, window):
        taps = firwin(ntaps, [lowcut, highcut], fs=fs, pass_zero=False, window=window, scale=False)
        return taps


class TailWaterDoorKarmanVortex(BandPassFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TailTubeWorkCondition:
    def __init__(self, **kwargs):
        """
        尾水管健康评估与故障诊断模块所需特征参数计算

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
        >>> obj = TailTubeWorkCondition()
        >>> for i in range(0, 1000):
        >>>     obj.workingConditionJudgement(i)
        >>>     peak2Peak = obj.pressurePulsePeak2Peak(list(np.random.rand(1000)))
        >>>     print(i, obj.condition, peak2Peak)
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
