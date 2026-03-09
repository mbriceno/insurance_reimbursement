import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router';
import { useAuthStore } from '../store/auth';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('../layouts/PublicLayout.vue'),
    children: [
      {
        path: '',
        redirect: '/login',
      },
      {
        path: 'login',
        name: 'login',
        component: () => import('../pages/LoginView.vue'),
        meta: { public: true },
      },
      {
        path: 'register',
        name: 'register',
        component: () => import('../pages/RegisterView.vue'),
        meta: { public: true },
      },
    ],
  },
  {
    path: '/',
    component: () => import('../layouts/AppLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: 'pets',
        name: 'pets',
        component: () => import('../pages/PetsListView.vue'),
      },
      {
        path: 'pets/:id',
        name: 'pet-detail',
        component: () => import('../pages/PetDetailView.vue'),
      },
      {
        path: 'insurance/create',
        name: 'insurance-create',
        component: () => import('../pages/InsuranceCreateView.vue'),
      },
      {
        path: 'claims/submit',
        name: 'claims-submit',
        component: () => import('../pages/ClaimSubmissionView.vue'),
      },
      {
        path: 'admin',
        name: 'admin-dashboard',
        component: () => import('../pages/AdminDashboard.vue'),
        meta: { requiresAdmin: true },
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();

  const hasToken = !!localStorage.getItem('access_token');
  const isAuthenticated = authStore.isAuthenticated || hasToken;
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
  } else if (to.meta.requiresAdmin && authStore.user?.role !== 'ADMIN') {
    next('/pets');
  } else if (to.meta.public && isAuthenticated) {
    next('/pets');
  } else {
    next();
  }
});

export default router;
