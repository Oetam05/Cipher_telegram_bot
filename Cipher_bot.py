from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import ChatAction
from hunspell import Hunspell

CIFRAR_TEXTO = 0
PEDIR_CLAVE=1
DESCIFRAR_TEXTO=2
DESCIFRAR_TEXTO_CLAVE=3
PEDIR_CLAVE_DESCIFRAR=4
h = Hunspell('/es_CO', '/es_CO')
LETTERS    = "ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚ0123456789,.;:-_+*!¡¿?#$%&/()="
SIMBOLOS=",.;:-_+*!¡¿?#$%&/()="
letters="abcdefghijklmnopqrstuvwxyzáéíóú"

def start(update, context):
    update.message.reply_text('Hola Bienvenido, qué deseas hacer?\n\n/cifrar para cifrar un mensaje\n/descifrar para descifrar de manera automática\n/descifrar_clave para descifrar usando una clave')

def ayuda(update, context):
    txt="Este bot cuenta con 3 comandos principales:\n\nEl comando /cifrar sirve para cifrar texto con el método del Cesar, se debe ingresar el texto y una llave (corrimiento).\n\nEl comando /descifrar descifra el texto que se le envíe usando el método del Cesar sin tener la llave (De manera automática), aunque si el texto tiene problemas de ortografía podría no funcionar.\n\nEl comando /descifrar_clave sirve para descifrar un texto cuando conozco la llave.\n\nPara cancelar cualquier accion digite el comando /cancelar"
    update.message.reply_text(txt)

def cifrar_command_handler(update, context):
    update.message.reply_text('Envíame el texto a cifrar')
    return CIFRAR_TEXTO

def descifrar_command_handler(update, context):
    update.message.reply_text('Envíame el texto a descifrar')
    return DESCIFRAR_TEXTO

def descifrar_clave_command_handler(update, context):
    update.message.reply_text('Envíame el texto a descifrar')
    return DESCIFRAR_TEXTO_CLAVE

def decode(message,key):
    translated = ""
    
    for symbol in message:
        if symbol in LETTERS:
            num = LETTERS.find(symbol)
            num = num - key
            if num >= len(LETTERS):
                num -= len(LETTERS)
            elif num < 0:
                num += len(LETTERS)

            translated += LETTERS[num]
        elif symbol in letters:
            num = letters.find(symbol)
            num = num - key
            if num >= len(letters):
                num -= len(letters)
            elif num < 0:
                num += len(letters)
            translated += letters[num]
        else:
            translated += symbol
    return translated

def dec(message):
    words=message.split()
    translated=[]
    sw=True
    key=0
    while sw:
        if key>len(LETTERS):
            sw=False
            return -1
        for word in words:
            if(word[-1] in SIMBOLOS or word[0] in SIMBOLOS):
                wrd=word
                if(word[-1] in SIMBOLOS):
                    wrd=wrd[0:-1]
                if(word[0] in SIMBOLOS):
                    wrd=wrd[1:]      
                if(h.spell(wrd.lower())):
                    translated.append(word)
                    sw=False
                else:
                    translated=[]
                    sw=True
                    key+=1
                    words=decode(message,key).split()
                    break          
            elif h.spell(word.lower()):
                translated.append(word)
                sw=False            
            else:
                translated=[]
                sw=True
                key+=1
                words=decode(message,key).split()
                break
    return translated

def encdec(message, key):
    translated = ""
    for symbol in message:
        if symbol in LETTERS:
            num = LETTERS.find(symbol)
            num = num + key
            if num >= len(LETTERS):
                num -= len(LETTERS)
            elif num < 0:
                num += len(LETTERS)
            translated += LETTERS[num]
        elif symbol in letters:
            num = letters.find(symbol)            
            num = num + key
            if num >= len(letters):
                num -= len(letters)
            elif num < 0:
                num += len(letters)

            translated += letters[num]
        else:
            translated += symbol            
    return translated

def send_text(message, chat):
    chat.send_action(
        action=ChatAction.TYPING,
        timeout=None
    )
    chat.send_message(text=message)


def cifrar_texto(update, context):
    text = update.message.text
    if(update.message.text=="/cancelar"):
        update.message.reply_text('Acción cancelada, ¿qué desea hacer?\n\n/cifrar para cifrar un mensaje\n/descifrar para descifrar de manera automática\n/descifrar_clave para descifrar usando una clave')
        return ConversationHandler.END
    context.user_data["text"] = text
    update.message.chat.send_message(text="Envíe el numero de clave")
    return PEDIR_CLAVE

def pedir_clave(update, context):    
    if(update.message.text=="/cancelar"):
        update.message.reply_text('Acción cancelada, ¿qué desea hacer?\n\n/cifrar para cifrar un mensaje\n/descifrar para descifrar de manera automática\n/descifrar_clave para descifrar usando una clave')
        return ConversationHandler.END
    if(update.message.text.isdigit()):
        key = int(update.message.text)
        if(key>len(LETTERS)):
            key=int(key%len(LETTERS))
    else:
        update.message.chat.send_message(text="Debe digitar un numero válido")
        return PEDIR_CLAVE
    text=context.user_data["text"]
    ciphertext=encdec(text, key)
    chat=update.message.chat
    send_text(ciphertext, chat)
    return ConversationHandler.END

def pedir_clave_descifrar(update, context):
    if(update.message.text=="/cancelar"):
        update.message.reply_text('Acción cancelada, ¿qué desea hacer?\n\n/cifrar para cifrar un mensaje\n/descifrar para descifrar de manera automática\n/descifrar_clave para descifrar usando una clave')
        return ConversationHandler.END
    if(update.message.text.isdigit()):
        key = int(update.message.text)
        if(key>len(LETTERS)):
            key=int(key%len(LETTERS))
    else:
        update.message.chat.send_message(text="Debe digitar un numero válido")
        return PEDIR_CLAVE_DESCIFRAR
    text=context.user_data["text"]
    translated=decode(text, key)
    chat=update.message.chat
    send_text(translated, chat)
    return ConversationHandler.END

def descifrar_texto_clave(update, context):
    if(update.message.text=="/cancelar"):
        update.message.reply_text('Acción cancelada, ¿qué desea hacer?\n\n/cifrar para cifrar un mensaje\n/descifrar para descifrar de manera automática\n/descifrar_clave para descifrar usando una clave')
        return ConversationHandler.END
    text = update.message.text
    context.user_data["text"] = text
    update.message.chat.send_message(text="Envíe el numero de clave")    
    return PEDIR_CLAVE_DESCIFRAR

def descifrar_texto(update, context):
    if(update.message.text=="/cancelar"):
        update.message.reply_text('Acción cancelada, ¿qué desea hacer?\n\n/cifrar para cifrar un mensaje\n/descifrar para descifrar de manera automática\n/descifrar_clave para descifrar usando una clave')
        return ConversationHandler.END
    text = update.message.text
    deciphertext=dec(text)    
    chat=update.message.chat
    if(deciphertext==-1):
        deciphertext="El mensaje no se pudo descifrar de manera automática\nIntente descifrar usando la clave:\n /descifrar_clave"
        send_text(deciphertext, chat)
    else:
        send_text(" ".join(deciphertext), chat)
    return ConversationHandler.END

if __name__ == '__main__':

    updater = Updater(token='5328278176:AAGIlohpSu1q8hYrTaUmSCv8djvCNXk66PY', use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('ayuda', ayuda))

    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('cifrar', cifrar_command_handler),
            CommandHandler('descifrar', descifrar_command_handler),
            CommandHandler('descifrar_clave', descifrar_clave_command_handler)
        ],
        states={
            CIFRAR_TEXTO: [MessageHandler(Filters.text, cifrar_texto)],
            PEDIR_CLAVE: [MessageHandler(Filters.text, pedir_clave)],
            DESCIFRAR_TEXTO:[MessageHandler(Filters.text, descifrar_texto)],
            DESCIFRAR_TEXTO_CLAVE:[MessageHandler(Filters.text, descifrar_texto_clave)],
            PEDIR_CLAVE_DESCIFRAR: [MessageHandler(Filters.text, pedir_clave_descifrar)]
        },
        fallbacks=[]
    ))

    updater.start_polling()
    updater.idle()