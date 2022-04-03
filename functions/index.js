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
        promises.add(sendAlert(doc.data().token, alert));
      });
    }).catch(err => {
      console.log(err);
    });
    return Promise.all(promises);
  });


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