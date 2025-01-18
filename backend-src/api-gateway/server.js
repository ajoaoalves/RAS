const express = require('express');
const axios = require('axios');
const cors = require('cors');

// Services for choosing routes, authentication, and rate limiting.
// const authRoutes = require('./routes/authRoutes');
// const serviceRoutes = require('./routes/serviceRoutes');
// const rateLimiter = require('./middlewares/rateLimiter');

// Configurations
const PORT = process.env.PORT || 8080;
const PROJECTS_BACKEND_URL = 'http://projects-api:18018/projects';
const STATIC_FILE_SERVER = '';

const app = express();

// Middlewares
app.use(express.json());
app.use(cors());

// Test endpoint
app.get('/', (req, res) => {
    res.send('API Gateway is running...');
});

// Route to create a new project
app.post('/projects', async (req, res) => {
    try {
        const response = await axios.post(`${PROJECTS_BACKEND_URL}`, req.body);
        res.status(response.status).send(response.data);
    } catch (error) {
        console.error('Error creating project:', error.message);
        res.status(error.response?.status || 500).send({ error: error.message });
    }
});

// Route to update a project
app.put('/projects/:projectId', async (req, res) => {
    const { projectId } = req.params;

    try {
        const response = await axios.put(`${PROJECTS_BACKEND_URL}/${projectId}`, req.body);
        res.status(response.status).send(response.data);
    } catch (error) {
        console.error('Error updating project:', error.message);
        res.status(error.response?.status || 500).send({ error: error.message });
    }
});

// Route to execute a project
app.put('/projects/:projectId/exec', async (req, res) => {
    const { projectId } = req.params;

    try {
        const response = await axios.put(`${PROJECTS_BACKEND_URL}/${projectId}/exec`, req.body);
        res.status(response.status).send(response.data);
    } catch (error) {
        console.error('Error running project:', error.message);
        res.status(error.response?.status || 500).send({ error: error.message });
    }
});

// Route to fetch project details
app.get('/projects/:projectId', async (req, res) => {
    const { projectId } = req.params;

    try {
        const response = await axios.get(`${PROJECTS_BACKEND_URL}/${projectId}`);
        res.status(response.status).send(response.data);
    } catch (error) {
        console.error('Error fetching project:', error.message);
        res.status(error.response?.status || 500).send({ error: error.message });
    }
});

// Route to list all projects
app.get('/projects', async (req, res) => {
    try {
        const response = await axios.get(`${PROJECTS_BACKEND_URL}`);
        res.status(response.status).send(response.data);
    } catch (error) {
        console.error('Error listing projects:', error.message);
        res.status(error.response?.status || 500).send({ error: error.message });
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`API Gateway is running on port ${PORT}`);
});
