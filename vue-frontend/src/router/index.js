import { createRouter, createWebHistory } from 'vue-router'
import LoadingView from '../views/LoadingView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: LoadingView
    }
  ]
})

export default router
