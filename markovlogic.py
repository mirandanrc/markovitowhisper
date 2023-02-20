#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import sounddevice as sd
from scipy.io.wavfile import write

global RECORDWAKEUPCALL
global RECORDCOMMAND
global INVALIDWAKEUPCALL
global COMMANDINTERPRETED
global EXITCALLDETECTED
RECORDWAKEUPCALL = False
RECORDCOMMAND = False
INVALIDWAKEUPCALL = False
COMMANDINTERPRETED = False
EXITCALLDETECTED = False

#callback process
def markovcallback(msg):
    global RECORDWAKEUPCALL
    global RECORDCOMMAND
    global INVALIDWAKEUPCALL
    global COMMANDINTERPRETED
    global EXITCALLDETECTED

    if(msg.data == "start" or msg.data=="spike"):
        RECORDWAKEUPCALL = True
        flagsamplitude.publish("silence")
        print("threshold detected")
    if(msg.data == "wakeupcall correct" or msg.data == "keep recording"):
        RECORDCOMMAND = True
        print("valid wakeup call")
    if(msg.data == "invalid wakeupcall"):
        INVALIDWAKEUPCALL = True
        print("invalid wakeup call")
    if(msg.data == "command interpreted"): 
        COMMANDINTERPRETED = True
        print("Command: ")  
    if(msg.data == "exit call detected"): 
        EXITCALLDETECTED = True
        print("exit call detected")
    

#callback transcript
def transcriptcallback(msg):
    rospy.loginfo(msg)

    
def wakeupcall():
    global RECORDWAKEUPCALL
    global RECORDCOMMAND
    global COMMANDINTERPRETED
    global INVALIDWAKEUPCALL
    global EXITCALLDETECTED

    while True:
        if(RECORDWAKEUPCALL == True):
            # recording wakeupcall
            seconds = 2
            print("Record your wakeup call:")
            wakeupcallrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            sd.wait()  
            write('audio/Markovito.wav', fs, wakeupcallrecording)
            print("Wakeup call recorded")
            flagsmarkov = String()
            flagsmarkov.data = "wakeupcall recorded"
            flagswhisper.publish(flagsmarkov) 
            RECORDWAKEUPCALL = False 

        if(RECORDCOMMAND == True):
            #recording command
            seconds = 5 
            print("Record your command:") 
            commandrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2) 
            sd.wait()
            write('audio/Command.wav', fs, commandrecording)  
            print("Command recorded")
            flagsmarkov = String()
            flagsmarkov.data = "command is ready" 
            flagswhisper.publish(flagsmarkov)
            RECORDCOMMAND = False 
            
        if(COMMANDINTERPRETED == True):
            rospy.loginfo("Command: ")
            COMMANDINTERPRETED = False

        if(INVALIDWAKEUPCALL == True):
            print("Invalid wakeup call")
            INVALIDWAKEUPCALL = False

        if(EXITCALLDETECTED == True): 
            print("Exit call detected")
            EXITCALLDETECTED = False

#main
if __name__ == '__main__':
    rospy.init_node('markovlogic')  
    rate= rospy.Rate(60)
    fs = 44100 

    #subscriber
    markovsub = rospy.Subscriber("/flags", String, markovcallback)
    transcriptsub = rospy.Subscriber("/whisperradio", String, transcriptcallback)

    #publisher
    flagswhisper = rospy.Publisher("/flags", String, queue_size=50)
    flagsamplitude = rospy.Publisher("/flags", String, queue_size=50)
    
    flagsamplitude.publish("start")
    
    wakeupcall()

    rospy.spin()

    rospy.loginfo("Node was stopped")