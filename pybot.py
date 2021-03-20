import logging
import dbworks
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, ForceReply
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters, ConversationHandler
bot=telegram.Bot(token='1672450404:AAGWI_wKkOk1b_snJVK01EYDMCKZbnclAQA')
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
SHOPPING, CARTING, ORDERING = range(3)
shop, cart, history, order = range(4)

def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Привет! Тебя приветствует DeliveryFoodMattBot.')
    dbworks.userins(update, context)
    keyboard = [
        [
            InlineKeyboardButton("Перейти в магазин", callback_data=str(shop))],
            [InlineKeyboardButton("Открыть корзину", callback_data=str(cart))],
            [InlineKeyboardButton("Посмотреть историю заказов", callback_data=str(history)),
        ],
    [InlineKeyboardButton("Оформить заказ", callback_data=str(order))],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Главное меню:', reply_markup=reply_markup)
def shop(update: Update, context: CallbackContext)-> int:
    query = update.callback_query
    keyboard=[[InlineKeyboardButton('Бакалея',callback_data='Бакалея')],
                [InlineKeyboardButton('Мясо',callback_data='Мясо')],
                  [InlineKeyboardButton('Рыба',callback_data='Рыба')],
                  [InlineKeyboardButton('Молоко',callback_data='Молоко')],
                  [InlineKeyboardButton('Назад',callback_data='Назад')]]
    reply_markup=InlineKeyboardMarkup(keyboard)
    bot.edit_message_reply_markup(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup)
        
def cart(update: Update, context: CallbackContext)-> int:
    print('dsa')
def order()-> None:
    print('gfd')
def button(update: Update, context: CallbackContext) -> int:
    chatid =  update.callback_query.message.chat.id
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    #query.edit_message_text(text=f"Переход: {query.data}")
    choice = query.data
    if choice == str(shop):
        shop(update,context)
    if choice == str(cart):
        cart(update,context)
    if choice == 'Бакалея':
        dbworks.shopsearch('Бакалея',chatid)
    if choice == 'Мясо':
        dbworks.shopsearch('Мясо',chatid)
    if choice == 'Рыба':
        dbworks.shopsearch('Рыба',chatid)
    if choice == 'Молоко':
        dbworks.shopsearch('Молоко',chatid)
    if choice == 'Назад':
        keyboard = [
        [InlineKeyboardButton("Перейти в магазин", callback_data=str(shop))],
        [InlineKeyboardButton("Открыть корзину", callback_data=str(cart))],
        [InlineKeyboardButton("Посмотреть историю заказов", callback_data=str(history)),
        ],
        [InlineKeyboardButton("Оформить заказ", callback_data=str(order))],
    ]
        reply_markup=InlineKeyboardMarkup(keyboard)
        bot.edit_message_reply_markup(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup)
    #if choice == str(good):
     #   price = dbworks.show_price(call.data)
      #  dbworks.addtocart(chatid,good,price)
       # x = str(good) + '1 штука добавлена в корзину'
        
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Напишите /start, чтобы начать работу с ботом.")


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("1672450404:AAGWI_wKkOk1b_snJVK01EYDMCKZbnclAQA")

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    #updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, updater))
    conv_handler = ConversationHandler(
      entry_points=[CommandHandler('start', start)],
                                     states={
             SHOPPING: [CallbackQueryHandler(shop, pattern='^' + str(shop) + '$'),
             MessageHandler(Filters.regex('^(Text)$'),
                                  shop),],
            
        },
        fallbacks=[CommandHandler('start', start)],
    )

    updater.dispatcher.add_handler(conv_handler)
    
    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
