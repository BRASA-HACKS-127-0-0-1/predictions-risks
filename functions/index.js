const functions = require("firebase-functions");
const admin = require('firebase-admin');
admin.initializeApp()
const axios = require('axios');
const db = admin.firestore();

exports.onAlertCreate = functions.firestore
  .document('alerts/{alertId}')
  .onCreate((change, context) => {
    const newValue = change.data();
    const alertId = context.params.alertId;
    const alert = {
      id: alertId,
      ...newValue
    };
    const promises = [];
    db.collection("notification_tokens").get().then(snapshot => {
      snapshot.forEach(doc => {
        promises.push(sendAlert(doc.data().token, alert));
      });
    }).catch(err => {
      console.log(err);
    });
    return Promise.all(promises);
  });

  exports.apiFetch = functions.pubsub.schedule('every 12 hours').onRun(() => {
    return getAlerts();
  });


  async function getAlerts(){
   const response = await axios.get('https://apiprevmet3.inmet.gov.br/avisos/ativos');
   if(response){
    const batch = db.batch();
      const {data} = response;
      const {hoje, futuro} = data;
      const alertsRef = db.collection('alerts');
      const alertsFutureRef = db.collection('alerts_future');
      hoje.forEach(item => {
        if(item.municipios.includes('Petrópolis')){
          batch.set(alertsRef.doc(item.id),{
            id: item.id,
            descricao: item.descricao,
            aviso_cor: item.aviso_cor,
            severidade: item.severidade,
            riscos: item.riscos,
            instrucoes: item.instrucoes,
          });
        }
      });
      futuro.forEach(item => {
        if(item.municipios.includes('Petrópolis')){
          batch.set(alertsFutureRef.doc(item.id),{
            id: item.id,
            descricao: item.descricao,
            aviso_cor: item.aviso_cor,
            severidade: item.severidade,
            riscos: item.riscos,
            instrucoes: item.instrucoes,
          });
        }
      });
      await batch.commit();
   }
  }
 async function sendAlert(token, alert){
   console.log('sendAlert');
  return axios.post('https://exp.host/--/api/v2/push/send', 
    {
      to: token,
      sound: 'default',
      title: alert.severidade,
      body: alert.descricao,
      data: alert,
    }, {
      headers: {
        Accept: 'application/json',
        'Accept-encoding': 'gzip, deflate',
        'Content-Type': 'application/json',
      }
    }
  );
 }