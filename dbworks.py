import mysql.connector
import telegram
import logging
import telebot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, ForceReply
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters, ConversationHandler
import telebot
from telebot import types
from telebot.types import Message
bot = telebot.TeleBot('1672450404:AAGWI_wKkOk1b_snJVK01EYDMCKZbnclAQA')
mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123567PRS",
        database="deliveryfoodbotdb"
        )
mycursor = mydb.cursor()
updater = Updater('1672450404:AAGWI_wKkOk1b_snJVK01EYDMCKZbnclAQA')

def userins(update,context):
    usID = update.message.from_user.id
    usName = update.message.from_user.first_name + "  " + update.message.from_user.last_name
    sql = "INSERT IGNORE INTO users (User_ID, Nickname) VALUES (%s, %s)"
    val = (usID, usName)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record has been inserted.")
    
def shopsearch(usermessage,chatid) -> int:
    keyboard = telebot.types.InlineKeyboardMarkup()
    query = "SELECT * FROM products WHERE Prod_Category LIKE %s"
    mycursor.execute(query,("%" + usermessage + "%",))
    for result in mycursor.fetchall():
        for n in range(2,5):
            if (n != 4):
                bot.send_message(chatid,result[n])
            else:
                good = result[2]
                keyboard = types.InlineKeyboardMarkup()
                cart_button= types.InlineKeyboardButton(text="Добавить в корзину", callback_data=str(good))
                keyboard.add(cart_button)
                bot.send_photo(chatid,result[n],reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
 if call.data == str(good):
     chatid = call.from_user.id
     price = show_price(call.data)
     dbfunctions.addtocart(chatid, call.data,price)
     x = str(call.data) + '(1) added to the cart'
     bot.send_message(call.message.chat.id,x)
                
def addtocart(id,item,price):
    query = "INSERT INTO cart VALUES(?,?,?)"
    mycursor.execute(query, (id,item,price))
    mydb.commit()

def summary(id):
    query = "SELECT Sum FROM cart WHERE user =:User_ID"
    mycursor.execute(query,{"User_ID" :id})
    ordsum = 0
    for item in mycursor.fetchall():
        ordsum += item[0]
    return ordsum

def empty_cart(id):
    query = "DELETE from cart WHERE user =:User_ID"
    mycursor.execute(query, {"User_ID" :id})
    mydb.commit()

def location(id,loc):
    query = "INSERT INTO orders(location) VALUES(?)"
    query = "UPDATE orders SET location = (?) WHERE User_ID = (?)"
    mycursor.execute(query,(loc,id))
    mydb.commit()
