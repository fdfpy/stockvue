// eslint-disable-next-line
/* eslint-disable */ 
import Vue from 'vue'
import Router from 'vue-router'
import Top from '@/components/Top'
import Chart from '@/components/Chart'

import Radiko from '@/components/Radiko'
import Otenki from '@/components/Otenki'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'top',
      component: Top
    },
    {
      path: '/chart/',
      name: 'chart',
      component: Chart
    },

    {
      path: '/radiko/',
      name: 'radiko',
      component: Radiko
    },
    {
      path: '/otenki/',
      name: 'otenki',
      component: Otenki
    },

  ]
})
