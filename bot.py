import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

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

async def post_init(application):
    # Aqui você pode adicionar qualquer lógica que precise ser executada após a inicialização
    logger.info("Bot iniciado com sucesso!")

async def main():
    application = ApplicationBuilder().token('SEU_TOKEN').post_init(post_init).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
