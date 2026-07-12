import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue'),
    },
    {
      path: '/pals',
      name: 'pals',
      component: () => import('../views/PalListView.vue'),
    },
    {
      path: '/pal/:id',
      name: 'pal-detail',
      component: () => import('../views/PalDetailView.vue'),
    },
  ],
})

export default router