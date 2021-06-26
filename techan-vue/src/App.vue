<template>
  <div id="app">


  
    <router-view></router-view>
 </div>


</template>

<script>
// eslint-disable-next-line
/* eslint-disable */ 
import Top from '/home/techan-vue/src/components/Top.vue'
export default {
  name: 'app',
  components:{
    Top
  },
    data() {
        return {
            mes: 'Hello Vue3!!'
        }
    }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>