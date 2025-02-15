# Docker Installation Steps for Ubuntu Server 24.04.1

## 1. Update System Packages

Update your existing package list and upgrade installed packages:

```bash
sudo apt update && sudo apt upgrade -y
```

## 2. Install Required Dependencies

Install necessary packages for Docker installation:

```bash
sudo apt install -y ca-certificates curl gnupg software-properties-common
```

## 3. Add Docker's GPG Key

Add Docker's official GPG key to ensure package integrity:

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

## 4. Set Up Docker Repository

Add the Docker repository to APT sources:

```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list
```

## 5. Update Package List

Update APT package list with Docker packages:

```bash
sudo apt update
```

## 6. Install Docker

Install Docker Engine and required components:

```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## 7. Verify Installation

Check Docker installation and version:

```bash
sudo docker --version
```

## 8. Check Docker Service

Verify that the Docker service is running:

```bash
sudo systemctl status docker
```

## 9. Configure User Permissions

Add your user to the docker group (optional but recommended):

```bash
sudo usermod -aG docker $USER
```

**Note:** Log out and log back in for these changes to take effect.

## 10. Test Docker Installation

Run a test container:

```bash
docker run hello-world
```

# Additional Configuration

## Enable Docker on Boot

Configure Docker to start automatically on system boot:

```bash
sudo systemctl enable docker
```

## Verify Docker Compose

Check Docker Compose installation:

```bash
docker compose version
```

# Uninstall Instructions

If you need to remove Docker, follow these steps:

1. Remove Docker packages:

```bash
sudo apt remove docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

2. Remove Docker data directories:

```bash
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
```

# Troubleshooting

If you encounter permission errors when running Docker commands:

1. Ensure you've added your user to the docker group
2. Log out and log back in
3. If issues persist, you can run Docker commands with `sudo`

# Useful Docker Commands

- Check Docker system info:

  ```bash
  docker info
  ```

- List running containers:

  ```bash
  docker ps
  ```

- List all containers:

  ```bash
  docker ps -a
  ```

- List Docker images:

  ```bash
  docker images
  ```

- Pull an image:

  ```bash
  docker pull [image-name]
  ```

- Stop a container:

  ```bash
  docker stop [container-id]
  ```

- Remove a container:

  ```bash
  docker rm [container-id]
  ```

# Additional Resources

[Official Docker Documentation](https://docs.docker.com/)

[Docker Hub](https://hub.docker.com/)

[Docker Compose Documentation](https://docs.docker.com/compose/)

