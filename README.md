# Requisitos e Arquiteturas de Software

Este repositório contém a implementação do Minimum Viable Product (MVP) da plataforma de gestão e edição de imagens em projetos. O sistema permite criar e gerir projetos, carregar imagens, adicionar ferramentas de edição e processar imagens com essas ferramentas.

## Funcionalidades Implementadas

- Criar e listar Projetos.
- Carregar uma Imagem para um Projeto.
- Adicionar uma Ferramenta de edição a um Projeto.
- Pré-visualizar o resultado da aplicação das Ferramentas de edição à Imagem atualmente selecionada.
- Aplicar as Ferramentas de edição a todas as Imagens do Projeto.
- Descarregar os resultados produzidos.

## Tecnologias Utilizadas

- **Back-end**: Node.js
- **Front-end**: Vue
- **Base de Dados**: MongoDB
- **Armazenamento de Imagens**: AWS S3 \([MinIO](https://min.io/)\)
- **Processamento de Imagem**: Python

## Instalação e Configuração

### Dependências 

Must have docker and docker-compose plugin to run the App

[Docker Installation Guide](docs/docker_install.md)

### Passos para instalação

1. Fazer Clone do repositório:

   ```bash
   git clone https://github.com/ajoaoalves/RAS.git
   ```

2. Mude para a pasta src:

   ```bash
   cd RAS/src
   ```

3. Corra o [docker-compose.yaml](src/docker-compose.yml)

   ```bash
   docker compose up
   ```

4. Aceda à aplicação no browser:

   ```bash
   http://localhost:80  
   ```

## Estrutura do Projeto

```
/RAS
├── src/ 
│   ├── backend_src/     # Código-fonte do back-end
│   ├── cloud_src/       # Código-fonte do setup cloud
│   ├── frontend_src/    # Código-fonte do front-end
│   └── tools_src/       # Código-fonte das tools
├── docs/  # Documentação do projeto
├── test_images/  # Imagens para teste
└── README.md  # Este ficheiro
```

## TODO

Create S3 bucket automatically 
PNG input not working