import numpy as np

def gerador_pings(N_x, N_y, N_p):
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
        return np.random.randint(ii[0],ii[1])
    
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
        if p > 0.75:
            wg = np.random.randint(1, 3)  # pesos iguais probabilidades peso 1 ou 2
            lat, long = ping(resto(), resto())

        else:
            cr += 1
            # zona de risco peso =3
            lat, long = ping(risco(), risco())
            wg = 3

        pingoo.append({'latitude': lat, 'longitude': long, 'weight': wg})

    return pingoo 

if __name__ == "__main__":
    print(gerador_pings(int(input("N_x: ")), int(input("N_y: ")), int(input("N_p: "))))
