import requests
#import firebase_admin
#from firebase_admin import db
import pyrebase

config = {
  "apiKey": "AIzaSyDkXIft0OEGQXwB9vfzWagKb1UP7vZyO5Y",
  "authDomain": "hacks22.firebaseapp.com",
  "projectId": "hacks22",
  "storageBucket": "hacks22.appspot.com",
  "messagingSenderId": "354618591630",
  "appId": "1:354618591630:web:cb9a454ed8f04481dcbcdf",
  "measurementId": "G-6HC3T3K2J3" }

firebase = pyrebase.initialize_app(config)

dados = firebase.database()


def main(city='Petrópolis'):
    """"
    input: nome da cidade a qual pesquisar alerta (standard: Petrópolis)

    will insert the alerts from https://alertas2.inmet.gov.br/ of the desired city to the database
    """

    r = requests.get('https://apiprevmet3.inmet.gov.br/avisos/ativos')

    hoje = r.json()["hoje"]
    futuro = r.json()["futuro"]

    out_hj = []
    out_fut = []
    ### Procurar por Petrópolis em Hoje

    for dic in hoje:  # Ciclo sobre as listas de 'hoje' (cada uma contem um dic de aviso)
        municipios = dic["municipios"]

        try:
            _ = municipios.index(city)
            data = {"descricao": dic["descricao"],
                    "aviso_cor": dic["aviso_cor"],
                    "severidade": dic["severidade"],
                    "riscos": dic["riscos"],
                    "instrucoes": dic["instrucoes"]}
            out_hj.append(data)
            dados.child("alerts").push(data)


        except:
            pass

    for dic in futuro:  # Ciclo sobre as listas de 'futuro' (cada uma contem um dic de aviso)
        municipios = dic["municipios"]
        try:
            _ = municipios.index(city)
            data = {"descricao": dic["descricao"],
                    "aviso_cor": dic["aviso_cor"],
                    "severidade": dic["severidade"],
                    "riscos": dic["riscos"],
                    "instrucoes": dic["instrucoes"]}
            out_fut.append(data)
            dados.child("alerts_future").push(data)


        except:
            pass

    #### Push para firebase

    # json
    df = {"hoje": out_hj,
          "futuro": out_fut}

    return df


if __name__ == "__main__":
    print(main())
