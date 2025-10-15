import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

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
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! ¿En qué puedo ayudarte?")

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

# Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot de UNEXCA activo ✅"

@app.route(f'/{os.environ.get("TELEGRAM_TOKEN")}', methods=['POST'])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.update_queue.put(update)
    return "ok", 200

# Inicializar bot
TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("❌ ERROR: TELEGRAM_TOKEN no definido")

application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Configurar webhook al iniciar Flask
@app.before_first_request
async def setup_webhook():
    url = os.environ.get("RENDER_EXTERNAL_URL")
    webhook_url = f"{url}/{TOKEN}"
    await application.bot.set_webhook(webhook_url)
    print(f"✅ Webhook configurado en {webhook_url}")
    # Arranca bot en background
    application.run_polling()
