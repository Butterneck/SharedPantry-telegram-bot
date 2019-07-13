import globalVariables as gv

def aggiungi_prodotto(update, context):
    context.message.reply_text("Ok, dimmi il nome del prodotto che vuoi aggiungere")
    return NOME

def aggiungi_nome(update, context):
    nome = update.message.text
    context.user_data['nome'] = nome
    update.message.reply_text("Benissimo, ora dimmi il prezzo di " + nome)
    return PREZZO


def aggiungi_prezzo(update, context):
    prezzo = update.message.text
    context.user_data['prezzo'] = prezzo
    update.message.reply_text("Benissimo, ora dimmi quanti " + context.user_data['nome'] + " ci sono")
    return QUANTITA


def aggiungi_quantita(update, context):
    qt = update.message.text
    update.message.reply_text("Ottimo, " + context.user_data['nome'] + " aggiunto alla dispensa")
    gv.db_manager.addProduct(context.user_data['nome'], context.user_data['prezzo'], qt)
    update.message.reply_text("Ok, dimmi il nome del prodotto che vuoi aggiungere")
    return

def done(update, context):
    context.user_data.clear()
    return ConversationHandelr.END
