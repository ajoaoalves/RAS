const amqp = require('amqplib');
const moment = require('moment'); // Para gerar o timestamp no formato datetime

// Função genérica para enviar mensagem para a fila com parâmetros específicos de cada procedimento
async function sendToQueue(projectId, image, tool, index) {
  try {
    const connection = await connectToRabbitMQ(); // Conectar ao RabbitMQ
    const channel = await connection.createChannel();

    // Gerar o nome da fila dinamicamente
    const queue = `${tool.procedure}-requests`;

    // Usar o ID da ferramenta (tool._id) como messageId
    const messageId = tool._id; // O ID da ferramenta será o messageId
    const timestamp = moment().format('YYYY-MM-DD HH:mm:ss'); // Gerar o timestamp no formato datetime

    // Estrutura básica da mensagem
    let message = {
      messageId,
      timestamp,
      procedure: tool.procedure,
      parameters: {
        inputImageURI: image,
      }
    };

    const imageName = image.substring(image.lastIndexOf('/') + 1);
    const outputImageURI = `/out/${projectId}/${index}/${imageName}`; // URI da imagem de saída

    // Usando switch para decidir os parâmetros adicionais ou modificados de cada tipo de procedimento
    switch (tool.procedure) {
      case 'binarization': {
        // Adicionar parâmetros específicos para binarization
        message.parameters.outputImageURI = outputImageURI;
        break;
      }

      case 'border': {
        // Adicionar parâmetros específicos para resize
        message.parameters.bordersize = tool.parameters.bordersize;
        message.parameters.bordercolor = tool.parameters.bordercolor;
        message.parameters.outputImageURI = outputImageURI;
        break;
      }

      case 'brightness': {
        // Adicionar parâmetros específicos para brightness
        message.parameters.brightnessValue = tool.parameters.brightnessValue;
        message.parameters.outputImageURI = outputImageURI;
        break;
      }

      case 'crop': {
        // Adicionar parâmetros específicos para crop
        message.parameters.crop_box = tool.parameters.crop_box;
        message.parameters.outputImageURI = outputImageURI;
        break;
      }

      case 'background-removal': {
        // Adicionar parâmetros específicos para background-removal
        message.parameters.outputImageURI = outputImageURI;
        break;
      }

      case 'resize': {
        // Adicionar parâmetros específicos para resize
        message.parameters.width = tool.parameters.width;
        message.parameters.height = tool.parameters.height;
        message.parameters.outputImageURI = outputImageURI;
        break;
      }

      case 'rotation': {
        // Adicionar parâmetros específicos para rotation
        message.parameters.angle = tool.parameters.angle;
        message.parameters.outputImageURI = outputImageURI;
        break;
      }

      case 'watermark': {
        // Adicionar parâmetros específicos para watermark
        message.parameters.outputImageURI = outputImageURI;
        break;
      }

      //count objects, count people
      default: {
        // Caso o procedimento não esteja listado, apenas manter os parâmetros padrão
        break;
      }
    }

    // Enviar a mensagem para a fila
    channel.sendToQueue(queue, Buffer.from(JSON.stringify(message)), {
      persistent: true, // Garante que a mensagem seja persistente
    });

    console.log(`Mensagem para o procedimento "${tool.procedure}" enviada para a fila "${queue}".`);

    // Fechar o canal e a conexão
    await channel.close();
    await connection.close();
  } catch (error) {
    console.error('Erro ao enviar mensagem para a fila:', error);
    throw error;
  }
}

async function executeProject(project) {
  try {
    // Verificar se o projeto tem imagens
    if (!project.images || project.images.length === 0) {
      console.log(`O projeto "${project._id}" não possui imagens para executar.`);
      return;
    }
    // Verificar se o projeto tem ferramentas
    if (!project.tools || project.tools.length === 0) {
      console.log(`O projeto "${project._id}" não possui ferramentas para executar.`);
      return;
    }

    const tool = project.tools[0]; // Obter a primeira ferramenta do projeto
    // Iterar sobre as ferramentas do projeto e enviar cada uma para a fila
    for (const image of project.images) {
      try {
        await sendToQueue(project._id, image.uri, tool, 0);
      }
      catch (error) {
        console.error(
          `Erro ao enviar a ferramenta "${tool._id}" do projeto "${project._id}" para a fila:`,
          error
        );
      }
    }

    console.log(`Execução do projeto "${project._id}" concluída.`);
  }
  catch (error) {
    console.error('Erro ao executar o projeto:', error);
    throw error;
  }
}

async function connectToRabbitMQ() {
  let retries = 5; // Number of retries
  while (retries) {
    try {
      const connection = await amqp.connect('amqp://rabbitmq:5672'); // Use RabbitMQ service name
      console.log('Connected to RabbitMQ');
      return connection;
    } catch (err) {
      console.error(`RabbitMQ connection failed: ${err.message}. Retrying...`);
      retries -= 1;
      await new Promise((res) => setTimeout(res, 10000)); // Wait 10 seconds before retrying
    }
  }
  throw new Error('Unable to connect to RabbitMQ after multiple retries');
}


async function processQueueResults() {
  try {

    const connection = await connectToRabbitMQ();
    const channel = await connection.createChannel();

    const resultQueue = 'results-queue'; // The name of the queue with results

    // Ensure the queue exists
    await channel.assertQueue(resultQueue, { durable: true });

    console.log(`Waiting for messages in queue: ${resultQueue}`);

    channel.consume(
      resultQueue,
      async (message) => {
        if (message !== null) {
          try {
            // Parse the message content
            const result = JSON.parse(message.content.toString());
            console.log('Message received from result queue:', result);

            // Perform necessary actions based on the result
            if (result.nextTool) {
              // Example: Call sendToQueue with the next tool
              const { projectId, image, tool, index } = result;
              await sendToQueue(projectId, image, tool, index);
            } else {
              console.log(`No next tool for project: ${result.projectId}`);
            }

            // Acknowledge the message
            channel.ack(message);
          } catch (error) {
            console.error('Error processing message:', error);
            // Optionally reject the message (and requeue it for processing later)
            channel.nack(message, false, true);
          }
        }
      },
      { noAck: false } // Ensure messages are acknowledged
    );
  } catch (error) {
    console.error('Error in processQueueResults:', error);
    throw error;
  }
}

// Start the worker thread
processQueueResults().catch((error) => {
  console.error('Error starting queue processor:', error);
});


module.exports = { executeProject, sendToQueue };

