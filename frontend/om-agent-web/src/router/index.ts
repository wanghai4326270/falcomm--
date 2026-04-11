import { createRouter, createWebHistory } from 'vue-router';

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'OmHome',
      component: () => import('@/views/om/OmAgentHome.vue'),
    },
  ],
});
