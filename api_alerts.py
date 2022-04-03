import requests
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./hacks22-firebase-adminsdk-hn1pi-3582006243.json")
firebase_admin.initialize_app(cred)
store = firestore.client()


def main(city='Petrópolis'):
    """"
    input: nome da cidade a qual pesquisar alerta (standard: Petrópolis)

    will insert the alerts from https://alertas2.inmet.gov.br/ of the desired city to the database
    """

    r = requests.get('https://apiprevmet3.inmet.gov.br/avisos/ativos')

    hoje = r.json()["hoje"]
    futuro = r.json()["futuro"]

    for dic in hoje:  # Ciclo sobre as listas de 'hoje' (cada uma contem um dic de aviso)
        municipios = dic["municipios"]

        try:
            _ = municipios.index(city)
            data = {"descricao": dic["descricao"],
                    "aviso_cor": dic["aviso_cor"],
                    "severidade": dic["severidade"],
                    "riscos": dic["riscos"],
                    "instrucoes": dic["instrucoes"]}
            doc_ref = store.collection(u'alerts')
            doc_ref.add(data)
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
            doc_ref = store.collection(u'alerts_future')
            doc_ref.add(data)
        except:
            pass

    return True


if __name__ == "__main__":
    print(main())
