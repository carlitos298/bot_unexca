import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ------------------ Config ------------------
TOKEN = os.environ.get("TELEGRAM_TOKEN")
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")  # ej: https://bot-unexca.onrender.com
PORT = int(os.environ.get("PORT", 5000))

if not TOKEN:
    raise RuntimeError("❌ ERROR: TELEGRAM_TOKEN no definido en Environment variables.")
if not RENDER_URL:
    # No es fatal pero recomendamos definirlo para auto-configurar webhook
    print("⚠️ Aviso: RENDER_EXTERNAL_URL no definido; tendrás que setear el webhook manualmente.")

# ------------------ Datos ------------------
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

# ------------------ Handlers ------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! ¿En qué puedo ayudarte?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").lower()
    if "hola" in text:
        await update.message.reply_text("¡Hola! ¿En qué puedo ayudarte?")
        return
    if "ayuda" in text:
        await update.message.reply_text(
            "Puedes preguntarme por: horarios, ubicación, teléfono, correo, inscripción, "
            "resagado, beca, constancia, requisitos, eventos, misión, visión, historia, "
            "carreras o servicios. 😊"
        )
        return
    if any(word in text for word in ["adiós", "chao", "bye"]):
        await update.message.reply_text("¡Adiós! Que tengas un buen día 😄")
        return

    for key, value in info.items():
        if key in text:
            await update.message.reply_text(value)
            return

    await update.message.reply_text("No entiendo eso 😅. Escribe 'ayuda' para ver qué puedo responder.")

# ------------------ Application (PTB) ------------------
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# ------------------ Flask (webhook endpoint) ------------------
flask_app = Flask(__name__)

@flask_app.get("/")
def home():
    return "Bot de UNEXCA activo ✅"

# Route para recibir updates: usamos la ruta segura con el token en la URL
@flask_app.post(f"/{TOKEN}")
def receive_update():
    """
    Endpoint que Telegram llamará mediante POST. Convierte JSON a Update
    y lo programa para que lo procese el Application en su loop.
    """
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    # schedule processing in the running event loop:
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    # application.process_update is async; la programamos sin bloquear la request
    asyncio.run_coroutine_threadsafe(application.process_update(update), loop)
    return "OK", 200

# ------------------ Iniciar application y Flask ------------------
def start_event_loop_and_bot():
    """
    Crea y establece el event loop, inicializa y arranca la Application
    (sin polling; usaremos webhook). También configura el webhook si RENDER_EXTERNAL_URL está definido.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def _init_start():
        await application.initialize()  # inicializa internals
        await application.start()       # arranca (necesario para application.bot, handlers, etc.)
        # configura webhook si tenemos la URL pública
        if RENDER_URL:
            webhook_url = f"{RENDER_URL}/{TOKEN}"
            await application.bot.set_webhook(webhook_url)
            print(f"✅ Webhook configurado en: {webhook_url}")
        print("🤖 Application (bot) inicializado en background.")

    loop.create_task(_init_start())
    # No bloqueamos aquí; Flask seguirá en foreground y el event loop correrá en background.
    return loop

if __name__ == "__main__":
    # Inicia event loop y bot en background
    loop = start_event_loop_and_bot()

    # Ejecuta Flask (bloqueante)
    flask_app.run(host="0.0.0.0", port=PORT)
