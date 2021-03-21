import mysql.connector
import telegram
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, ForceReply
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters, ConversationHandler
bot=telegram.Bot(token='1672450404:AAGWI_wKkOk1b_snJVK01EYDMCKZbnclAQA')
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

def show_price(good):
    query = "SELECT Prod_Price FROM products WHERE product =: Prod_Name"
    mycursor.execute(query, {"Prod_Name" :product})
    all = mycursor.fetchall()
    lst = list()
    for e in all:
        e = e[0]
        lst.append(e)
    return lst[0]

def empty_cart(id):
    query = "DELETE from cart WHERE user =:User_ID"
    mycursor.execute(query, {"User_ID" :id})
    mydb.commit()

def location(id,loc):
   print('dsd')
