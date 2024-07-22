import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime
import io
import logging
from matplotlib import pyplot as plt

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

#Функция для чтения токена из файла
def read_token_from_file(filename):
  try:
      with open(filename, 'r') as file:
          token = file.read().strip()
      return token
  except FileNotFoundError:
      logger.error(f"Файл {filename} не найден")
      return None
  except Exception as e:
      logger.error(f"Ошибка при чтении файла {filename}: {e}")
      return None
#
## Ваш токен, полученный от BotFather
TOKEN_FILE = 'token.txt'
TOKEN = read_token_from_file(TOKEN_FILE)

if not TOKEN:
    logger.error("Токен не может быть пустым")
    exit(1)

SERVER_URL = 'http://35.225.1.29:8000/api/v1/sensor/'

# Импортируем нужные части matplotlib

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    commands = (
        "/start - Показать все команды\n"
        "/last - Получить последнюю запись\n"
        "/last3 - Получить три последних замера\n"
        "/plot - Показать график за последние 30 измерений\n"
        "/plot_Q - Показать график расхода\n"
        "/last_for_user - Получить последнюю измерение\n"
        "/last3_for_user - Получить последнии измерения\n"
    )
    await update.message.reply_text(f'Привет! Я ваш бот. Вот доступные команды:\n\n{commands}')

# Функция для обработки команды /last
async def last(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        response = requests.get(SERVER_URL)
        response.raise_for_status()
        data = response.json()

        if data:
            last_record = data[-1]
            reading_date = datetime.fromisoformat(last_record['reading_date']).strftime('%Y-%m-%d %H:%M:%S')

            formatted_data = (
                f"Номер датчика: {last_record['sensor_id']}\n"
                f"L,м: {round(last_record['degree'], 3)}\n"
                f"H: {round(last_record['reika'], 3)}\n"
                f"Q: {round(last_record['rate'], 3)}\n"
                f"Заряд: {last_record['charge']}\n"
                f"Сигнал: {last_record['signal']}\n"
                f"Время считывания датчика: {reading_date}\n"
            )
            await update.message.reply_text(f'Последний замер:\n{formatted_data}')
        else:
            await update.message.reply_text("Нет данных")
    except requests.RequestException as e:
        logger.error(f'Ошибка при получении данных: {e}')
        await update.message.reply_text(f'Ошибка при получении данных: {e}')
    except Exception as e:
        logger.error(f'Непредвиденная ошибка: {e}')
        await update.message.reply_text(f'Непредвиденная ошибка: {e}')

# Функция для обработки команды /last3
async def last3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        response = requests.get(SERVER_URL)
        response.raise_for_status()
        data = response.json()

        if data:
            recent_records = data[-3:]
            formatted_data = ""
            for record in recent_records:
                reading_date = datetime.fromisoformat(record['reading_date']).strftime('%Y-%m-%d %H:%M:%S')
                formatted_data += (
                    f"Номер датчика: {record['sensor_id']}\n"
                    f"L,м: {round(record['degree'], 3)}\n"
                    f"H: {round(record['reika'], 3)}\n"
                    f"Q: {round(record['rate'], 3)}\n"
                    f"Заряд: {record['charge']}\n"
                    f"Сигнал: {record['signal']}\n"
                    f"Время считывания датчика: {reading_date}\n"
                    f"\n"
                )

            await update.message.reply_text(f'Три последних замера:\n{formatted_data}')
        else:
            await update.message.reply_text("Нет данных")
    except requests.RequestException as e:
        logger.error(f'Ошибка при получении данных: {e}')
        await update.message.reply_text(f'Ошибка при получении данных: {e}')
    except Exception as e:
        logger.error(f'Непредвиденная ошибка: {e}')
        await update.message.reply_text(f'Непредвиденная ошибка: {e}')

async def last_for_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        response = requests.get(SERVER_URL)
        response.raise_for_status()
        data = response.json()

        if data:
            last_record = data[-1]
            reading_date = datetime.fromisoformat(last_record['reading_date']).strftime('%Y-%m-%d %H:%M:%S')

            formatted_data = (
                f"Уровень рейки: {round(last_record['reika'], 3)}\n"
                f"Расход воды: {round(last_record['rate'], 3)}\n"
            )
            await update.message.reply_text(f'Последний замер:\n{formatted_data}')
        else:
            await update.message.reply_text("Нет данных")
    except requests.RequestException as e:
        logger.error(f'Ошибка при получении данных: {e}')
        await update.message.reply_text(f'Ошибка при получении данных: {e}')
    except Exception as e:
        logger.error(f'Непредвиденная ошибка: {e}')
        await update.message.reply_text(f'Непредвиденная ошибка: {e}')

async def last3_for_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        response = requests.get(SERVER_URL)
        response.raise_for_status()
        data = response.json()

        if data:
            recent_records = data[-3:]
            formatted_data = ""
            for record in recent_records:
                reading_date = datetime.fromisoformat(record['reading_date']).strftime('%Y-%m-%d %H:%M:%S')
                formatted_data += (
                    f"Уровень рейки: {round(record['reika'], 3)}\n"
                    f"Расход воды: {round(record['rate'], 3)}\n"
                    f"\n"
                )

            await update.message.reply_text(f'Три последних замера:\n{formatted_data}')
        else:
            await update.message.reply_text("Нет данных")
    except requests.RequestException as e:
        logger.error(f'Ошибка при получении данных: {e}')
        await update.message.reply_text(f'Ошибка при получении данных: {e}')
    except Exception as e:
        logger.error(f'Непредвиденная ошибка: {e}')
        await update.message.reply_text(f'Непредвиденная ошибка: {e}')

# Функция для обработки команды /plot
async def plot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        response = requests.get(SERVER_URL)
        response.raise_for_status()
        data = response.json()

        if data:
            recent_records = data[-30:]
            dates = [datetime.fromisoformat(record['reading_date']) for record in recent_records]
            degrees = [record['degree'] for record in recent_records]
            reikas = [record['reika'] for record in recent_records]
            rates = [record['rate'] for record in recent_records]

            plt.figure(figsize=(10, 6))
            plt.plot(dates, degrees, label='L,м')
            plt.plot(dates, reikas, label='H')
            plt.plot(dates, rates, label='Q')
            plt.xlabel('Дата и время')
            plt.ylabel('Значение')
            plt.title('График параметров за последние 30 измерений')
            plt.legend()
            plt.grid(True)

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plt.close()

            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=buf)
        else:
            await update.message.reply_text("Нет данных")
    except requests.RequestException as e:
        logger.error(f'Ошибка при получении данных: {e}')
        await update.message.reply_text(f'Ошибка при получении данных: {e}')
    except Exception as e:
        logger.error(f'Непредвиденная ошибка: {e}')
        await update.message.reply_text(f'Непредвиденная ошибка: {e}')

# Функция для обработки команды /plot_Q
async def plot_Q(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        response = requests.get(SERVER_URL)
        response.raise_for_status()
        data = response.json()

        if data:
            recent_records = data[:]
            dates = [datetime.fromisoformat(record['reading_date']) for record in recent_records]
            rates = [record['rate'] for record in recent_records]

            plt.figure(figsize=(10, 6))
            plt.plot(dates, rates, label='Q')
            plt.xlabel('Дата и время')
            plt.ylabel('Значение')
            plt.title('График расхода')
            plt.legend()
            plt.grid(True)

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plt.close()

            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=buf)
        else:
            await update.message.reply_text("Нет данных")
    except requests.RequestException as e:
        logger.error(f'Ошибка при получении данных: {e}')
        await update.message.reply_text(f'Ошибка при получении данных: {e}')
    except Exception as e:
        logger.error(f'Непредвиденная ошибка: {e}')
        await update.message.reply_text(f'Непредвиденная ошибка: {e}')

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("last", last))
    application.add_handler(CommandHandler("last3", last3))
    application.add_handler(CommandHandler("last_for_user", last_for_user))
    application.add_handler(CommandHandler("last3_for_user", last3_for_user))
    application.add_handler(CommandHandler("plot", plot))
    application.add_handler(CommandHandler("plot_Q", plot_Q))

    # Запускаем бота
    try:
        application.run_polling()
    except Exception as e:
        logger.error(f'Ошибка при запуске бота: {e}')

if __name__ == '__main__':
    main()
