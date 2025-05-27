from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Dicionário de pedidos para simulação
pedidos = {
    '12345': 'Pedido enviado e a caminho.',
    '67890': 'Pedido processado e aguardando envio.',
    '54321': 'Pedido entregue com sucesso.'
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Olá! Envie o número do seu pedido para rastrear.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pedido = update.message.text.strip()
    status = pedidos.get(pedido, 'Pedido não encontrado.')
    await update.message.reply_text(f'Status do pedido {pedido}: {status}')

def main():
    application = ApplicationBuilder().token('SEU_TOKEN').build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
