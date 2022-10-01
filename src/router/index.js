import { createRouter, createWebHistory } from 'vue-router'
import Landing from '../views/Landing.vue'
import Report from '../views/Report.vue'
import About from '../views/About.vue'
import Contact from '../views/Contact.vue'
import Home from '../views/Home.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: Landing
    },
    {
      path:'/about',
      name: 'about', 
      component: About 
    }, 
    {
      path:'/contact',
      name: 'contact', 
      component: Contact
    },
    {
      path:'/home',
      name: 'home', 
      component: Home
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/Dashboard.vue')
    },
    {
      path:'/report',
      name: 'report', 
      component: Report
    }
  ]
})

export default router
