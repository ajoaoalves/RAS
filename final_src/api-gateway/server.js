const express = require('express');
const axios = require('axios');
const cors = require('cors');

// Configurations
const PORT = process.env.PORT || 8080;
const PROJECTS_BACKEND_URL = 'http://projects-api:18018';
const USERS_BACKEND_URL = 'http://users-api:19019';
const STATIC_FILE_SERVER = '';


const app = express();

// Middlewares
app.use(express.json({ limit: '50mb' }));
app.use(cors());

// Test endpoint
app.get('/', (req, res) => {
    res.send('API Gateway is running...');
});




// Route to create a new project for a specific user
app.post('/users/:userId/projects', async (req, res) => {
    const { userId } = req.params;

    try {
        // Forward the request to the backend service with the userId
        const response = await axios.post(`${PROJECTS_BACKEND_URL}/users/${userId}/projects`, req.body);
        res.status(response.status).send(response.data);
    } catch (error) {
        console.error('Error creating project for user:', error.message);
        res.status(error.response?.status || 500).send({ error: error.message });
    }
});


// Route to update a project for a specific user
app.put('/users/:userId/projects/:projectId', async (req, res) => {
    const { userId, projectId } = req.params;

    try {
        // Forward the request to the backend service with the userId and projectId
        const response = await axios.put(`${PROJECTS_BACKEND_URL}/users/${userId}/projects/${projectId}`, req.body);
        res.status(response.status).send(response.data);
    } catch (error) {
        console.error('Error updating project for user:', error.message);
        res.status(error.response?.status || 500).send({ error: error.message });
    }
});

// Route to execute a project for a specific user
app.put('/users/:userId/projects/:projectId/exec', async (req, res) => {
    const { userId, projectId } = req.params;

    try {
        // Forward the request to the backend service with userId and projectId
        const response = await axios.put(`${PROJECTS_BACKEND_URL}/users/${userId}/projects/${projectId}/exec`, req.body);
        res.status(response.status).send(response.data);
    } catch (error) {
        console.error('Error executing project for user:', error.message);
        res.status(error.response?.status || 500).send({ error: error.message });
    }
});

// Route to fetch project details for a specific user
app.get('/users/:userId/projects/:projectId', async (req, res) => {
    const { userId, projectId } = req.params;

    try {
        // Forward the request to the backend service with userId and projectId
        const response = await axios.get(`${PROJECTS_BACKEND_URL}/users/${userId}/projects/${projectId}`);
        res.status(response.status).send(response.data);
    } catch (error) {
        console.error('Error fetching project for user:', error.message);
        res.status(error.response?.status || 500).send({ error: error.message });
    }
});

app.delete('/users/:userId/projects/:projectId', async (req, res) => {
    const { userId, projectId } = req.params;
    try {
        // Forward the request to the backend service with userId and projectId
        const response = await axios.delete(`${PROJECTS_BACKEND_URL}/users/${userId}/projects/${projectId}`);
        res.status(response.status).send(response.data);
    } catch (error) {
        console.error('Error deleting project for user:', error.message);
        res.status(error.response?.status || 500).send({ error: error.message });
    }
});

// Route to list all projects for a specific user
app.get('/users/:userId/projects', async (req, res) => {
    const { userId } = req.params;

    try {
        // Forward the request to the backend service with the userId
        const response = await axios.get(`${PROJECTS_BACKEND_URL}/users/${userId}/projects`);
        res.status(response.status).send(response.data);
    } catch (error) {
        console.error('Error listing projects for user:', error.message);
        console.error('Request:' + `${PROJECTS_BACKEND_URL}/users/${userId}/projects`);
        res.status(error.response?.status || 500).send({ error: error.message });
    }
});

// Route to list all projects
app.get('/projects', async (req, res) => {
    try {
        // Forward the request to the backend service
        const response = await axios.get(`${PROJECTS_BACKEND_URL}/projects`);
        res.status(response.status).send(response.data);
    } catch (error) {
        console.error('Error listing projects:', error.message);
        res.status(error.response?.status || 500).send({ error: error.message });
    }
});



// USERS

app.post('/users', async (req, res) => {

    console.log('Incoming request to /users:', req.body);
    try {

        // Forward the request to the backend service with the userId
        const response = await axios.post(`${USERS_BACKEND_URL}/users`, req.body);
        res.status(response.status).send(response.data);
    } catch (error) {
        console.error('Error creating user:', error.message);
        res.status(error.response?.status || 500).send({ error: error.message });
    }
});

app.put('/users/:userId', async (req, res) => {
    const { userId } = req.params;

    try {
        // Forward the request to the backend service with the userId and projectId
        const response = await axios.put(`${USERS_BACKEND_URL}/users/${userId}`, req.body);
        res.status(response.status).send(response.data);
    } catch (error) {
        console.error('Error updating user:', error.message);
        res.status(error.response?.status || 500).send({ error: error.message });
    }
});

app.get('/users/:userId', async (req, res) => {
    const { userId } = req.params;

    try {
        // Forward the request to the backend service with userId and projectId
        const response = await axios.get(`${USERS_BACKEND_URL}/users/${userId}`);
        res.status(response.status).send(response.data);
    } catch (error) {
        console.error('Error fetching project for user:', error.message);
        res.status(error.response?.status || 500).send({ error: error.message });
    }
});

app.get('/users', async (req, res) => {
    try {
        // Forward the request to the backend service with the userId
        const response = await axios.get(`${USERS_BACKEND_URL}/users`);
        res.status(response.status).send(response.data);
    } catch (error) {
        console.error('Error listing projects for user:', error.message);
        console.error('Request:' + `${USERS_BACKEND_URL}/users`);
        res.status(error.response?.status || 500).send({ error: error.message });
    }
});

app.post('/users/login', async (req, res) => {
    try {
        // Forward the request to the backend service with the userId
        const response = await axios.post(`${USERS_BACKEND_URL}/users/login`, req.body);
        res.status(response.status).send(response.data);
    } catch (error) {
        console.error('Error creating user:', error.message);
        res.status(error.response?.status || 500).send({ error: error.message });
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`API Gateway is running on port ${PORT}`);
});
