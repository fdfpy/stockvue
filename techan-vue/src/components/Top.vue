<template>



  <div class=page>



    <h1>株式投資アプリver0.27</h1>
   
       <h4>  <font size="6"> 状態 :{{ $data.result }} </font> </h4>
       <!--
        <div class="float_test150">
           <p><font size="3" color="#000000" face="Meiryo"> 米国10年金利(%) </font></p>
           <p><font size="8" color="#000000" face="Meiryo"> <a href='https://m.finance.yahoo.co.jp/stock?code=%5ETNX&d=1w' target="_blank"> {{ Math.round(100*$data.kakusyudat_matrix.yield10)/100 }} </a></font></p>
           <p><font v-if="$data.kakusyudat_matrix.yield10_delta>=0" color="green" size="4" face="Meiryo"> (前日差 :{{ Math.round(100*$data.kakusyudat_matrix.yield10_delta)/100 }} )</font></p>
           <p><font v-if="$data.kakusyudat_matrix.yield10_delta<0" color="red" size="4" face="Meiryo" > (前日差 :{{ Math.round(100*$data.kakusyudat_matrix.yield10_delta)/100 }} )</font></p>            
        </div>
       -->


        <div class="float_test150">
           <p><font size="3" color="#000000" face="Meiryo"> VIX指数 </font></p>
           <p><font size="8" color="#000000" face="Meiryo"> <a v-on:click="goNewTask($data.datlen-1)"> {{ Math.round(100*$data.vix)/100 }} </a></font></p>
           <p><font v-if="$data.vixdif>=0" color="green" size="4" face="Meiryo"> (前日差 :{{ Math.round(100*$data.vixdif)/100 }} )</font></p>
           <p><font v-if="$data.vixdif<0" color="red" size="4" face="Meiryo"> (前日差 :{{ Math.round(100*$data.vixdif)/100 }} )</font></p>           
        </div>
        <div class="float_test150">
           <p><font size="3" color="#000000" face="Meiryo"> 原油($) </font></p>
           <p><font size="8" color="#000000" face="Meiryo"> <a v-on:click="goNewTask($data.datlen-5)"> {{ Math.round(100*$data.genyu)/100 }} </a></font></p>
           <p><font v-if="$data.genyudif>=0" color="green" size="4" face="Meiryo"> (前日差 :{{ Math.round(100*$data.genyudif)/100 }} )</font></p>
           <p><font v-if="$data.genyudif<0" color="red" size="4" face="Meiryo"> (前日差 :{{ Math.round(100*$data.genyudif)/100 }} )</font></p>           
        </div>
        <div class="float_test150">
           <p><font size="3" color="#000000" face="Meiryo"> 米ドル円(円/$) </font></p>
           <p><font size="8" color="#000000" face="Meiryo"> <a v-on:click="goNewTask($data.datlen-3)"> {{ Math.round(100*$data.doller_en)/100 }} </a></font></p>
           <p><font v-if="$data.doller_en_dif>=0" color="green" size="4" face="Meiryo"> (前日差 :{{ Math.round(100*$data.doller_en_dif)/100 }} )</font></p>
           <p><font v-if="$data.doller_en_dif<0" color="red" size="4" face="Meiryo"> (前日差 :{{ Math.round(100*$data.doller_en_dif)/100 }} )</font></p>   
        </div>

        <div class="float_test150">
           <p><font size="3" color="#000000" face="Meiryo"> SP500 </font></p>
           <p><font size="8" color="#000000" face="Meiryo"> <a v-on:click="goNewTask($data.datlen-4)"> {{ Math.round($data.sp500) }} </a></font></p>
           <p><font v-if="$data.sp500dif>=0" color="green" size="4" face="Meiryo"> (前日差:{{ Math.round($data.sp500dif) }} )</font></p>
           <p><font v-if="$data.sp500dif<0" color="red" size="4" face="Meiryo"> (前日差:{{ Math.round($data.sp500dif) }} )</font></p>                
        </div> 


        <div class="float_test150">
           <p><font size="3" color="#000000" face="Meiryo"> 日経225 </font></p>
           <p><font size="8" color="#000000" face="Meiryo"> <a v-on:click="goNewTask($data.datlen-2)"> {{ Math.round($data.nikkei225) }} </a></font></p>
           <p><font v-if="$data.nikkei225dif>=0" color="green" size="4" face="Meiryo"> (前日差:{{ Math.round($data.nikkei225dif) }} )</font></p>
           <p><font v-if="$data.nikkei225dif<0" color="red" size="4" face="Meiryo"> (前日差:{{ Math.round($data.nikkei225dif) }} )</font></p>                
        </div>    


      <br><br><br><br><br><br><br><br><br><br><br><br><br><br>
      <h6>銘柄データ登録</h6>
      <p>WTI原油先物 : ^CLF ,   SP500 : ^GSPC ,   円ドル : ^JPYX ,   日経225 : ^N225 ,   VIX指数 : ^VIX</p> 
    　　<p>
        銘柄番号<input type="text" id="stock_num" v-model="stock_num"> 
    　　会社名<input type="text"  id="c_name" v-model="c_name"> 
    　　一株益<input type="number" id="eps" v-model="eps"> 
        </p>
        <p> 
        決算日<input type="date" id="kessan" v-model="kessan">  
        会社URL<input type="text" id="url" v-model="url">
        配当<input type="text" id="haitoub" v-model="haitoub">
        HOLD <input type="checkbox" id="hold"  v-model="hold">
        {{$data.hold}}
        </p>

        <p> 会社概要 </p>
        <p>
        <textarea cols="70" rows="4" id="kaisya" v-model="kaisya"></textarea>     
        </p>

        
        <p><input type="button" id="regdata" value="register" class="btn-gradient-radius" @click="regdata"></p>   <!-- ボタン -->
        

      <h6>登録銘柄一覧表</h6>
         登録銘柄は毎日19:00にデータが自動更新されます。<br>
         <a href='https://nikkei225jp.com/data/shutai.php' target="_blank">外国人投資家動向</a>
          <h4>  <font size="4"> 状態 :{{ $data.result }} </font> </h4>
      <br>表示銘柄<br>
      <p> <input type="radio" name="d_mei" value="ALL" v-model="dis_meigara"> 全銘柄 
          <input type="radio" name="d_mei" value="HOLD" v-model="dis_meigara"> HOLD銘柄
          <input type="radio" name="d_mei" value="A0" v-model="dis_meigara"> [A0]
          <input type="radio" name="d_mei" value="A1" v-model="dis_meigara"> [A1]
          <input type="radio" name="d_mei" value="A2" v-model="dis_meigara"> [A2] 
          <input type="radio" name="d_mei" value="PB" v-model="dis_meigara"> [parabolic] 
          <input type="radio" name="d_mei" value="BOL" v-model="dis_meigara"> [bolinjer] </p>
         <!--
        <p><input type="button" value="全銘柄株価取得" class="btn-gradient-radius" @click="allgetdat()"></p>
         -->
        <!-- ★★★ 銘柄パラメータを増やすときに追記する箇所★★★★★★★   -->
        <table border="2" align="center">
          <tr>
            <th>分析<br>結果</th>
            <th>情報<br>読出</th>
            <th>会社<br>概要</th>  
            <th>削除</th>                
            <th>銘柄番号</th>         
            <th>会社名</th>      
            <th>本日株価<br>(昨日差)</th>
            <th>決算日</th>   
            <th>配当<br>利回り</th> 
            <th>Bolinjer</th>
            <th>一目<br>均衡表</th>
            <th>パラボリック</th>
            <th>AR</th>  
            <th>c_ratio</th>                                  
            <th>株価<br>取得</th>           
          </tr>

<!--          <tr v-for="(element,index) in stockdata_matrix" v-if="dis_meigara=='ALL' ? 'true' : element[0].hold==TRU">   -->


            <tr v-for="(element,index) in stockdata_matrix"  v-if="dis_meigara=='ALL' ? 'true' : 
                                                                   dis_meigara=='HOLD' ? element[0].hold==TRU : 
                                                                   dis_meigara=='A0' ? element[0].meigara_sta==0 : 
                                                                   dis_meigara=='A1' ? element[0].meigara_sta==10 || element[0].meigara_sta==11 :
                                                                   dis_meigara=='A2' ? element[0].meigara_sta==20 || element[0].meigara_sta==21 :
                                                                   dis_meigara=='PB' ? 
                                                                   (
                                                                     (Math.round(element[0].sta)<=-15 && (element[0].ar>=0.16 && element[0].ar<=0.2))   ||
                                                                     (( Math.round(element[0].sta)>=4 &&  Math.round(element[0].sta)<=15) && (element[0].ar>=0.06 && element[0].ar<=0.14))
                                                                   )
                                                                   :
                                                                   dis_meigara=='BOL' ?
                                                                   (
                                                                      element[0].bol>2   || element[0].bol=='U90' || element[0].bol< -2   || element[0].bol=='D10'
                                                                   )
                                                                   :
                                                                   (
                                                                     element[0].bol>2   || element[0].bol=='U90' || element[0].bol< -2   || element[0].bol=='D10'
                                                                    
                                                                   )
                                                                    ">
                                            


            <th><input type="button" value="TECH" @click="goNewTask(index)"></th> 
            <th><input type="button" value="読取" @click="readMEIGARA(index)"></th>  
            <th>
             <input type="button" value='概要'  @click="openModal(index)" >
              <div id="overlay" v-show="showContent"> <!-- 読み取りボタンをクリックすればモーダル表示される -->
                <div id="content">
                  <p>銘柄番号:{{stock_num}}  {{c_name}}</p>
                  <p>{{kaisya}}</p>
                  <p>四季報</p>
                      <img :src=" image_path(stock_num) "> 
             
                  <button v-on:click="closeModal">Close</button>
                </div>
              </div>
            
            <th><input type="button" value="削除" @click="deldata(index)"></th> 
            <th><a v-bind:href='element[0].buffet_url' target="_blank">{{element[0].stock_num}}</a></th>
            <th><a v-bind:href='element[0].url' target="_blank">{{element[0].c_name}}</a></th>    
            <th>{{Math.round(10*element[0].today)/10}}  <br>            
              <font v-if="Math.round(element[0].dif)>=0" color="green">( {{Math.round(100*element[0].dif)/100}})</font>
              <font v-if="Math.round(element[0].dif)< 0" color="red">( {{Math.round(100*element[0].dif)/100}})</font>
            </th>

       <!--      <th>{{element[0].kessan.split("-")[1]  +"/"  + element[0].kessan.split("-")[2]   }}  </th>  --> 

            <th v-if="datediff(element[0].kessan)=='ZERO'" bgcolor='red'> {{ element[0].kessan.split("-")[1]  +"/"  + element[0].kessan.split("-")[2]   }}  </th>
            <th v-else-if="datediff(element[0].kessan)=='BEFORE'" bgcolor=#FF99E5> {{ element[0].kessan.split("-")[1]  +"/"  + element[0].kessan.split("-")[2]   }}  </th>
            <th v-else-if="datediff(element[0].kessan)=='AFTER'" bgcolor=#4edc4e> {{ element[0].kessan.split("-")[1]  +"/"  + element[0].kessan.split("-")[2]   }}  </th>
            <th v-else> {{ element[0].kessan.split("-")[1]  +"/"  + element[0].kessan.split("-")[2]   }}  </th>            

            <th v-if="element[0].haitoub==0">  'NA'  </th>
            <th v-else-if="Math.round( 100*(element[0].haitoub/element[0].today)*10 )/10 >=4" bgcolor=#CB0098> {{Math.round( 100*(element[0].haitoub/element[0].today)*10 )/10}} %  </th>
            <th v-else-if="Math.round( 100*(element[0].haitoub/element[0].today)*10 )/10 >3" bgcolor=#FF99E5> {{Math.round( 100*(element[0].haitoub/element[0].today)*10 )/10}} %  </th>
            <th v-else>{{Math.round( 100*(element[0].haitoub/element[0].today)*10 )/10}} %</th>

            <!-- ボリンジャー値により着色を行う。 --> 
            <th v-if="element[0].bol==sig0_1" bgcolor=#edfced>{{element[0].bol}}  </th>
            <th v-else-if="element[0].bol==sig1_2" bgcolor=#4edc4e>{{element[0].bol}}  </th>
            <th v-else-if="element[0].bol==sig2_3" bgcolor=#1d8d1d>{{element[0].bol}}  </th>
            <th v-else-if="element[0].bol==sig3" bgcolor=#0e470e>{{element[0].bol}}  </th>
            <th v-else>{{element[0].bol}}</th>
            <!--  ボリンジャー終わり --> 
            <!--  一目均衡表状況 -->
            <th v-if="Math.round(element[0].meigara_sta)==20" bgcolor=#4edc4e>[A{{Math.round(element[0].meigara_sta)}}]</th> 
            <th v-else-if="Math.round(element[0].meigara_sta)==21" bgcolor=#4edc4e>[A{{Math.round(element[0].meigara_sta)}}]</th>             
            <th v-else-if="Math.round(element[0].meigara_sta)==0" bgcolor=#1d8d1d>[A{{Math.round(element[0].meigara_sta)}}]</th> 
            <th v-else-if="Math.round(element[0].meigara_sta)==10" bgcolor=#1d8d1d>[A{{Math.round(element[0].meigara_sta)}}]</th> 
            <th v-else-if="Math.round(element[0].meigara_sta)==11" bgcolor=#1d8d1d>[A{{Math.round(element[0].meigara_sta)}}]</th> 
            <th v-else>[A{{Math.round(element[0].meigara_sta)}}]</th> 
            <!--  パラボリック -->

            <th v-if="(Math.round(element[0].sta)<=16 && Math.round(element[0].sta)>=4) || Math.round(element[0].sta)<=-15" bgcolor=#209EDB>{{Math.round(element[0].sta)}}</th> 
            <th v-else-if="Math.round(element[0].sta)<=3 && Math.round(element[0].sta)>=-3" bgcolor="yellow">{{Math.round(element[0].sta)}}</th> 
            <th v-else-if="(Math.round(element[0].sta)>0 && Math.round(element[0].sta)<4) || Math.round(element[0].sta)>16">U↑</th> 
            <th v-else-if="Math.round(element[0].sta)>-15 && Math.round(element[0].sta)<-3">D↓</th>             


            <!--  AR -->

            <th v-if="Math.round(element[0].sta)>0  &&  element[0].ar>=0.02 && element[0].ar<=0.14" bgcolor=#209EDB>{{Math.round(100*element[0].ar)/100}}</th> 
            <th v-else-if="Math.round(element[0].sta)>0  &&  element[0].ar>0.14">U↑</th> 
            <th v-else-if="Math.round(element[0].sta)<0  &&  element[0].ar<0.16">D↓</th> 
            <th v-else-if="Math.round(element[0].sta)<0  &&  element[0].ar>=0.16" bgcolor=#209EDB>{{Math.round(100*element[0].ar)/100}}</th>     






            <!--  culmer ratio -->
            <th>{{Math.round(100*element[0].cratio)/100}}</th> 
            <!--  株価取得 -->                                   
            <th><input type="button" value="取得" @click="getdata(index)"></th> 
          </tr>      

        </table>
                     <!-- ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★   -->

     <p>Buy条件(パラボリック解析),　「上昇トレンド継続期間:4～15日,  AR:0.06～0.14」  「下降トレンド継続期間:15日～, AR:0.16～0.2」</p>


    <p>一目均衡表記号の説明1</p>
    <img src="../assets/meigara_sta.png">
            <p><th><input type="button" class="btn-gradient-radius"  value="RADIKO" @click="goradiko()"></th></p>
            <p><th><input type="button" class="btn-gradient-radius"  value="OTENKI" @click="gootenki()"></th></p>                          

                             <!--   {{$data.stockdata_matrix}}   -->
日経225EPS1
{{$data.kakusyudat_matrix.nikkei225eps}}

  </div>

</template>



<script>
// eslint-disable-next-line
/* eslint-disable */ 
import * as d3 from 'd3'  //有効にする
import * as types from '../store/mutation-types'
import { mapGetters, mapActions } from 'vuex'
const consts = require('./const')
//const url='25.32.185.252' 
//const url='192.168.99.100' 

export default {

  name: 'top',

  methods:{


    //【R-1】銘柄の株価データを登録する
    regdata:function(){
        this.result= "register data"
        console.log( "register data")
        console.log( consts.url)
        //paramsに登録する銘柄データのパラメータを含んでいる。paramsに格納されたデータをbkendに送る。
        this.$axios.get('http://' + consts.url + ':3000/reg',

          {params:
                {
                  stock_num:this.stock_num,
                  c_name:this.c_name,
                  eps:this.eps,
                  kessan:this.kessan,
                  url:this.url,
                  kaisya:this.kaisya,
                  haitoub:this.haitoub,
                  hold:this.hold
                }          
          })
          .then(function(response){
            console.log("response.data.message")
            //console.log(response.data.message)  //バックエンドから返却された演算結果をconsole.logしている。
            this.result= response.data.message.mes
            //console.log("#1#1")          
            //console.log(response.data)
            this.stockdata_matrix=this.csvorder(response.data.message.stockdata[0])


            //console.log("this.stockdata_matrix")
            //console.log(this.stockdata_matrix)           

            }.bind(this))  //Promise処理を行う場合は.bind(this)が必要
          .catch(function(error){  //バックエンドからエラーが返却された場合に行う処理について
                   console.log("ERR")     
            this.result="サーバーエラー発生"
            }.bind(this))
          .finally(function(){
            }.bind(this))
    },


    // 読み込む画像アドレスを自動生成している。
    image_path: function(slug){
      try{
        return require("@/assets/" + slug + ".png");
      }catch(e){
        return require("@/assets/" + 0 + ".png");
      }
    },

    //【vuex】demo.jsからメソッドを読み出す。
    ...mapActions([
        'update_DATA',
        'update_TODAY',
        'update_DIF',
        'update_CNAME',
        'update_SIGVAL',
        'update_EPS',
        'update_COEFF',
        'update_CONFVAL',
        'update_TENKAN',
        'update_KAGENCHI',
        'update_STA',        
        'update_AR', 
        'update_SAR',                 
    ]),

    //【vuex】データをdemo.jsを介し、Top.vueからChart.vueに送る
    okButtonClick: function (i) {
      var stoch_numb=this.stockdata_matrix[i][0].stock_num=='9999'? 'USDJPY':this.stockdata_matrix[i][0].stock_num
      this.update_DATA(stoch_numb)
      this.update_TODAY(this.stockdata_matrix[i][0].today)  
      this.update_DIF(this.stockdata_matrix[i][0].dif)
      this.update_CNAME(this.stockdata_matrix[i][0].c_name)
      this.update_SIGVAL(this.stockdata_matrix[i][0].sigval)
      this.update_EPS(this.stockdata_matrix[i][0].eps)
      this.update_COEFF(this.stockdata_matrix[i][0].coeff)
      this.update_CONFVAL(this.stockdata_matrix[i][0].confval)
      this.update_TENKAN(this.stockdata_matrix[i][0].tenkan)
      this.update_KAGENCHI(this.stockdata_matrix[i][0].kagenchi) 
      this.update_STA(this.stockdata_matrix[i][0].sta) 
      this.update_AR(this.stockdata_matrix[i][0].ar)       
      this.update_SAR(this.stockdata_matrix[i][0].sar)        
         //console.log(this.$store.getters.newTodo)    
         //this.test_dat()
    },

    //登録された銘柄データをDBから読み出し,「銘柄データ登録」に読み出す。
    readMEIGARA: function (index) {
        this.result= "getting data"
        this.$axios.get('http://' +  consts.url + ':3000/meigarainfo',{params:{dat:this.stockdata_matrix[index][0].stock_num}})
          .then(function(response){
 
            
            this.result= response.data.message.mes     
            this.meigara_info=this.csvorder_meigarainfo(response.data.message.stockdata[0])
            //銘柄データ登録のBOXに登録情報を読み込む
            this.stock_num=this.meigara_info[0][0].stock_num //銘柄番号
            this.c_name=this.meigara_info[0][0].c_name  //会社名
            this.eps=this.meigara_info[0][0].eps //一株益
            this.kessan=this.meigara_info[0][0].kessan //決算日
            this.url=this.meigara_info[0][0].url //会社URL
            this.haitoub=this.meigara_info[0][0].haitoub //配当利回り
            this.kaisya=this.meigara_info[0][0].kaisya //会社概要
            this.hold=(this.meigara_info[0][0].hold=='true') //銘柄保持有無 文字型のtrueではなくBoolen型のtrueを入れなければ意図しない動作をするので注意

            //location.reload();
            }.bind(this))  //Promise処理を行う場合は.bind(this)が必要
          .catch(function(error){  //バックエンドからエラーが返却された場合に行う処理について
            this.result="サーバーエラー発生"
            }.bind(this))
          .finally(function(){

            }.bind(this))

    },


    //chart.vueに移動する
    goNewTask: function (i) {
      //console.log(this.stockdata_matrix[i][0].stock_num)
      this.okButtonClick(i)
      this.$router.push('chart')   //chart.vueに移動する

    },

    //登録した全銘柄の株価データを取得する。
    allgetdat:function(){
        this.result= "getting data"
        this.$axios.get('http://'+ consts.url  + ':3000/apiall',{params:{dat:"1111"}})
          .then(function(response){
            //console.log("allgetdat")
            //console.log(response.data.message)  //バックエンドから返却された演算結果をconsole.logしている。

            this.result= response.data.message.mes      
            this.kakusyudat_matrix=this.kakusyu_csvorder(response.data.message.stockdata[1])                  
            this.stockdata_matrix=this.csvorder(response.data.message.stockdata[0]) 
          

            //location.reload();
            }.bind(this))  //Promise処理を行う場合は.bind(this)が必要
          .catch(function(error){  //バックエンドからエラーが返却された場合に行う処理について
            this.result="サーバーエラー発生1"
            this.result= response.data.message.mes      
            this.kakusyudat_matrix=this.kakusyu_csvorder(response.data.message.stockdata[1])                  
            this.stockdata_matrix=this.csvorder(response.data.message.stockdata[0])              
            }.bind(this))
          .finally(function(){
                 //console.log("this.kakusyudat_matrix")
                 //console.log(this.kakusyudat_matrix)
                 //console.log("this.stockdata_matrix")
                 //console.log(this.stockdata_matrix)                 
                 this.stock_num="^N225"
                 this.c_name="日経225"
                 this.eps=1606
                 this.kessan='2018-01-01',
                 this.url="https://www.yahoo.co.jp"
                 this.kaisya="日経225",
                 this.haitoub=2
                 this.hold=true
                 location.reload();
            }.bind(this))
    },


    //指定した銘柄の株価データを取得する。
    getdata:function(index){
        this.result= "getting data"
        this.$axios.get('http://' + consts.url  + ':3000/api',{params:{dat:this.stockdata_matrix[index][0].stock_num}})
          .then(function(response){
            //console.log(response.data.message)  //バックエンドから返却された演算結果をconsole.logしている。
            this.result= response.data.message.mes
            this.stockdata_matrix=this.csvorder(response.data.message.stockdata[0])
            //location.reload();
            }.bind(this))  //Promise処理を行う場合は.bind(this)が必要
          .catch(function(error){  //バックエンドからエラーが返却された場合に行う処理について
            this.result="サーバーエラー発生"
            }.bind(this))
          .finally(function(){
            }.bind(this))
    },
      
    //原油、米国国債・・・をマトリックスに整理する関数
    kakusyu_csvorder:function(dat){
      //console.log("dat")
      //console.log(dat)
      let divdats=dat.split(",")  //datデータを","で分割し、配列に格納する
      let divdats_length=divdats.length  
      var stockdat_matrix = new Array(divdats_length-1) 
      //console.log("divdats")
      //console.log(divdats)
      //各銘柄情報をマトリックスに格納する。各データにはキー値を付与している。
  
      let tmp=[]
      //各データにはキー値を付与している。
      tmp={
        yield10:divdats[6],
        yield10_delta:divdats[7].split("（")[0].split(":")[0],
        genyu:divdats[8],
        genyu_delta:divdats[9],
        nikkei225eps:divdats[10]
      } 
      //console.log("tmp")   //for debug
      //console.log(tmp)   //for debug
      return tmp
    },


    //各銘柄情報をマトリックスに整理する関数
    csvorder:function(dat){
      //console.log("dat")
      //console.log(dat)
      let divdats=dat.split("\n")  //datデータを"\n"で分割し、配列に格納する
      let divdats_length=divdats.length  
      var stockdat_matrix = new Array(divdats_length-1) 
      console.log("divdats")
      console.log(divdats)

      //各銘柄情報をマトリックスに格納する。各データにはキー値を付与している。
      divdats.forEach(function(divdat,k){
      let tmp=[]
      //各データにはキー値を付与している。
      //('STOCK_NUM','TODAY','DIF','C_NAME','EPS','BAND','P1SIG','P05SIG','N1SIG','N05SIG','KESSAN','URL','KAISYA','HAITOUB','HOLD','MEIGARA_STA','TENKAN','CONFVAL0','CONFVAL1','CONFVAL2','COEFF0','COEFF1','COEFF2','KAGENCHI0','KAGENCHI1','KAGENCHI2')
      //★★★ 銘柄パラメータを増やすときに追記する箇所★★★★★★★  
      tmp.push({
        id:k,
        stock_num:divdat.split(",")[0],
        today:divdat.split(",")[1],
        dif:divdat.split(",")[2],
        c_name:divdat.split(",")[3],
        eps:divdat.split(",")[4],
        url:divdat.split(",")[11],
        kaisya:divdat.split(",")[12],
        haitoub:divdat.split(",")[13],      
        buffet_url:'https://monex.ifis.co.jp/index.php?sa=report_zaimu&bcode=' +   divdat.split(",")[0],
        kessan:divdat.split(",")[10],
        bol:divdat.split(",")[5],   //ボリンジャーσ値位置   
        sigval:{sigp1:divdat.split(",")[6], sigp05 :divdat.split(",")[7], sign05 :divdat.split(",")[9], sign1:divdat.split(",")[8]},
        hold:divdat.split(",")[14],
        meigara_sta:divdat.split(",")[15],
        tenkan:divdat.split(",")[16], //転換線最新値
        confval:{confval0:divdat.split(",")[17],confval1:divdat.split(",")[18],confval2:divdat.split(",")[19]}, //明日下落値算出時に設定した確率
        coeff:{coeff0:divdat.split(",")[20],coeff1:divdat.split(",")[21],coeff2:divdat.split(",")[22]}, //明日下落値算出時近似直線当てはまり度合い
        kagenchi:{kagenchi0:divdat.split(",")[23],kagenchi1:divdat.split(",")[24],kagenchi2:divdat.split(",")[25]},//明日下落値
        sar:divdat.split(",")[26],//パラボリックSAR値
        sta:divdat.split(",")[27],//パラボリックSTA値
        sratio:divdat.split(",")[28],//sharp ratio
        cratio:divdat.split(",")[29],//culmer ratio
        ar:divdat.split(",")[30],//パラボリックAR値
        })
      //★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★  


        //最終行に余計な空白行が入ることを阻止するために入れたコード
         if(k<divdats_length-1){ 
          stockdat_matrix[k]=tmp
        }
      })
      //console.log("stockdat_matrix[0]") 
      //console.log(stockdat_matrix[0])   //for debug
      return stockdat_matrix
    },



    //新規銘柄登録直後に、登録銘柄一覧表に読み出すデータ。csvorderと異なるのは、読み出すパラメータの違い。csvorder_meigarainfoの方が読み出すパラメータは少ない
    csvorder_meigarainfo:function(dat){

      let divdats=dat.split("\n")  //datデータを"\n"で分割し、配列に格納する
      let divdats_length=divdats.length  
      var stockdat_matrix = new Array(divdats_length-1) 

      //各銘柄情報をマトリックスに格納する。各データにはキー値を付与している。
      divdats.forEach(function(divdat,k){
      let tmp=[]
      //各データにはキー値を付与している。

      //★★★ 銘柄パラメータを増やすときに追記する箇所★★★★★★★  
      tmp.push({
        stock_num:divdat.split(",")[0],
        c_name:divdat.split(",")[3],
        eps:divdat.split(",")[4],
        kessan:divdat.split(",")[10],
        url:divdat.split(",")[11],
        haitoub:divdat.split(",")[13],
        kaisya:divdat.split(",")[12],      
        hold:divdat.split(",")[14],      
        })
      //★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★  
        //console.log("#7")

        //最終行に余計な空白行が入ることを阻止するために入れたコード
         if(k<divdats_length-1){ 
          stockdat_matrix[k]=tmp
        }
      })
      //console.log(stockdat_matrix)   //for debug
      return stockdat_matrix
    },


     //銘柄の株価データを削除する
    deldata:function(index){
        this.result= "register data"
        var del_stocknum
        //初期読み込み時this.stockdata_matrix[index][0].stock_numは空データでエラーになるので、初期読み取り時del_stocknum=0とする。
          try{
            del_stocknum=this.stockdata_matrix[index][0].stock_num
              }catch(e){
            del_stocknum=0
           }         

        //paramsに登録する銘柄データのパラメータを含んでいる。paramsに格納されたデータをbkendに送る。
        this.$axios.get('http://' + consts.url + ':3000/del',

          {params:
                {
                  stock_num:del_stocknum
                }          
          })
          .then(function(response){
            

            this.result= response.data.message.mes              
            this.stockdata_matrix=this.csvorder(response.data.message.stockdata[0])  
            console.log("this.stockdata_matrix2222")
            //console.log(this.stockdata_matrix) 
            console.log("this.stockdata_matrix")
            console.log(this.stockdata_matrix) 
            this.beikokuichi()  //米国銘柄の開始位置を特定する
            console.log("A1")
            this.nikkei225=this.stockdata_matrix[this.datlen-2][0].today //日経225読み取り
            this.nikkei225dif=this.stockdata_matrix[this.datlen-2][0].dif //日経225前日比
            this.doller_en=this.stockdata_matrix[this.datlen-3][0].today //米ドル読み取り
            this.doller_en_dif=this.stockdata_matrix[this.datlen-3][0].dif //米ドル前日比
            this.sp500=this.stockdata_matrix[this.datlen-4][0].today //SP500読み取り
            this.sp500dif=this.stockdata_matrix[this.datlen-4][0].dif //SP500前日比
            this.genyu=this.stockdata_matrix[this.datlen-5][0].today  //WTI原油
            this.genyudif=this.stockdata_matrix[this.datlen-5][0].dif //WTI原油前日比
            this.vix=this.stockdata_matrix[this.datlen-1][0].today  //WTI原油
            this.vixdif=this.stockdata_matrix[this.datlen-1][0].dif //WTI原油前日比            

            console.log("A2")
            this.datlen=this.stockdata_matrix.length-1 //データ行数
            }.bind(this))  //Promise処理を行う場合は.bind(this)が必要
          .catch(function(error){  //バックエンドからエラーが返却された場合に行う処理について
            this.result="サーバーエラー発生"
            console.log("A3")
            }.bind(this))
          .finally(function(){

            console.log("A4")
            this.beikokuichi()
            //console.log("A5")
            }.bind(this))
    },   

     //モーダルに表示するデータを記載したメソッド
    openModal: function(i){
      this.stock_num=this.stockdata_matrix[i][0].stock_num
      this.c_name=this.stockdata_matrix[i][0].c_name
      this.kaisya=this.stockdata_matrix[i][0].kaisya
      this.showContent = true
    },

     //モーダルを閉じる
    closeModal: function(){
      this.showContent = false
    },


    //radiko.vueに移動する
    goradiko: function (i) {
      this.$router.push('radiko')   

    },

    //otenki.vueに移動する
    gootenki: function () {
      this.$router.push('otenki')   

    },


    //2つの日付の差を算出する。
    datediff:function (predat) {
        let flag=''
        var d1 = new Date(predat);
        var today = new Date(new Date().getFullYear(),new Date().getMonth(),new Date().getDate(),9,0,0);  //本日の日付を取得している。
        var msDiff = d1.getTime() - today.getTime();
        var daysDiff = msDiff / (1000 * 60 * 60 *24);
        if (daysDiff== 0)  flag="ZERO"
        else if ( daysDiff>-8 & daysDiff <0 ) flag="BEFORE"
        else if ( daysDiff>0 & daysDiff <8 ) flag="AFTER"
        else  flag="NONE"
        return flag
    },

    //米国銘柄の開始位置を特定する
    beikokuichi: function () {

      //this.stock_num=this.stockdata_matrix[i][0].stock_num 
      //console.log("this.stockdata_matrix.length")
      //console.log(this.stockdata_matrix.length)

      var bei_index
      var stocknum_matrix = new Array(this.stockdata_matrix.length);

      this.stockdata_matrix.forEach(function(ele,k){
        stocknum_matrix[k]=ele[0].stock_num 
        if (isNaN(stocknum_matrix[k])==false){
        
        bei_index=k

        }
        });
      //console.log("bei_index")   
      //console.log(bei_index)   

      this.beikoku_index=bei_index //米国銘柄の開始位置
      //console.log("this.beikoku_index")   
      //console.log(this.beikoku_index)
      this.datlen=this.stockdata_matrix.length
      //console.log("this.datlen")   
      //console.log(this.datlen)     
    }



  },





  created:function(){

    d3.select("svg").remove()  //ページをオープンしたときにsvgオブジェクトを削除する。
    this.deldata() //銘柄データを取得するだけのダミーコマンド。stock_num=0を削除するメソッドになっているが、stock_num=0は存在しないため、現在登録されている銘柄データを取得できる
    console.log("A6")   


  },
 
  computed: {
     //【vuex】銘柄番号をdemo.jsを介してChart.vueに送る。
    ...mapGetters({
      meigara_num:'MEIGARA_NUM',
    }),
      get_meigara: {     
       get () {
        //  return [this.$store.getters.BCDATA, this.$store.getters.UPDATING_DONE]
        return this.meigara_num
        },
       }
  },


  data: function(){
    return { 
        message:'',  //入力データを格納する変数。
        result :'',  //演算結果を格納する変数。
        stock_num:0, //銘柄番号  stock_num:0は初期読込に必要。変更しないこと
        c_name:'', //会社名
        eps:'', //一株益
        stockdata_matrix:'', //銘柄データマトリックス
        kessan:'2020-01-01',
        url:'https://www.yahoo.co.jp', //会社URL
        kaisya:'',
        haitoub:'', //配当利回り
        meigara_info:'', //銘柄登録情報マトリックス
        showContent: false, //モーダル表示を有効にする変数
        sigval:'', // ±1σ, ±0,5値の株価を格納する
        hold:false, //銘柄保有でtrue, 否でfalse
        sig0_1:'0<=σ<1', //文字列'0<=σ<1'を定数化する。
        sig1_2:'1<=σ<2', //文字列'0<=σ<2'を定数化する。
        sig2_3:'2<=σ<3', //文字列'2<=σ<3'を定数化する。   
        sig3  :'3<=σ', //文字列'3<=σ'を定数化する。 
        sign_2_3:'-3<=σ<-2', //文字列'-3<=σ<-2'を定数化する。
        sign_3:'σ<-3', //文字列'σ<-3'を定数化する。        
        TRU:'true',
        dis_meigara:"ALL", //全銘柄を表示する
        holddis:false, //HOLD銘柄のみを表示する。       
        meigara_sta:'', //一目均衡表ステータス  
        url_shikihou: "../../static/6246.png",
        kakusyudat_matrix:'', //各種データ(金利、国債など)マトリックス
        nikkei225:'', //本日の日経225
        nikkei225dif:'', //日経225前日比
        genyu:'', //本日のWTI原油
        genyudif:'', //本日のWTI原油前日比
        sp500:'', //本日のS&P500
        sp500dif:'',//本日のS&P500前日比
        vix:'', //本日のVIX指数
        vixdif:'',//本日のVIX指数前日比
        doller_en:'', //本日の米ドル円
        doller_en_dif:'', //本日の米ドル円前日差
        datlen:'', //データ数
        beikoku_index:0 //銘柄一覧表の中で米国株の列挙が開始される位置
        
    }
  },

}  

</script>


<style>


  #large_block {
    width: 1000px;
    height: 200px;
    padding: 0px;
    margin: 10px;
    float :left; /* 左側を起点にする */
    border: solid 0.5px; /* 領域のボーダーラインの設定 */
  }   

  .float150 {
    height: 150px;              /* 高さ指定 */
    width: 150px;               /* 幅指定 */
    background-color: #FFF;     /* 背景色指定 */
    margin:  23px;              /* 周りの余白指定 */
    float:  left;   /* 回り込み指定(左から順番に配置していくということ) */
    border: solid 2px #6091d3;/*線*/
    border-radius: 10px;/*角の丸み*/
    padding: 0px;
  }

  .float300 {
    height: 150px;              /* 高さ指定 */
    width: 300px;               /* 幅指定 */
    background-color: #FFF;     /* 背景色指定 */
    margin:  23px;              /* 周りの余白指定*/
    float:  left;   /* 回り込み指定(左から順番に配置していくということ) */
    border: solid 2px #6091d3;/*線*/
    border-radius: 10px;/*角の丸み*/
    padding: 0px;
  }

  h6 {
    font-size: 1.0em;
    padding: 1.5em;
    color: #494949;
    background: #fffaf4;
    border-left: solid 2px #ffaf58;

  } 


  .page {
    width: auto;
    max-width: 900px;
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




/***** radio button css  *********/


.cp_ipradio {
	width: 21%;
	margin: 2em;
	text-align: left;
}
@keyframes click-wave {
	0% {
		position: relative;
		width: 30px;
		height: 30px;
		opacity: 0.35;
	}
	100% {
		width: 200px;
		height: 200px;
		margin-top: -80px;
		margin-left: -80px;
		opacity: 0;
	}
}
.cp_ipradio .option-input {
	position: relative;
	position: relative;
	top: 13.33333px;
	right: 0;
	bottom: 0;
	left: 0;
	width: 30px;
	height: 30px;
	margin-right: 0.5rem;
	cursor: pointer;
	transition: all 0.15s ease-out 0s;
	color: #ffffff;
	border: none;
	outline: none;
	background: #d7cbcb;
	-webkit-appearance: none;
	        appearance: none;
}
.cp_ipradio .option-input:hover {
	background: #d6a9a9;
}
.cp_ipradio .option-input:checked {
	background: #da3c41;
}
.cp_ipradio .option-input:checked::before {
	font-size: 20px;
	line-height: 30px;
	position: absolute;
	display: inline-block;
	width: 30px;
	height: 30px;
	content: '✔';
	text-align: center;
}
.cp_ipradio .option-input:checked::after {
	position: relative;
	display: block;
	content: '';
	-webkit-animation: click-wave 0.65s;
	        animation: click-wave 0.65s;
	background: #da3c41;
}
.cp_ipradio .option-input.radio {
	border-radius: 50%;
}
.cp_ipradio .option-input.radio::after {
	border-radius: 50%;
}
.cp_ipradio label {
	line-height: 40px;
	display: block;
}
.cp_ipradio .option-input:disabled {
	cursor: not-allowed;
	background: #b8b7b7;
}
.cp_ipradio .option-input:disabled::before {
	font-size: 30px;
	line-height: 30px;
	position: absolute;
	display: inline-block;
	width: 30px;
	height: 30px;
	content: '✖︎';
	text-align: center;
}
.cp_ipradio .disabled {
	color: #9e9e9e;
}

.float_test150 {
    height: 200px;              /* 高さ指定 */
    width: 150px;               /* 幅指定 */
    background-color: #FFF;     /* 背景色指定 */
    margin:  10px;              /* 周りの余白指定 */
    float:  right;   /* 回り込み指定 */
    border: solid 3px #6091d3;/*線*/
    border-radius: 10px;/*角の丸み*/
}



</style>



  