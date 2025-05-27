# Biblioteca Online – COM759

Aplicação web para gerenciamento de biblioteca com cadastro e login de usuários, gerenciamento de livros, reservas com QR code e diferentes perfis de usuário (aluno e bibliotecário).

## Funcionalidades

- Cadastro e login de usuários com autenticação JWT
- Aprovação manual de alunos pelo bibliotecário
- CRUD completo de livros pelo bibliotecário
- Reserva de livros pelos alunos, com geração de QR code após aprovação
- Telas separadas para alunos e bibliotecários
- Interface moderna e responsiva desenvolvida em Vue.js

## Tecnologias Utilizadas

- Frontend: Vue 3 (build estático via Vite)
- Backend: Flask, PyMongo, Flask-JWT-Extended
- Banco de Dados: MongoDB Atlas

## Instalação e Uso

### Backend

1. Acesse a pasta `backend/`
2. Crie e ative o ambiente virtual
3. Instale as dependências:

   pip install -r requirements.txt

4. Verifique se a pasta `frontend_dist/` está presente

5. Execute o backend:

   python run.py

6. Acesse no navegador: [http://localhost:5000]

## Usuários de Teste

| Tipo          | Email                      | Senha    |
| ------------- | -------------------------- | -------- |
| Bibliotecário | [admin@biblioteca.com]     | admin123 |
| Aluno         | [aluno@teste.com]          | aluno123 |