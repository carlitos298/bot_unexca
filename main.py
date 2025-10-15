import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters

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

# Funciones del bot
def start(update: Update, context):
    update.message.reply_text("¡Hola! ¿En qué puedo ayudarte?")

def handle_message(update: Update, context):
    text = update.message.text.lower()
    if "hola" in text:
        update.message.reply_text("¡Hola! ¿En qué puedo ayudarte?")
    elif "ayuda" in text:
        update.message.reply_text(
            "Puedes preguntarme por: horarios, ubicación, teléfono, correo, inscripción, "
            "resagado, beca, constancia, requisitos, eventos, misión, visión, historia, "
            "carreras o servicios. 😊"
        )
    elif any(word in text for word in ["adiós", "chao", "bye"]):
        update.message.reply_text("¡Adiós! Que tengas un buen día 😄")
    else:
        for key, value in info.items():
            if key in text:
                update.message.reply_text(value)
                return
        update.message.reply_text("No entiendo eso 😅. Escribe 'ayuda' para ver qué puedo responder.")

# Configuración del bot
TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("❌ ERROR: La variable de entorno TELEGRAM_TOKEN no está definida.")

bot = Bot(TOKEN)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Flask
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Bot de UNEXCA activo ✅"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok", 200

# Set webhook en Telegram (solo una vez)
@app.before_first_request
def set_webhook():
    # URL pública de tu servicio en Render
    url = os.environ.get("RENDER_EXTERNAL_URL")
    webhook_url = f"{url}/{TOKEN}"
    bot.set_webhook(webhook_url)
    print(f"✅ Webhook configurado en {webhook_url}")

# Ejecutar Flask
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
