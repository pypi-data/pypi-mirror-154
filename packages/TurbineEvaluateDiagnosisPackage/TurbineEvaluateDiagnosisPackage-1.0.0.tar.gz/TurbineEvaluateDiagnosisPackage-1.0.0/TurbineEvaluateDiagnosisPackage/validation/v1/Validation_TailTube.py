import numpy as np
import matplotlib.pyplot as plt

from scipy.fft import fft

from TurbineEvaluateDiagnosisPackage.toolbox.v1.Method_TailTube import TailWaterDoorKarmanVortex
from TurbineEvaluateDiagnosisPackage.toolbox.v1.Method_TailTube import TailTubeWorkCondition


def mainBandPassFilter():
    samplingFreq = 1000
    x = np.linspace(0, 3, samplingFreq * 3)
    signal = 20 * np.sin(2 * np.pi * 50 * x)
    signal_noise = signal + np.sin(2 * np.pi * 335 * x) + np.sin(2 * np.pi * 485 * x)
    obj = TailWaterDoorKarmanVortex(999, 1000, 48, 52, window="bohman")
    obj.filter(signal_noise)
    print(obj.peak2peak)

    freq_list = np.arange(samplingFreq*3)
    yy = fft(obj.filtered)  # 快速傅里叶变换
    yf = abs(yy)  # 取模

    plt.figure()
    plt.subplot(411)
    plt.plot(signal[500:1000], 'r', label="信号")
    plt.plot(signal_noise[500:1000], 'b', label="噪声信号")
    plt.legend()
    plt.subplot(412)
    plt.plot(obj.filtered[500:1000], 'r', label="滤波后信号")
    plt.plot(signal[500:1000], 'b', label="信号")
    plt.legend()
    plt.subplot(413)
    plt.plot(obj.firFilter, 'y', label="滤波器")
    plt.legend()
    plt.subplot(414)
    freqs = np.linspace(0, 1, len(yf)) * samplingFreq
    amps = yf / (samplingFreq * 3 / 2)
    plt.plot(freqs[:int(len(freqs)/2)], amps[:int(len(amps)/2)])
    plt.show()


def main_TailTubeWorkCondition():
    # 工况的判断
    obj = TailTubeWorkCondition()
    for i in range(0, 1000):
        obj.workingConditionJudgement(i)
        print(i, obj.condition)


def main_TailTubePressurePeak2Peak():
    # 峰峰值计算
    obj = TailTubeWorkCondition()
    for i in range(0, 1000):
        peak2Peak = obj.pressurePulsePeak2Peak(list(np.random.rand(1000)))
        print(i, peak2Peak)
