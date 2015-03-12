from db_models import Squadra, Giocatore, Formazione
from db_models import Voto, Partita
from db_models import db
from tools.calendar import componi_stagione
from werkzeug.exceptions import NotFound
import platform


if platform.system() == 'Linux':
    PATH_TO_TXT = r'/giornate/'
else:
    PATH_TO_TXT = r'\\giornate\\'
PATH_TO_TEAMS = r''


def importa_txt(path, progressbar=None):
    """
    importa_txt(path, progressbar=None)

    importa il txt dei voti ed inserisce i valori nel database

    :param path: str path file di input
    """
    num = path.split('.txt')[0][-2:]
    with open(path) as input_file:
        data = input_file.readlines()
    count = 0
    for item in data:
        codice, nome, squadra_reale, fanta_voto, voto_nudo, valore = \
            item.split('|')
        # print nome
        giocatore, msg = crea_aggiorna_giocatore(codice=codice,
                                                 squadra_reale=squadra_reale,
                                                 valore=valore, nome=nome)

        if progressbar:
            progressbar.progress(count, newmsg=msg)

        msg = crea_aggiorna_voto(giocatore=giocatore, num=num,
                           voto_nudo=voto_nudo, fanta_voto=fanta_voto,
                           valore=valore)
        if progressbar:
            progressbar.progress(count, newmsg=msg)
        count += 1

    if progressbar:
        progressbar.Destroy()


def crea_aggiorna_giocatore(codice, squadra_reale, valore, nome):
    """
    crea_aggiorna_giocatore(codice, squadra_reale, valore, nome) -> object
                                                                    Giocatore,
                                                                    str

    preleva i dati dal txt: Se il calciatore e' assente, viene
    creato, altrimenti vengono aggiornati i valori dell'oggetto
    calciatore. Ritorna l'oggetto Giocatore e una stringa con messaggio di esito

    :param codice: str codice gazzetta
    :param squadra_reale: str squadra proprietaria cartellino
    :param valore: str valore gazzetta
    :param nome: str nome giocatore
    :return giocatore: object db_models.Giocatore
    :return msg: str messaggio esito
    """
    giocatore = Giocatore.query.filter_by(codice=int(codice)).first()

    if giocatore:
        giocatore.squadra_reale = squadra_reale.strip()
        giocatore.valore = int(valore.strip())
        giocatore.nome = nome.strip().upper()
        giocatore.valore_asta = 0
        db.session.commit()
        msg = 'INFO: Aggiorno i valori di {}'.format(nome)
    else:
        giocatore = Giocatore(codice=int(codice), nome=nome.strip(),
                              squadra_reale=squadra_reale.strip(),
                              valore=int(valore.strip()), valore_asta=0)
        db.session.add(giocatore)
        db.session.commit()
        msg = 'INFO: nuovo {} {} inserito'.format(giocatore.ruolo, nome)
    return giocatore, msg


def crea_aggiorna_voto(giocatore, num, voto_nudo, fanta_voto, valore):
    """
    crea_aggiorna_voto(giocatore, num, voto_nudo, fanta_voto, valore) -> str

    preleva i dati dal txt: Se il voto e' assente, viene creato,
    altrimenti vengono aggiornati i valori dell'oggetto voto.
    Ritorna una stringa con un messaggio di esito

    :param num: str giornata
    :param voto_nudo: str voto senza bonus-malus
    :param fanta_voto: str voto con bonus-malus
    :param valore: str valore gazzetta
    :return msg: str messaggio esito
    """
    voto_obj = Voto.query.filter_by(giocatore=giocatore,
                                    giornata=int(num)).first()
    if voto_obj:
        voto_obj.voto_nudo = float(voto_nudo)
        voto_obj.fanta_voto = float(fanta_voto)
        voto_obj.valore = int(valore)
        db.session.commit()
        msg = 'INFO: Aggiorno <VOTO> di {} gg.: {}'.format(giocatore.nome, num)
    else:
        n_voto = Voto(giocatore=giocatore, giornata=int(num),
                      voto_nudo=float(voto_nudo),
                      fanta_voto=float(fanta_voto))
        db.session.add(n_voto)
        db.session.commit()
        msg = 'INFO: nuovo <VOTO> per {} {} inserito'.format(giocatore.nome,
                                                             num)
    return msg
    

def popola_squadre(lega):
    """
    popola_squadre(lega)

    Popola le squadre con i giocatori presenti nel database.
    Questa funzione viene chiamata SOLO dopo che i giocatori
    sono stati inseriti nel database.
    Le squadre vengono estrapolate dal file di excel.
    Il nome della squadra deve avere come prefisso il '!'

    :param lega: object db_models.Lega
    """
    print 'INFO: lettura file...'
    try:
        with open(r'{}teams.txt'.format(PATH_TO_TEAMS)) as input_file:
            data = input_file.readlines()

        for line in data:
            if '!' in line:
                nome = line[1:].strip()
                try:
                    squadra = Squadra.query.filter_by(
                        nome=nome.upper()).first_or_404()
                    print 'INFO: Squadra: <%s> presente' % squadra
                except NotFound:
                    print 'INFO: Squadra inesistente...creazione.'
                    squadra = Squadra(nome=nome.upper())
                    db.session.add(squadra)
                    print 'INFO: Squadra %s --> creata.' % squadra.nome

            else:
                nome = line.strip().upper()
                try:
                    giocatore = Giocatore.query.filter_by(
                        nome=nome.upper()).first_or_404()
                    giocatore.squadra = squadra
                    print 'INFO: %s JOIN %s' % (squadra.nome, giocatore.nome)
                    db.session.commit()
                except NotFound:
                    print 'WARNING: %s non trovato: controllare nome' % nome
        print 'INFO:: inserisco squadre in lega %s' % lega.nome

        for s in Squadra.query.all():
            lega.squadre_lega.append(s)
            db.session.commit()
            print 'INFO: squadra %s --->> lega %s' % (s.nome, lega.nome)
        print 'INFO:: ...operazione terminata con successo!'

    except IOError:
        print 'ERROR: file non trovato'


def popola_calendario(lega, progressbar=None):
    """
    popola_calendario(lega, progressbar=None) -> list

    Popola il calendario con le squadre inserite a database:

    :param lega: object db_models.Lega
    :param progressbar: object Progressbar
    :return calendar: list di oggetti db_models.Partita
    """
    squadre = [s.nome for s in Squadra.query.all()]
    a_r = lega.option.a_r
    if not squadre:
        print "WARNING: nessuna squadra presente a database"
    else:
        calendar = componi_stagione(teams=squadre, num=a_r)
        # print calendar # DEBUG
        count = 0
        for item in calendar:
            gg, casa, fuori = item.split(',')
            sq_casa = Squadra.query.filter_by(nome=casa).first()
            sq_fuori = Squadra.query.filter_by(nome=fuori).first()
            print sq_casa, sq_fuori
            partita = Partita(lega=lega, giornata=gg, casa=sq_casa,
                              fuori=sq_fuori)
            msg = "INFO: inserita gg.{} {} - {}".format(gg, sq_casa, sq_fuori)
            if progressbar:
                progressbar.progress(count, newmsg=msg)
            db.session.add(partita)
            db.session.commit()
            count += 1
        print "INFO: Calendario creato con successo!"
        return calendar
        

def inserisci_formazione_da_file(nome_squadra, num):  # in fase di test
    """
    inserisci_formazione_da_file(nome_squadra, num)

    Popola la formazione da file, per la squadra data:

    :param nome_squadra: str nome di squadra
    :param num: int numero di giornata
       """
    print 'INFO:: lettura file...'
    with open(r'{}formazione.txt'.format(PATH_TO_TXT)) as input_file:
        data = input_file.readlines()
    try:
        squadra = Squadra.query.filter_by(
            nome=nome_squadra.upper()).first_or_404()
    except NotFound:
        print 'WARNING: {} non trovata!'.format(nome_squadra)
    else:
        formazione = Formazione.query.filter_by(squadra=squadra,
                                                giornata=num).first()
        if formazione:
            print "INFO: formazione esistente....cancellazione e ricreazione."
            db.session.delete(formazione)
            db.session.commit()
        else:
            print "INFO: formazione non trovata...inserimento."
        formazione = Formazione(squadra=squadra, giornata=num)
        db.session.add(formazione)
        db.session.commit()
        print "INFO: Inserimento giocatori..."

        for line in data:
            pos, nome = line.split('\t')
            nome = nome.strip()
            try:
                if pos.upper() == 'T':
                    titolare = Giocatore.query.filter_by(
                        nome=nome.rstrip().upper()).first_or_404()
                    print titolare
                    formazione.titolari.append(titolare)
                    print "INFO: Aggiunto %s ai titolari di %s" % (nome,
                                                                   squadra)
                    db.session.commit()
                elif pos.upper() == 'R':
                    panchinaro = Giocatore.query.filter_by(
                        nome=nome.rstrip().upper()).first_or_404()
                    formazione.panchinari.append(panchinaro)
                    print "INFO: Aggiunto %s alla panchina di %s" \
                          % (nome, squadra)
                    db.session.commit()
                else:
                    print "ERROR: Errore nel file, controllare..."
            except NotFound:
                print "WARNING: {} non trovato!".format(nome.strip())


#  Privata: solo in fase di testing
def _import_formazioni_da_file(model, giornata, lega):
    """
    _import_formazioni_da_file(model, giornata, lega)

    Importa le formazioni presenti sul file 'formazioni.txt, ricavabili dal
    file MCBEG*.xls

    :param model: object model.ModelFanta
    :param giornata: str giornata
    :param lega: object db_models.Lega
    """
    squadra = ''
    giornata = int(giornata)
    print 'INFO: inserimento giornata %s...' % giornata
    with open('formazioni.txt') as inputfile:
        data = [l for l in inputfile.readlines()
                if l.strip() != 'Nome (Squadra)']
    d = {}
    for line in data:
        print line
        if '!' in line:
            squadra = line.strip()[1:].upper()
            d[squadra] = []
        elif ',' not in line:
            giocatore = line.strip()
            res = model.get_giocatore_per_nome(giocatore)
            if not res:
                print 'WARNING: Controllare giocatore: ', giocatore
            d[squadra].extend([giocatore.upper()])
    print 'INFO: Nomi giocatori corretti!!'
    for k in d:
        model.salva_formazione(lega=lega.nome, squadra=k,
                               giornata=giornata, giocatori=d[k])
    print 'INFO: formazioni lega %s giornata %s inserite!' % (lega.nome,
                                                              giornata)