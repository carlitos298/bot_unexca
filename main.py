import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
from flask import Flask

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

# Respuestas básicas
def start(update: Update, context: CallbackContext):
    update.message.reply_text("¡Hola! En qué puedo ayudarte?")

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.lower()

    if "hola" in text:
        update.message.reply_text("¡Hola! ¿En qué puedo ayudarte?")
    elif "ayuda" in text:
        update.message.reply_text(
            "Puedes preguntarme por: horarios, ubicación, teléfono, correo, inscripción, "
            "resagado, beca, constancia, requisitos, eventos, misión, visión, historia, "
            "carreras o servicios. 😊"
        )
    elif "adiós" in text or "chao" in text or "bye" in text:
        update.message.reply_text("¡Adiós! Que tengas un buen día 😄")
    else:
        found = False
        for key, value in info.items():
            if key in text:
                update.message.reply_text(value)
                found = True
                break
        if not found:
            update.message.reply_text("No entiendo eso 😅. Escribe 'ayuda' para ver qué puedo responder.")

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

# Para mantener vivo el bot en Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot de UNEXCA activo ✅"

if name == 'main':
    main()
