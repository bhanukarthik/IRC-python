
import socket, select, string, sys
import traceback
import os
#from termcolor import colored
from colorama import init, Fore, Back, Style
from random import randint

color=randint(0,6)

FORES = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE ]

STYLES = [ Style.DIM, Style.NORMAL, Style.BRIGHT ]

#prompt everytime.
def prompt() :

    sys.stdout.write(Fore.WHITE+'<You> ')
    sys.stdout.flush()
 
#main function
if __name__ == "__main__":
     
    commands="\n\n\tList of commands\n\t1.register\n\t Usgae :/register username passowrd\n\t2.exit\n\t Usage :/exit\n\t3.msg\n\t Usage :/msg to message\n\t4.create_room\n\t Usage: /create_room roomname\n\t5.join\n\t Usage : /join roomname \n\t 6.inroom\n\t Usage :/inroom roomname message\n\t7.listrooms\n\t Usage :/listrooms\n\t8.login\n\t Usage :/login username password \n\t9.ban\n\t Usage :/ban room user\n\t10.clear\n\t Usage :/clear\n\t11.nick\n\t Usage :/nick newusername\n\t12.pwd\n\t Usage :/pwd newpassword\n\t13.leave\n\t Usage :/leave roomname\n\t14.Invite\n\t Usage :/invite roomname user-list\n\t15.allow\n\t Usage :/allow roomname username\n"	



     
    host = "localhost"
    port = 5008
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.settimeout(20)
     
    # server connection
    try :
        s.connect((host, port))
    except Exception, err:
    	print traceback.format_exc()
        print Fore.RED+Style.BRIGHT+'Unable to connect'+Style.RESET_ALL+Fore.RESET
        sys.exit()
    c= True	
    flag=0
	#registration and Login module.
    while c is True:
        print Fore.GREEN+Style.BRIGHT+'If new User ,User Register Command,Syntax /register username password \n'+Style.RESET_ALL+Fore.RESET
        print Fore.GREEN+Style.BRIGHT+'else use,User Login command,Syntax /login username password \n'+Style.RESET_ALL+Fore.RESET
        sys.stdout.write('<You> ')	    
        msg = sys.stdin.readline()	
        s.send(msg)
     
	data = s.recv(4096)
 	try:
	 if data == "welcome" :
	    os.system('cls' if os.name=='nt' else 'clear')
	    print Fore.GREEN+Style.BRIGHT+'####################<WELCOME TO IRC !>#########################'+Style.RESET_ALL+Fore.RESET
	    prompt()
	    c=False
    	 elif data == "wrong":
	    print Fore.RED+Style.BRIGHT+'SERVER:wrong password!Server rejected connection!!'+Style.RESET_ALL+Fore.RESET
	    prompt()
	    continue	
	   
    	 elif data == "exist":
	    print Fore.BLUE+Style.BRIGHT+'SERVER:Username already exist,choose differnt user name'+Style.RESET_ALL+Fore.RESET
	    continue	
	    
	 elif data == "syn" :
	    print Fore.BLUE+Style.BRIGHT+'SERVER:Syntax error'+Style.RESET_ALL+Fore.RESET
	    prompt()
	    continue	  
	 else:
	        sys.stdout.write(FORES[color]+Style.BRIGHT+data+Style.RESET_ALL+Fore.RESET)
		prompt()
		continue
	except:
		print Fore.BLUE+Style.BRIGHT+'SERVER DOWN,please try after some minutes'+Style.RESET_ALL+Fore.RESET
    # chat module, user and server communication.  
      
    while 1:
        	socket_list = [sys.stdin, s]
    		color=randint(0,6)
      
        	
        	r_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        	for sock in r_sockets:
        	#input from socket:
        		    if sock == s:
        		        data = sock.recv(4096)
        		    	if not data :
                    			print Fore.YELLOW+Style.BRIGHT+'\nSorry Server is DOWN'+Style.RESET_ALL+Fore.RESET
                    			sys.exit()
                	    	elif data == 'bye':
		    			print  Fore.YELLOW+Style.BRIGHT+'\nDisconnected from chat server'+Style.RESET_ALL+Fore.RESET
	
                    			sys.exit()	
                	    	else :

		    			color=randint(0,6)
                    			sys.stdout.write(FORES[color]+Style.BRIGHT+data+Style.RESET_ALL+Fore.RESET)
                    			prompt()
             
            #input from stdin
            		    else :
                		msg = sys.stdin.readline()
                		msg = msg.strip('\n')
				if msg =='/clear':
					os.system('cls' if os.name=='nt' else 'clear')
			                print Fore.GREEN+Style.BRIGHT+'####################<WELCOME TO IRC ########################'+Style.RESET_ALL+Fore.RESET
					prompt() 
				elif msg == '/man':
					print Fore.BLUE+Style.BRIGHT+commands+Style.RESET_ALL+Fore.RESET
					prompt()			
				else:
					s.send(msg)
        	        		prompt()
                

     #except:		
	# print Fore.BLUE+Style.BRIGHT+'SERVER is busy serving other clients....please try again after few minutes'+Style.RESET_ALL+Fore.RESET
	 #break	

    s.close()

 	
