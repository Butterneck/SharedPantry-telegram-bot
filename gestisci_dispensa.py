''' NOT USED, why here????
import globalVariables as gv

def aggiungi_prodotto(update, context):
    context.message.reply_text("Ok, dimmi il nome del prodotto che vuoi aggiungere")
    return NOME

def aggiungi_nome(update, context):
    nome = update.message.text
    if nome is None or nome == "":
        update.message.reply_text("Nome non valido, per favore reinseriscilo")
        return NOME
    context.user_data['nome'] = nome
    update.message.reply_text("Benissimo, ora dimmi il prezzo di " + nome)
    return PREZZO


def aggiungi_prezzo(update, context):
    prezzo = update.message.text
    print(prezzo)
    if prezzo is None or not prezzo.replace('.', '', 1).isdigit() or not prezzo.replace(',', '', 1).isdigit():
        update.message.reply_text("Prezzo non valido, per favore reinseriscilo")
        return PREZZO

    if ',' in prezzo:
        prezzo = prezzo.replace(',', '.')

    context.user_data['prezzo'] = prezzo
    update.message.reply_text("Benissimo, ora dimmi quanti " + context.user_data['nome'] + " ci sono")
    return QUANTITA


def aggiungi_quantita(update, context):
    qt = update.message.text
    if qt is None or not qt.isdigit():
        update.message.reply_text("Quantità non valida, per favore reinseriscilo")
        return QUANTITA
    update.message.reply_text("Ottimo, " + context.user_data['nome'] + " aggiunto alla dispensa")
    gv.db_manager.addProduct(context.user_data['nome'], context.user_data['prezzo'], qt)
    update.message.reply_text("Ok, dimmi il nome del prodotto che vuoi aggiungere")
    return

def done(update, context):
    context.user_data.clear()
    return ConversationHandelr.END
'''