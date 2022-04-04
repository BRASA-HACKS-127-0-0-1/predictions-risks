const functions = require("firebase-functions");
const admin = require('firebase-admin');
admin.initializeApp()
const axios = require('axios');
const db = admin.firestore();

exports.onAlertCreate = functions.firestore
    .document('alerts/{alertId}')
    .onCreate((change, context) => sendAlerts(change, context));
exports.onAlertCreate = functions.firestore
    .document('alerts_future/{alertId}')
    .onCreate((change, context) => sendAlerts(change, context, true));

exports.apiFetch = functions.pubsub.schedule('every 2 hours').onRun(() => {
    return getAlerts();
});


async function getAlerts() {
    const response = await axios.get('https://apiprevmet3.inmet.gov.br/avisos/ativos');
    if (response) {
        const batch = db.batch();
        const {data} = response;
        const {hoje, futuro} = data;
        const alertsRef = db.collection('alerts');
        const alertsFutureRef = db.collection('alerts_future');
        hoje.forEach(item => {
            if (item.municipios.includes('Petrópolis')) {
                batch.set(alertsRef.doc(`${item.id}`), {
                    id: item.id,
                    descricao: item.descricao,
                    data_inicio: item.data_inicio,
                    hora_inicio: item.hora_inicio,
                    data_fim: item.data_fim,
                    hora_fim: item.hora_fim,
                    aviso_cor: item.aviso_cor,
                    severidade: item.severidade,
                    riscos: item.riscos,
                    instrucoes: item.instrucoes,
                });
            }
        });
        futuro.forEach(item => {
            if (item.municipios.includes('Petrópolis')) {
                batch.set(alertsFutureRef.doc(`${item.id}`), {
                    id: item.id,
                    descricao: item.descricao,
                    data_inicio: item.data_inicio,
                    hora_inicio: item.hora_inicio,
                    data_fim: item.data_fim,
                    hora_fim: item.hora_fim,
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

async function sendAlerts(change, context) {
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
}

async function sendAlert(token, alert, isFuture = false) {
    return axios.post('https://exp.host/--/api/v2/push/send',
        {
            to: token,
            sound: 'default',
            title: `${isFuture ? 'Futuro' : 'Hoje'} - ${alert.severidade}`,
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
