// eslint-disable-next-line
/* eslint-disable */ 
// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios' 
import store from './store'



Vue.config.productionTip = false
Vue.prototype.$axios = axios
//export const eventBus = new Vue();
/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  template: '<App/>',
  components: { App },
})