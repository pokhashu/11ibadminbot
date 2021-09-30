
TOKEN = ''

import telebot
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

bot = telebot.TeleBot(TOKEN)
hw = {}
settings = {}
# @bot.message_handler(content_types=["text"])
# def repeat_all_messages(message):
#     bot.send_message(279714843, message)

@bot.message_handler(commands=['n'])
def absent(message):
	bot.send_message(279714843, f"{message.text[2::]} будет отсутствовать")

@bot.message_handler(commands=['hw'])
def homework(message):
	for ok in message.text:
		if ok in ['ok', 'done', 'ок', 'готово']:
			msg = ""
			for i in hw:
				msg += i + " " + hw[i] + "\n"
			bot.send_message(-1001543181940, msg)

	if message.text == "/hw":
		msg = ""
		for i in hw:
			msg += i + " " + hw[i] + "\n"
		bot.send_message(message.chat.id, msg)
	if message.chat.id == message.from_user.id and len(message.text)>3:
		hw[message.text[3::].split()[0]] = message.text[3::].split()[1]

@bot.message_handler(commands=['mute'])
def mute(message):
	time = message.text[7::] * 60
	bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.json['from']['id'], can_send_messages = False, until_date=time)
	bot.delete_message(message.chat.id, message.id)

@bot.message_handler(commands=['unmute'])
def unmute(message):
	bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.json['from']['id'], can_send_messages = True)
	bot.delete_message(message.chat.id, message.id)



@bot.message_handler(commands=['restrict'])
def restrict(message):
	perms = message.text[10:17:].split()
	indx = 0
	for i in perms:
		print(i)
		if perms[indx] == 0:
			i = False
		elif int(i) == 1:
			perms[indx] = True
		else:
			perms[indx] = False
		indx += 1
	bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.json['from']['id'],
	 can_send_media_messages = perms[0], can_send_polls = perms[1], can_change_info = perms[2], can_pin_messages = perms[3])
	bot.delete_message(message.chat.id, message.id)

@bot.message_handler(commands=['promote'])
def promote(message):
	pass

@bot.message_handler(commands=['paec']) #parental advisory explıcıt content
def paec(message):
	pass
	

@bot.message_handler(commands=['all'])
def all(message):
	members_id = {}
	msg = ""
	for i in members:
		msg += "@" + bot.get_chat_member(message.chat.id, members[i]) + "\n"
	bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['schedule'])
def schedule(message):
	
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
	
	reg_url1 = "http://www.mtk-bks.by/rasklad/" # reg_url1 = "http://www.mtk-bks.by/rasklad/?id=11-ИБ" СДЕЛАЙ БЛЯ ПЖШКА
	req1 = Request(url=reg_url1, headers=headers) 
	html1 = urlopen(req1)
	charset1=html1.info().get_content_charset()
	content1=html1.read().decode('utf-8')
	
	reg_url2 = "http://www.mtk-bks.by/rasklad2/"
	req2 = Request(url=reg_url2, headers=headers) 
	html2 = urlopen(req2)
	charset2=html2.info().get_content_charset()
	content2=html2.read().decode('utf-8')
	
	soup1 = BeautifulSoup(content1, features="html.parser")
	table1 = soup1.find_all("table")[0]
	date_str = table1.find("h1").text
	
	l = len(date_str)
	integ = []
	i = 0
	while i < l:
	    s_int = ''
	    a = date_str[i]
	    while '0' <= a <= '9':
	        s_int += a
	        i += 1
	        if i < l:
	            a = date_str[i]
	        else:
	            break
	    i += 1
	    if s_int != '':
	        integ.append(int(s_int))
	date1 = int(integ[1])
	
	
	
	soup2 = BeautifulSoup(content2, features="html.parser")
	table2 = soup2.find_all("table")[0]
	date_str2 = table2.find("h1").text
	
	
	l = len(date_str2)
	integ2 = []
	i = 0
	while i < l:
	    s_int = ''
	    a = date_str2[i]
	    while '0' <= a <= '9':
	        s_int += a
	        i += 1
	        if i < l:
	            a = date_str2[i]
	        else:
	            break
	    i += 1
	    if s_int != '':
	        integ2.append(int(s_int))
	date2 = int(integ2[1])
	
	
	
	if date1 > date2:
		table = soup1.find_all("table")[1]
		pars = table.find_all("td")
		pary = []
		for i in pars:
			if "\xa0" in i.text:
				continue
			pary.append(i.text)
		for i in pary:
			if i == "":
				pary.remove(i)
		for i in pary:
			try:
				if "пара" in pary[pary.index(i)+1]:
					pary.insert(pary.index(i)+1, "\n")
			except:
				break
		for i in pary:
			try:
				if "пара" in pary[pary.index(i)-1]:
					pary[pary.index(i)] = pary[pary.index(i)] + " | Аудитория"
			except:
				break
		string = ""
		for i in pary:
			try:
				if "\n" in pary[pary.index(i)+1]:
					pary.remove(pary.index(i)+1)
			except:
				break
		for i in pary:
			string += i + " "
		bot.send_message(message.chat.id, string)
		bot.pin_chat_message(message.chat.id, message.id + 1)
	
	elif date2 > date1:
		table = soup2.find_all("table")[1]
		pars = table.find_all("td")
		pary = []
		for i in pars:
			if "\xa0" in i.text:
				continue
			pary.append(i.text)
		for i in pary:
			if i == "":
				pary.remove(i)
		for i in pary:
			try:
				if "пара" in pary[pary.index(i)+1]:
					pary.insert(pary.index(i)+1, "\n")
			except:
				break
		for i in pary:
			try:
				if "пара" in pary[pary.index(i)-1]:
					pary[pary.index(i)] = pary[pary.index(i)] + " | Аудитория"
			except:
				break
		string = ""
		for i in pary:
			try:
				if "\n" in pary[pary.index(i)+1]:
					pary.remove(pary.index(i)+1)
			except:
				break
		for i in pary:
			string += i + " "
		bot.send_message(message.chat.id, string)
		bot.pin_chat_message(message.chat.id, message.id + 1)


	


if __name__ == '__main__':
     bot.infinity_polling()
