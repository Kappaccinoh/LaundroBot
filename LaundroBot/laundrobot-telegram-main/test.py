import logging
import telegram
from telegram import *
from telegram.ext import *
import requests
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

api_url = 'https://laundrobot-api.onrender.com'
api_url = 'http://localhost:3002'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def returnMinutesLeft(updatedAt, timeLeftUserInput):
    yymmdd = updatedAt[0:10]
    hour = updatedAt[11:13]
    minute = updatedAt[14:16]
    updated_at_str = f'{yymmdd} {hour}:{minute}'

    curr_time = (datetime.now(ZoneInfo('UTC')))
    curr_time_str = curr_time.strftime("%Y-%m-%d %H:%M")
    new_curr_time_dt = datetime.strptime(curr_time_str, "%Y-%m-%d %H:%M")

    updated_at_dt = datetime.strptime(updated_at_str, "%Y-%m-%d %H:%M")
    washer_dt_end = updated_at_dt + timedelta(minutes=timeLeftUserInput)
    minutes_left = int((washer_dt_end-new_curr_time_dt).total_seconds() / 60)
    if minutes_left >= 0:
        return f"{minutes_left:02}"
    else:
        return '00'
    

def extractUpdatedAt(date):
    yymmdd = date[0:10]
    hour = date[11:13]
    minute = date[14:16]
    
    print([yymmdd, hour, minute])
    return f'{yymmdd} {hour}:{minute}'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[KeyboardButton("Status"), KeyboardButton("Main Menu")], [KeyboardButton("Update Floor 9 Washers")], [KeyboardButton("Update Floor 9 Dryers")],
                [KeyboardButton("Update Floor 17 Washers")], [KeyboardButton("Update Floor 17 Dryers")]]
    text = 'Hello! I am Laundrobot!\n' \
        'I am here to assist with all laundry related matters. Here are ' \
        'some of the things that I can do!\n\n' \
        'Status - Displays the status of all machines\n' \
        'Update - Updates the specific machines accordingly\n\n' \
        'Please contact @limpotato for any enquiries/issues'

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=ReplyKeyboardMarkup(buttons))

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    text = message.text

    if text == 'Status':
        washers_response_API = requests.get(f'{api_url}/washers')
        washers_data = washers_response_API.text
        washers_data_parsed = json.loads(washers_data)
        dryers_response_API = requests.get(f'{api_url}/dryers')
        dryers_data = dryers_response_API.text
        dryers_data_parsed = json.loads(dryers_data)
        final_str = '`Floor|  Item   | Time Left\n'
        for washer in washers_data_parsed:
            minutes_left = returnMinutesLeft(washer["updatedAt"],washer["timeLeftUserInput"])
            final_str += f'  9  | {washer["name"]}|   {minutes_left}\n'
        for dryer in dryers_data_parsed:
            minutes_left = returnMinutesLeft(dryer["updatedAt"],dryer["timeLeftUserInput"])
            final_str += f'  9  | {dryer["name"][:-1]} {dryer["name"][-1]}|   {minutes_left}\n'

        washers_response_API = requests.get(f'{api_url}/seventeenWashers')
        washers_data = washers_response_API.text
        washers_data_parsed = json.loads(washers_data)
        dryers_response_API = requests.get(f'{api_url}/seventeenDryers')
        dryers_data = dryers_response_API.text
        dryers_data_parsed = json.loads(dryers_data)
        for washer in washers_data_parsed:
            minutes_left = returnMinutesLeft(washer["updatedAt"],washer["timeLeftUserInput"])
            final_str += f' 17  | {washer["name"]}|   {minutes_left}\n'
        for dryer in dryers_data_parsed:
            minutes_left = returnMinutesLeft(dryer["updatedAt"],dryer["timeLeftUserInput"])
            final_str += f' 17  | {dryer["name"][:-1]} {dryer["name"][-1]}|   {minutes_left}\n'
        final_str += '`'
        await context.bot.send_message(chat_id=update.effective_chat.id, text=final_str, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)
    elif text == 'Update Floor 9 Washers':
        buttons = [[KeyboardButton('Update F9W1'), KeyboardButton('Update F9W2'), KeyboardButton('Update F9W3')],
                    [KeyboardButton('Update F9W4'), KeyboardButton('Update F9W5'), KeyboardButton('Main Menu')]]
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Updating Floor 9 Washers......", reply_markup=ReplyKeyboardMarkup(buttons))
    elif text == 'Update Floor 9 Dryers':
        buttons = [[KeyboardButton('Update F9D1'), KeyboardButton('Update F9D2'), KeyboardButton('Update F9D3')],
                    [KeyboardButton('Update F9D4'), KeyboardButton('Update F9D5'), KeyboardButton('Main Menu')]]
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Updating Floor 9 Dryers......", reply_markup=ReplyKeyboardMarkup(buttons))
    elif text == 'Update Floor 17 Washers':
        buttons = [[KeyboardButton('Update F17W1'), KeyboardButton('Update F17W2'), KeyboardButton('Update F17W3')],
                    [KeyboardButton('Update F17W4'), KeyboardButton('Update F17W5'), KeyboardButton('Main Menu')]]
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Updating Floor 17 Washers......", reply_markup=ReplyKeyboardMarkup(buttons))
    elif text == 'Update Floor 17 Dryers':
        buttons = [[KeyboardButton('Update F17D1'), KeyboardButton('Update F17D2'), KeyboardButton('Update F17D3')],
                    [KeyboardButton('Update F17D4'), KeyboardButton('Update F17D5'), KeyboardButton('Main Menu')]]
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Updating Floor 17 Dryers......", reply_markup=ReplyKeyboardMarkup(buttons))
    elif len(text) >7 and len(text) < 13 and text[:6] == 'Update':
        #await context.bot.send_message(chat_id=update.effective_chat.id, text=text[:7])
        await update_machine_get_user_input(update, context)
    elif text[:3] == 'Set':
        if text[5:7] == '17':
            #17 F
            floor = '17'
            w_or_d = text[8]
            machine_number = text[9]
            timeLeftUserInput = int(text[11:14])

        elif text[5] == '9':
            #9 F
            floor = '9'
            w_or_d = text[7]
            machine_number = text[8]
            timeLeftUserInput = int(text[10:13])
        final_str = f'{floor} {w_or_d}{machine_number} {timeLeftUserInput}'
        context.user_data['machine_number_str'] = machine_number
        context.user_data['W_or_D_str'] = w_or_d
        context.user_data['floor_number_str'] = floor
        context.user_data['timeLeftUserInput'] = timeLeftUserInput
        await update_machine_with_user_input(update, context)

    elif text == 'tester':
        await tester(update, context)
    elif text == 'Main Menu':
        await start(update, context)
    else:
        await start(update, context)



async def update_machine_get_user_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    machine_number_str = msg[-1]
    W_or_D_str = msg[-2]
    if len(msg) == 12:
        floor_number_str = msg[8:10]
    else:
        floor_number_str = msg[8]
    text = f"Please reply with the number of minutes left " \
    f"for Floor {floor_number_str} {W_or_D_str}{machine_number_str}: \n\n" \
    "(Sorry the options are kinda scuffed rn) "
    keyboard_str = f"Set F{floor_number_str} {W_or_D_str}{machine_number_str}: "
    keyboard_arr = [
        [KeyboardButton(keyboard_str + str(5) + ' minutes'), KeyboardButton(keyboard_str + str(10) + ' minutes'), KeyboardButton(keyboard_str + str(15) + ' minutes')],
        [KeyboardButton(keyboard_str + str(20) + ' minutes'), KeyboardButton(keyboard_str + str(25) + ' minutes'), KeyboardButton(keyboard_str + str(30) + ' minutes')],
        [KeyboardButton('Main Menu')]
    ]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=ReplyKeyboardMarkup(keyboard_arr))

async def update_machine_with_user_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #user_input = int(update.message.text)
    json_body = {}
    if context.user_data['W_or_D_str'].upper() == 'W':
        json_body["name"] = f"Washer {context.user_data['machine_number_str']}"
    elif context.user_data['W_or_D_str'].upper() == 'D':
        json_body["name"] = f"Dryer {context.user_data['machine_number_str']}"
    json_body["timeLeftUserInput"] = context.user_data["timeLeftUserInput"]
    if context.user_data['floor_number_str'] == '9' and context.user_data['W_or_D_str'].upper() == 'W':
        r = requests.put(f'{api_url}/washers/update', json=json_body)
    elif context.user_data['floor_number_str'] == '17' and context.user_data['W_or_D_str'].upper() == 'W':
        r = requests.put(f'{api_url}/seventeenWashers/update', json=json_body)
    elif context.user_data['floor_number_str'] == '9' and context.user_data['W_or_D_str'].upper() == 'D':
        r = requests.put(f'{api_url}/dryers/update', json=json_body)
    elif context.user_data['floor_number_str'] == '17' and context.user_data['W_or_D_str'].upper() == 'D':
        r = requests.put(f'{api_url}/seventeenDryers/update', json=json_body)
    
    if r.ok:
        final_str = f'Successfully updated Floor {context.user_data["floor_number_str"]} {json_body["name"]} to have {json_body["timeLeftUserInput"]} minutes left'
        await context.bot.send_message(chat_id=update.effective_chat.id, text=final_str, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)



async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    
# async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     text_caps = ' '.join(context.args).upper()
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

# async def nine(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     washers_response_API = requests.get('http://localhost:3002/washers')
#     washers_data = washers_response_API.text
#     washers_data_parsed = json.loads(washers_data)
#     dryers_response_API = requests.get('http://localhost:3002/dryers')
#     dryers_data = dryers_response_API.text
#     dryers_data_parsed = json.loads(dryers_data)
#     final_str = 'Information on Level 9 machines:\n'
#     for washer in washers_data_parsed:
#         minutes_left = returnMinutesLeft(washer["updatedAt"],washer["timeLeftUserInput"])
#         final_str += f'{washer["name"]} : *{minutes_left}* minutes left\n'
#     for dryer in dryers_data_parsed:
#         minutes_left = returnMinutesLeft(dryer["updatedAt"],dryer["timeLeftUserInput"])
#         final_str += f'{dryer["name"]} : *{minutes_left}* minutes left\n'
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=final_str, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)

# async def seventeen(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     washers_response_API = requests.get('http://localhost:3002/seventeenWashers')
#     washers_data = washers_response_API.text
#     washers_data_parsed = json.loads(washers_data)
#     dryers_response_API = requests.get('http://localhost:3002/seventeenDryers')
#     dryers_data = dryers_response_API.text
#     dryers_data_parsed = json.loads(dryers_data)
#     final_str = 'Information on Level 17 machines:\n'
#     for washer in washers_data_parsed:
#         minutes_left = returnMinutesLeft(washer["updatedAt"],washer["timeLeftUserInput"])
#         final_str += f'{washer["name"]} : *{minutes_left}* minutes left\n'
#     for dryer in dryers_data_parsed:
#         minutes_left = returnMinutesLeft(dryer["updatedAt"],dryer["timeLeftUserInput"])
#         final_str += f'{dryer["name"][:-1]}  {dryer["name"][-1]}: *{minutes_left}* minutes left\n'
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=final_str, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)

# async def burner(item, time, context, update):
#     json_body = {
# 	"name" : "Washer 5",
# 	"timeLeftUserInput" : 555
#     }
#     r = requests.put('http://localhost:3002/washers/update', json=json_body)
#     if r.ok:
#         final_str = f'Successftes left'
#         await context.bot.send_message(chat_id=update.effective_chat.id, text=final_str, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)

# async def update(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     #/update floor item timeleft
#     floor = context.args[0]
#     item = context.args[1]
#     timeLeft = context.args[2]
#     # body = {
# 	# "name" : "Washer 5",
# 	# "timeLeftUserInput" : 555
#     # }
#     # r = requests.put('http://localhost:3002/washers/update', json =body)
#     # print(r)
#     json_body = {}
#     if item[0].upper() == 'W':
#         json_body["name"] = f"Washer {item[1]}"
#     elif item[0].upper() == 'D':
#         json_body["name"] = f"Dryer {item[1]}"
#     json_body["timeLeftUserInput"] = timeLeft
#     if floor == '9' and item[0].upper() == 'W':
#         r = requests.put('http://localhost:3002/washers/update', json=json_body)
#     elif floor == '17' and item[0].upper() == 'W':
#         r = requests.put('http://localhost:3002/seventeenWashers/update', json=json_body)
#     elif floor == '9' and item[0].upper() == 'D':
#         r = requests.put('http://localhost:3002/dryers/update', json=json_body)
#     elif floor == '17' and item[0].upper() == 'D':
#         r = requests.put('http://localhost:3002/seventeenDryers/update', json=json_body)
    
#     if r.ok:
#         final_str = f'Successfully updated Floor {floor} {json_body["name"]} to have {json_body["timeLeftUserInput"]} minutes left'
#         await context.bot.send_message(chat_id=update.effective_chat.id, text=final_str, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)

# async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [
#     [
#         InlineKeyboardButton("Option 1", callback_data='1'),
#         InlineKeyboardButton("Option 2", callback_data='2'),
#     ],
#     [InlineKeyboardButton("Option 3", callback_data='3')],
# ]
    
#     reply_markup = InlineKeyboardMarkup(keyboard)

#     await update.message.reply_text("Please choose:", reply_markup=reply_markup)

# async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Parses the CallbackQuery and updates the message text."""
#     query = update.callback_query

#     # CallbackQueries need to be answered, even if no notification to the user is needed
#     # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
#     await query.answer()

#     await query.edit_message_text(text=f"Selected option: {query.data}")

# async def showAll(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     buttons = [[KeyboardButton("Status")], [KeyboardButton("Update Floor 9 "), KeyboardButton("Update Floor 17 ")]]
#     await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome!", reply_markup=ReplyKeyboardMarkup(buttons))


async def pick_floor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    reply_keyboard = [["Boy", "Girl", "Other"]]
    await update.message.reply_text(
        f"floor? {user_input}",
    )
    context.user_data['update_response'] = user_input
    return 1

async def pick_machine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    reply_keyboard = [["Boy", "Girl", "Other"]]
    await update.message.reply_text(
        f"machine? {user_input}",
    )
    context.user_data['floor'] = user_input
    return 2

async def send_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    reply_keyboard = [["Boy", "Girl", "Other"]]
    await update.message.reply_text(
        f"time? {user_input}",
    )
    context.user_data['machine'] = user_input
    return 3

async def final(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"machine {context.user_data['machine']} floor {context.user_data['floor']} time {update.message.text}",
    )
    return ConversationHandler.END
async def number_two(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    if user_input== '1':
        await update.message.reply_text(
        f'ok {update.message.text}'
        )
    else:
        await update.message.reply_text(
        f'ok {update.message.text}'
    )
        return ConversationHandler.END
    

    

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    await update.message.reply_text(
        "Invalid Input, please select an action again"
    )

    return ConversationHandler.END

async def update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[KeyboardButton("Update Floor 9 Washers")], [KeyboardButton("Update Floor 9 Dryers")],
                [KeyboardButton("Update Floor 17 Washers")], [KeyboardButton("Update Floor 17 Dryers")]]
    text = 'You selected update. Please continue'

    await update.message.reply_text(text=text, reply_markup=ReplyKeyboardMarkup(buttons))


    return 0

online_token = 'REDACTED'
testing_token = 'REDACTED'
if __name__ == '__main__':
    application = ApplicationBuilder().token(testing_token).build()
    
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), message)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("Update a machine"), update)],
        states= {
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, pick_floor)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, pick_machine)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, send_time)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, final)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    application.add_handler(start_handler)
    application.add_handler(conv_handler)
    application.add_handler(message_handler)
    application.add_handler(unknown_handler)
    application.run_polling()
    
