import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./hacks22-firebase-adminsdk-hn1pi-3582006243.json")
firebase_admin.initialize_app(cred)
store = firestore.client()

um = [
    {'latitude': -22.50397340939699,
     'longitude': -43.24537251630015},
    {'latitude': -22.50874068403227,
     'longitude': -43.23872246516382},
    {'latitude': -22.50537192754704,
     'longitude': -43.23648295805497},
    {'latitude': -22.49671897999712,
     'longitude': -43.23274678206963},
    {'latitude': -22.494361379528353,
     'longitude': -43.23497319494598},
    {'latitude': -22.493548647660667,
     'longitude': -43.238244491230255},
    {'latitude': -22.494366254677235,
     'longitude': -43.24194729546746},
    {'latitude': -22.495268951524693,
     'longitude': -43.245542001169405},
    {'latitude': -22.49616720955332,
     'longitude': -43.24616671437901},
    {'latitude': -22.50121382978169,
     'longitude': -43.24696566434815},
    {'latitude': -22.50317543679685,
     'longitude': -43.24612019449911}
]

dois = [
    {'latitude': -22.493385821358142,
     'longitude': -43.18408891412829},
    {'latitude': -22.51312265035196,
     'longitude': -43.20786684155072},
    {'latitude': -22.517565558111777,
     'longitude': -43.207501917732294},
    {'latitude': -22.525831716675295,
     'longitude': -43.20607905373375},
    {'latitude': -22.529413479559594,
     'longitude': -43.20283893943706},
    {'latitude': -22.52617876506964,
     'longitude': -43.175648836248946},
    {'latitude': -22.522185606946607,
     'longitude': -43.1733754238663},
    {'latitude': -22.515963803149226,
     'longitude': -43.17268063933231},
    {'latitude': -22.4998150272382,
     'longitude': -43.173012936896846},
    {'latitude': -22.499776468503327,
     'longitude': -43.173024828165694},
    {'latitude': -22.4968969406655,
     'longitude': -43.17402729597528},
    {'latitude': -22.4921586875028,
     'longitude': -43.17793806959647}
]

tres = [
    {'latitude': -22.533195650793104,
     'longitude': -43.14497267286389},
    {'latitude': -22.538881007028934,
     'longitude': -43.14883049891951},
    {'latitude': -22.543028570334553,
     'longitude': -43.14676173170478},
    {'latitude': -22.54696588177003,
     'longitude': -43.14069751986387},
    {'latitude': -22.54715327279648,
     'longitude': -43.13566725569794},
    {'latitude': -22.54278555008239,
     'longitude': -43.132652349829016},
    {'latitude': -22.536349052852326,
     'longitude': -43.133242510057784},
    {'latitude': -22.53200305509532,
     'longitude': -43.135459401277025},
    {'latitude': -22.53150049235205,
     'longitude': -43.14153174147727}
]

doc_ref = store.collection(u'polygon')
doc_ref.add({"coordinates": um, "weight": 30})
doc_ref.add({"coordinates": dois, "weight": 19})
doc_ref.add({"coordinates": tres, "weight": 16})
