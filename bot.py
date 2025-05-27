from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update, context):
    await update.message.reply_text('Olá! Envie o número do seu pedido para rastrear.')

async def handle_message(update, context):
    pedido = update.message.text.strip()
    status = pedidos.get(pedido, 'Pedido não encontrado.')
    await update.message.reply_text(f'Status do pedido {pedido}: {status}')

async def main():
    application = ApplicationBuilder().token('SEU_TOKEN').post_init()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
