import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
    ConversationHandler,
)

# Configuração do log
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Estados da conversa
SUPORTE, RASTREIO = range(2)

# Token do bot (substitua pelo seu token real)
BOT_TOKEN = "7304383872:AAH9jS7Vgix9TrgwjDWRBfg1ejgN6haik-0"

# Função de início
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [InlineKeyboardButton("📦 Código de Rastreio", callback_data="rastreio")],
        [InlineKeyboardButton("🛠️ Suporte", callback_data="suporte")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Olá! Eu sou o Bot de Atendimento.\nComo posso ajudar você hoje?",
        reply_markup=reply_markup,
    )
    return ConversationHandler.END

# Função para lidar com os botões
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    choice = query.data

    if choice == "rastreio":
        await query.edit_message_text("Por favor, envie seu CPF para buscar os códigos de rastreio.")
        return RASTREIO
    elif choice == "suporte":
        await query.edit_message_text("Descreva seu problema e nossa equipe de suporte entrará em contato.")
        return SUPORTE

# Função para lidar com o CPF
async def handle_cpf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    cpf = update.message.text
    # Aqui você implementaria a lógica para buscar os códigos de rastreio associados ao CPF
    # Por exemplo:
    codigos = ["AB123456789BR", "CD987654321BR"]
    resposta = f"Os códigos de rastreio associados ao CPF {cpf} são:\n" + "\n".join(codigos)
    await update.message.reply_text(resposta)
    return ConversationHandler.END

# Função para lidar com mensagens de suporte
async def handle_suporte(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    mensagem = update.message.text
    # Aqui você implementaria a lógica para encaminhar a mensagem para a equipe de suporte
    await update.message.reply_text("Sua mensagem foi encaminhada para nossa equipe de suporte. Entraremos em contato em breve.")
    return ConversationHandler.END

# Função principal
def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Conversa para rastreio
    rastreio_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern="^rastreio$")],
        states={
            RASTREIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_cpf)],
        },
        fallbacks=[],
    )

    # Conversa para suporte
    suporte_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern="^suporte$")],
        states={
            SUPORTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_suporte)],
        },
        fallbacks=[],
    )

    application.add_handler(rastreio_handler)
    application.add_handler(suporte_handler)

    # Inicia o bot
    application.run_polling()

if __name__ == "__main__":
    main()
