<template>
  <div class="perfil">
    <router-link to="/home" class="btn-voltar">Voltar ao menu</router-link>

    <h2>Meu Perfil</h2>

    <form @submit.prevent="atualizar" class="form-perfil">
      <label for="nome">Nome:</label>
      <input id="nome" v-model="usuario.nome" required />

      <label for="email">Email:</label>
      <input id="email" type="email" v-model="usuario.email" required />

      <label for="senha">Senha:</label>
      <input id="senha" type="password" v-model="usuario.senha" placeholder="Nova senha (opcional)" />

      <button type="submit">Atualizar</button>
    </form>

    <p v-if="msg" class="mensagem">{{ msg }}</p>
  </div>
</template>

<script>
import axios from '../services/api'

export default {
  data() {
    return {
      usuario: {
        nome: '',
        email: '',
        senha: ''
      },
      msg: ''
    }
  },
  async mounted() {
    try {
      const id = localStorage.getItem('user_id')
      const res = await axios.get(`/usuarios/${id}`)
      this.usuario.nome = res.data.nome
      this.usuario.email = res.data.email
    } catch {
      this.usuario.nome = ''
      this.usuario.email = ''
    }
  },
  methods: {
    async atualizar() {
      try {
        const id = localStorage.getItem('user_id')
        const payload = {
          nome: this.usuario.nome,
          email: this.usuario.email
        }
        if (this.usuario.senha) payload.senha = this.usuario.senha

        await axios.put(`/usuarios/${id}`, payload)
        this.msg = 'Dados atualizados com sucesso.'
      } catch {
        this.msg = 'Erro ao atualizar dados.'
      }
    }
  }
}
</script>

<style scoped>
.perfil {
  max-width: 600px;
  margin: 60px auto 80px;
  padding: 30px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(32, 54, 71, 0.12);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #203647;
}
h2 {
  text-align: center;
  margin-bottom: 25px;
  font-weight: 700;
  font-size: 1.8rem;
}
label {
  display: block;
  margin-top: 20px;
  font-weight: 600;
  font-size: 1rem;
  color: #34495e;
}
input {
  width: 100%;
  padding: 14px;
  margin-top: 8px;
  margin-bottom: 15px;
  border-radius: 8px;
  border: 1px solid #ccd6dd;
  font-size: 1rem;
  color: #203647;
  background-color: #f8f9fa;
}
button {
  width: 100%;
  margin-top: 20px;
  padding: 16px;
  background-color: #e91e63;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
button:hover {
  background-color: #c2185b;
}
.mensagem {
  margin-top: 20px;
  font-weight: 700;
  color: #27ae60;
  text-align: center;
  font-size: 1rem;
}
.btn-voltar {
  display: inline-block;
  margin-bottom: 30px;
  padding: 12px 25px;
  background-color: #34495e;
  color: white;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}
.btn-voltar:hover {
  background-color: #203647;
}
</style>
