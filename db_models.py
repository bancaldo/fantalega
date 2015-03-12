from flask import Flask
# noinspection PyUnresolvedReferences
from flask.ext.sqlalchemy import SQLAlchemy
# noinspection PyUnresolvedReferences
from flask.ext.script import Manager
# noinspection PyUnresolvedReferences
from flask.ext.migrate import Migrate, MigrateCommand


DB_NAME = 'fantalega.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % DB_NAME
app.config['SQLALCHEMY_ECHO'] = False
db = SQLAlchemy(app)

MODULI = ('3-4-3', '3-5-2', '4-3-3', '4-4-2', '4-5-1', '5-3-2', '5-4-1')

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# M2M secondary tables
leghe_squadre = db.Table('leghe_squadre',
                         db.Column('lega_id', db.Integer,
                                   db.ForeignKey('lega.id')),
                         db.Column('squadra_id', db.Integer,
                                   db.ForeignKey('squadra.id')))

punteggi_squadre = db.Table('punteggi_squadre',
                            db.Column('punteggio_id', db.Integer,
                                      db.ForeignKey('punteggio.id')),
                            db.Column('squadra_id', db.Integer,
                                      db.ForeignKey('squadra.id')))


# M2M secondary Association object
class FormazioniGiocatori(db.Model):
    __tablename__ = 'formazioni_giocatori'
    giocatore_id = db.Column(db.Integer, db.ForeignKey('giocatore.id'),
                             primary_key=True)
    formazione_id = db.Column(db.Integer, db.ForeignKey('formazione.id'),
                              primary_key=True)
    position = db.Column(db.Integer)
    giocatore = db.relationship('Giocatore',
                                backref=db.backref('form_ass', lazy='dynamic'))


class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lega = db.relationship('Lega', backref='option', uselist=False)
    budget = db.Column(db.Integer)
    max_mercati = db.Column(db.Integer)
    max_portieri = db.Column(db.Integer)
    max_difensori = db.Column(db.Integer)
    max_centrocampisti = db.Column(db.Integer)
    max_attaccanti = db.Column(db.Integer)
    a_r = db.Column(db.Integer)
    offset = db.Column(db.Integer)

    def __init__(self, lega=lega, budget=500, max_mercati=6, max_portieri=3,
                 max_difensori=9, max_centrocampisti=9,
                 max_attaccanti=7, a_r=4, offset=1):
        self.budget = budget
        self.max_mercati = max_mercati
        self.max_portieri = max_portieri
        self.max_difensori = max_difensori
        self.max_centrocampisti = max_centrocampisti
        self.max_attaccanti = max_attaccanti
        self.a_r = a_r
        self.offset = offset
        self.lega = lega

    def __repr__(self):
        return '<Option %r>' % self.lega.nome


class Lega(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), unique=True)
    option_id = db.Column(db.Integer, db.ForeignKey('option.id'))
    partite = db.relationship('Partita', backref='lega', lazy='dynamic')
    punteggi = db.relationship('Punteggio', backref='lega', lazy='dynamic')

    def __init__(self, nome):
        self.nome = nome

    def __repr__(self):
        return '<Lega %r>' % self.nome


class Punteggio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lega_id = db.Column(db.Integer, db.ForeignKey('lega.id'))
    giornata = db.Column(db.Integer())
    punti = db.Column(db.Integer())
    vinta = db.Column(db.Integer())
    pareggiata = db.Column(db.Integer())
    persa = db.Column(db.Integer())
    gol_fatti = db.Column(db.Integer())
    gol_subiti = db.Column(db.Integer())
    differenza_reti = db.Column(db.Integer())
    punti_rosa = db.Column(db.Float())

    def __init__(self, lega):
        self.lega = lega

    def __repr__(self):
        return '<Punteggio [%r] %r>' % (self.id, self.giornata)


class Squadra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    leghe = db.relationship('Lega', secondary=leghe_squadre,
                            backref=db.backref('squadre_lega', lazy='dynamic'))
    punteggi = db.relationship('Punteggio', secondary=punteggi_squadre,
                               backref=db.backref('punteggio_squadre',
                                                  lazy='dynamic'))
    nome = db.Column(db.String(50), unique=True)
    allenatore = db.Column(db.String(50), nullable=True)
    budget = db.Column(db.Integer())
    op_mercato = db.Column(db.Integer())

    giocatori = db.relationship('Giocatore', backref='squadra', lazy='dynamic')

    formazioni = db.relationship('Formazione', backref='squadra',
                                 lazy='dynamic')
    mercati = db.relationship('Mercato', backref='squadra', lazy='dynamic')

    def __init__(self, nome):
        self.nome = nome

    def __repr__(self):
        return '<Squadra %r>' % self.nome


class Giocatore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # relazione con Squadra
    squadra_id = db.Column(db.Integer, db.ForeignKey('squadra.id'),)

    codice = db.Column(db.Integer())
    nome = db.Column(db.String(30))
    squadra_reale = db.Column(db.String(3))
    valore = db.Column(db.Integer())
    valore_asta = db.Column(db.Integer())
    ruolo = db.Column(db.String(15))
    voti = db.relationship('Voto', backref='giocatore', lazy='dynamic')

    def __init__(self, codice, nome, squadra_reale, valore, valore_asta=0):
        self.codice = int(codice)
        self.nome = nome
        self.squadra_reale = squadra_reale
        self.valore = int(valore)
        self.valore_asta = int(valore_asta)
        if self.codice < 200:
            self.ruolo = 'portiere'
        elif 200 < self.codice < 500:
            self.ruolo = 'difensore'
        elif 500 < self.codice < 800:
            self.ruolo = 'centrocampista'
        else:
            self.ruolo = 'attaccante'

    def __repr__(self):
        return '<%s> %s [%s]' % (self.ruolo, self.nome, self.squadra_reale)


class Partita (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # relazione con Lega
    lega_id = db.Column(db.Integer, db.ForeignKey('lega.id'))

    giornata = db.Column(db.Integer())

    # relazioni con Squadra_casa
    casa_id = db.Column(db.Integer, db.ForeignKey('squadra.id'),)
    fuori_id = db.Column(db.Integer, db.ForeignKey('squadra.id'),)
    casa = db.relationship('Squadra', foreign_keys='Partita.casa_id',
                           primaryjoin="Partita.casa_id==Squadra.id")
    fuori = db.relationship('Squadra', foreign_keys='Partita.fuori_id',
                           primaryjoin="Partita.fuori_id==Squadra.id")
    gol_casa = db.Column(db.Integer(), nullable=True)
    gol_fuori = db.Column(db.Integer(), nullable=True)

    def __repr__(self):
        return '[%s] %s - %s' % (self.giornata, self.casa, self.fuori)


class Formazione (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # relazione con Squadra
    squadra_id = db.Column(db.Integer, db.ForeignKey('squadra.id'))
    # relazioni con Giocatore
    giocatori = db.relationship('Giocatore', secondary='formazioni_giocatori',
                             backref=db.backref('formazioni', lazy='dynamic'))

    giornata = db.Column(db.Integer())
    pts = db.Column(db.Float(), nullable=True)
    timestamp = db.Column(db.DateTime)

    def __init__(self, squadra, giocatori, giornata, pts=0.0):
        self.squadra = squadra
        self.giocatori = giocatori
        self.giornata = giornata
        self.pts = pts

    def __repr__(self):
        return 'form. %s gg: %s' % (self.squadra_id, self.giornata)


class Voto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # relazione con Giocatore
    giocatore_id = db.Column(db.Integer, db.ForeignKey('giocatore.id'))
    giornata = db.Column(db.Integer())
    voto_nudo = db.Column(db.Float())
    fanta_voto = db.Column(db.Float())

    def __init__(self, giornata, voto_nudo, fanta_voto, giocatore):
        self.giornata = giornata
        self.voto_nudo = voto_nudo
        self.fanta_voto = fanta_voto
        self.giocatore = giocatore

    def __repr__(self):
        return '%s gg.: %s' % (self.giocatore, self.giornata)


class Mercato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Relazione con squadra
    squadra_id = db.Column(db.Integer, db.ForeignKey('squadra.id'),)

    # Relazione con giocatori
    giocatore_id = db.Column(db.Integer, db.ForeignKey('giocatore.id'),)
    giocatore = db.relationship('Giocatore',
                    foreign_keys='Mercato.giocatore_id',
                    primaryjoin="Mercato.giocatore_id==Giocatore.id")
    verso = db.Column(db.String(3))

    def __repr__(self):
        return '<mercato> %r - %r' % (self.giocatore, self.verso)


if __name__ == '__main__':
    manager.run()
