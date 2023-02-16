#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import pyaudio
import numpy as np

CHUNK = 1024
RATE = 44100
THRESHOLD =700

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16,
                 channels=1,
                 rate=RATE,
                 input=True,
                 frames_per_buffer=CHUNK)

checking = True



if __name__ == '__main__':
     rospy.init_node('amplitudetest')
     rate= rospy.Rate(60)

     #publisher
     commandpub = rospy.Publisher("/flags", String, queue_size=50)

     commandpub.publish("spike")

     while True:
         if checking:
             data = stream.read(CHUNK)
             data = np.fromstring(data, dtype=np.int16)
             ampl = np.abs(np.average(data))
             if ampl > THRESHOLD:
                 commandpub.publish("spike")
                 print("Amplitude:", ampl)
                 print("spike")
                 checking = False
                 input()
             print("Amplitude:", ampl)
         else:
             restart = input("Press R to restart: ")
             if restart == 'r':
                 checking = True

     stream.stop_stream()
     stream.close()

     p.terminate()

     rospy.spin()

     rospy.loginfo("Node was stopped")