<template>

  <div class="page">
        <h1>家電制御アプリ</h1>
          <h4> サーキュレータ制御 </h4>
         　　　 
        <p><input type="button" value="ON" class="btn-gradient-radius" @click="ciron()"></p>
        <p><input type="button" value="OFF" class="btn-gradient-radius" @click="ciroff()"></p>
        <p><input type="button" value="戻る" class="btn-gradient-radius"　@click="goNewTask()"></p>

  </div>
                       
</template>


<script>
// eslint-disable-next-line
/* eslint-disable */ 
import Vue from 'vue'
const consts = require('./constrdk')

export default {
  name: 'kaden',
  methods:{

    //GPIO出力をH信号に設定するpythonコードにアクセスする。
    ciron: function(){

        this.$axios.get('http://' + consts.urlz +'/on')
          .then(function(response){
            
           }.bind(this))  //Promise処理を行う場合は.bind(this)が必要
          .catch(function(error){  //バックエンドからエラーが返却された場合に行う処理について

            }.bind(this))

     },

    //GPIO出力をL信号に設定するpythonコードにアクセスする。
    ciroff:function(){

        //再生したい番組の日にちと時間のデータをバックエンドに転送する。
        this.$axios.get('http://' + consts.urlz +'/off')
          .then(function(response){
          
           }.bind(this))  //Promise処理を行う場合は.bind(this)が必要
          .catch(function(error){  //バックエンドからエラーが返却された場合に行う処理について

            }.bind(this))

     },

     //Radiko.vueに移動する
    goNewTask: function () {

      this.$router.push('radiko')   //Radiko.vueに移動する
    },
 
   },

 
  data: function(){
    return { 

        }  
    }
}
</script>


<style>
 


  .page {
    width: auto;
    max-width: 800px;
    margin: 0 auto;
    border: 5px solid #ccc;
    padding: 1em;
    background: white;
    border-radius: 1.5em;
  }
  #overlay{
    /*　要素を重ねた時の順番　*/
    z-index:1;
    /*　画面全体を覆う設定　*/
    position:fixed;
    top:0;
    left:0;
    width:100%;
    height:100%;
    background-color:rgba(0,0,0,0.2);    /*　rgb(0,0,0)は黒, a=0.2は透明度　*/
    /*　画面の中央に要素を表示させる設定　*/
    display: flex;
    align-items: center;
    justify-content: center;
  }
  #content{
    z-index:2;
    width:66%;    /*　overlay表示時の白画面が占める大きさ　*/
    padding: 1em;
    background:#fff;
  }
h4 {
  background: #b0dcfa; /*背景色*/
  padding: 0.5em;/*文字周りの余白*/
  color: white;/*文字を白に*/
  border-radius: 0.5em;/*角の丸み*/
}
 /*　ボタン　*/
.btn-gradient-radius {
  display: inline-block;
  padding: 7px 20px;
  border-radius: 25px;
  text-decoration: none;
  color: #FFF;
  background-image: linear-gradient(45deg, #FFC107 0%, #ff8b5f 100%);
  transition: .4s;
}
.btn-gradient-radius:hover {
  background-image: linear-gradient(45deg, #FFC107 0%, #f76a35 100%);
}

</style>
