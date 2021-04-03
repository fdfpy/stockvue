// eslint-disable-next-line to ignore the next line.
/* eslint-disable */ 
import * as types from '../mutation-types'
import Vue from 'vue'
import Vuex from 'vuex'
//import fs from  '/home/node_modules/fs'


Vue.use(Vuex)

const state = {
  meigara_num: 1570,
  today: '',
  dif:'',
  c_name:'',
  sigval:'',
  eps:'',
  tenkan:'',
  kagenchi:'',
  confval:'',
  coeff:'', 
  sta:'',
  ar:'',
  sar:'',
}

  
const getters = {
  MEIGARA_NUM: state => state.meigara_num,
  TODAY: state => state.today,
  DIF: state => state.dif,
  C_NAME: state => state.c_name,
  SIGVAL:state => state.sigval,
  EPS:state => state.eps,
  TENKAN:state => state.tenkan,
  KAGENCHI:state => state.kagenchi,
  CONFVAL:state => state.confval,
  COEFF:state => state.coeff,
  STA:state => state.sta,
  AR:state => state.ar,
  SAR:state => state.sar,
}

// actions
const actions = {

  update_DATA ({dispatch,commit},value) {
     
    commit(types.MEIGARA_NUM, value)

    },

  update_TODAY ({dispatch,commit},value) {
     
      commit(types.TODAY, value)
  
    },

  update_DIF ({dispatch,commit},value) {
     
      commit(types.DIF, value)
  
  },

  update_CNAME ({dispatch,commit},value) {
     
    commit(types.C_NAME, value)

},

update_SIGVAL ({dispatch,commit},value) {
     
  commit(types.SIGVAL, value)

},

update_EPS ({dispatch,commit},value) {
     
  commit(types.EPS, value)

},

update_TENKAN ({dispatch,commit},value) {
     
  commit(types.TENKAN, value)

},

update_KAGENCHI ({dispatch,commit},value) {
     
  commit(types.KAGENCHI, value)

},

update_CONFVAL ({dispatch,commit},value) {
     
  commit(types.CONFVAL, value)

},

update_COEFF ({dispatch,commit},value) {
     
  commit(types.COEFF, value)
},

update_STA ({dispatch,commit},value) {
     
  commit(types.STA, value)
},

update_AR ({dispatch,commit},value) {
     
  commit(types.AR, value)
},

update_SAR ({dispatch,commit},value) {
     
  commit(types.SAR, value)
},


}

// mutations
const mutations = {

  [types.MEIGARA_NUM](state, data){
   state.meigara_num = data
  },

  [types.TODAY](state, data){
    state.today = data
   },

  [types.DIF](state, data){
    state.dif = data
   },

  [types.C_NAME](state, data){
    state.c_name = data
   },

   [types.SIGVAL](state, data){
    state.sigval = data
   },

   [types.EPS](state, data){
    state.eps = data
   },

   [types.TENKAN](state, data){
    state.tenkan = data
   },

   [types.KAGENCHI](state, data){
    state.kagenchi = data
   },

   [types.CONFVAL](state, data){
    state.confval = data
   },

   [types.COEFF](state, data){
    state.coeff = data
   },

   [types.STA](state, data){
    state.sta = data
   },

   [types.AR](state, data){
    state.ar = data
   },

   [types.SAR](state, data){
    state.sar = data
   },


}
  
  export default {
    state,
    getters,
    actions,
    mutations
  }