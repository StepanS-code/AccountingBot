from logging import info
from time import strftime
from typing import Text
import telebot
from telebot import types
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from Sending import senddata

bot = telebot.TeleBot("2075697630:AAHOAZM6iSNcoXqQO-QI1alKEvq1jAPsI5g")

datum = list()


@bot.message_handler(commands='start')
def transaction(message):
    global datum
    datum = []
    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard= True, one_time_keyboard= True)
    Food = types.KeyboardButton("Food")
    Transport = types.KeyboardButton("Transport")
    Housing = types.KeyboardButton("Housing")
    Health = types.KeyboardButton("Health")
    Education = types.KeyboardButton("Education")
    Culture = types.KeyboardButton("Culture")
    Gifts = types.KeyboardButton("Gifts")
    Other = types.KeyboardButton("Other")
    markup_reply.add(Food,Transport,Housing,Health,Education,Culture,Gifts,Other)

    msg = bot.send_message(message.chat.id,"Choose a category", reply_markup=markup_reply)
    bot.register_next_step_handler(msg, spending)

def spending(message):
    removemarkup = types.ReplyKeyboardRemove()
    if message.text not in ["Food","Transport","Housing","Health","Education","Culture","Gifts","Other"]:
        print('love')
        msg = bot.send_message(message.chat.id,"The category you've entered does not exist", reply_markup= removemarkup)
        bot.register_next_step_handler(msg, transaction)
    else:
        global datum
        datum.append(message.text)
        msg = bot.send_message(message.chat.id, "How much have you spent?",reply_markup= removemarkup)
        bot.register_next_step_handler(msg, inputing)

def inputing(message):
    try:
        markup_inline = types.InlineKeyboardMarkup()
        item_yes = types.InlineKeyboardButton(text = "Yep👍", callback_data= "yes",)
        item_no = types.InlineKeyboardButton(text="Nope👎", callback_data= 'no')
        markup_inline.add(item_yes,item_no)
        if message.text.lower() == "done":
            bot.register_next_step_handler(bot.send_message(message.chat.id, "Exited"), nothing)
        else:  
            float(message.text)
            # print(datum)
            global datum
            datum.append(message.text)
            ts = message.date
            date = datetime.utcfromtimestamp(ts).strftime("%d.%m.%Y")
            datum.append(date)
            a = str(datum[0])
            b = str(datum[1])
            c= str(datum[2])
            d = a+" | "+b+' | '+ c
            mes = bot.send_message(message.chat.id,f''' 
            {d} \nSave this transaction?  ''',reply_markup= markup_inline )
    except: 
        msg = bot.send_message(message.chat.id, "Invalid input")
        bot.register_next_step_handler(msg, spending)


def nothing():
    pass

@bot.callback_query_handler(func= lambda call: True)
def answer(call):
    global datum
    new = [datum]
    print(new)
    if call.data == 'yes':
        senddata(new)
    if call.data == 'no':
        pass
        



bot.infinity_polling()