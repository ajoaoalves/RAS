const axios = require('axios');

// Configuração da URL base do servidor
const BASE_URL = 'http://localhost:8080';

async function testConnection() {
    try {
        const response = await axios.get(`${BASE_URL}/`);
        console.log('Resposta do servidor:', response.data);
    } catch (error) {
        console.error('Erro ao testar a conexão:', error.message);
    }
}

async function createProject() {
    const projectData = {
        _id: "1234abcd-5678-efgh-9101-ijklmnopqrst",
        name: "Projeto de Teste",
        user_id: "9876abcd-5432-efgh-1011-qrstuvwxwzyz",
        images: [
            {
                _id: "image123",
                uri: "https://example.com/test-image.jpeg"
            }
        ]
    };

    try {
        const response = await axios.post(`${BASE_URL}/projects`, projectData);
        console.log('Projeto criado com sucesso:', response.data);
    } catch (error) {
        console.error('Erro ao criar projeto:', error.response.data || error.message);
    }
}

async function updateProject(projectId) {
    const updateData = {
        name: "Projeto Atualizado",
        images: [
            {
                _id: "image123",
                uri: "https://example.com/updated-image.jpeg"
            }
        ]
    };

    try {
        const response = await axios.put(`${BASE_URL}/projects/${projectId}`, updateData);
        console.log('Projeto atualizado com sucesso:', response.data);
    } catch (error) {
        console.error('Erro ao atualizar projeto:', error.response.data || error.message);
    }
}

async function executeProject(projectId) {
    const execData = {
        parameter: "execValue" // Exemplo de dados de execução
    };

    try {
        const response = await axios.put(`${BASE_URL}/projects/${projectId}/exec`, execData);
        console.log('Projeto executado com sucesso:', response.data);
    } catch (error) {
        console.error('Erro ao executar projeto:', error.response.data || error.message);
    }
}

async function getProjectDetails(projectId) {
    try {
        const response = await axios.get(`${BASE_URL}/projects/${projectId}`);
        console.log('Detalhes do projeto:', response.data);
    } catch (error) {
        console.error('Erro ao obter detalhes do projeto:', error.response.data || error.message);
    }
}

async function listProjects() {
    try {
        const response = await axios.get(`${BASE_URL}/projects`);
        console.log('Lista de projetos:', response.data);
    } catch (error) {
        console.error('Erro ao listar projetos:', error.response.data || error.message);
    }
}

// Função principal para executar os testes
(async () => {
    console.log('== Testando conexão com o servidor ==');
    await testConnection();

    console.log('\n== Criando um novo projeto ==');
    await createProject();

    console.log('\n== Listando todos os projetos ==');
    await listProjects();

    console.log('\n== Atualizando um projeto ==');
    await updateProject('1234abcd-5678-efgh-9101-ijklmnopqrst');

    console.log('\n== Executando um projeto ==');
    await executeProject('1234abcd-5678-efgh-9101-ijklmnopqrst');

    console.log('\n== Obtendo detalhes de um projeto ==');
    await getProjectDetails('1234abcd-5678-efgh-9101-ijklmnopqrst');
})();
