import { createRouter, createWebHistory } from 'vue-router'

import Login from '../components/Login.vue'
import Home from '../components/Home.vue'
import Perfil from '../components/Perfil.vue'
import Acervo from '../components/Acervo.vue'
import Reservas from '../components/Reservas.vue'
import AprovarUsuarios from '../components/AprovarUsuarios.vue'

const routes = [
  { path: '/', component: Login },
  { path: '/home', component: Home },
  { path: '/perfil', component: Perfil },
  { path: '/acervo', component: Acervo },
  { path: '/reservas', component: Reservas },
  { path: '/aprovar', component: AprovarUsuarios },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router