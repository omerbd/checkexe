# Omer Ben David, Israel
# April 2019


import subprocess
import socket
from ip2geotools.databases.noncommercial import DbIpCity
import ipaddress
import urllib.request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import sys



def get_PID(exe_name):
	"""checks if there is a process and gets the PID"""
	table_cmd ='tasklist |awk "{ print $1\\" \\"$2 }" > tasklist.txt"'
	table_create =subprocess.check_output(table_cmd, shell =True, universal_newlines =True) # runs the upper line through cmd, prints tasklist to a text file
	table = open ('tasklist.txt', 'r')
	pid_list=[]
	for line in table: # runs through every line of the file, seperating process' names and PIDs
		end=line.find('.exe')
		process_name = line[:end]
		process_pid = line[end+5:-1]
		if process_name==exe_name: # if the process is found, get its PID to the list
			pid_list.append(process_pid)
	table.close()
	if len(pid_list)!=0: # if the list is not empty, return it. if not, the process is not running
		return pid_list
	else:
		return "ERROR"


def get_IP(pid_list):
	""" takes the pids and returns their foreign IPs in a list inside a list"""
	netstat_cmd='netstat -nao > netstat.txt'
	table_create=subprocess.check_output(netstat_cmd, shell =True, universal_newlines =True) # prints netstat into a text file through cmd
	file =open('netstat.txt', 'r')
	ip_list=[] #the list which will be returned
	for pid in pid_list:
		ip_cmd= 'awk "$5 == '+pid+' { print $0 }" netstat.txt|awk "{ print $3 }"|awk -F: " { print $1 }"|sort /uniq' # takes only Foreign IPs from netstat.txt and checks they are unique
		list_create = subprocess.check_output(ip_cmd, shell = True, universal_newlines=True)
		if list_create!='': # if not a blank line, split and move to the other list
			list_create=list_create.split()
			for IP in list_create:
				try:
					IP=ipaddress.ip_address(IP)
					IP=str(IP)
					ip_list.append(IP)
				except ValueError:
					pass
	file.close() # close the file
	return ip_list


def which_ports(ip_list):
	""" check what every port is used for, returns a list of in and out ports and their use"""
	for IP in ip_list:
		in_port =subprocess.check_output('more netstat.txt|findstr " '+IP+'"|awk "{ print $2 }"|awk -F: "{ print $2 }"',shell = True, universal_newlines=True)
		in_port=in_port.split()
		out_port =subprocess.check_output('more netstat.txt|findstr " '+IP+'"|awk "{ print $3 }"|awk -F: "{ print $2 }"',shell = True, universal_newlines=True)
		out_port=out_port.split()
		text_file=open("ports.txt", "a+") # write all the in and out ports with their use into a file
		text_file.write("In ports:")
		text_file.write('\n')
		for port in in_port:
			try: # not all the ports are known (1-1024 are assigned)
				socket.getservbyport(int(port))
				text_file.write(str(port)+" is "+socket.getservbyport(int(port)))
				text_file.write('\n') # new line
			except OSError or AttributeError: 
				text_file.write("port "+port+ "  is unknown")
				text_file.write('\n')
		text_file.write("Out ports:")
		text_file.write('\n')
		for port in out_port:
			try:
				socket.getservbyport(int(port))
				text_file.write(str(port)+" is "+socket.getservbyport(int(port)))
				text_file.write('\n')
			except OSError or AttributeError:
				text_file.write(" port "+port+ " is unknown")
				text_file.write('\n')
	try:
		text_file.close() # close the file
	except UnboundLocalError:
		pass


def where_from_IP(ip_list):
	""" check from where each foreign IP comes from"""
	text_file=open("IPLocation.txt", "a+") # write it all into a text file
	for IP in ip_list:
		try: # some IPs have an unknown location
			response = DbIpCity.get(IP, api_key='free')
			text_file.write("IP: " +IP +"    Country:   "+response.country+"    Region:   "+response.region+"    City:   "+response.city)
			text_file.write('\n')
		except KeyError:
			pass
	text_file.close() # close the file


def blacklist_ip(ip_list):
	""" using a pre-prepared list of blacklist IPs by CISCO and checking them in the list of IPs"""
	file_black = open ('blacklist.txt', 'r') # the pre-made list
	file_ip = open ('ip_list.txt','a+')
	file_result=open('ip_results.txt', 'a+')
	for ip in ip_list: # making a text file of all IPs, so we can check it with the blacklist
		file_ip.write(ip)
		file_ip.write('\n')
	for ip in file_ip:
		for line in file_black:
			if ip==line: # write in file if dangerous
				file_result.write(IP+" is dangerous.")
	file_black.close()
	file_ip.close()
	file_result.close()

def one_file():
	""" getting all previous files into one big text file"""
	end_file=open('endfile.txt', 'a+')
	end_file.write('blacklisted ip: ')
	black_file=open ('ip_results.txt','r')
	for ip in black_file: # writing all bad IPs
		end_file.write(ip)
	black_file.close()
	end_file.write('\n')
	end_file.write('all the IPs location:')
	end_file.write('\n')
	where_file=open('IPLocation.txt', 'r')
	for where in where_file: # writing every IP and its location
		end_file.write(where)
	where_file.close()
	end_file.write('\n')
	end_file.write('all the used ports:')
	end_file.write('\n')
	port_file=open('ports.txt','r')
	for port in port_file: # writing every port and its use (if known)
		end_file.write(port)
	port_file.close()
	end_file.close()

def send_mail(mail):
	""" sending the file via mail"""
	points=0
	if os.stat('ip_results.txt').st_size != 0: # if file is empty, there are no blacklisted IP so no points
		points+=2
	file_ports=open('ports.txt','r')
	for line in file_ports: # if one of the out ports is not recognized, add a point
		if line=='Out Ports:':
			while line!='In Ports:':
				if line.find('unknown')!=-1:
					points+=1
					break
	fline='your .exe got '+str(points)+ ' out of 3. 0 means clean and 3 means most dangerous.'
	with open('endfile.txt', 'r+') as f: # add the line as a first line
		content = f.read()
		f.seek(0, 0)
		f.write(fline.rstrip('\r\n') + '\n' + content)
	mail_content = '''Hello, here are the files of your recent lookup.Your file got '''+ str(points)+''' Out of 3, while 0 is the best and 3 is the worst. Have a good day!
	p.s. don't worry about the file, it's a .txt and its safe.
	'''
	sender_address = 'checkexebox@gmail.com'
	sender_pass = 'cyberproject'
	receiver_address = mail
	message = MIMEMultipart() # setting the message via MIME
	message['From'] = sender_address
	message['To'] = receiver_address
	message['Subject'] = 'Your recent CheckExe lookup'
	message.attach(MIMEText(mail_content, 'plain'))
	attach_file_name = 'endfile.txt'
	attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
	payload = MIMEBase('application', 'octate-stream')
	payload.set_payload((attach_file).read())
	encoders.encode_base64(payload) #encode the attachment
	#add payload header with filename
	payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
	message.attach(payload)
	#Create SMTP session for sending the mail
	session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
	session.ehlo() # introducing to the SMTP server
	session.starttls() #enable security
	session.login(sender_address, sender_pass) #login with mail_id and password
	text = message.as_string()
	session.sendmail(sender_address, receiver_address, text)
	session.quit() # closing session
			

def main():
	mail=sys.argv[1]
	name = input("please enter the exact name of the process:") # getting the name of the exe
	# setting all the functions to work, PIDs, IPs and such
	PIDs=get_PID(name)
	if PIDs and PIDs!="ERROR":
		IPs=get_IP(PIDs)
		if IPs and IPs!="ERROR":
			where_from_IP(IPs)
			which_ports(IPs)
			blacklist_ip(IPs)
			one_file() # setting it all to one text file
			if mail!='':
				send_mail(mail) # sending the mail
				# removing all previous text file so it won't append last sessions
				os.remove('ports.txt')
				os.remove('tasklist.txt')
				os.remove('netstat.txt')
				os.remove('IPLocation.txt')
				os.remove('ip_list.txt')
				os.remove('ip_results.txt')
				os.remove('endfile.txt')
			else:
				print ('no mail was entered')
		else:
			print ("ERROR, no internet use")
		
	else:
		print ("ERROR, no such process")
if __name__=="__main__":
	main()