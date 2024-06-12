from flask import Flask, render_template, request, session, redirect, url_for, Markup
from flask_sqlalchemy import SQLAlchemy
from openai import OpenAI
from abc import ABC

app = Flask(__name__)
app.secret_key = '101112'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///minhabase.sqlite3'
db = SQLAlchemy(app)

@app.route("/")
def introducao():
    return '''
        <head>
            <link rel="stylesheet" type="text/css" href="./static/index.css">
            <style>
                body{
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    background-image:url("https://segredosdomundo.r7.com/wp-content/uploads/2020/08/inferno-o-que-diz-a-religiao-e-a-filosofia-sobre-o-ambiente-de-dor-e-pecado-4.jpg");
                    background-repeat: no-repeat;
                    background-size:cover;
                }

                .intromain{
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    align-self: center;
                    margin: 20px 0 20px 0;
                    background-color: black;
                    padding: 30px;
                    color:white;
                    font-size: 23px;
                    width: 500px;
                    border-radius: 20px;
                }
            </style>
        </head>
        <body>
            <main class="intromain">
                <h1 class="titulo-principal">Bem-vindo às Profundezas do Inferno</h1>
                <p>
                    Você é Morfeu, mais do que o Senhor dos Sonhos, você é o próprio conceito de Sonho antropomorfizado.
                    Você está no inferno, em busca de uma das suas 3 relíquias lendárias que complementam seu poder, o seu elmo.
                    A jornada não tem sido exatamente fácil, foi preciso atravessar as partes mais perigosas do inferno para chegar até aqui,
                    enfim, as portas do palácio de Lúcifer se encontram diante de ti.
                </p>

                <p>
                    Como seres eternos, uma batalha no sentido mundano seria redundante, logo, a batalha será no formato do "Jogo mais Antigo",
                    em que vocês deveram participar de um jogo de palavras, com o intuito de: ou derrotar o seu oponente ou sobreviver um ataque dele.
                </p>

                <p>
                    Exemplo:<br><br>

                    -Lúcifer: Eu sou um lobo feroz, perseguidor de presas.<br>
                    -Você: Eu sou um caçador, arqueiro preciso, matador de lobos.
                </p>

                <p>Para terminar o jogo, você deve derrotar Lúcifer ou admitir derrota.</p>

                <a href="https://pedropedro.pythonanywhere.com/palacio-de-lucifer"><button class="botaoestilizado">Começar a Batalha</button></a>
            </main>
        </body>
    '''

@app.route("/login", methods=['POST', 'GET'])
def login():
    if 'username' in session:
        return redirect(url_for('log'))
    else:
        if request.method == 'POST' and Usuario.query.filter_by(nome=request.form['username'], senha=request.form['senha']).first() is not None:
            session['username'] = request.form['username']
            return redirect(url_for('log'))
        return '''
            <head>
            <link rel="stylesheet" type="text/css" href="./static/index.css">
                <style>
                    *{
                        color:white;
                    }

                    body{
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        background-image:url("https://picfiles.alphacoders.com/102/10229.jpg");
                        background-repeat: no-repeat;
                        background-size:cover;
                    }

                    .container{
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        background-color: black;
                        width: 400px;
                        margin: auto;
                        padding: 20px;
                        border: 3px solid white;
                        border-radius: 50px;
                        margin-top: 7%;
                    }

                    .input-box{
                        background-color: black;
                        border-color: white;
                        width: 100px;
                        padding: 10px;
                        border-radius: 50px;
                        font-size: 21px;
                        color: white;
                        margin-bottom: 15px;
                    }

                    h1{
                        font-size: 30px;
                    }

                    .login-box{
                        width: 250px;
                    }

                    .input-text{
                        font-size: 21px;
                        margin-bottom: 5px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Login</h1>
                    <form method="post">
                        <p class="input-text">Nome de Admin:</p>
                        <input class="input-box login-box" type=text name=username>

                        <p class="input-text">Senha:</p>
                        <input class="input-box login-box" type=password name=senha>

                        <p><input class="botaoestilizado" type=submit value=Login>
                    </form>
                    <a href="https://pedropedro.pythonanywhere.com/palacio-de-lucifer"><button class="botaoestilizado">Voltar</button></a>
                </div>
            </body>
        '''

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('introducao'))

@app.route("/usuario", methods=['POST', 'GET'])
def addAdmin():
    if 'username' in session:
        if request.method == 'POST':
            nome = request.form['nome']
            senha = request.form['senha']
            user = Usuario(nome, senha)
            db.session.add(user)
            db.session.commit()
        users = Usuario.query.all()
        return render_template('usuario.html', usuarios=users)
    else:
        return '''
        <body>
            Você não tem permissão para acessar essa página, <a href="https://pedropedro.pythonanywhere.com/">voltar ao início</a>
        </body>
        '''

@app.route("/palacio-de-lucifer", methods = ['POST', 'GET'])
def chatgpt():
    if request.method == 'POST':
        prompt = request.form['questao']

        fachada = FachadaTribunal()
        fachada.criarLucifer(prompt)
        fachada.criarJuiz()

        resposta = fachada.lutar()
        chat_hist = Historico.query.all()
        resposta = fachada.julgar(chat_hist)

        chat_atual = Historico(resposta)
        db.session.add(chat_atual)
        db.session.commit()
        fachada.passar_sentenca()

        return render_template("questao.html", resposta=resposta)
    return render_template("questao.html")

@app.route("/history-log", methods = ['POST', 'GET'])
def log():
    if 'username' in session:
        chat_hist = Historico.query.all()
        return render_template("history-log.html", chat_hist=chat_hist)
    else:
        return '''
        <body>
            Você não tem permissão para acessar essa página, <a href="https://pedropedro.pythonanywhere.com/">voltar ao início</a>
        </body>
        '''

@app.route("/deletar", methods = ['POST', 'GET'])
def deletarChat():
    identidade = request.form['identidade']
    sql_delete_query = """DELETE from Historico where id = :identidade"""
    db.session.execute(sql_delete_query, {'identidade': identidade})
    db.session.commit()
    return redirect(url_for('log'))

@app.route("/trocar", methods = ['POST', 'GET'])
def trocarChat():
    novoTexto = request.form['novoChat']
    identidade = request.form['identidade']
    sql_update_query = """Update Historico set chat = :novoTexto where id = :identidade"""
    db.session.execute(sql_update_query, {'identidade': identidade, 'novoTexto': novoTexto})
    db.session.commit()
    return redirect(url_for('log'))

@app.route("/editar", methods = ['POST', 'GET'])
def editarChat():
    if 'username' in session:
        texto = request.form['texto']
        identidade = request.form['identidade']
        trocar_url = url_for('trocarChat')
        edicao_html = Markup(f'''
            <html>
            <head>
                <link rel="stylesheet" type="text/css" href="./static/index.css">
            </head>
            <body class="chatBody">
                <main class="chatContainer">
                    <h1>Alterar Chat</h1>
                    <form action="{trocar_url}" method="post">
                        <input class="chatInputBox" type="text" name="novoChat" value="{texto}"><br>
                        <input type="hidden" name="identidade" value="{identidade}">
                        <input class="botaoestilizado" type="submit" value="Trocar">
                    </form>
                    <a href="https://pedropedro.pythonanywhere.com/history-log"><button class="botaoestilizado">Voltar</button></a>
                <main>
            </body>
            </html>
        ''')
        return edicao_html
    else:
        return redirect(url_for('log'))

@app.route("/adicionar", methods = ['POST', 'GET'])
def adicionarChat():
    addChat = request.form['addChat']
    chat_adicionado = Historico(addChat)
    db.session.add(chat_adicionado)
    db.session.commit()
    return redirect(url_for('log'))

@app.route("/criar", methods = ['POST', 'GET'])
def criarChat():
    if 'username' in session:
        adicionar_url = url_for('adicionarChat')
        adicao_html = Markup(f'''
            <html>
            <head>
                <link rel="stylesheet" type="text/css" href="./static/index.css">
            </head>
            <body class="chatBody">
                <main class="chatContainer">
                    <h1>Adicionar Chat ao Histórico</h1>
                    <form action="{adicionar_url}" method="post">
                        <input class="chatInputBox" type="text" name="addChat"><br>
                        <input class="botaoestilizado" type="submit" value="Adicionar">
                    </form>
                    <a href="https://pedropedro.pythonanywhere.com/history-log"><button class="botaoestilizado">Voltar</button></a>
                </main>
            </body>
            </html>
        ''')
        return adicao_html
    else:
        return redirect(url_for('log'))

class Chat_gpt(ABC):
    chave = 'chave_aqui'
    modelo_de_inteligencia = 'gpt-3.5-turbo-0125'
    formato_de_resposta = {"type": "text"}
    conexao = OpenAI(api_key = chave)

    def __init__(self):
        pass

class Lucifer(Chat_gpt):
    def __init__(self, prompt, corte):
        super().__init__()
        self.prompt = prompt
        self.corte = corte
        self.resposta = ""
        self.corte.apontar_acusado(self)

    def lutar(self):
        response = self.conexao.chat.completions.create(
            model = self.modelo_de_inteligencia,
            response_format= self.formato_de_resposta,
            messages=[
                {"role": "system", "content": "Você responderá participando do jogo mais antigo, da história de sandman, lembre-se de não sair de personagem, a batalha continua até que um de nós vença, a batalha segue uma sequência estilo:Batalhador n°1 - 'eu sou um urso faminto e selvagem', em seguida, Batalhador n°2(você) - 'Eu sou um caçador destemível, matador de ursos', você não é morfeu nem nenhum dos eternos de sandman, CONTINUE A BATALHA, se o seu oponente admitir derrota, diga que ele deverá partir de mãos vazias, se a pergunta for algo não relacionada à batalha, pergunte se o seu oponente está confuso, evite mencionar super-heróis, pessoas não derrotam bactérias, evite repetir a mesma resposta durante uma batalha, evite mencionar cientistas ou qualquer outra profissão moderna, a ideia é que a batalha tenha um cenário que vá de mais medieval até um cenário mais místico, com batalhas de coisas como, o esquecimento, a arrogância e etc, se o seu oponente aumentar a escala da batalha, digamos, dizendo ser uma pandemia ou algo de muita destruição, evite reduzir a escala da batalha, ou seja, uma resposta para algo dessa escala deve ser algo de escala semelhante, evite criar personagens aleatórios, tome cuidado para que suas repostas não ultrapassem 25 palavras com frequência, se você julgar apropriado, admita derrota, entregando ao seu oponente o elmo, você não pode dizer ser algum tipo de guardião mágico, não use coisas que não existem, contenha-se a coisas físicas e metafísicas, vale ressaltar que você deve tentar me destruir ou sobreviver aos meus 'ataques' '"},
                {"role": "user", "content": self.prompt}
                ]
        )
        self.resposta = response.choices[0].message.content
        return self.resposta

    def entregar_resposta(self):
        return self.resposta

    def entregar_prompt(self):
        return self.prompt

class Juiz(Chat_gpt):
    def __init__(self, corte):
        super().__init__()
        self.corte = corte
        self.corte.escolher_juiz(self)

    def analisar_chat(self, analise):
        self.analise = analise
        response = self.conexao.chat.completions.create(
            model = self.modelo_de_inteligencia,
            response_format= self.formato_de_resposta,
            messages=[
                {"role": "system", "content": "Você analisará as duas frases recebidas, e comparará o quão similares elas são, dando um nota entre 0 e 10, a sua resposta deve ser unicamente o número da nota e nada mais, isso é absolutamente importante, exemplo: '7', sem pontuação, palavras extras, nada, somente o número, quanto mais parecida as duas frases forem, maior a nota"},
                {"role": "user", "content": self.analise}
                ]
        )
        self.nota = response.choices[0].message.content
        return self.nota

    def julgar(self, historico):
        chat_hist = historico
        self.veredito = self.corte.enviar_evidencia()
        for chat_atual in chat_hist:
            analise = "Frase 1:" + chat_atual.chat + "Frase 2:" + self.veredito
            self.nota = self.analisar_chat(analise)
            numero_atual = ''
            for numero in self.nota:
                if numero.isdigit():
                    numero_atual += numero
            if int(numero_atual) > 7:
                self.veredito = "Agghr, admito a minha derrota dessa vez, tome o seu elmo e vá, suma da minha frente, Morfeu!"
                return self.veredito
        return self.veredito

    def limparHistorico(self):
        db.session.execute("DELETE FROM HISTORICO")
        db.session.commit()

    def passar_sentenca(self):
        prompt = self.corte.enviar_prompt().lower()
        if "admito" in prompt and "derrota" in prompt or self.veredito == "Agghr, admito a minha derrota dessa vez, tome o seu elmo e vá, suma da minha frente, Morfeu!":
            self.limparHistorico()

class Tribunal:
    __instance = None

    def __new__(cls):
        if Tribunal.__instance is None:
            Tribunal.__instance = super().__new__(cls)
        return Tribunal.__instance

    def __init__(self):
        pass

    def apontar_acusado(self, acusado):
        self.acusado = acusado

    def escolher_juiz(self, juiz):
        self.juiz = juiz

    def enviar_evidencia(self):
        return self.acusado.entregar_resposta()

    def enviar_prompt(self):
        return self.acusado.entregar_prompt()

class FachadaTribunal:
    def __init__(self):
        self.corte = Tribunal()
        self.lucifer = None
        self.juiz = None

    def criarLucifer(self, prompt):
        self.lucifer = Lucifer(prompt, self.corte)

    def criarJuiz(self):
        self.juiz = Juiz(self.corte)

    def lutar(self):
        return self.lucifer.lutar()

    def julgar(self, historico):
        return self.juiz.julgar(historico)

    def passar_sentenca(self):
        self.juiz.passar_sentenca()

class Historico(db.Model):
    __tablename__ = "historico"

    id = db.Column(db.Integer, primary_key=True)
    chat = db.Column(db.String)

    def __init__(self, chat):
        self.chat = chat

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, unique=True)
    senha = db.Column(db.String)

    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
