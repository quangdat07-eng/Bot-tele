from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
import requests, os, json, re
from io import BytesIO


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
    [InlineKeyboardButton("➕ Me adicione ao seu grupo", url="https://t.me/ULP_Lookup_bot?startgroup=true")]
]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🔍 *Comandos disponíveis:*\n\n"
        "🌐 `/url URL` - Analisar URL completa\n"
        "🔗 `/ur URL` - Versão curta do comando\n"
        "⚡ `/u URL` - Comando mais rápido\n"
        "💬 *Ou simplesmente envie qualquer mensagem* - Farei uma busca automática!\n\n"
        "📝 *Qualquer mensagem enviada será usada para busca*\n\n"
        "👥 Quer me usar em um grupo? Me adicione!",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )


async def tudo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    info = update.message
    if not info:
        info = update.edited_message
    idc = info.chat.id
    idm = info.message_id

    padrao = [[InlineKeyboardButton(" DELETA 🚮", callback_data='delete')]]
    enviap = InlineKeyboardMarkup(padrao)

    dois = [[InlineKeyboardButton("LOGIN:SENHA", callback_data='LOGIN')],[InlineKeyboardButton("URL:LOGIN:SENHA", callback_data='URL')],[InlineKeyboardButton(" DELETA 🚮", callback_data='delete')]]
    doist = InlineKeyboardMarkup(dois)

    while True:

        url = re.sub(r'/url|/ur|/u','', info.text.lower()).strip()

        if len(url) < 3:

            await context.bot.send_message(chat_id=idc, text=f'''<b>
                                        
⚠️  3 CARACTERES É O MÍNIMO
❌  3 CHARACTERS IS THE MINIMUM
</b>
''',parse_mode='HTML',reply_to_message_id=idm, reply_markup=enviap)
            return

        anome = re.sub(r'\s+',' ', url)
        prov = ''
        if len(anome.split(' ')) > 1:
            anome =  ' '.join(anome.split(' ')[:2])
            anome, prov = anome.split(' ')
            if '@' not in prov:
                anome = f'{anome}_@{prov}'

        if '_' not in anome:
            anome = f'{anome}_{prov}-'

        ap = [ap for ap in os.listdir('files') if anome in ap]

        if len(ap) > 0 and len(ap) < 2:

            total = int(ap[0].split('-')[1].replace('.txt',''))

            await context.bot.send_message(chat_id=idc, text=f'''<b>=>
☑️  URL: <code>{url}</code>

🧵  LINHAS / ROWS: <code>{total:,}</code>

FIXO: {ap[0]} | {idm}
</b>

    ''',parse_mode='HTML', reply_to_message_id=idm, reply_markup=doist)

            break

        try:

            u = f'https://ulpcloud.site/url?k=rwldJ8XjK2yg71Jgticl&q={url}&t=1'

            he = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0'}

            r = requests.get(u, timeout=12,headers=he)

            if r.status_code == 200:
                try:
                    nome = r.headers['Content-Disposition'].split('filename=')[1].replace('"','')
                except:

                    await context.bot.send_message(chat_id=idc, text=f'''<b>
🔎  URL: <code>{url}</code>

⚠️  BUSCA NÃO ENCONTRADO
❌  SEARCH NOT FOUND
</b>
''',parse_mode='HTML',reply_to_message_id=idm, reply_markup=enviap)
                    return

                total = int(nome.split('-')[1].replace('.txt','').replace('"',''))

                with open(f'files/{nome}','a', encoding='utf-8') as ss:
                    ss.write(r.text)

                await context.bot.send_message(chat_id=idc, text=f'''<b>=>
☑️  URL: <code>{url}</code>

🧵  LINHAS / ROWS: <code>{total:,}</code>

FIXO: {nome} | {idm}</b>
''',parse_mode='HTML', reply_to_message_id=idm, reply_markup=doist)

            elif r.status_code == 404:
                await context.bot.send_message(chat_id=idc, text=f'''<b>
🔎  URL: <code>{url}</code>

⚠️  BUSCA NÃO ENCONTRADO
❌  SEARCH NOT FOUND
</b>
''',parse_mode='HTML',reply_to_message_id=idm, reply_markup=enviap)

            break

        except Exception as e:
            er = str(e)
            print('Error', e)
            break

async def Botoes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    try:
        info = update.callback_query
        id = info.from_user.id
        idc = info.message.chat.id
        typ = info.message.chat.type
        mtext = str(info.message.text)

    except Exception as e:
        message = f"<b> ⚠️ BOT ONLINE !!!\n⚠️\n</b>"
        print(e)
        await context.bot.send_message(chat_id=update.effective_chat.id,text=message, parse_mode='HTML')
        return
    
    padrao = [[InlineKeyboardButton(" DELETA 🚮", callback_data='delete')]]
    enviap = InlineKeyboardMarkup(padrao)

    option = info.data.split(' ')

    try:
        idx = info.message.reply_to_message.from_user.id
    except:
        if typ == 'private':
            idx = id

    if option[0] == 'URL':

        if int(idx) != int(id):
            await info.answer(
            text="""⚠️   VOCÊ NãO ENVIOU DA MENSAGEM\n
⚠️  YOU DO NOT OWNER THE MESSAGE""",
            show_alert=True,
            cache_time=0)
            return
        
        try:
            await info.message.delete()
        except:
            return

        file, idm = mtext.split('FIXO: ')[1].split(' | ')
        mtext = mtext+'\n\n<b>URL:LOGIN:SENHA</b>'

        await context.bot.send_document(chat_id=idc, caption=mtext, reply_markup=enviap, reply_to_message_id=idm, document=f'files/{file}', parse_mode='html')


# PARTE LOGIN:SENHA ####################

    elif option[0] == 'LOGIN':

        if int(idx) != int(id):
            await info.answer(
            text="""⚠️   VOCÊ NãO ENVIOU DA MENSAGEM\n
⚠️  YOU DO NOT OWNER THE MESSAGE""",
            show_alert=True,
            cache_time=0)
            return
        
        try:
            await info.message.delete()
        except:
            return

        file, idm = mtext.split('FIXO: ')[1].split(' | ')
        mtext = mtext+'\n\n<b>LOGIN:SENHA</b>'

        with open(f'files/{file}','r', errors='replace', encoding='utf-8') as dd:

            ff =  list(map(lambda x: f'{x.split(':')[1]}:{x.split(':')[2]}', dd))

        fila = BytesIO(''.join(ff).encode('utf-8'))

        fila.name = file
        
        await context.bot.send_document(chat_id=idc, caption=mtext, reply_markup=enviap, reply_to_message_id=idm, document=fila, parse_mode='html')

    elif option[0] == 'delete':

        if typ  == 'private':
            Dono = info.from_user.id
        
        if int(id) == 1268314769 or int(Dono) == int(id):
            try:
                await info.message.delete()
                return
            except Exception as e:
                er = str(e)

                if 'Message to delete not found' in er:
                    message = f"<b>⚠️  Bot LIGADO !!!\n\n⚠️  Bot ON AGAIN !!!\n</b>"
                    await context.bot.send_message(chat_id=idc, text=message, parse_mode='HTML')
                    return
                return
            
        await info.answer(
            text="⚠️ Você Não Tem Permissão Para Deleta",
            show_alert=True,
            cache_time=0)
        

def main():

    TOKEN = token()

    if not TOKEN:
        print('TOKEN Não é válido - Not valid\n')
        return

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(CommandHandler("url", tudo))
    app.add_handler(CommandHandler("ur", tudo))
    app.add_handler(CommandHandler("u", tudo))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tudo))
    app.add_handler(CallbackQueryHandler(Botoes))

    print("Bot rodando...")
    app.run_polling()


def token():

    if not os.path.exists('token.json'):

        with open('token.json','w') as ww:
            ww.write('{"token": "here-aqui-token"}')

        return False

    if os.path.exists('token.json'):

        with open('token.json','r') as rr:

            TOKEN = json.load(rr)['token']

        if 'here-aqui-token' == TOKEN:
            return False

        return TOKEN


if __name__ == "__main__":
    try:
        
        

        os.makedirs('files',exist_ok=True)

        main()

    except:
        print('Parou - Reiniciar | Restart Stop')

