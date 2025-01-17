const amqp = require('amqplib');
var Project = require('../models/project')

async function sendToQueue(msg) {
  try {
    const connection = await amqp.connect('amqp://localhost');
    const channel = await connection.createChannel();
    
    const queue = 'requestQueue'; // Fila de pedidos
    await channel.assertQueue(queue, { durable: true });
    
    channel.sendToQueue(queue, Buffer.from(JSON.stringify(msg)), {
      persistent: true, // A mensagem será mantida mesmo se o servidor falhar
    });

    console.log('Pedido enviado para a fila:', msg);
    await channel.close();
    await connection.close();
  } catch (error) {
    console.error('Erro ao enviar mensagem para fila:', error);
  }
}

module.exports = sendToQueue;
