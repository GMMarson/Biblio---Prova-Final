<template>
  <div class="login-container">
    <h2>Login</h2>
    <p class="subtitulo">Digite os seus dados de acesso no campo abaixo.</p>
    <form @submit.prevent="login" class="form-login">
      <label for="email">E-mail</label>
      <input id="email" type="email" v-model="form.email" placeholder="Digite seu e-mail" required />
      
      <label for="senha">Senha</label>
      <input id="senha" type="password" v-model="form.senha" placeholder="Digite sua senha" required />
      
      <button type="submit">Acessar</button>
    </form>

    <p v-if="erro" class="erro">{{ erro }}</p>

    <hr />

    <h3>Criar conta</h3>
    <form @submit.prevent="registrar" class="form-cadastro">
      <label for="nome">Nome completo</label>
      <input id="nome" type="text" v-model="novo.nome" placeholder="Digite seu nome completo" required />
      
      <label for="emailNovo">E-mail</label>
      <input id="emailNovo" type="email" v-model="novo.email" placeholder="Digite seu e-mail" required />
      
      <label for="senhaNovo">Senha</label>
      <input id="senhaNovo" type="password" v-model="novo.senha" placeholder="Digite sua senha" required />
      
      <label for="tipo">Tipo de conta</label>
      <select id="tipo" v-model="novo.tipo" required>
        <option disabled value="">Selecione o tipo</option>
        <option value="aluno">Aluno</option>
        <option value="bibliotecario">Bibliotecário</option>
      </select>
      
      <button type="submit">Cadastrar</button>
    </form>

    <p v-if="msg" class="mensagem">{{ msg }}</p>
  </div>
</template>

<script>
import axios from '../services/api'

export default {
  data() {
    return {
      form: { email: '', senha: '' },
      novo: { nome: '', email: '', senha: '', tipo: '' },
      erro: '',
      msg: ''
    }
  },
  methods: {
    async login() {
      this.erro = ''
      try {
        const res = await axios.post('/login', this.form)
        localStorage.setItem('token', res.data.token)
        localStorage.setItem('user_id', res.data.user_id)
        localStorage.setItem('tipo', res.data.tipo)

        if (res.data.tipo === 'bibliotecario') {
          this.$router.push('/aprovar')
        } else {
          this.$router.push('/home')
        }
      } catch {
        this.erro = 'Credenciais inválidas.'
      }
    },
    async registrar() {
      this.msg = ''
      try {
        const endpoint = this.novo.tipo === 'bibliotecario' ? '/registro' : '/solicitar-cadastro'
        await axios.post(endpoint, this.novo)
        this.msg = this.novo.tipo === 'bibliotecario'
          ? 'Bibliotecário criado! Agora faça login.'
          : 'Cadastro solicitado! Aguarde aprovação.'
        this.novo = { nome: '', email: '', senha: '', tipo: '' }
      } catch {
        this.msg = 'Erro ao criar conta.'
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  max-width: 380px;
  margin: 100px auto;
  background: #fff;
  padding: 30px 35px;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #203647;
}
h2 {
  margin-bottom: 10px;
  font-weight: 700;
  font-size: 28px;
  text-align: center;
}
.subtitulo {
  font-size: 14px;
  color: #606c76;
  margin-bottom: 25px;
  text-align: center;
}
h3 {
  margin: 40px 0 20px;
  font-weight: 600;
  font-size: 20px;
  color: #203647;
  text-align: center;
}
label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
}
input, select {
  width: 100%;
  padding: 12px 14px;
  margin-bottom: 18px;
  border-radius: 6px;
  border: 1px solid #ced4da;
  font-size: 15px;
  color: #203647;
  background-color: #f8f9fa;
  transition: border-color 0.3s ease;
}
input::placeholder, select {
  color: #a1aebc;
}
input:focus, select:focus {
  border-color: #e91e63;
  outline: none;
  background-color: #fff;
}
button {
  width: 100%;
  padding: 14px 0;
  margin-top: 10px;
  background-color: #e91e63;
  color: white;
  font-weight: 700;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}
button:hover {
  background-color: #c2185b;
}
.erro {
  color: #d32f2f;
  font-weight: 600;
  margin-top: 15px;
  text-align: center;
}
.mensagem {
  color: #388e3c;
  font-weight: 600;
  margin-top: 15px;
  text-align: center;
}
hr {
  border: none;
  border-top: 1px solid #e0e0e0;
  margin: 40px 0;
}
</style>
