import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

# Configuração de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Dicionário de pedidos simulados
pedidos = {
    '12345678901': ['ABC123', 'XYZ456'],
    '98765432100': ['LMN789', 'DEF012']
}

# Função de saudação e menu inicial
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Suporte", callback_data='suporte')],
        [InlineKeyboardButton("Código de Rastreio", callback_data='rastreamento')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Olá! Eu sou o Assistente Virtual. Como posso ajudá-lo hoje?",
        reply_markup=reply_markup
    )

# Função para lidar com os botões do menu
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'suporte':
        await query.edit_message_text("Você será atendido em breve. Por favor, aguarde...")
        # Lógica para redirecionar para atendimento humano pode ser implementada aqui
    elif query.data == 'rastreamento':
        await query.edit_message_text("Por favor, envie seu CPF para rastrear seu pedido.")

# Função para processar o CPF e retornar os códigos de rastreio
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    cpf = update.message.text.strip()
    if cpf in pedidos:
        rastreios = ', '.join(pedidos[cpf])
        await update.message.reply_text(f"Seus códigos de rastreio: {rastreios}")
    else:
        await update.message.reply_text("CPF não encontrado. Por favor, verifique e tente novamente.")

# Função principal para configurar o bot
async def main() -> None:
    application = ApplicationBuilder().token('7304383872:AAH9jS7Vgix9TrgwjDWRBfg1ejgN6haik-0').build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
