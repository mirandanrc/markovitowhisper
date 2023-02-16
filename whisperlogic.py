import rospy
import whisper
from std_msgs.msg import String

#callback subs
def whispercallback(msg):
    validwakeupcalls = [" Markovito", " Markovito.", " markovito", " markovito.", " Marcovito", " Marcovito.", " marcovito", " marcovito.", " Marko Vito", " Marko Vito.", " Marko vito", " Marko vito.", " marko Vito", " marko Vito.", " marko vito", " marko vito.", " Marco Vito", " Marco Vito.", " Marco vito", " Marco vito.", " marco Vito", " marco Vito.", " marco vito", " marco vito."]
    exitcalls = ["Exit", "exit", "Exit.", "exit."]
    model = whisper.load_model("base")

    #AQUI EMPIEZA EL CÓDIGO
    
    #Analiza si hay un markovito
    if (msg.data == "wakeupcall recorded"): #Si la mandera que le llegó es que ya existe grabación de la wakeupcall...
        wakedata = True 

        while (wakedata == True):
            rospy.loginfo("Flag Status: Wakeupcall is ready") #Te avisa que encontró la bandera de que ya existe la grabación de wakeupcall
            wakeresult = model.transcribe("audio/Markovito.wav") #Transcribe el audio de la grabación deñwakeupcall
            wakeupcall = String()
            wakeupcall.data = wakeresult["text"]
            rospy.loginfo(wakeupcall) #Te muestra qué obtuvo al transcribir la grabación de la wakeupcall

            if wakeupcall.data in validwakeupcalls: #Checa si la transcripción de la grabación de la wakeupcall coincide con las wakeupcalls válidas (si dice markovito o no)
                rospy.loginfo("Valid wakeupcall") #Te avisa que sí coincide
                flagswhisper = String()
                flagswhisper.data = "wakeupcall correct"
                flagsmarkov.publish(flagswhisper) #Publica la bandera de que sí dijeron Markovito
                rospy.loginfo("Valid wakeupcall flag sent") #Te avisa que ya mandó la bandeta de que sí dice Markovito
                wakedata = False #corta el ciclo para no seguir checando   ----- PASAR A MARKOVITO
            else: #Si no coincide con Markovito ...
                rospy.loginfo("Invalid wakeupcall") #Te avisa que no encontró una wakeupcall válida
                flagsmarkov.publish("invalid wakeupcall") #Publica una bandera de que no dijeron Markovito 
                wakedata = False #corta el ciclo para dejar de checar  ----- PASAR A MARKOVITO
        #else:
        #    print("else de p2")
    
    #Hay un audio con posible comando
    if (msg.data == "command is ready"): #Si recibe la bandera de que ya existe el archivo de la instruccióm
        commanddata = True
                        
        while (commanddata == True):                
            rospy.loginfo("Flag Status: Command is ready") #Te avisa que recibió la bandera de que la grabación está lista
            comresult = model.transcribe("audio/Command.wav") #Transcribe la grabación
            command = String()
            command.data = comresult["text"] #Aquí guarda la trascripción de la instruccion completa
            exitcheck = String()
            exitcheck.data = comresult["text"].split() #Aquí la divide para buscar la palabra de salida
            print(exitcheck) #La imprime para que la puedas visualizar
            rospy.loginfo(command)
            #publish transcript is ready
            flagswhisper = String()
            flagswhisper.data = "command interpreted" #Manda una bandera de que ya transcribió la instruccion
            flagsmarkov.publish(flagswhisper)
            rospy.loginfo("Command flag sent") #Te avisa que ya mandó la bandera de que está lista la transcipción
            #publish full command
            rospy.sleep(2)
            whisperpub.publish(command) #Manda tu comando al tópico especial para la transcipción
            rospy.loginfo("Command transcript sent")  #Te avisa que ya mandṕ el comando la trasncripción

            rospy.sleep(2)

            if exitcheck.data[-1] in exitcalls: #Si en la instrucción encuentra la palabra de salida...
                rospy.loginfo("Exit call detected") #Te avisa que la encontró
                exitflag = String()
                exitflag.data = "exit call detected"
                flagsmarkov.publish(exitflag) #Manda una bandera de que la encontró
                commanddata = False #Rompe el ciclo de transcipción de instrucción ---- PASAR A MARKOVITO
            else: #Si no encuentra palabra de salida (osea que te siguen diciendo la instrucción)
                rospy.loginfo("Exit call  not detected, recording will continue") #Te avisa que no encontró palabra de salida y seguirá grabando
                keeprecording = String()
                keeprecording.data = "keep recording" 
                flagsmarkov.publish(keeprecording) # Te indica que grabes otro audio de instruccion
                commanddata = False #Rompe ciclo de transcripción de instruccion ---- PASAR A MARKOVITO
        
#main
if __name__ == '__main__': 
    rospy.init_node('whisperlogic')
    rate = rospy.Rate(60) 
        
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
    
    flagsmarkov.publish("spike")
    
    rospy.spin()
     
    rospy.loginfo("Node was stopped")