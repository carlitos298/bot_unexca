import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Respuestas predefinidas
INFO = {
    "horarios": "Sábados desde las 8:00 am a 4:00 pm.",
    "ubicación": "Monte Bello, centro, Puerto Ayacucho, Amazonas.",
    "teléfono": "04269002328",
    "correo": "contacto@unexca.org",
    "inscripción": "La inscripción se realiza en la sede principal con los requisitos correspondientes.",
    "resagado": "Los estudiantes rezagados pueden inscribirse con autorización de la coordinación académica.",
    "beca": "Se ofrecen becas según el rendimiento académico y situación socioeconómica.",
    "constancia": "Las constancias se solicitan en el departamento de control de estudios.",
    "requisitos": "Copia de cédula, notas certificadas, fotos tipo carnet y título de bachiller.",
    "eventos": "La institución realiza eventos culturales, deportivos y tecnológicos durante el año.",
    "misión": "Formar profesionales con ética, compromiso social y competencia tecnológica.",
    "visión": "Ser una universidad reconocida por su excelencia académica e innovación.",
    "historia": "La UNEXCA nació como un proyecto educativo para fomentar el desarrollo regional.",
    "carreras": "Ingeniería en Sistemas, Turismo y Educación.",
    "servicios": "Biblioteca, comedor, wifi, atención estudiantil y actividades extracurriculares."
}

# Función principal de mensajes
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "hola" in text:
        await update.message.reply_text("¡Hola! 👋 ¿En qué puedo ayudarte? Puedes preguntar por horarios, carreras, requisitos, becas o servicios.")
        return

    if "adiós" in text or "chao" in text:
        await update.message.reply_text("¡Adiós! 👋 Que tengas un excelente día.")
        return

    if "ayuda" in text:
        await update.message.reply_text("Puedes preguntarme sobre: horarios, ubicación, carreras, requisitos, becas, servicios, misión, visión y más.")
        return

    for key, value in INFO.items():
        if key in text:
            await update.message.reply_text(value)
            return

    await update.message.reply_text("No entiendo lo que dices 🤔. Escribe 'ayuda' para ver las opciones disponibles.")

# Iniciar el bot
if name == "main":
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot iniciado correctamente...")
    app.run_polling()
