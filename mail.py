from email.header import Header
from email.mime.text import MIMEText
from pathlib import Path
import argparse
import smtplib

def sendEmail(sender,receiver,subject,msg, mail_host, mail_user,mail_pass):
	message = MIMEText(msg, 'plain', 'utf-8')
	message['From'] = sender
	message['To'] = ','.join(receiver)
	message['Cc'] = ','.join([sender]) #抄送一份给自己，避免当成垃圾邮件
	message['Subject'] = Header(subject, 'utf-8')
	try:
		smtpObj = smtplib.SMTP()
		smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
		smtpObj.login(mail_user,mail_pass)
		smtpObj.sendmail(sender, receiver, message.as_string())
		smtpObj.quit()
		print("邮件发送成功")
	except Exception as e:
		print(e)
		print("Error: 无法发送邮件")


def sendEmailByArgs(subject,msg):
	parser = argparse.ArgumentParser()
	# parser.add_argument('-f', '--file')
	parser.add_argument('-s', '--sender')
	parser.add_argument('-r', '--receiver')
	parser.add_argument('--host')
	parser.add_argument('-u', '--username')
	parser.add_argument('-p', '--password')

	args = parser.parse_args()
	sender = args.sender
	receiver = args.receiver
	host = args.host
	username = args.username
	password = args.password

	print(args)
	print(sender)
	print(receiver)
	print(type(receiver))
	receiver = list(map(str, receiver.split(',')))
	print(receiver)
	print(type(receiver))

	sendEmail(sender, receiver, subject, msg, host, username, password)

	

def main():

	file = Path('./result.txt')
	# file = Path(args.file)
	msg =""
	with file.open() as f:
		msg = f.read()
	print(msg)

	sendEmailByArgs("Freenom-Renew",msg)


if __name__ == '__main__':
	# main()
	sendEmailByArgs("sub","msg")
