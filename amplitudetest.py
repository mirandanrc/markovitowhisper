#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import pyaudio
import numpy as np
import time

CHUNK = 1024
RATE = 44100
THRESHOLD = 250

global CHECKING1 
global CHECKING2
CHECKING1 = True
CHECKING2 = False

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)


def amplitudecallback(msg):
    global CHECKING1
    global CHECKING2
    
    if (msg.data == "start" or msg.data == "invalid"):
        print("Restart")
        CHECKING1 = True
        CHECKING2 = False
    elif (msg.data == "Markovito"):
        print("Waiting for silence")
        CHECKING2 = True
        CHECKING1 = False

def escuchar():
    global CHECKING1
    global CHECKING2
    counter = 0
    silence_time = 0
    start_time = time.time()
   
    while True:
        data = stream.read(CHUNK)
        data = np.fromstring(data, dtype=np.int16)
        ampl = np.abs(np.average(data))
        print("Amplitude:", ampl)

        if (CHECKING1 == True and CHECKING2 == False):
            if ampl > THRESHOLD and ampl < 500:
                counter+=1
            else:
                counter = 0

            if counter >= 1:
                #CHECKING = False
                amplitudepub.publish("spike")
                print("Amplitude OK:", ampl)
                print("spike")
                counter = 0
                CHECKING1 = False
                start_time = time.time()

        if (CHECKING2 == True and CHECKING1 == False):
            if ampl < THRESHOLD:
                counter+=1
                if silence_time == 0:
                    silence_time = time.time()
                elif (time.time()-silence_time) > 10: 
                    whisperpub.publish("silence")
                    print("Amplitude DOWN:", ampl)
                    print("silence")
                    counter = 0
                    CHECKING2 = False

            else:
                counter = 0
                silence_time == 0

        # if time.time() - start_time > 10 and THRESHOLD < 700:
        #     print("flag silence sent")
        #     amplitudepub.publish("silence")
        #     print("Amplitude DOWN:", ampl)
        #     print("silence")
        #     counter = 0
        #     CHECKING2 = False

                #stream.stop_stream()
                #stream.close()
                #p.terminate()
            

if __name__ == '__main__':
    rospy.init_node('amplitudetest')
    rate = rospy.Rate(60)

    #subscriber
    amplitudesub = rospy.Subscriber("/amplitude", String, amplitudecallback)
    #publisher
    amplitudepub = rospy.Publisher("/flags", String, queue_size=50)
    whisperpub = rospy.Publisher("/amplitudeflags", String, queue_size=50)


    escuchar()

    rospy.spin()

    rospy.loginfo("Node was stopped")