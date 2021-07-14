import telebot
import logging
# import time
import os


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
log_channel = os.environ['LOG_CHANNEL']
bot_token = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(bot_token, parse_mode=None)


# setup delete stickers file
delete_stickers_file = open("deletestickers.txt", "r")
delete_stickers_list = delete_stickers_file.readlines()
delete_stickers_file.close()

# setup ban stickers file
ban_stickers_file = open("banstickers.txt", "r")
ban_stickers_list = ban_stickers_file.readlines()
ban_stickers_file.close()


@bot.message_handler(content_types=['sticker'])
def delete_sticker(message):
    sticker = message.sticker.set_name
    # bot.reply_to(message, message.id)
    # noinspection PyBroadException
    try:
        if sticker in delete_stickers_list:  # Check if the pack name matches the delete stickers list.
            users_id = message.from_user.id
            bot.forward_message(log_channel, message.chat.id, message.id)
            bot.send_message(log_channel, str(r"[" + message.from_user.first_name + "]" + r"(tg://user?id=" + str(
                users_id) + ")") + " posted the above sticker\! The pack is on the delete list\!",
                             parse_mode='MarkdownV2')

            bot.reply_to(message, str(
                r"[" + message.from_user.first_name + "]" + r"(tg://user?id=" + str(users_id) + ")" + str(
                    "This sticker pack is banned from this chat\! Depending on the circumstances, you might be warned "
                    "verbally, or via the bot\.")),
                         parse_mode='MarkdownV2')

            bot.delete_message(message.chat.id, message.id)

        elif sticker in ban_stickers_list:
            users_id = message.from_user.id
            bot.forward_message(log_channel, message.chat.id, message.id)
            bot.send_message(log_channel, str(r"[" + message.from_user.first_name + "]" + r"(tg://user?id=" + str(
                users_id) + ")") + "posted the above sticker\! The pack is on the BAN list\! They have been YEETED "
                                   "from the chat\!", parse_mode='MarkdownV2')
            bot.kick_chat_member(message.chat.id, users_id, revoke_messages=True)
            bot.delete_message(message.chat.id, message.id)
        else:
            pass
    except:
        print("an error occurred")


bot.polling()
