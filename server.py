from termcolor import colored
import socket, select
import csv 
import os
import traceback

#method to send default messages in common room.

def default_post (sock, message):
    for socket in SOCK_LIST:
        if socket != server and socket != sock :
            try :
                socket.send(message)
       
	    except :
               
                socket.close()
                SOCK_LIST.remove(socket)
#methos to send private message.

def msg (socket_to,message) :
	u = str(socket_to.getpeername())
        u = usernames[u].strip()
			    
	try :
                socket_to.send(message)
        except :
                socket_to.close()
                SOCK_LIST.remove(socket)
		defailt_post("\r SERVER::"+u+"Left IRC\n")


def room_chat (socket_to,sock,message) :
	for socket in socket_to:
        	if socket != sock :	
			try :
                		socket.send(message)
       			except :
                                socket_to.close()
                		SOCK_LIST.remove(socket)

 
if __name__ == "__main__":
     
    
    SOCK_LIST = [] #list of connections
    RECV_BUFFER = 5120
    PORT = 5008
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", PORT))
    server.listen(10)
 
    # Dictionries used in program,instead of database.
    usernames={}	#socket adress username map.
    logtable={}		#username passowrd map
    address={}		#username connection object map
    rooms ={}		#room name ,list of connection objects of members connected map.
    user_room={}	#username ,list of rooms user joined in.
    room_owners={}	#owners of rooms.
    ban_list={}		#banned users in rooms				
    SOCK_LIST.append(server)
 
    print "SERVER STARTED..... " + str(PORT)
       


    while 1:
        
	r_sockets,w_sockets,e_sockets = select.select(SOCK_LIST,[],[])
	 		
	for sock in r_sockets:
		command = 0
		
             
		if sock == server:

			sockfd, addr = server.accept()
			while True :	

				while True :
					data = sockfd.recv(RECV_BUFFER)        		
					try :
						command,username,password=data.split(" ")
						break
					except :
						print 'Syntax error'
						try :
							sockfd.send("syn")
						except :
							print 'Clinet left '
							break


				if command == "/register" :
						temp_name=str(sockfd.getpeername())		
						print usernames
						if username in logtable :	 
		   					sockfd.send("exist")
								                                         	
						else :
							usernames[temp_name]=str(username)
		    					logtable[username]=password	         
							SOCK_LIST.append(sockfd)
							address[username]=sockfd
							roomlist=[]
							user_room[username]=roomlist	
	                				print "Client "+temp_name+" with name "+username+" connected" 
							sockfd.send("welcome")			
							default_post(sockfd, username+" entered room\n" )				
							break
             			elif command == "/login" :
				  try:
					temp_pass =logtable[username]
					temp_pass=temp_pass.strip()
					password=password.strip()
					if username not in address:
					  if   password == temp_pass :
						temp_name=str(sockfd.getpeername())
						usernames[temp_name]=str(username)							
						SOCK_LIST.append(sockfd)
						address[username]=sockfd
						sockfd.send("welcome")
						default_post(sockfd, "\r"+username+" entered room\n")	
						break		
	  	                	  else :
                        	        	sockfd.send("wrong")
						continue
					else:
						sockfd.send("\rSERVER::you are already loged in\n")
						break	

			          except :
					sockfd.send("\rSERVER::Username dose not exist\n")	
	          		
				else :
				  break      			
                
 	        else:
  	           try:
                            data = sock.recv(RECV_BUFFER)
    			    command =0		    	    
			    username = str(sock.getpeername())
			    username = usernames[username].strip()
			    buff= data.split(" ")        		    
	    

			    if 	buff[0].strip() == "/exit":
				print 'exit'
                    		print  username+" left room "
				default_post(sock, "\r"+ username + ' left room  \n ' )
				sock.send("bye")			
				sock.close()
	                	SOCK_LIST.remove(sock)
				del address[username]
				continue			    	

			                

			    elif buff[0] == '/msg' :
				try:												
					to = buff[1]
				 	if to in logtable :
						to=address[buff[1].strip()]
						length=len(buff)
						ping="" 					
						for i in range(2,length) : 						
							ping+=str(buff[i])
							ping+=" "
						msg(to,"\r" + 'private message from' + username + ':: ' +ping+'\n')
						continue		
				 	else :
						sock.send("no")
						continue
				except :
					sock.send('\rSERVER::Wrong syntax,use man command to check syntax\n')
					continue
		
			    elif buff[0] == '/create' :
				try:							
					room = buff[1].strip()
					if room in rooms:					
						sock.send ('\rSERVER::Sorry ! room name already exisit,choose new name \n')
						continue
					else :	
						sock_room=[]
						ban_user=[]
						rooms[room]=sock_room
						ban_list[room]=ban_user
						room_owners[room]=username
						sock.send('\rSERVER::Sucessfully created room! use join command \n')	
			    			continue
				except :
					sock.send('\rSERVER::Wrong syntax,use man command to check syntax\n')
					continue

			    elif buff[0] == '/join' :
				try:
					room= buff[1].strip()
					if room in rooms:
					 ban_users=ban_list[room]
					 owner = room_owners[room]
					 room_list=user_room[username]	
					 if room not in room_list:						    
					     if username not in ban_users :					
						sock_room=rooms[room]
						sock_room.append(sock)						
						room_list.append(room)
						ping = "\r"+username+" ENTERD room"+room+"\n"	
						room_chat(sock_room,sock,ping)
						
					     else:
						sock.send('\rSERVER::You are currenlty on ban ,contact room Admin '+owner +'\n')	
						
												
					 else:
						sock.send('\rSERVER::You are already member of this room\n')
						
					    
					else :
						sock.send('\rSERVER::Sorry no room with that name\n')					
						
			    	except :
					sock.send('\rSERVER::Wrong syntax,use man command to check syntax\n')
					continue
                            elif buff[0] == '/ban' :
				try:
					room= buff[1].strip()
					member = buff[2].strip()
					
					
					if room in rooms:	
					    owner =room_owners[room].strip()					
					    if owner==username:	
						sock_room=rooms[room]
						try:	
							ban_sock=address[member]
							sock_room.remove(ban_sock)						
							room_list=user_room[member]						
							room_list.remove(room)
							ban_user=ban_list[room]
							ban_users.append(member)
							ping = "\r"+username+":: "+member+",you are BANED FROM room"+room+" > \n"	
							ban_sock.send(ping)
							continue						
						except:
							sock.send('\rSERVER::No user with the give name exisit\n')
							continue
					    else:
						sock.send('\rSERVER::You are not authorised to BAN!\n')	
						continue
					else :
						sock.send('\rSERVER::Sorry no room with that name\n')					
						continue

				except :
					sock.send('\rSERVER::Wrong syntax,use man command to check syntax\n')
					continue
                            


				
			    elif buff[0] == '/allow' :
				try:
					room= buff[1].strip()
					member = buff[2].strip()
					if room in rooms:	
					    owner =room_owners[room].strip()					
					    if owner==username:	
						sock_room=rooms[room]
						ban_user=ban_list[room]
						if member in ban_user:
						  try:	
							unban_sock=address[member]
							ban_users.remove(member)
							ping = "\r"+username+":: "+member+",you are Allowed to join room "+room+" > \n"	
							unban_sock.send(ping)
							continue						
						  except:
							sock.send('\rSERVER::No user with the give name exisit\n')
							continue

						else :
							sock.send('\rSERVER::That user is not in BanList\n')
					    else:
						sock.send('\rSERVER::You are not authorised to BAN!\n')	
						continue
					else :
						sock.send('\rSERVER::Sorry no room with that name\n')					
						continue
			    
			    	except :
					sock.send('\rSERVER::Wrong syntax,use man command to check syntax\n')
					continue
                            
			    elif buff[0] == '/inroom' :
				try:
					room = buff[1].strip()
					room_list=user_room[username]
					if room in rooms:
						if room in room_list:
							sock_room=rooms[room]
							length=len(buff)
							ping="" 					
							for i in range(2,length) : 						
								ping+=str(buff[i])
								ping+=" "
							ping = "\r"+username+" from room "+ room +":: "+ping+" \n" 
							room_chat(sock_room,sock,ping)
							continue
						else :	
							sock.send('\rSERVER::You are not in this room\n')
							continue
					else :
						sock.send ('\rSERVER::No room with the specified name!\n')
						continue
				except :
					sock.send('\rSERVER::Wrong syntax,use man command to check syntax\n')
					continue	
			    elif buff[0] =='/listrooms' :
				
				if rooms:
					list_rooms="\r\n\n\t\t List of rooms \n\n\t\t"
					list_rooms+='\n\t\t'.join(rooms)
					list_rooms+='\n\n'
					sock.send(list_rooms)
					print list_rooms
					
				else :
					sock.send('\rSERVER::No rooms exist\n')		

			    elif buff[0] =='/invite' :
				num=len(buff)
				room=buff[1]
				if room in rooms:
				 owner = room_owners[room]
				 room_list=user_room[username]
				 if username == owner or room in room_list : 
				   for i in range(2,num) : 
					if buff[i] in address :
						sock_i=address[buff[i].strip()]
						sock_i.send("\rSERVER::"+username+"Invited you to join room"+room+"\n")
					else :
						sock.send(buff[i].strip()+ "dose not exist\n")
				 else :
					sock.send("\rSERVER::You should be owner of room or memeber of room to invite others\n")
				else :
					
					sock.send("\rSERVER::No room with given name exist\n")
									
				
			    



			    elif buff[0] == '/leave':
			     try:						
				room= buff[1].strip()
				room_list=user_room[username]
				if room in rooms:					
					if room in room_list:						
						sock_room=rooms[room]
						sock_room.remove(sock)						
						room_list.remove(room)
						ping = "\r"+username+" Left room "+room+"\n"	
						room_chat(sock_room,sock,ping)
						continue
					else :
						sock.send('\rSERVER::You are not in the room\n')					
						continue
				else :
						sock.send ('\rSERVER::No room with the specified name!\n')
			     except :
					sock.send('\rSERVER::Wrong syntax,use man command to check syntax\n')
					continue	
			    
			    elif buff[0] == '/nick':
			     try:						
				n_uname= buff[1].strip()
				print n_uname	
				if n_uname not in logtable:
						
						logtable[n_uname]=logtable.pop(username)
						addr=str(sock.getpeername())
						usernames[addr]=n_uname
						address[n_uname]=address.pop(username)						
						ping = "\r"+username+" is now "+n_uname+"\n"
						sock.send('\rSERVER::Username changed sucessfully\n')
			        		default_post(sock,ping)
						continue
				else :
						sock.send('\rSERVER::Already taken user name\n')					
						continue
				
			     except :
				print traceback.format_exc()	
				sock.send('\rSERVER::Wrong syntax,use man command to check syntax\n')
				continue	
			
			    elif buff[0] == '/pwd':
			     try:						
				n_pwd= buff[1].strip()
				if n_pwd:
						
						logtable[username]=n_pwd
						sock.send('\rSERVER::Password changed sucessfully\n')
						continue
				else :
						sock.send('\rSERVER::Password should not be empty\n')					
						continue
				
			     except :
				print traceback.format_exc()	
				sock.send('\rSERVER::Wrong syntax,use man command to check syntax\n')
				continue	
		




	
			    elif buff[0] == '/list':
			     try:				
				room= buff[1].strip()
				room_list=user_room[username]
				if room in rooms:					
					if room in room_list:						
						sock_room=rooms[room]
						peer_list=[]
						peer_list_str="\r\n\n\t Members in Room "+room+"\n\t"
						for s in sock_room:
							peer = str(s.getpeername())						
							peer =usernames[peer]
							peer_list.append(peer)
						peer_list_str +='\n\t'.join(peer_list)
						peer_list_str +='\n'
						sock.send(peer_list_str)					
						continue
					else :
						sock.send('\rSERVER::You are not in the room\n')					
						continue
				else :
						sock.send ('\rSERVER::No room with the specified name!\n')
			    

			     except :
					sock.send('\rSERVER::Wrong syntax,use man command to check syntax\n')
					continue	
			
												        	 
			    elif data :		 
				default_post(sock, "\r"+ username + ':: ' + data +'\n')

        	    
		   except:
				print traceback.format_exc()
				username = str(sock.getpeername())
			    	username = usernames[username].strip()
			        default_post(sock, "\r "+username+" left room\n")
                		print username+" left room\n"
                		sock.close()
             			SOCK_LIST.remove(sock)
           			continue
		     
    server.close()

