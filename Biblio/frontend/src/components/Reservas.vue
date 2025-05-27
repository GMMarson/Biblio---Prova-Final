<template>
  <div class="reservas">
    <router-link to="/home" class="btn-voltar">Voltar ao menu</router-link>

    <h2>Minhas Reservas</h2>

    <div v-if="reservas.length === 0" class="sem-reservas">
      Nenhuma reserva encontrada.
    </div>

    <div v-for="reserva in reservas" :key="reserva._id" class="reserva-card">
      <p><strong>Livro:</strong> {{ reserva.livro_nome || reserva.livro_id }}</p>
      <p><strong>Status:</strong>
        <span :class="{'aprovada': reserva.aprovada, 'pendente': !reserva.aprovada}">
          {{ reserva.aprovada ? 'Aprovada' : 'Pendente' }}
        </span>
      </p>
      <div v-if="reserva.aprovada && qrCodes[reserva._id]">
        <img :src="qrCodes[reserva._id]" alt="QR Code" class="qrcode" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from '../services/api'

export default {
  data() {
    return {
      reservas: [],
      qrCodes: {}
    }
  },
  async mounted() {
    try {
      const res = await axios.get('/minhas-reservas')
      this.reservas = res.data

      for (const reserva of this.reservas) {
        if (reserva.aprovada) {
          try {
            const response = await axios.get(`/reservas/qrcode/${reserva._id}`, {
              responseType: 'blob'
            })
            const url = URL.createObjectURL(response.data)
            this.qrCodes[reserva._id] = url
          } catch (error) {
            console.error('Erro ao carregar QR code:', error)
          }
        }
      }
    } catch {
      this.reservas = []
    }
  }
}
</script>

<style scoped>
.reservas {
  max-width: 800px;
  margin: 60px auto 80px;
  padding: 0 15px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #203647;
}
h2 {
  color: #203647;
  margin-bottom: 25px;
  text-align: center;
  font-weight: 700;
  font-size: 2rem;
}
.sem-reservas {
  text-align: center;
  font-style: italic;
  color: #7a8a99;
  margin-bottom: 30px;
}
.reserva-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 25px;
  box-shadow: 0 8px 20px rgba(32, 54, 71, 0.12);
  border: 1px solid #ccd6dd;
}
.reserva-card p {
  margin: 8px 0;
  font-weight: 600;
}
.aprovada {
  color: #27ae60;
}
.pendente {
  color: #e67e22;
}
.qrcode {
  margin-top: 15px;
  width: 120px;
  height: 120px;
  border-radius: 12px;
  border: 1px solid #ccd6dd;
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
  transition: background-color 0.3s ease;
  cursor: pointer;
}
.btn-voltar:hover {
  background-color: #203647;
}
</style>
