import { createRouter, createWebHistory } from 'vue-router'
import LoadingView from '../views/LoadingView.vue'
import AboutView from '../views/AboutView.vue'
import LoginView from '../views/LoginView.vue'
import RecipesView from '../views/RecipesView.vue'
import NotFoundView from '../views/404View.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: LoadingView
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView
    }, 
    {
      path: '/login',
      name: 'login',
      component: LoginView
    }, 
    {
      path: '/recipes',
      name: 'recipes',
      component: RecipesView
    }, {
      path: '/:pathMatch(.*)*',
      component: NotFoundView
    }
  ]
})

export default router
