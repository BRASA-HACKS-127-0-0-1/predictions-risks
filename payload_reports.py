import numpy as np
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./hacks22-firebase-adminsdk-hn1pi-3582006243.json")
firebase_admin.initialize_app(cred)
store = firestore.client()


def createDataPoints(centroidLocation, numSamples, clusterDeviation):
        # Create random data and store in feature matrix X and response vector y.
        X, y = make_blobs(n_samples=numSamples, centers=centroidLocation, 
                          cluster_std=clusterDeviation,random_state=42)
        Xx = []
        for it,i_y in zip(X,y):
            wg = np.random.randint(1,3)
            if i_y==4 or i_y==0:
                wg = 3
            #Xx.append({'latitude': it[0], 'longitude': it[1], 'weight': 10*wg})

            #pingoo.append({'latitude': lat, 'longitude': long, 'weight': wg})
            doc_ref = store.collection(u'reports')
            doc_ref.add({'latitude': it[0], 'longitude': it[1], 'weight': 10*wg})
            
        
        return Xx, y
    

if __name__ == "__main__":
    print(X,yy = createDataPoints([(-22.5,-43.24),(-22.5,-43.18),(-22.54,-43.14),(-22.52,-43.20),(-22.52,-43.18)],600,0.003))
