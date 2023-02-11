import rospy
import whisper
from std_msgs.msg import String

#callback subs
def whispercallback(msg):
    validwakeupcalls = [" Markovito", " Markovito.", " markovito", " markovito.", " Marcovito", " Marcovito.", " marcovito", " marcovito.", " Marko Vito", " Marko Vito.", " Marko vito", " Marko vito.", " marko Vito", " marko Vito.", " marko vito", " marko vito.", " Marco Vito", " Marco Vito.", " Marco vito", " Marco vito.", " marco Vito", " marco Vito.", " marco vito", " marco vito."]
    exitcalls = ["Exit", "exit", "Exit.", "exit."]
    model = whisper.load_model("base")

    if (msg.data == "wakeupcall recorded"):
        wakedata = True

        while (wakedata == True):
            rospy.loginfo("Flag Status: Wakeupcall is ready")
            wakeresult = model.transcribe("audio/Markovito.wav")
            wakeupcall = String()
            wakeupcall.data = wakeresult["text"]
            #wakeupcallcheck = String()
            #wakeupcallcheck.data = wakeresult["text"].split()
            rospy.loginfo(wakeupcall)

            if wakeupcall.data in validwakeupcalls:
                rospy.loginfo("Valid wakeupcall")
                flagswhisper = String()
                flagswhisper.data = "wakeupcall correct"
                flagsmarkov.publish(flagswhisper)
                rospy.loginfo("Valid wakeupcall flag sent")
                wakedata = False
            else:
                rospy.loginfo("Invalid wakeupcall")
                flagsmarkov.publish("invalid wakeupcall")
                #rospy.sleep(1)
                #flagstart = String()
                #flagstart.data = "init flag"
                #initpub.publish(flagstart)
                wakedata = False

    if (msg.data == "command is ready"):
        commanddata = True
                        
        while (commanddata == True):                
            rospy.loginfo("Flag Status: Command is ready")
            comresult = model.transcribe("audio/Command.wav")
            command = String()
            command.data = comresult["text"]
            exitcheck = String()
            exitcheck.data = comresult["text"].split()
            print(exitcheck)
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

            rospy.sleep(2)


            if exitcheck.data[-1] in exitcalls:
                rospy.loginfo("Exit call detected")
                exitflag = String()
                exitflag.data = "exit call detected"
                flagsmarkov.publish(exitflag)
                commanddata = False
            else:
                rospy.loginfo("Exit call  not detected, recording will continue")
                keeprecording = String()
                keeprecording.data = "keep recording"
                flagsmarkov.publish(keeprecording)
                commanddata = False
        
#main
if __name__ == '__main__': 
    rospy.init_node('whisperlogic')
    rate = rospy.Rate(2) 
        
    #publisher
    flagsmarkov = rospy.Publisher("/flags", String, queue_size=50)
    #initpub = rospy.Publisher("/flaginit", String, queue_size=50)
    #flagplease = rospy.Publisher("/whisperradio", String, queue_size=50)
    #flagexit = rospy.Publisher("/whisperradio", String, queue_size=50)
    whisperpub = rospy.Publisher("/whisperradio", String, queue_size=50)

    #subscriber
    #startsub = rospy.Subscriber("/flaginit", String, startcallback)
    whispersub = rospy.Subscriber("/flags", String, whispercallback)
    #whispersub3 = rospy.Subscriber("/flags", String, whispercallback3)
    
    while not rospy.is_shutdown():
        rate.sleep()
     
    rospy.loginfo("Node was stopped")