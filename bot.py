import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

pedidos = {
    '12345': 'Pedido enviado e a caminho.',
    '67890': 'Pedido processado e aguardando envio.',
    '54321': 'Pedido entregue com sucesso.'
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Olá! Por favor, envie o número do seu pedido para consultar o status.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    numero_pedido = update.message.text.strip()
    status = pedidos.get(numero_pedido)
    if status:
        await update.message.reply_text(f'Status do pedido {numero_pedido}: {status}')
    else:
        await update.message.reply_text('Desculpe, não encontramos um pedido com esse número.')

async def main():
    application = ApplicationBuilder().token('SEU_TOKEN_AQUI').build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot está rodando...")
    await application.run_polling()

if __name__ == '__main__':
    main()
