This IRC application is ubuntu based,not comaptible with windows,built using python 2.7.
In this application no database is used,all the data is stored in program memory,using dictionries.
Mutliple client handling is achived by using "select.select()" function present in python,which is similar to unix select.

1.
execute server.py

python server.py

2.In new terminal or from another computer execute client.py

python client.py



List of commands that can be used by client

1.register
 Usgae :/register username passowrd
 description :This is the command to use for user registration.
	example :
		/register user1 password1


2.exit 
 Usage :/exit
 description :Once registerd,you can chat or exit from the room,to exit you have to use this command.
	example:
		/exit

3.msg
 Usage :/msg to message
 description :This is command to send private message to a particular user .
	example:
		/msg user2 hello		


4.create
	 Usage: /create roomname
	 description:This is the command to create a room,one should use " join " command to join room.
		example :
			/create #cs591 	

5.join
	 Usage : /join roomname
         description:This is the command to join a room 
		example:
			/join #cs591
	 
6.inroom
 	Usage :/inroom roomname message
	description:This is the command to post in a room ,if you are member of the room.
			example:
				/inroom #cs591 I am karthik.
		 
	
7.listrooms

	 Usage :/listrooms
	 description:This is the command to list the rooms present in IRC.
			example:
				/listrooms


8.login
		 Usage :/login username password 
		 description:This is the command to  login into IRC.
			example:
				/login user1 password1

	
9.ban 
	Usage :/ban room user
	description:This command is to ban a user from a particular room(only room owner can do this)
			example:
				/ban #cs591 user10
	
10.clear
	 Usage :/clear
         description:This command is to clear user screen,similar to "clear" in unix shell.
	
			
		
11.nick
	 Usage :/nick newusername
	description:This command is to change one's username.
		example:
			/nick karthik.

12.pwd
	 Usage :/pwd newpassword
	 decription:This command is to change one's password.
		example:
			/pwd pass
13.leave
 
	Usage :/leave roomname
	decription:This command is to leave a room.
		
		example:
			/leave #cs591

14.Invite
 	Usage :/invite roomname user-list
	decription:This command is to invite users to join room.
		
			example:
				/invite #cs591 user1 user2 ....userx

15.allow
	
	Usage :/allow roomname user
	decription:This command is to remove ban on user in a particular room.
		
			example:
				/allow #cs591 user1 
	
