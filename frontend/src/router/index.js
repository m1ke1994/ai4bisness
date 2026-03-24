import { createRouter, createWebHistory } from 'vue-router'
import Home from '~/pages/Home.vue'
import Policy from '~/pages/Policy.vue'
import Terms from '~/pages/Terms.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
  },
  {
    path: '/policy',
    name: 'policy',
    component: Policy,
    alias: ['/privacy-policy'],
  },
  {
    path: '/terms',
    name: 'terms',
    component: Terms,
    alias: ['/public-offer', '/user-agreement'],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }

    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
      }
    }

    return { top: 0 }
  },
})

export default router
