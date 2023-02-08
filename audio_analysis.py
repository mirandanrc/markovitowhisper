from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import rospy
from std_msgs.msg import String

def analysis_threshold(msg):
    if msg=="hay_audio":
        threshold_audio=0.03
        samplerate, data = wavfile.read('/home/hp/pruebas/markovtest3.wav')
        length = data.shape[0] / samplerate
        # print(f"length = {length}s")
        data2=abs(data)
        data2[data2 <0.01]=0
        data2[data2 >0.2]=0
        data2=data2[9000:]
        promedio=np.mean(data2[1])
        maximo=np.max(data2[1])
        # print('El maximo es:',maximo)
        if maximo>=threshold_audio:
            pub.publish("Umbral_superado")
        else:
            pass

if __name__ == '__main__':
    rospy.init_node('audio_thresholdpy')
    pub = rospy.Publisher("/width_flag", String, queue_size=50)
    sub= rospy.Subscriber("/width_flag", String, analysis_threshold)
    rate= rospy.Rate(10)
    # print(f"number of channels = {data.shape[1]}")
    # print(data.dtype)
    rospy.spin






# time = np.linspace(0., length, data2.shape[0])
# print("El promedio es: ",promedio)
# plt.plot(time, data2[:, 1], label="Right channel")
# plt.legend()
# plt.xlabel("Time [s]")
# plt.ylabel("Amplitude")
# plt.show()