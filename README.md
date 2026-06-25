# 🎬 StreamPy — Plataforma de streaming (similar à Netflix)

<img width="2752" height="1536" alt="crie_uma_thumbnail_para_meu_202606250734" src="https://github.com/user-attachments/assets/9465ec52-06af-4471-8db5-1d150923dd4a" />

Sistema de streaming de vídeos inspirado em plataformas como Netflix, desenvolvido em Python.
O projeto simula funcionalidades essenciais de uma plataforma moderna de mídia, com foco em arquitetura backend, organização de conteúdo e experiência do usuário.

---

# Visão Geral

## O StreamPy é um aplicativo web que permite:

Navegação por catálogo de vídeos

<img width="1366" height="733" alt="Screenshot_2026-06-22_20-36-55" src="https://github.com/user-attachments/assets/2ee0cc26-9567-4b0d-8621-00b1c434c617" />


Sistema de categorias (ex: ação, drama, documentário)

---

<img width="1366" height="733" alt="Screenshot_2026-06-22_20-34-56" src="https://github.com/user-attachments/assets/a45c5737-58fc-42ae-802f-244b0bba8051" />


Página de reprodução de vídeo

---

<img width="1366" height="733" alt="Screenshot_2026-06-22_20-35-29" src="https://github.com/user-attachments/assets/99c9c44f-74e6-4078-a76d-82638bb4d085" />


Sistema de usuários (login/autenticação)

---

<img width="1366" height="733" alt="Screenshot_2026-06-22_20-37-12" src="https://github.com/user-attachments/assets/4f94c30e-9200-43ad-8587-99f1539c6173" />


Interface simples inspirada em plataformas de streaming

---

<img width="1366" height="733" alt="Screenshot_2026-06-22_20-35-59" src="https://github.com/user-attachments/assets/521317bc-1e85-48ef-81d0-37fe0f3e85ef" />


## O objetivo principal é demonstrar domínio de backend, organização de dados e estruturação de aplicações escaláveis.

---

## O projeto segue uma estrutura modular:

* app.py→ ponto de entrada da aplicação/.
* routes/→ rotas da aplicação (auth, vídeos, catálogo)
* models/→ modelos de dados (usuários, vídeos, categorias)
* database/→ configuração do banco de dados
* templates/→ interface (HTML se aplicável)
* static/→ recursos (CSS, JS, imagens)

---

## Tecnologias Utilizadas

* Python 3.x
* Flask (ou Django, ajuste aqui)
* SQLAlchemy
* SQLite / PostgreSQL
* HTML5 / CSS3 (caso front-end simples)
* Jinja2 (se Frasco)

---

# Instalação

## Clone o repositório:

git clone https://github.com/jdevc9/streampy.git
cd streampy

## Crie um ambiente virtual:

python -m venv venv

# Ative o ambiente:

## Windows

venv\Scripts\activate

## Linux / Mac

source venv/bin/activate

## Instale as dependências:

pip install -r requirements.txt

## Execute o projeto:

python app.py

--

# Funcionalidades

* Registro e login de usuários
* Sessões autenticadas
* Catálogo dinâmico de vídeos
* Sistema de categorias
* Página de reprodução
* Estrutura preparada para API futura

# Objetivo Técnico

## Este projeto foi construído com foco em:

* Organização de código escalável
* Separação de responsabilidades (routes, models, services)
* Boas práticas de backend
* Preparação para expansão (API, microserviços, etc.)

## Possíveis melhorias futuras

* Sistema de recomendação por algoritmo
* Upload de vídeos por usuários
* API REST completa
* Frontend React/Vue
* Streaming real com HLS
* Painel administrativo

# Observações

Este projeto não utiliza streaming real em tempo de produção.
O foco está na simulação da arquitetura de uma plataforma de streaming.

---

