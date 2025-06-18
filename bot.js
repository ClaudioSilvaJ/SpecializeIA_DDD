const { useMultiFileAuthState, default: makeWASocket, DisconnectReason } = require("@whiskeysockets/baileys");
const axios = require('axios');
const qrcode = require('qrcode-terminal');

const lastMessageTimestamps = new Map();
const messageBuffers = new Map();
const messageTimers = new Map();

async function connectWhats() {
  const { state, saveCreds } = await useMultiFileAuthState('./auth_info.json');

  const sock = makeWASocket({
    auth: state,
  });

  sock.ev.on('connection.update', (update) => {
    const { connection, lastDisconnect, qr } = update;

    if (qr) {
      console.log('⚠️ Escaneie o QR Code abaixo para conectar:');
      qrcode.generate(qr, { small: true });
    }

    if (connection === 'close') {
      const error = (lastDisconnect?.error)?.output?.statusCode;
      console.log(`❌ Conexão encerrada. Código de erro: ${error}`);
      const shouldReconnect = error != DisconnectReason.loggedOut;
      if (shouldReconnect) {
        console.log('🔁 Tentando reconectar...');
        setTimeout(() => connectWhats(), 5000);
      }
    } else if (connection === 'open') {
      console.log('✅ Conexão estabelecida com sucesso!');
    }
  });

  sock.ev.on('creds.update', saveCreds);

  sock.ev.on('messages.upsert', async m => {
    if (m.messages[0].key.fromMe) return;
    const message = m.messages[0];
    const remoteJid = message.key.remoteJid;
    const userMessage = message.message.conversation;
    const now = Date.now();
    const lastTimestamp = lastMessageTimestamps.get(remoteJid) || 0;

    if (now - lastTimestamp > 600000) {
      lastMessageTimestamps.set(remoteJid, now);
      await sock.sendMessage(remoteJid, {
        text: 'Olá! Esse bot se encontra em versão experimental, siga as instruções:\nDescreva seus sintomas em sequência. Não é necessário separar por mensagens ou usar linguagem técnica.'
      });
      return;
    }

    if (!messageBuffers.has(remoteJid)) {
      messageBuffers.set(remoteJid, []);
    }
    messageBuffers.get(remoteJid).push(userMessage);

    if (messageTimers.has(remoteJid)) {
      clearTimeout(messageTimers.get(remoteJid));
    }

    messageTimers.set(remoteJid, setTimeout(async () => {
      const messages = messageBuffers.get(remoteJid).join(' ');
      messageBuffers.delete(remoteJid);
      messageTimers.delete(remoteJid);

      if (messages.length < 10) {
        await sock.sendMessage(remoteJid, { text: `Sua mensagem é muito curta! Seja mais específico.` });
        return;
      }

      try {
        const response = await axios.post('http://127.0.0.1:8000/analyze-symptoms', { message: messages });
      
        const sintomas = response.data.extracted_symptoms;
        const especialidade = response.data.suggested_specialties;

        if (sintomas[0] === 'Nenhum') {
          await sock.sendMessage(remoteJid, { text: `Infelizmente não consegui obter nenhum sintoma da sua mensagem. Pode tentar novamente?` });
          return;
        }

        if (!especialidade) {
          await sock.sendMessage(remoteJid, { text: `Seus sintomas: ${sintomas.join(', ')}\nConsulte com um médico geral.` });
        } else {
          await sock.sendMessage(remoteJid, { text: `Seus sintomas: ${sintomas.join(', ')}\nConsulte com um especialista em: ${especialidade}` });
        }
      } catch (error) {
        console.error("Erro ao chamar a API:", error);
        await sock.sendMessage(remoteJid, { text: "Houve um erro ao processar sua mensagem." });
      }
    }, 5000));
  });
}

connectWhats();
