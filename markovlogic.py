#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import sounddevice as sd
from scipy.io.wavfile import write

# def check_start(msg):
#    print("data en check start",msg)
#    if(msg.data=="start"):        
#        return 1
#    else:
#        return 0

#callback process
def markovcallback(msg):
    # comprobar = check_start(msg)
    # print("comprobar value return ",comprobar)
    # if(comprobar == 1):

    if(msg.data == "spike"):
        # AQUI EMPIEZA EL CODIGO (Grabación WakeupCall)
        # recording wakeupcall
        secondswakeupcall = 2  # Duration of recording
        rospy.loginfo("Wakeup call:")  # Te avisa que empezó a grabar
        wakeupcallrecording = sd.rec(int(secondswakeupcall * fs), samplerate=fs, channels=2)  # Aquí graba
        sd.wait()  # Wait until recording is finished
        write('audio/Markovito.wav', fs, wakeupcallrecording)  # Save as WAV file (Guarda la grabación)
        flag_wakeupcall = True  # Variable para indicar que terminó de grabar
        rospy.loginfo("Wakeup call recorded")  # Te avisa que terminó de grabar
        # flag wakeup call
        if (flag_wakeupcall == True):  # Si ya terminó de grabar ...
            flagsmarkov = String()
            flagsmarkov.data = "wakeupcall recorded"
            wakeupcallpub.publish(flagsmarkov)  # Manda bandera de que ya terminó de grabar y ya creó el archivo ----- PASAR A WHISPER

    #Segunda parte 
    if(msg.data == "wakeupcall correct" or msg.data == "keep recording"): #Si recibe una bandera de que sí dijeron Markovito // A partir de aqui es donde se repite si no encontró palabra de salida
        #recording command
        secondscommand = 5  # Duration of recording
        rospy.loginfo("Record your command:") #Te avisa que empieza a grabar la instrucción
        commandrecording = sd.rec(int(secondscommand * fs), samplerate=fs, channels=2) #Graba la instruccion
        sd.wait()  # Wait until recording is finished
        write('audio/Command.wav', fs, commandrecording)  # Save as WAV file  (guarda la instrucción)
        flag_command = True #Variable para indicar que terminó de grabar
        rospy.loginfo("Command recorded") #Te avisa que terminó de grabar la instrucción
        #flag command
        if (flag_command == True): #Si terminó de grabar...
            flagsmarkov = String()
            flagsmarkov.data = "command is ready" 
            commandpub.publish(flagsmarkov) #Manda una bandera de que terminó de grabar --- PASAR A WHISPER

    #AQUI RECIBE LAS DIFERENTES BANDERAS DEPENDIENDO DE LO QUE ENCONTRÓ WHISPER
    if(msg.data == "invalid wakeupcall"): #Si la wakeupcall no fue Markovito
        rospy.loginfo("Invalid wakeup call")

    if(msg.data == "command interpreted"): #La bandera de que ya terminó de transcribir la instrucción
        rospy.loginfo("Command: ")

    if(msg.data == "exit call detected"): #La bandera de que encontró la palabra de salida
        rospy.loginfo("Exit call detected")

#callback transcript
def transcriptcallback(msg): #Aquí llega la transcripción del comando
    rospy.loginfo(msg)

#main
if __name__ == '__main__':
    rospy.init_node('markovlogic')  
    rate= rospy.Rate(60)
    fs = 44100  # Recording sample rate

    #subscriber
    #initsub = rospy.Subscriber("/flaginit", String, initcallback)
    markovsub = rospy.Subscriber("/flags", String, markovcallback)
    #markovsub2 = rospy.Subscriber("/flags", String, check_start)
    transcriptsub = rospy.Subscriber("/whisperradio", String, transcriptcallback)

    #publisher
    wakeupcallpub = rospy.Publisher("/flags", String, queue_size=50)
    commandpub = rospy.Publisher("/flags", String, queue_size=50)
    #startpub = rospy.Publisher("/flaginit", String, queue_size=50)

    rospy.spin()

    rospy.loginfo("Node was stopped")