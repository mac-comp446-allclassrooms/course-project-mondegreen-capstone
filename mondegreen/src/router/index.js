import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SongView from '../views/StatsView.vue'
import HowToView from '../views/HowToView.vue'
import GameView from '../views/GameView.vue'

// routes for the app
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/game',
      name: 'game',
      component: GameView,
    },
    {
      path: '/user',
      name: 'user',
      component: SongView,
    },
    {
      path: '/howto',
      name: 'howto',
      component: HowToView,
    },
  ],
})

export default router
