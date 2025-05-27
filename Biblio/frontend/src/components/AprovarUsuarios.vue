<template>
  <div class="painel">
    <router-link to="/acervo" class="btn-acervo">Ir para Acervo</router-link>

    <h2>Solicitações de Cadastro</h2>
    <div v-if="pendentes.length === 0" class="vazio-msg">Nenhum aluno pendente.</div>
    <div v-for="user in pendentes" :key="user._id" class="card">
      <p><strong>Nome:</strong> {{ user.nome }}</p>
      <p><strong>Email:</strong> {{ user.email }}</p>
      <div class="btn-group">
        <button @click="avaliar(user._id, true)" class="btn-aprovar">Aprovar</button>
        <button @click="avaliar(user._id, false)" class="btn-rejeitar">Rejeitar</button>
      </div>
    </div>

    <h2>Reservas Pendentes</h2>
    <div v-if="reservas.length === 0" class="vazio-msg">Nenhuma reserva pendente.</div>
    <div v-for="reserva in reservas" :key="reserva._id" class="card">
      <p><strong>Reserva ID:</strong> {{ reserva._id }}</p>
      <p><strong>Livro:</strong> {{ reserva.livro_nome }}</p>
      <p><strong>Aluno:</strong> {{ reserva.usuario_nome }}</p>
      <button @click="aprovarReserva(reserva._id)" class="btn-aprovar">Aprovar Reserva</button>
    </div>

    <button @click="logout" class="btn-sair">Sair</button>
  </div>
</template>

<script>
import axios from '../services/api'

export default {
  data() {
    return {
      pendentes: [],
      reservas: []
    }
  },
  async mounted() {
    await this.carregarUsuarios()
    await this.carregarReservas()
  },
  methods: {
    async carregarUsuarios() {
      const res = await axios.get('/usuarios/pendentes')
      this.pendentes = res.data
    },
    async avaliar(id, aprovar) {
      await axios.post(`/usuarios/avaliar/${id}`, { aprovar })
      this.carregarUsuarios()
    },
    async carregarReservas() {
      const res = await axios.get('/reservas/pendentes')
      this.reservas = res.data
    },
    async aprovarReserva(id) {
      await axios.post(`/reservas/aprovar/${id}`)
      this.carregarReservas()
    },
    logout() {
      localStorage.clear()
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.painel {
  max-width: 900px;
  margin: 60px auto 80px;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #203647;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}
h2 {
  margin-bottom: 20px;
  border-bottom: 2px solid #203647;
  padding-bottom: 6px;
  font-weight: 700;
}
.vazio-msg {
  font-style: italic;
  color: #7a8a99;
  margin-bottom: 25px;
  text-align: center;
}
.card {
  background: #f7f9fb;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 25px;
  box-shadow: 0 4px 15px rgba(32, 54, 71, 0.07);
  border: 1px solid #d4dbe0;
}
.card p {
  margin: 8px 0;
  font-weight: 600;
}
.btn-group {
  margin-top: 10px;
}
button {
  padding: 10px 18px;
  margin-right: 10px;
  border-radius: 8px;
  border: none;
  font-weight: 700;
  cursor: pointer;
  transition: background-color 0.3s ease;
  color: white;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.btn-aprovar {
  background-color: #e91e63;
}
.btn-aprovar:hover {
  background-color: #c2185b;
}
.btn-rejeitar {
  background-color: #9e9e9e;
}
.btn-rejeitar:hover {
  background-color: #7e7e7e;
}
.btn-sair {
  display: block;
  width: 150px;
  margin: 40px auto 0;
  background-color: #c2185b;
  font-weight: 700;
}
.btn-sair:hover {
  background-color: #e91e63;
}
.btn-acervo {
  display: inline-block;
  margin-bottom: 25px;
  padding: 12px 25px;
  background-color: #203647;
  color: white;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 700;
  transition: background-color 0.3s ease;
  cursor: pointer;
}
.btn-acervo:hover {
  background-color: #405968;
}
</style>
