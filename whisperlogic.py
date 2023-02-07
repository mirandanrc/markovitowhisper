import rospy
import whisper
from std_msgs.msg import String

#callback subs

def whispercallback(msg):
    validwakeupcalls = [" Markovito", " markovito", " Marcovito", " marcovito", " Marko Vito", " Marko vito", " marko Vito", " marko vito", " Marco vito", " Marco Vito", " marco vito", " marco Vito"]

    if (msg.data == "wakeupcall recorded"):
        wakedata = True

        while (wakedata == True):
            rospy.loginfo("Flag Status: Wakeupcall is ready")
            model = whisper.load_model("small")
            wakeresult = model.transcribe("audio/Markovito.wav")
            wakeupcall = String()
            wakeupcall.data = wakeresult["text"]
            rospy.loginfo(wakeupcall)

            if wakeupcall.data in validwakeupcalls:
                rospy.loginfo("Valid wakeupcall")
                flagswhisper = String()
                flagswhisper.data = "wakeupcall correct"
                #rospy.loginfo(flagswhisper[0])
                flagsmarkov.publish(flagswhisper)
                rospy.loginfo("Valid wakeupcall flag sent")
                wakedata = False
            else:
                rospy.loginfo("Invalid wakeupcall")
                flagsmarkov.publish("invalid wakeupcall")
                wakedata = False

    if (msg.data == "command is ready"):
        commanddata = True
                        
        while (commanddata == True):                
            rospy.loginfo("Flag Status: Command is ready")
            model = whisper.load_model("small")
            comresult = model.transcribe("audio/Command.wav")
            command = String()
            command.data = comresult["text"]
            exitcheck = String()
            exitcheck.data = comresult["text"].split()
            rospy.loginfo(command)
            #publish transcript is ready
            flagswhisper = String()
            flagswhisper.data = "command recorded"
            flagsmarkov.publish(flagswhisper)
            rospy.loginfo("Command flag sent")
            #publish full command
            rospy.sleep(2)
            whisperpub.publish(command)
            rospy.loginfo("Command transcript sent")
            commanddata = False
                

        
#main
if __name__ == '__main__': 
    rospy.init_node('whisperlogic')
    rate= rospy.Rate(2) 
        
    #publisher
    flagsmarkov = rospy.Publisher("/flags", String, queue_size=50)
    #flagplease = rospy.Publisher("/whisperradio", String, queue_size=50)
    #flagexit = rospy.Publisher("/whisperradio", String, queue_size=50)
    whisperpub = rospy.Publisher("/whisperradio", String, queue_size=50)

    #subscriber
    whispersub = rospy.Subscriber("/flags", String, whispercallback)
    #whispersub2 = rospy.Subscriber("/flags", String, whispercallback2)
    #whispersub3 = rospy.Subscriber("/flags", String, whispercallback3)
         
    while not rospy.is_shutdown():
        rate.sleep()
     
    rospy.loginfo("Node was stopped")