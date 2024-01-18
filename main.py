import telebot
import info
from telebot import types
import json
token = ""
bot = telebot.TeleBot(token=token)
@bot.message_handler(commands=['start']) #/start
def start(message):
      try:
            bot.send_message(message.chat.id, f"Здравствуйте, {message.from_user.first_name}.\nЯ бот, в котором ты можешь пройти тестирование на знание столиц стран мира!.")
            bot.send_message(message.chat.id, "Нажмите на команду, чтобы начать /start_test")
            with open("users.json", "r") as f:
                  users = json.load(f)
            if str(message.chat.id) not in users:
                  users[message.chat.id] = {"id": message.chat.id, "step": 1, "total": 0}
            with open("users.json", "w") as f:
                  json.dump(users, f, ensure_ascii=False)
      except:
            bot.send_message(message.chat.id, "Произошла ошибка.")

@bot.message_handler(commands=['help']) #/help
def help(message):
      bot.send_message(message.chat.id, "Команды:\n/start - запуск бота\n/help - все команды\n/start_test - начать тест")

@bot.message_handler(commands=['start_test'])
def s(message):
      try:
            f = open("users.json", "r")
            users = json.load(f)
            f.close()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(info.capitals[users[str(message.chat.id)]["step"]][0])
            btn2 = types.KeyboardButton(info.capitals[users[str(message.chat.id)]["step"]][1])
            btn3 = types.KeyboardButton(info.capitals[users[str(message.chat.id)]["step"]][2])
            markup.add(btn1, btn2, btn3)
            sent_msg = bot.send_message(message.chat.id, f"Столица {info.countries[users[str(message.chat.id)]['step']]}?", reply_markup=markup)
            bot.register_next_step_handler(sent_msg, answer)
            f = open("users.json", "w")
            json.dump(users, f, ensure_ascii=False)
            f.close()
      except:
            bot.send_message(message.chat.id, "Произошла ошибка.")

def answer(message):
      try:
            f = open("users.json", "r")
            users = json.load(f)
            f.close()
            if message.text == info.answers[users[str(message.chat.id)]["step"]]:
                  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                  btn1 = types.KeyboardButton("Продолжить")
                  markup.add(btn1)
                  sent_msg = bot.send_message(message.chat.id, "Правильно! Нажмите кнопку или напишите любое слово, чтобы продолжить.", reply_markup=markup)
                  users[str(message.chat.id)]["total"] += 1
                  users[str(message.chat.id)]["step"] += 1
                  if users[str(message.chat.id)]["step"] == 11:
                        bot.register_next_step_handler(sent_msg, final)
                  else:
                        bot.register_next_step_handler(sent_msg, s)
            elif message.text in info.capitals[users[str(message.chat.id)]["step"]]:
                  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                  btn1 = types.KeyboardButton("Продолжить")
                  markup.add(btn1)
                  sent_msg = bot.send_message(message.chat.id, "Неправильно:( Нажмите кнопку или напишите любое слово, чтобы продолжить.", reply_markup=markup)
                  users[str(message.chat.id)]["step"] += 1
                  if users[str(message.chat.id)]["step"] == 11:
                        bot.register_next_step_handler(sent_msg, final)
                  else:
                        bot.register_next_step_handler(sent_msg, s)
            else:
                  sent_msg = bot.send_message(message.chat.id, "Нажмите на кнопку")
                  bot.register_next_step_handler(sent_msg, answer)
            f = open("users.json", "w")
            json.dump(users, f, ensure_ascii=False)
            f.close()
      except:
            bot.send_message(message.chat.id, "Произошла ошибка.")

def final(message):
      try:
            f = open("users.json", "r")
            users = json.load(f)
            f.close()
            a = telebot.types.ReplyKeyboardRemove()
            if users[str(message.chat.id)]['total'] < 5:
                  bot.send_message(message.chat.id, f"Вы прошли тест. У вас {users[str(message.chat.id)]['total']} баллов. Вам стоит повторить географию. Чтобы начать заново нажмите на команду /start", reply_markup=a)
                  bot.send_animation(message.chat.id,"https://img03.rl0.ru/afisha/-x-i/daily.afisha.ru/uploads/images/6/f7/6f7524fb86a803bb55b70bd083e84a49.gif")
            elif users[str(message.chat.id)]['total'] >= 5 and users[str(message.chat.id)]['total'] < 8:
                  bot.send_message(message.chat.id, f"Вы прошли тест. У вас {users[str(message.chat.id)]['total']} баллов. Хороший результат! Чтобы начать заново нажмите на команду /start", reply_markup=a)
                  bot.send_animation(message.chat.id,"https://i.pinimg.com/originals/e1/90/aa/e190aa8e51e65ecb5c0d0b9f9d5efb5c.gif                                                                                                                                                                  м                                                     2  ")
            elif users[str(message.chat.id)]['total'] >= 8:
                  bot.send_message(message.chat.id, f"Вы прошли тест. У вас {users[str(message.chat.id)]['total']} баллов. ТЫ ГЕНИЙ!!! Чтобы начать заново нажмите на команду /start", reply_markup=a)
                  bot.send_animation(message.chat.id, "https://media.tenor.com/F6n-iwjb8m8AAAAM/genius-%D0%B3%D0%B5%D0%BD%D0%B8%D0%B9.gif")
            del users[str(message.chat.id)]
            f = open("users.json", "w")
            json.dump(users, f, ensure_ascii=False)
            f.close()
      except:
            bot.send_message(message.chat.id, "Произошла ошибка.")

bot.polling()