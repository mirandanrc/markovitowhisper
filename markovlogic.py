#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import sounddevice as sd
from scipy.io.wavfile import write

#callback process
def markovcallback(msg):
    if(msg.data == "wakeupcall correct" or msg.data == "keep recording"):
        #rospy.loginfo("Valid wakeupcall")
        #recording command
        secondscommand = 5  # Duration of recording
        rospy.loginfo("Record your command:")
        commandrecording = sd.rec(int(secondscommand * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        write('audio/Command.wav', fs, commandrecording)  # Save as WAV file 
        flag_command = True
        rospy.loginfo("Command recorded")
        #flag command
        if (flag_command == True):
            flagsmarkov = String()
            flagsmarkov.data = "command is ready"
            commandpub.publish(flagsmarkov)
    
    if(msg.data == "invalid wakeupcall"):
        rospy.loginfo("Invalid wakeup call")

    if(msg.data == "command recorded"):
        rospy.loginfo("Command: ")

    if(msg.data == "exit call detected"):
        rospy.loginfo("Exit call detected")
        
#callback transcript
def transcriptcallback(msg):
    rospy.loginfo(msg)


#main
if __name__ == '__main__':
    rospy.init_node('markovlogic')  
    rate= rospy.Rate(2)
    fs = 44100  # Recording sample rate
    
    #subscriber
    #initsub = rospy.Subscriber("/flaginit", String, initcallback)
    markovsub = rospy.Subscriber("/flags", String, markovcallback)
    transcriptsub = rospy.Subscriber("/whisperradio", String, transcriptcallback)
    


    #publisher
    wakeupcallpub = rospy.Publisher("/flags", String, queue_size=50)
    commandpub = rospy.Publisher("/flags", String, queue_size=50)
    #startpub = rospy.Publisher("/flaginit", String, queue_size=50)  
    

    #recording wakeupcall
    secondswakeupcall = 2  # Duration of recording
    rospy.loginfo("Wakeup call:")
    wakeupcallrecording = sd.rec(int(secondswakeupcall * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write('audio/Markovito.wav', fs, wakeupcallrecording)  # Save as WAV file 
    flag_wakeupcall = True
    rospy.loginfo("Wakeup call recorded")      
    #flag wakeup call
    if (flag_wakeupcall == True):
        flagsmarkov = String()
        flagsmarkov.data = "wakeupcall recorded"
        wakeupcallpub.publish(flagsmarkov) 

    while not rospy.is_shutdown():
        rate.sleep()
        
    rospy.loginfo("Node was stopped")