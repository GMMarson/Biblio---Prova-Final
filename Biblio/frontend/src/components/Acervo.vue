<template>
  <div class="acervo">
    <router-link v-if="tipo === 'aluno'" to="/home" class="btn-voltar">
      Voltar ao menu
    </router-link>
    <router-link v-else to="/aprovar" class="btn-voltar">
      Voltar ao menu
    </router-link>

    <h2>Acervo da Biblioteca</h2>

    <div v-if="tipo === 'bibliotecario'" class="formulario">
      <h3>Adicionar Livro</h3>
      <form @submit.prevent="adicionarLivro" class="form-livro">
        <input v-model="novo.titulo" placeholder="Título" required />
        <input v-model="novo.autor" placeholder="Autor" required />
        <input v-model="novo.ano" placeholder="Ano" required />
        <input v-model="novo.genero" placeholder="Gênero" required />
        <input v-model.number="novo.quantidade" placeholder="Quantidade" min="1" required />
        <button type="submit">Cadastrar Livro</button>
      </form>
    </div>

    <div v-if="livros.length === 0" class="sem-livros">
      Nenhum livro disponível.
    </div>

    <div v-for="livro in livros" :key="livro._id" class="livro-card">
      <h3>{{ livro.titulo }}</h3>
      <p><strong>Autor:</strong> {{ livro.autor }}</p>
      <p><strong>Gênero:</strong> {{ livro.genero }}</p>
      <p><strong>Ano:</strong> {{ livro.ano }}</p>
      <p><strong>Quantidade:</strong> {{ livro.quantidade }}</p>

      <div v-if="tipo === 'aluno'">
        <button @click="reservar(livro._id)">Reservar</button>
      </div>
      <div v-else>
        <button @click="deletarLivro(livro._id)">Excluir Livro</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '../services/api'

export default {
  data() {
    return {
      livros: [],
      tipo: localStorage.getItem('tipo'),
      novo: {
        titulo: '',
        autor: '',
        ano: '',
        genero: '',
        quantidade: 1
      }
    }
  },
  async mounted() {
    await this.carregarLivros()
  },
  methods: {
    async carregarLivros() {
      try {
        const res = await axios.get('/livros')
        this.livros = res.data
      } catch {
        alert('Erro ao carregar livros.')
      }
    },
    async reservar(livro_id) {
      try {
        await axios.post('/reservas', { livro_id })
        alert('Reserva solicitada!')
      } catch {
        alert('Erro ao reservar.')
      }
    },
    async adicionarLivro() {
      try {
        await axios.post('/livros', this.novo)
        this.novo = { titulo: '', autor: '', ano: '', genero: '', quantidade: 1 }
        await this.carregarLivros()
        alert('Livro cadastrado!')
      } catch {
        alert('Erro ao cadastrar livro.')
      }
    },
    async deletarLivro(id) {
      if (confirm('Deseja mesmo excluir este livro?')) {
        try {
          await axios.delete(`/livros/${id}`)
          await this.carregarLivros()
          alert('Livro excluído.')
        } catch {
          alert('Erro ao excluir livro.')
        }
      }
    }
  }
}
</script>

<style scoped>
.acervo {
  max-width: 900px;
  margin: 50px auto 80px;
  padding: 0 15px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #203647;
}
h2 {
  color: #203647;
  margin-bottom: 30px;
  text-align: center;
  font-weight: 700;
}
.formulario {
  background: #fff;
  padding: 25px 20px;
  margin-bottom: 40px;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(32, 54, 71, 0.12);
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}
.form-livro input {
  padding: 14px;
  margin-bottom: 18px;
  border: 1px solid #ccd6dd;
  border-radius: 8px;
  font-size: 15px;
  width: 100%;
  color: #203647;
  background-color: #f8f9fa;
}
.form-livro input::placeholder {
  color: #94a3b8;
}
.form-livro button {
  width: 100%;
  background-color: #e91e63;
  color: white;
  border: none;
  padding: 16px;
  font-weight: 700;
  border-radius: 12px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.form-livro button:hover {
  background-color: #c2185b;
}
.sem-livros {
  text-align: center;
  font-style: italic;
  color: #7a8a99;
  margin-bottom: 30px;
}
.livro-card {
  background: #fff;
  padding: 25px 20px;
  border-radius: 12px;
  margin-bottom: 25px;
  box-shadow: 0 8px 20px rgba(32, 54, 71, 0.12);
  border: 1px solid #ccd6dd;
}
.livro-card h3 {
  margin-bottom: 10px;
  color: #203647;
}
.livro-card p {
  margin: 6px 0;
  font-weight: 600;
}
button {
  background-color: #e91e63;
  color: white;
  border: none;
  padding: 14px 20px;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 15px;
}
button:hover {
  background-color: #c2185b;
}
.btn-voltar {
  display: inline-block;
  margin-top: 35px;
  padding: 12px 30px;
  background-color: #34495e;
  color: white;
  border-radius: 10px;
  text-decoration: none;
  font-weight: 600;
  transition: background-color 0.3s ease;
  text-align: center;
}
.btn-voltar:hover {
  background-color: #203647;
}
</style>
