import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters, ContextTypes

# Información del centro universitario
info = {
    "horarios": "Sábados desde las 8:00 am a 4:00 pm.",
    "ubicación": "M93G+QMW, Puerto Ayacucho 7101, Amazonas, Venezuela.",
    "teléfono": "04269002328",
    "correo": "contacto@unexca.org",
    "inscripción": "Puedes inscribirte directamente en la sede o a través del correo contacto@unexca.org.",
    "resagado": "Los estudiantes rezagados deben comunicarse con la coordinación académica.",
    "beca": "Se otorgan becas según el rendimiento académico y necesidad económica.",
    "constancia": "Las constancias se solicitan en la oficina administrativa o por correo.",
    "requisitos": "Cédula, notas certificadas, título de bachiller, y foto tamaño carnet.",
    "eventos": "Revisa los eventos actuales en la sede principal o en redes sociales.",
    "misión": "Formar profesionales competentes con valores éticos y compromiso social.",
    "visión": "Ser una institución líder en educación universitaria integral en Venezuela.",
    "historia": "La UNEXCA fue creada para democratizar el acceso a la educación superior.",
    "carreras": "Ingeniería en Sistemas, Turismo y Educación.",
    "servicios": "Orientación académica, biblioteca, comedor y soporte tecnológico."
}

# Función /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! ¿En qué puedo ayudarte?")

# Función para manejar mensajes
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if "hola" in text:
        await update.message.reply_text("¡Hola! ¿En qué puedo ayudarte?")
    elif "ayuda" in text:
        await update.message.reply_text(
            "Puedes preguntarme por: horarios, ubicación, teléfono, correo, inscripción, "
            "resagado, beca, constancia, requisitos, eventos, misión, visión, historia, "
            "carreras o servicios. 😊"
        )
    elif any(word in text for word in ["adiós", "chao", "bye"]):
        await update.message.reply_text("¡Adiós! Que tengas un buen día 😄")
    else:
        for key, value in info.items():
            if key in text:
                await update.message.reply_text(value)
                return
        await update.message.reply_text("No entiendo eso 😅. Escribe 'ayuda' para ver qué puedo responder.")

# Inicialización de Flask
server = Flask(__name__)

# Obtener token de entorno
TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN no definido en variables de entorno")

bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)  # workers=0 porque Render maneja las peticiones

# Añadir handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Ruta principal del webhook
@server.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# Ruta para prueba de servidor
@server.route('/')
def home():
    return "Bot de UNEXCA activo ✅"

# Configurar webhook con Telegram
if __name__ == "__main__":
    # Tu dominio en Render (ejemplo): https://tu-app.onrender.com
    WEBHOOK_URL = f"{os.environ.get('RENDER_EXTERNAL_URL')}/{TOKEN}"
    bot.delete_webhook()
    bot.set_webhook(WEBHOOK_URL)
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
