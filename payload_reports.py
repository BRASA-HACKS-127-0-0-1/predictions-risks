import numpy as np
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./hacks22-firebase-adminsdk-hn1pi-3582006243.json")
firebase_admin.initialize_app(cred)
store = firestore.client()


def gerador_pings(N_x=500, N_y=500, N_p=27777):
    """"
    N_x: len x_axis (The greater the better)
    N_y: len y_axis (ideally N_y===N_x)
    N_p: Number of ping
    output: {'latitude': ,'longitude': ,'weight': }


    This function generates N_p number of pings for our database
    """
    ## Coordenadas do nosso mapa
    x0, y0 = -22.56470395707823, -43.25086811053996
    x1, y1 = -22.471493728332902, -43.1235671880782


    def risco():
        """Igual probabilidade de selecionar qualquer uma das regioes de risco."""
    
        ss = N_x
    
        reg_0 = (0,20*ss//100)
        reg_1 = (40*ss//100,47*ss//100) 
        reg_3 = (ss-21*ss//100,ss)
    
        reg = [reg_0,reg_1,reg_3]
        i = np.random.randint(0,4)
        if i>=2:
            i=-1
        ii =  reg[i]  # Selecionar uma das tres
        return np.random.randint(ii[0],ii[1]),np.random.randint(ii[0],ii[1])
    
    def resto():
        ss = N_x
    
        return np.random.randint(0,ss)

    dx = (x1 - x0) / (N_x - 1)
    dy = (y1 - y0) / (N_y - 1)

    def ping(x, y):
        return x0 + dx * x, y0 + dy * y

    pingoo = []

    cr = 0
    for p in np.random.random(N_p):
        wg = np.random.randint(1, 4)  # pesos iguais probabilidades... 

        ### 75% de chances do ping se referir a uma area de risco
        if p > 0.85 :
            wg = np.random.randint(1, 3)  # pesos iguais probabilidades peso 1 ou 2
            lat, long = ping(resto(), resto())

        else:
            cr += 1
            # zona de risco peso =3
            lat, long = ping(risco())
            wg = 3

        #pingoo.append({'latitude': lat, 'longitude': long, 'weight': wg})
        doc_ref = store.collection(u'reports')
        doc_ref.add({'latitude': lat, 'longitude': long, 'weight': wg*10})

    return pingoo 


if __name__ == "__main__":
    print(gerador_pings())
