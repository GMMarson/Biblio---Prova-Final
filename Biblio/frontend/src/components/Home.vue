<template>
  <div class="home">
    <h1>Bem-vindo à Biblioteca</h1>
    <p>Olá, {{ nome }}!</p>

    <div class="menu-botoes">
      <router-link to="/acervo"><button>Ver Acervo</button></router-link>
      <router-link to="/reservas"><button>Minhas Reservas</button></router-link>
      <router-link to="/perfil"><button>Perfil</button></router-link>
    </div>

    <button @click="logout" class="btn-sair">Sair</button>
  </div>
</template>

<script>
import axios from '../services/api'

export default {
  data() {
    return {
      nome: ''
    }
  },
  async mounted() {
    try {
      const id = localStorage.getItem('user_id')
      const res = await axios.get(`/usuarios/${id}`)
      this.nome = res.data.nome
    } catch {
      this.nome = 'Usuário'
    }
  },
  methods: {
    logout() {
      localStorage.clear()
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.home {
  max-width: 600px;
  margin: 80px auto 100px;
  text-align: center;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #203647;
}
h1 {
  font-weight: 700;
  margin-bottom: 20px;
  font-size: 2.4rem;
}
p {
  font-size: 1.2rem;
  margin-bottom: 40px;
  color: #586e75;
}
.menu-botoes {
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 300px;
  margin: 0 auto 50px;
}
button {
  padding: 14px 0;
  font-size: 18px;
  border-radius: 10px;
  border: none;
  background-color: #2c3e50;
  color: white;
  font-weight: 700;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 100%;
  min-width: 180px;
  text-align: center;
}
button:hover {
  background-color: #34495e;
}
.btn-sair {
  background-color: #c2185b;
  max-width: 300px;
  margin: 0 auto;
  display: block;
  transition: background-color 0.3s ease;
}
.btn-sair:hover {
  background-color: #e91e63;
}
</style>
