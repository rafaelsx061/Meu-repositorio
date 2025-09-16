# Meu-repositorio
# Desenvolvimento de Sistemas: Web, Desktop e Mobile

## 📌 Introdução
### 🎯 Objetivo
Este documento explica as diferenças entre os ambientes de desenvolvimento **Web**, **Desktop** e **Mobile**.  
Também apresenta nossos projetos práticos, desenvolvidos para exemplificar cada um dos ambientes.

### 💡 Importância
Entender esses ambientes é essencial para escolher a melhor tecnologia para cada projeto.  
No nosso repositório temos:
- 🌐 Um projeto **Django** para loja de roupas online (Web)
- 📱 Um projeto **Kivy** para cadastro e listagem de filmes (Mobile)

Esses exemplos mostram na prática como funcionam os conceitos de **front-end, back-end, banco de dados e navegação entre telas**.

---

## 📂 Projeto Web – Loja Online (Django)
Nosso repositório contém um **projeto web** feito em **Django**, que funciona como uma **loja online de roupas**.  
As principais funcionalidades implementadas são:

- 🛍️ **Tela da Loja** → Lista de produtos das marcas **Nike**, **Puma** e **Lacoste**  
- 🛒 **Carrinho de Compras** → Adicionar, remover e visualizar total de itens  
- 🔑 **Login/Cadastro** → Sistema de autenticação de usuários  
- 🗄️ **Banco de dados SQLite** → Armazena produtos e usuários  

Esse projeto mostra como o desenvolvimento web pode ser usado para criar **aplicativos de e-commerce completos**.

---

## 📂 Projeto Mobile – Lista de Filmes (Kivy)
Também desenvolvemos um **aplicativo Mobile** usando **Kivy**, focado em um CRUD simples de filmes.  
Ele possui duas telas principais:

- 🎬 **Tela de Cadastro** → Inputs para título, gênero e ano do filme, além de botão "Salvar"  
- 📋 **Tela de Lista** → Mostra todos os filmes já cadastrados na sessão  

Este projeto demonstra:
- Uso de **ScreenManager** para navegação entre telas  
- Persistência simples de dados (em memória ou SQLite)  
- Interface gráfica responsiva em Python  

---

## 🌐 Desenvolvimento Web – O que é?
O desenvolvimento web é a criação de sites e aplicativos que rodam no navegador.

### 🖋️ Principais linguagens e frameworks
- **HTML**, **CSS**, **JavaScript**
- **Frameworks:** Django (nosso projeto), React, Angular, Vue.js

### 🛠️ Ferramentas usadas
- Visual Studio Code
- Navegadores (Chrome, Firefox)
- Git/GitHub

### 📌 Exemplos de projetos
- E-commerce (Amazon, Shopee)
- Aplicativos como Trello, Google Docs
- **Nosso projeto de Loja Online em Django**

### ✅ Vantagens e ❌ Limitações
**Vantagens:** Acessível em qualquer dispositivo, fácil de atualizar, não precisa instalar.  
**Limitações:** Depende da internet, pode ter problemas de compatibilidade entre navegadores.

---

## 🖥️ Desenvolvimento Desktop – O que é?
São programas que rodam no computador, direto no sistema operacional.

### 🖋️ Linguagens comuns
- C#, Java, Python, C++

### 🛠️ IDEs usados
- Visual Studio, Eclipse, IntelliJ, PyCharm

### 📌 Exemplos de uso
- Microsoft Word, Excel
- Adobe Photoshop
- VLC Media Player

### ✅ Vantagens e ❌ Limitações
**Vantagens:** Funciona offline, melhor desempenho.  
**Limitações:** Precisa instalar em cada computador, pode depender do sistema operacional.

---

## 📱 Desenvolvimento Mobile – O que é?
É o desenvolvimento de aplicativos para smartphones e tablets.

### 🔄 Diferenças
- **Nativo:** Feito para uma plataforma específica (Android ou iOS)
- **Híbrido:** Usa tecnologias web dentro de um contêiner
- **PWA:** Site que funciona como app instalado

### 🛠️ Ferramentas/Frameworks
- Flutter, React Native
- **Kivy (nosso projeto)**
- Android Studio, Xcode

### 📌 Exemplos práticos
- WhatsApp
- Instagram
- Uber
- **Nosso app de Lista de Filmes**

### ✅ Vantagens e ❌ Limitações
**Vantagens:** Integração com recursos do aparelho (GPS, câmera), notificações push.  
**Limitações:** Precisa passar pelas lojas de apps, custo maior para desenvolver apps nativos.

---

## 📊 Comparação Web, Desktop e Mobile

| Aspecto                | Web 🌐              | Desktop 🖥️           | Mobile 📱          |
|----------------------|------------------|-------------------|----------------|
| Instalação           | Não precisa      | Necessária        | Instalação do APK ou via loja |
| Acesso Offline       | Limitado         | Completo          | Completo |
| Atualizações         | Automáticas      | Manual            | Requer atualizar app |
| Performance          | Média           | Alta             | Média |
| Compatibilidade      | Todos os navegadores | Depende do SO | Depende da plataforma |

---

Com iniciar os projetos:
Agora vou ensinar o passo a passo de como rodar os projetos

📌 Python:
Instale o Python:
pip install Python

Criar e ativar um ambiente virtual:
python -m venv .venv
.\.venv\Scripts\activate

Se for no macOS/Linux fica:
python3 -m venv .venv
source .venv/bin/activate

📌 Django:
Rodar o projeto Django que é o Web:

Instale o django:
pip install django

Criar projeto/app:
django-admin startproject loja
cd loja
python manage.py startapp catalog

📌 Kivy:
Rodar o projeto Kivy:

Navegue até a pasta do seu projeto Kivy:
cd caminho/para/seu/projeto

Ativar o ambiente virtual: 
.\.venv\Scripts\activate

Instale o kivy:
pip install kivy

Criar um arquivo: 
Main.py
Depois disso você já pode criar seu código, primeiro importando as funções já.
Ex: From kivy.app import App
From kivy.uix.button import Button









