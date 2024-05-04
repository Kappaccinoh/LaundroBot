import logging
import telegram
from telegram import *
from telegram.ext import *
import requests
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import asyncio


api_url = 'https://free-api-ryfe.onrender.com'
#api_url = 'https://laundrobot-api.onrender.com/'
#api_url = 'http://localhost:3002'
online_token = 'REDACTED'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def returnMinutesLeft(updatedAt, timeLeftUserInput):
    # Takes in the original time left (in minutes) input by the user to the bot
    # as well as the automatically generated time of update from the backend
    # does calculations to return the current time left in minutes


    #below is the code to do the simple boolean on/off
    # if timeLeftUserInput == 45:
    #     return f"  IN USE  "
    # else:
    #     return "NOT IN USE"
    #above is the code to do the simple boolean on/off

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
    

def return_formatted_current_datetime():
    # Returns a nicely formatted string of the current date and time
    singapore_datetime = datetime.now(ZoneInfo('Singapore'))
    curr_time_str = singapore_datetime.strftime("%Y\-%m\-%d %H:%M")
    return curr_time_str

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Start the bot with /start
    buttons = [
        [KeyboardButton("Status")],
        # [KeyboardButton("Update a machine")],
        # [KeyboardButton("Main Menu")]
    ]
    text = 'Hello! I am Laundrobot!\n' \
        'I am here to assist with all laundry related matters. Here are ' \
        'some of the things that I can do!\n\n' \
        'Status - Displays the status of all machines\n' \
        'Update a machine - Update the status of a specific machine\n' \
        'Main Menu - Main Menu\n\n' \
        'Please use this google form https://forms.gle/gHjJWCFcfDZJbK5m8 for any enquiries/issues'

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=ReplyKeyboardMarkup(buttons))

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Function that processes any messages received by the bot
    message = update.message
    text = message.text

    if text == 'Status':
        # washers_response_API = requests.get(f'{api_url}/washers')
        # washers_data = washers_response_API.text
        # print(washers_data)
        # washers_data_parsed = json.loads(washers_data)
        # dryers_response_API = requests.get(f'{api_url}/dryers')
        # dryers_data = dryers_response_API.text
        # dryers_data_parsed = json.loads(dryers_data)
        final_str = '`Floor|  Item   | Time Left\n'
        # for washer in washers_data_parsed:
        #     minutes_left = returnMinutesLeft(washer["updatedAt"],washer["timeLeftUserInput"])
        #     final_str += f'  9  | {washer["name"]}|   {minutes_left}\n'
        # for dryer in dryers_data_parsed:
        #     minutes_left = returnMinutesLeft(dryer["updatedAt"],dryer["timeLeftUserInput"])
        #     final_str += f'  9  | {dryer["name"][:-1]} {dryer["name"][-1]}|   {minutes_left}\n'

        washers_response_API = requests.get(f'{api_url}/seventeenWashers')
        washers_data = washers_response_API.text
        washers_data_parsed = json.loads(washers_data)
        # dryers_response_API = requests.get(f'{api_url}/seventeenDryers')
        # dryers_data = dryers_response_API.text
        # dryers_data_parsed = json.loads(dryers_data)
        for washer in washers_data_parsed:
            minutes_left = returnMinutesLeft(washer["updatedAt"],washer["timeLeftUserInput"])
            final_str += f' 17  | {washer["name"]}|   {minutes_left}\n'
        # for dryer in dryers_data_parsed:
        #     minutes_left = returnMinutesLeft(dryer["updatedAt"],dryer["timeLeftUserInput"])
        #     final_str += f' 17  | {dryer["name"][:-1]} {dryer["name"][-1]}|   {minutes_left}\n'
        final_str += '`'
        await context.bot.send_message(chat_id=update.effective_chat.id, text=final_str, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)
    elif text == 'Main Menu':
        await start(update, context)
    else:
        await start(update, context)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Function to handle any unknown messages
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command. Please press /start to start again.")

# async def update_machine(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     reply_keyboard = [[KeyboardButton("Update Floor 9")],
#                 [KeyboardButton("Update Floor 17")]]
#     text = 'Updating machines...... \nPlease select a floor.\n\nPress /cancel to return to Main Menu'

#     await update.message.reply_text(text=text, reply_markup=ReplyKeyboardMarkup(reply_keyboard))


#     return 1

# async def pick_machine(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     if update.message.text not in ["Update Floor 9", "Update Floor 17"]:
#         await update.message.reply_text(text="Sorry I am unable to process your response. Please click on /start to try again", reply_markup=ReplyKeyboardRemove())
#         return ConversationHandler.END
#     user_input = update.message.text[-2:]
#     context.user_data['floor'] = user_input
#     reply_keyboard = [[KeyboardButton("W1"),KeyboardButton("W2"),KeyboardButton("W3"),KeyboardButton("W4"),KeyboardButton("W5")],
#                       [KeyboardButton("D1"),KeyboardButton("D2"),KeyboardButton("D3"),KeyboardButton("D4"),KeyboardButton("D5")]]
#     text = f'You selected Floor {context.user_data["floor"]}...... \nPlease select a machine.\n\nPress /cancel to return to Main Menu'
#     await update.message.reply_text(text=text, reply_markup=ReplyKeyboardMarkup(reply_keyboard))

#     return 2

# async def send_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     if update.message.text not in ["W1","W2","W3","W4","W5","D1","D2","D3","D4","D5"]:
#         await update.message.reply_text(text="Sorry I am unable to process your response. Please click on /start to try again", reply_markup=ReplyKeyboardRemove())
#         return ConversationHandler.END
#     user_input = update.message.text
#     context.user_data['machine'] = user_input
#     reply_keyboard = [[KeyboardButton("15")], [KeyboardButton("30")]]
#     text = f'You selected Floor {context.user_data["floor"]} Machine {context.user_data["machine"]} \n*You can either reply to me with the specific number of minutes remaining for this machine \(E\.g\. 7, 15, 18\)*, or click the buttons below \n\n Press /cancel to return to Main Menu'


#     await update.message.reply_text(text=text, reply_markup=ReplyKeyboardMarkup(reply_keyboard), parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)

#     return 3

async def final(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.text.isnumeric():
        await update.message.reply_text(text="Sorry I am unable to process your response. Please click on /start to try again", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    user_input = update.message.text
    context.user_data['time'] = user_input

    timeLeftUserInput = int(context.user_data['time'])
    w_or_d = context.user_data["machine"][0]
    machine_number = context.user_data["machine"][1]
    floor_number_int = int(context.user_data["floor"])

    json_body = {}
    if w_or_d.upper() == 'W':
        json_body["name"] = f"Washer {machine_number}"
        context.user_data['machine_name'] = f"Washer {machine_number}"
    elif w_or_d.upper() == 'D':
        json_body["name"] = f"Dryer {machine_number}"
        context.user_data['machine_name'] = f"Dryer {machine_number}"
    json_body["timeLeftUserInput"] = timeLeftUserInput
    if floor_number_int == 9 and w_or_d.upper() == 'W':
        r = requests.put(f'{api_url}/washers/update', json=json_body)
    elif floor_number_int == 17 and w_or_d.upper() == 'W':
        r = requests.put(f'{api_url}/seventeenWashers/update', json=json_body)
    elif floor_number_int == 9 and w_or_d.upper() == 'D':
        r = requests.put(f'{api_url}/dryers/update', json=json_body)
    elif floor_number_int == 17 and w_or_d.upper() == 'D':
        r = requests.put(f'{api_url}/seventeenDryers/update', json=json_body)
    
    if r.ok:

        final_str = f'Successfully updated Floor {floor_number_int} {json_body["name"]} to have {json_body["timeLeftUserInput"]} minutes left.\n\n' \
             'Would you like me to send you a reminder when your machine is almost done? '
        reply_keyboard = [[KeyboardButton("Yes"), KeyboardButton("No")]]
        await update.message.reply_text(text=final_str, reply_markup=ReplyKeyboardMarkup(reply_keyboard))
    else:
        await update.message.reply_text(text="Error submitting information to server. /start to return to Main Menu", reply_markup=ReplyKeyboardRemove())
    return 4

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f'You cancelled. /start to begin again.'    
    await update.message.reply_text(text=text, reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""
    job = context.job
    await context.bot.send_message(job.chat_id, text=f"Beep Boop! Your laundry at Floor {job.data['floor']} {job.data['machine_name']} will be done in two minutes!")

async def reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text not in ["Yes", "No"]:
        text="Sorry I am unable to process your response." \
                " I will not be sending you a reminder. However, your machine has been updated." \
                "\n\n If you still want a reminder, you have to set the timing for the machine again. Press /start to begin."
        await update.message.reply_text(text=text, reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    user_input = update.message.text
    if int(context.user_data['time']) < 3:
        text=f"I will not send you a reminder as your laundry will be done soon. Thank you! Press /start to begin again."
    elif user_input == "Yes":
        chat_id = update.effective_message.chat_id
        context.job_queue.run_once(alarm, (float(context.user_data['time'])-2) * 60, chat_id=chat_id, name=str(chat_id), data={'floor': context.user_data['floor'], 'machine_name' : context.user_data['machine_name']})
        text=f"I will send you a reminder when your laundry is 2 minutes from being done! Press /start to begin again."
    else:
        text=f"I will not send you a reminder. Thank you! Press /start to begin again."

    await update.message.reply_text(text=text, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def start_update_loop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.job_queue.run_repeating(update_status_message, interval=60, first=1)

    await update.message.reply_text(text="Update Loop Started")


async def secretchannelmessage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:# async def nine(update: Update, context: ContextTypes.DEFAULT_TYPE)
    """Send the alarm message."""
    message = await context.bot.send_message('-1001932990612', text=f"Test Message")
    message_id = message.message_id
    print(message_id)

async def update_status_message(context: ContextTypes.DEFAULT_TYPE) -> None:

    # Constructing Final String for Lvl 9 Washers and Dryers
    # washers_response_API = requests.get(f'{api_url}/washers')
    # washers_data = washers_response_API.text

    # washers_data_parsed = json.loads(washers_data)
    # dryers_response_API = requests.get(f'{api_url}/dryers')
    # dryers_data = dryers_response_API.text
    # dryers_data_parsed = json.loads(dryers_data)
    # updated_time = return_formatted_current_datetime()
    # final_str = 'This message will be automatically updated every 1 minute \n\n' \
    # f'Last updated at {updated_time} \n\n'
    final_str = '`Floor|  Item   | Time Left\n'
    # for washer in washers_data_parsed:
    #     minutes_left = returnMinutesLeft(washer["updatedAt"],washer["timeLeftUserInput"])
    #     final_str += f'  9  | {washer["name"]}|   {minutes_left}\n'
    # for dryer in dryers_data_parsed:
    #     minutes_left = returnMinutesLeft(dryer["updatedAt"],dryer["timeLeftUserInput"])
    #     final_str += f'  9  | {dryer["name"][:-1]} {dryer["name"][-1]}|   {minutes_left}\n'

    # Constructing Final String for Lvl 17 Washers and Dryers
    washers_response_API = requests.get(f'{api_url}/seventeenWashers')
    washers_data = washers_response_API.text
    washers_data_parsed = json.loads(washers_data)
    # dryers_response_API = requests.get(f'{api_url}/seventeenDryers')
    # dryers_data = dryers_response_API.text
    # dryers_data_parsed = json.loads(dryers_data)
    for washer in washers_data_parsed:
        minutes_left = returnMinutesLeft(washer["updatedAt"],washer["timeLeftUserInput"])
        final_str += f' 17  | {washer["name"]}|   {minutes_left}\n'
    # for dryer in dryers_data_parsed:
    #     minutes_left = returnMinutesLeft(dryer["updatedAt"],dryer["timeLeftUserInput"])
    #     final_str += f' 17  | {dryer["name"][:-1]} {dryer["name"][-1]}|   {minutes_left}\n'
    final_str = final_str[:-1]
    final_str += '`'
    await context.bot.edit_message_text( final_str, chat_id='-1001932990612', message_id='14', parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)

if __name__ == '__main__':
    application = ApplicationBuilder().token(online_token).build()

    start_handler = CommandHandler('start', start)
    start_update_loop_handler = CommandHandler('start_update_loop', start_update_loop)
    secretchannelmessage_handler = CommandHandler('secretchannelmessage', secretchannelmessage)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), message)

    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    # update_handler = ConversationHandler(
    #     entry_points=[MessageHandler(filters.Regex("Update a machine"), update_machine)],
    #     states= {
    #         #0: [MessageHandler(filters.TEXT & ~filters.COMMAND, pick_floor)],
    #         1: [MessageHandler(filters.TEXT & ~filters.COMMAND, pick_machine)],
    #         2: [MessageHandler(filters.TEXT & ~filters.COMMAND, send_time)],
    #         3: [MessageHandler(filters.TEXT & ~filters.COMMAND, final)],
    #         4: [MessageHandler(filters.TEXT & ~filters.COMMAND, reminder)]
    #     },
    #     fallbacks=[CommandHandler("cancel", cancel)],
    # )
    application.add_handler(start_update_loop_handler)
    application.add_handler(secretchannelmessage_handler)
    application.add_handler(start_handler)
    # application.add_handler(update_handler)
    application.add_handler(message_handler)
    #need to start update loop whenever bot runs agian
    application.add_handler(unknown_handler)
    application.run_polling()
    