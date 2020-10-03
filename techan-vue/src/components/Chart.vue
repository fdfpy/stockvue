<template>




  <div class="hello">
      <h1>株価チャートテクニカル分析アプリ</h1>
      <input type="button" value="戻る" class="btn-gradient-radius"　@click="returnButtonClick()">

      <p><font size="3" color="#000000" face="Meiryo">(銘柄番号:{{get_meigara[0]}})  {{get_meigara[3]}}</font></p>

        <div class="float_test150">
           <p><font size="3" color="#000000" face="Meiryo"> PER </font></p>
           <p><font size="12" color="#000000" face="Meiryo"> {{Math.round(10*get_meigara[1]/get_meigara[5])/10}}</font></p>
        </div>

        <div class="float_test300">
          <p> <font size="2.5" color="red" face="Meiryo"> 売買指標  </font> </p>
          <p> <font size="2" color="#000000" face="Meiryo"> 転換線 : {{this.tenkan}} (下落値:{{Math.round(get_meigara[1] - this.tenkan)}}) </font> </p>
          <p> <font size="2" color="#000000" face="Meiryo"> {{Math.round(100*(1-this.confval.confval0))}}%下限値  : {{this.kagenchi.kagenchi0}} (下落値:{{Math.round(get_meigara[1] - this.kagenchi.kagenchi0)}}) R2:{{Math.round(100*this.coeff.coeff0)/100 }}  </font></p>
          <p> <font size="2" color="#000000" face="Meiryo"> {{Math.round(100*(1-this.confval.confval1))}}%下限値 : {{this.kagenchi.kagenchi1}} (下落値:{{Math.round(get_meigara[1] -this.kagenchi.kagenchi1)}}) R2:{{Math.round(100*this.coeff.coeff1)/100 }}</font></p>
          <p> <font size="2" color="#000000" face="Meiryo"> {{Math.round(100*(1-this.confval.confval2))}}%下限値 : {{this.kagenchi.kagenchi2}}  (下落値:{{Math.round(get_meigara[1] -this.kagenchi.kagenchi2)}}) R2:{{Math.round(100*this.coeff.coeff2)/100 }}</font></p>  
        </div>
      
        <div class="float_test150">
          <p><font size="2" color="#000000" face="Meiryo">最新株価</font></p>
          <p><font size="6" color="#000000" face="Meiryo">{{Math.round(100*get_meigara[1])/100}}</font></p>
          <p><font size="6" color="#000000" face="Meiryo">({{Math.round(100*get_meigara[2])/100}})</font></p>       
        </div>



        <div class="cp_ipradio">

          <div class="box2">

            <label>
    	        <input type="radio" class="option-input radio" name="cpipr02" id="box1" value="0" v-model="type" checked="checked">
    	        <font size="2"> ろうそく足 ＋ 移動平均線 </font>
    	      </label>
  
    	      <label>
    	        <input type="radio" class="option-input radio" name="cpipr02" id="box2" value="1" v-model="type">
    	        <font size="2">ろうそく足 + ボリンジャーバンド</font>
    	      </label>
	  
            <label>
    	        <input type="radio" class="option-input radio" name="cpipr02" id="box3" value="2" v-model="type">
    	        <font size="2">ろうそく足 + 一目均衡表</font>
      	    </label>

          </div>

        </div>

  </div>


</template>



<script>
// eslint-disable-next-line
/* eslint-disable */ 
import * as d3 from 'd3'  //有効にする
import techan from 'techan'  //有効にする
const consts = require('./const')
import TECH0 from '../tech'
import * as types from '../store/mutation-types'
import { mapGetters, mapActions } from 'vuex'


export default {
  name: 'chart',

  data () {
    return {
      type:0,
      colors:[],
      meigara_num:'',
      dat_path:"../static/" + "1570" + ".csv",
      today_kabuka:0,
      dif_kabuka:0,
      epsnum:2000
    }
 
  },

  //typeを監視し、typeの数値が変更になればfunctionの中身を実行する。
  watch:{
    type:function(newvalue){
    d3.select("svg").remove()  //すでに描写されたsvgデータを消去している
    this.executeall(newvalue)  //newvalueにあたるテクニカルチャートを描写する。
    },
  },


  //起動時一度のみexecuteallを実行する。
  created:function(){
     d3.select("svg").remove()  //すでに描写されたsvgデータを消去している
    
     this.dat_path="../static/" + this.stock_num + ".csv"
     this.executeall(0)
  },


  computed: {

    ...mapGetters({
        stock_num:'MEIGARA_NUM',
        today:'TODAY',
        dif:'DIF',
        c_name:'C_NAME',
        sigval:'SIGVAL',
        eps:'EPS',
        tenkan:'TENKAN',
        kagenchi:'KAGENCHI',
        confval:'CONFVAL',
        coeff:'COEFF'
    }),


    get_meigara: {     
        get () {
      //  return [this.$store.getters.BCDATA, this.$store.getters.UPDATING_DONE]
        return [this.stock_num,this.today,this.dif,this.c_name,this.sigval,this.eps,this.tenkan,this.kagenchi,this.confval,this.coeff]
       },
    },


  },


  methods:{
    //executeallは一連の描写作業を行う。

    returnButtonClick: function () {
        d3.select("svg").remove()  //すでに描写されたsvgデータを消去している
        this.$router.go(-1) // 1つ戻る
    },

    uploading:function() { 
        d3.select("svg").remove()  //すでに描写されたsvgデータを消去している
        console.log("this.stock_num")
        console.log(this.stock_num)        
        //this.meigara_num=this.get_meigara()
        this.dat_path="../static/" + this.stock_num + ".csv"
        //this.dat_path="../static/" + this.stock_num + ".csv"       
        this.executeall(this.type)
    },

    executeall: function(type) {


      //###########################################################
      //################# (1)変数の定義をする。######################
      //###########################################################

      //****  (1-1) グラフの表示画面の大きさを定義している。 *******
 
      var dim = {
        width: 960+300, height: 500+50+5*2+((5+65)+5)*2,
        margin: { top: 25+50, right: 50, bottom: 30, left: 50 },
        ohlc: { height: 305 },
        indicator: { height: 65, padding: 5+5 }
      };
      dim.plot = {
        width: dim.width - dim.margin.left - dim.margin.right,
        height: dim.height - dim.margin.top - dim.margin.bottom
      };
      dim.indicator.top = dim.ohlc.height+dim.indicator.padding;
      dim.indicator.bottom = dim.indicator.top+dim.indicator.height+dim.indicator.padding;
      dim.indicator.bottom1 = dim.indicator.bottom+dim.indicator.height+dim.indicator.padding;
      dim.indicator.bottom2 = dim.indicator.bottom1+dim.indicator.height+dim.indicator.padding;

      var indicatorTop = d3.scaleLinear().range([dim.indicator.top, dim.indicator.bottom]);
      //indicatorTop(0)=dim.indicator.top    indicatorTop(1)=dim.indicator.bottom
      var indicatorTop1 = d3.scaleLinear().range([indicatorTop(1), dim.indicator.bottom1]);
      //indicatorTop1(0)=indicatorTop(1)    indicatorTop1(1)=dim.indicator.bottom1
      var indicatorTop2 = d3.scaleLinear().range([indicatorTop1(1), dim.indicator.bottom2]);
      //indicatorTop1(0)=indicatorTop(1)    indicatorTop1(1)=dim.indicator.bottom1
   
      var datlength=consts.DATLENGTH; //描写する対象の日数を設定する 
      var meigara_name=consts.MEIGARA_NAME; //銘柄名を設定する。


      //##################################################################
      //################# (2)ヘルパー関数の定義をする。######################
      //##################################################################

      //***********************************************************************************************************
      //(2-1) timeParse 日付、曜日、時間などフォーマット変換   "2017-10-25" ->  Sun Oct 25 2015 00:00:00 GMT+0900 (Japan Standard Time)
      //***********************************************************************************************************

      var parseDate = d3.timeParse("%Y-%m-%e");  
      var timeForm=d3.timeFormat("%Y/%m/%d")

      //***********************************************************************************************************
      //(2-2) 全体の描写エリアの設定のためのヘルパー関数を定義している。
      //***********************************************************************************************************

      var x = techan.scale.financetime().range([0, dim.plot.width]);  //x(0)=0,  x(1)=dim.plot.width

      var x0=x(0)   //x(0)=0
      var x1=x(1)   //x(1)=dim.plot.width

      var y = d3.scaleLinear().range([dim.ohlc.height, 0]); //y(0)=dim.ohlc.height, y(1)=0  第1描写エリアのy軸の範囲を算出している。

      var xAxis = d3.axisBottom(x); //x軸の配置場所を定めたヘルパー関数
      var yAxis = d3.axisRight(y);  //y軸の配置場所を定めたヘルパー関数
      var yPercent = y.copy();   // Same as y at this stage, will get a different domain later
      var yInit, yPercentInit, zoomableInit;
      var timeAnnotation = techan.plot.axisannotation()    //x軸のプロパティーを定めるヘルパー関数
            .axis(xAxis)
            .orient('bottom')
            .format(d3.timeFormat('%Y-%m-%d'))
            .width(65)
            .translate([0, dim.plot.height]);

      var ohlcAnnotation = techan.plot.axisannotation()   //y軸のプロパティーを定めるヘルパー関数
            .axis(yAxis)
            .orient('right')
            .format(d3.format(',.2f'))
            .translate([x(1), 0]);




      //**************************************************
      // (2-3) 第1描写エリアの設定のためのヘルパー関数を定義している。
      //**************************************************


      var candlestick = techan.plot.candlestick().xScale(x).yScale(y); //ろうそく足に関する設定
      // Set the accessor to a ohlc accessor so we get highlighted bars
      var yVolume = d3.scaleLinear().range([y(0), y(0.2)]); //y(0)=dim.ohlc.height, y(0.2)=0.8*dim.ohlc.height
      var volume = techan.plot.volume().accessor(candlestick.accessor()).xScale(x).yScale(yVolume);

      //第1描写エリア右軸の設定のための関数を定義している
      var percentAxis = d3.axisLeft(yPercent).tickFormat(d3.format('+.1%'));
      var percentAnnotation = techan.plot.axisannotation().axis(percentAxis).orient('left');

      //第1描写エリア出来高の軸描写設定の関数を定義している
      var volumeAxis = d3.axisRight(yVolume).ticks(3).tickFormat(d3.format(",.3s"));

      //第1描写エリア出来高の描写設定の関数を定義している。
      var volumeAnnotation = techan.plot.axisannotation()
            .axis(volumeAxis)
            .orient("right")
            .width(35);


      //##################################################################
      //################# (3)描写系の設定をする。######################
      //##################################################################
 
      //****************************************** 
      //   (3-1) グラフを書く領域を設定している。
      //******************************************

      var svg = d3.select("body").append("svg")
            .attr("width", dim.width)
            .attr("height", dim.height);

      var defs = svg.append("defs");

      svg = svg.append("g")
            .attr("transform", "translate(" + dim.margin.left + "," + dim.margin.top + ")");

      //**************************************
      //    (3-2) 文字の記載を行う。
      //**************************************

      //銘柄名の記載
      svg.append('text')
            .attr("class", "symbol")
            .attr("x", 20)
            .attr("y", 0)         
            .text(meigara_name);

  
      //*************************************************
      //  (3-4) 第1描写エリアの設定をする。   
      //*************************************************

      svg.append("g")  //y軸(左側)の配置場所を設定している。
            .attr("class", "x axis")
            .attr("transform", "translate(0," + dim.plot.height + ")");

      var ohlcSelection = svg.append("g")  //ろうそく足を描写するエリアを確保している
            .attr("class", "ohlc")
            .attr("transform", "translate(0,0)");

      ohlcSelection.append("g")   //y軸(右側) と Price(yen)の配置場所を設定している。
            .attr("class", "axis")
            .attr("transform", "translate(" + x(1) + ",0)")
            .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", -12)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text("Price (yen)");


      ohlcSelection.append("g") //ろうそく足を配置する箇所をくりぬいている(clip-path)
                 .attr("class", "candlestick")
                 .attr("clip-path", "url(#ohlcClip)");


      ohlcSelection.append("g")
            .attr("class", "percent axis");

      ohlcSelection.append("g")
            .attr("class", "volume axis");




      //*********************************************************
      // (3-5)  第2描写エリア、第3描写エリア、第4描写エリア、第5描写エリアに該当するDOMを作る。   
      //*********************************************************

      //<g class="macd indicator">xxxxxxxx</g> ,  <g class="*** indicator">xxxxxxxx</g> を生成する。
      var indicatorSelection = svg.selectAll("svg > g.indicator").data(["second_area","third_area","forth_area","fifth_area"]).enter()
             .append("g")
             .attr("class", function(d) { return d + " indicator"; });


      //##################################################################
      //################# (4)Main処理を行う。##############################
      //##################################################################

      
      var epsnum=this.get_meigara[5]  //一株益

      d3.csv(this.dat_path,  function(error, data) {

        var datlength=data.length; //描写する対象の日数を設定する 
        //var datlength=40; //描写する対象の日数を設定する 
        console.log("this.epss")
        console.log(epsnum)
        //***********************************************************************************************************
        //(2-1) timeParse 日付、曜日、時間などフォーマット変換   "2017-10-25" ->  Sun Oct 25 2015 00:00:00 GMT+0900 (Japan Standard Time)
        //***********************************************************************************************************

        var parseDate = d3.timeParse("%Y-%m-%e");  
        var timeForm=d3.timeFormat("%Y/%m/%d")


        //########## (4-1)クラスからオブジェクトを生成する。########//
 
        var Tech = new TECH0(data.length) 
        var Draw = new DRAW()


        var accessor = techan.plot.candlestick().xScale(x).yScale(y).accessor();
          //var accessor = Assign.candlestick.accessor();
        var   indicatorPreRoll = 33;  // Don't show where indicators don't have data
          //data.sliceは最新の株価から過去にさかのぼっていくつのデータを取得するか
        data = data.slice(0, datlength).map(function(d) {
            return {
                date: parseDate(d.DATE),                
                close: +d.CLOSE,
                open: +d.OPEN,
                high: +d.HIGH,
                low: +d.LOW,
                volume: +d.VOL
            };
        }).sort(function(a, b) { return d3.ascending(accessor.d(a), accessor.d(b)); });


        let Assign = new ASSIGN(type)

        //チャートを描写する
 
        Assign.chart_put(
          Tech,Draw,
          data,x,y,yVolume,indicatorPreRoll,xAxis,
          consts.S_PERIOD,consts.M_PERIOD,consts.L_PERIOD,
          consts.BOL_N,
          consts.TENKAN_DELAY,consts.KIJYUN_DELAY,consts.CHIKOU_DELAY,consts.SENKOU1,consts.SENKOU2_P,consts.SENKOU2_F,
          "g.second_area","Variation",
          "g.third_area","当日,前日株価変化率2乗の移動平均",consts.CLOSE_OPEN_PERIOD,consts.CLOSE_T_Y,
              //          "g.forth_area","KAIRI(%)",consts.M_PERIOD,
          "g.forth_area","KAIRI(%)",consts.KIJYUN_DELAY+consts.MOMIAI,
          "g.fifth_area","PER",epsnum
        )
  
       //(4-2-4)ろうそく足にカーソルを重ねたときに、日にちと終値を表示させる。
        dataput(data);

      });




       //console.log("kabuka.today")
       //this.today_kabuka=kabuka

      //**********************************************************//
      //***************  ASSIGNクラスの定義を行う *******************//
      //**********************************************************//

        class ASSIGN{
          constructor(type){
          this.type=type
          }   



          chart_put = function(
            tech,draw,
            data,x,y,yVolume,indicatorPreRoll,xAxis,
            s_period,m_period,l_period,
            bol_n,
            tenkan_delay,kijyun_delay,chikou_delay,senkou1,senkou2_p,senkou2_f,
            dom1,title1,
            dom2,title2,period0,period1,
            dom3,title3,period2,
            dom4,title4,period3,
          )
          
            {
  
              if(this.type==0){

                 draw.candle_put(data,x,y,yVolume,indicatorPreRoll,xAxis,type,tech)   // ろうそく足と出来高を描写する
                 draw.sma_put(data,s_period,m_period,l_period,tech)   //移動平均線を描写する
              }else if(this.type==1){

                 draw.candle_put(data,x,y,yVolume,indicatorPreRoll,xAxis,type,tech)   // ろうそく足と出来高を描写する
                 draw.bollinger_put(bol_n,data,tech)　　//★ ボリンジャーバンドを描写する ★

              }else if(this.type==2){

                 draw.candle_put(data,x,y,yVolume,indicatorPreRoll,xAxis,type,tech)   // ろうそく足と出来高を描写する
                 draw.ichimoku_put(data,tenkan_delay,kijyun_delay,chikou_delay,senkou1,senkou2_p,senkou2_f,tech) //★ 一目均衡表を描写する ★
              }




              //*********************************************************************************   
              //******************** (4-4) 第2エリアに描写を行う。 *************************************
              //*********************************************************************************  

              var variation_dat = tech.val_get(data,0)
              //console.log("variation_dat")               
              //console.log(variation_dat)
              //前日の株価との変化率時系列を描写している
              //indicatorTop(0)=dim.indicator.top    indicatorTop(1)=dim.indicator.bottom
              draw.get_seriesline(variation_dat[0],x0,x1,indicatorTop(0)+dim.indicator.height,indicatorTop(0),dom1,title1)

              //*********************************************************************************   
              //******************** (4-5) 第3エリアに描写を行う。 *********************************
              // **(選択1) close値-open値の移動平均値,close値(本日)-close値(昨日)の移動平均値の描写を行うコード
              // **(選択2) )当日 vs 前日株価変化率2乗値移動平均グラフ描写
              //*********************************************************************************  

              //棒グラフのプロパティーを取得する  [delta0,delta1,dw,n] 
              var barchart_property = display_dayclose(tech.n)  


              //******** (1)close値-open値の移動平均値,close値(本日)-close値(昨日)の移動平均値の描写を行うコード
              
              //close値-open値の移動平均値を計算している。period0は移動平均線の期間を表している。
              //var sma_oc = tech.sma_close_open(data, period0)
              //close値(本日)-close値(昨日)の移動平均値を計算している。period1は移動平均線の期間を表している。
              //var sma_cy_cy_d = tech.sma_ct_cy(data, period1)
              //draw.get_barline_smad(sma_oc, sma_cy_cy_d, x0, x1, indicatorTop(1)+dim.indicator.height, indicatorTop(1), barchart_property, dom2,title2,period0,period1)
  
              //*** (2)当日 vs 前日株価変化率2乗値移動平均グラフ描写

              //var variation_dat = tech.val_get(data,0)
              var val2_dat = tech.val_get(data,0)[1]
              //console.log("val2_dat")
              //console.log(val2_dat)
              draw.get_barline_sma(val2_dat,x0,x1,indicatorTop(1)+dim.indicator.height, indicatorTop(1),barchart_property,dom2,title2,consts.VAL2_SMA+1)


              //******************************************************************************************   
              //******************** (4-6) 第4エリアに描写を行う。 
              //*** (移動平均,ボリンジャー表示) 株価と移動平均線乖離の棒グラフを表示する****
              //*** (一目均衡表表示) もみ合い判定結果を表示する。
              //******************************************************************************************  


              var sma_kairi_val = tech.sma_kairi(data,consts.M_PERIOD)
              var momiai_hantei = tech.momiai(data,kijyun_delay)

              //console.log("momiai_hantei2")     
              //console.log(momiai_hantei)     
              //y軸の描写設定、実際のデータの描写を行う関数  
              //min_val:描写するデータ系列の最小値 , max_val:描写するデータ系列の最大値
              //dat:データ
              //x0 : ｘデータ(日付データ)の描写開始座標値
              //x1 : xデータ(日付データ)の描写完了座標値
              // yaxis_min : yデータを描写する座標開始値 
              // yaxis_max : yデータを描写する座標終了値 
              // average : variation計算値の平均値
              // sigma  : variation計算値の終了値
              //axis_right : DOM名 x軸(右側)
              //axis_left :  DOM名 y軸(左側)
              //title : グラフのタイトル


              if(this.type==2){
                //もみ合い判定結果を表示する。
                 draw.get_barline_sma(momiai_hantei,x0,x1,indicatorTop1(1)+dim.indicator.height, indicatorTop1(1),barchart_property,dom3,title3,consts.MOMIAI+consts.KIJYUN_DELAY)
              } else {
                //株価と移動平均線乖離の棒グラフを表示する
                 draw.get_barline_sma(sma_kairi_val,x0,x1,indicatorTop1(1)+dim.indicator.height, indicatorTop1(1),barchart_property,dom3,title3,consts.M_PERIOD)

              }

               //*********************************************************************************   
               //******************** (4-6) 第5エリアに描写を行う。 *************************************
               //*********************************************************************************  

               //PER時系列を描写している
               var per_series = tech.get_per(data,period3)
               draw.getper_seriesline(per_series,x0,x1,indicatorTop2(1)+dim.indicator.height,indicatorTop2(1),dom4,title4,period3)


            }


        }


      //**********************************************************//
      //***************  DRAWクラスの定義を行う *******************//
      //**********************************************************//

        class DRAW {


          //*********************************************************
          // (3-6)  ローソク足を描写する関数
          //*********************************************************


          candle_put = function(data,x,y,yVolume,indicatorPreRoll,xAxis,type,tech){
            //*******************************************************************************************   
            //********************* (4-2) 第1エリアのx軸,y軸の数値範囲設定をする ***************************
            //*******************************************************************************************  

            if(type==2){          //一目均衡表先行スパン1,2のために26日先の日付を元々の株価データdataに追加する。 
              var dataself=data
              data=tech.dateadd(data,26,data[data.length-1].date)
            }

           x.domain(techan.scale.plot.time(data).domain());  //日付のデータを取得しx軸に割り当てている。
           y.domain(techan.scale.plot.ohlc(data.slice(indicatorPreRoll)).domain()); //全期間における株価の最小値と最大値を算出し、y軸に割り当てている。       
           yVolume.domain(techan.scale.plot.volume(data).domain()); //全期間における出来高の最大値を算出し、[0-最大値]をy軸に割り当てている
           svg.select("g.x.axis").call(xAxis); //x軸に日付のデータを加える。




           //*********************************************************************************   
           //******************** (4-3) 第1エリアに描写を行う。 *************************************
           //*********************************************************************************  

           //★★★★
           //☆☆☆☆☆☆☆☆　ろうそく足と出来高の表示を行う  ☆☆☆☆☆☆☆☆
           //★★★★


           svg.select("g.candlestick").datum(data).call(candlestick); //ろうそく足の画像を生成する。
           svg.select("g.volume").datum(data).call(volume); //出来高の画像を生成する。
           svg.select("g.ohlc .axis").call(yAxis);// y軸の描写を行う。
           //svg.select("g.volume.axis").call(volumeAxis);// y軸中のvolume軸の描写を行う。
           svg.select("g.volume").call(volume.refresh);    //  出来高の描写を行う。
           svg.select("g.percent.axis").call(percentAxis);  // y軸中のpresent軸の描写を行う。
           // // ろうそく足の描写を行う。
           // //svg.select("g.candlestick").call(candlestick.refresh);


           //一目均衡表先行スパン1,2のために26日先の日付追加した株価データを追加前の元の状態に戻す。 
            if(type==2){          
              var data=dataself
            }
          } 


          //(1)移動平均(短期、中期、長期)を描写する

         sma_put = function(data,s_period,m_period,l_period,tech){


            var smaday_short = tech.sma_close(data, consts.S_PERIOD)   //close値の移動平均短期を計算している。
            var smaday_middle = tech.sma_close(data, consts.M_PERIOD)   //close値の移動平均短期を計算している。
            var smaday_long = tech.sma_close(data, consts.L_PERIOD)   //close値の移動平均短期を計算している。


            //(2)移動平均のデータを描写する。 

            //(2-1)短期移動平均線描写

            var sma_s = d3.line().x(function(d) { return x(d.date); }).y(function(d) { return y(d.val); });
            ohlcSelection.append("path").datum(smaday_short).attr("class", "lineidou_s").attr("d",sma_s)

            //(2-2)中期移動平均線描写

            var sma_m = d3.line().x(function(d) { return x(d.date); }).y(function(d) { return y(d.val); });

            ohlcSelection.append("path")   
                .datum(smaday_middle)
                .attr("class", "lineidou_m")
                .attr("d",sma_m)

            //(2-3)長期移動平均線描写


            var sma_l = d3.line()    
                .x(function(d) { return x(d.date); })
                .y(function(d) { return y(d.val); });

            ohlcSelection.append("path")   
                .datum(smaday_long)
                .attr("class", "lineidou_l")
                .attr("d",sma_l)
         }

         　//(2)ボリンジャーバンドを描写する。
          bollinger_put = function(boln,data,tech){


            //(1)ボリンジャーバンドデータの計算を実施している。

            var bandsData1 = tech.getBollingerBands(consts.BOL_N, 1, data);  //n:対象とする日数, k: k*σのkを表す, data:対象とするデータを表す。 
            var bandsData2 = tech.getBollingerBands(consts.BOL_N, 2, data);  //n:対象とする日数, k: k*σのkを表す, data:対象とするデータを表す。
            var bandsData3 = tech.getBollingerBands(consts.BOL_N, 3, data);  //n:対象とする日数, k: k*σのkを表す, data:対象とするデータを表す。
            var line = d3.line().x(function(d) { return x(d.date); }).y(function(d) { return y(d.close); });

            //(2)ボリンジャーバンドのデータを描写する。     


            var lowBand = d3.line()
                    .x(function(d) { return x(d.date); })
                    .y(function(d) { return y(d.low); });
            var highBand = d3.line()
                    .x(function(d) { return x(d.date); })
                    .y(function(d) { return y(d.high); });
            var bandsArea = d3.area()  //y0とy1の間を領域と定義している。
                    .x(function(d) { return x(d.date); })
                    .y0(function(d) { return y(d.low); })
                    .y1(function(d) { return y(d.high); })

                ohlcSelection.append("path")
                        .datum(bandsData1)
                        .attr("class", "line bands")
                        .attr("d", lowBand)
                ohlcSelection.append("path")
                        .datum(bandsData2)
                        .attr("class", "line bands")
                        .attr("d", lowBand);
                ohlcSelection.append("path")
                        .datum(bandsData3)
                        .attr("class", "line bands")
                        .attr("d", lowBand); 

                ohlcSelection.append("path")
                        .datum(bandsData1)
                        .attr("class", "line bands")
                        .attr("d", highBand); 
                ohlcSelection.append("path")
                        .datum(bandsData2)
                        .attr("class", "line bands")
                        .attr("d", highBand); 
                ohlcSelection.append("path")
                        .datum(bandsData3)
                        .attr("class", "line bands")
                        .attr("d", highBand); 
                ohlcSelection.append("path")
                        .datum(bandsData2)
                        .attr("class", "area bands")
                        .attr("d", bandsArea);
                ohlcSelection.append("path")
                        .datum(data)
                        .attr("class", "line")
                        .attr("d", line);

         }

          //*********************************************************
          // (3-6)  前日との株価変化率の時系列を算出し、描写する関数(@第2,第3,第4,・・・に描写する関数)
          //*********************************************************

          //y軸の描写設定、実際のデータの描写を行う関数  
          //datsbox:データ
          //x0 : ｘデータ(日付データ)の描写開始座標値
          //x1 : xデータ(日付データ)の描写完了座標値
          // yaxis_min : yデータを描写する座標開始値 
          // yaxis_max : yデータを描写する座標終了値 
          //dom1 :  DOM名 x軸(右側)  描写エリアの指定名
          //title : グラフのタイトル
          get_seriesline(datsbox,x0,x1,yaxis_min,yaxis_max,dom1,title)  {


            var dats = datsbox.variation
            var average = datsbox.average
            var sigma = datsbox.sigma

            //min_val:描写するデータ系列の最小値 , max_val:描写するデータ系列の最大値
            var max_val=d3.max(dats, function(d) { return d.val; })
            var min_val=d3.min(dats, function(d) { return d.val; })


            //*** 第2描写エリア右軸の設定をしている。*******
            indicatorSelection.append("g")
                    .attr("class", "axis right")
                    .attr("transform", "translate(" + x1 + ",0)");//x(0)=0,  x(1)=dim.plot.width  x(1) -> x1
        
            //*** 第2描写エリア左軸の設定をしている。*******
            indicatorSelection.append("g")
                    .attr("class", "axis left")
                    .attr("transform", "translate(" + x0 + ",0)")   //x(0) ->x0

            //*** 第2描写エリアのデータを表示する場所を設定している。*******
            indicatorSelection.append("g")
                    .attr("class", "indicator-plot")
                    .attr("transform", "translate(0,0)");

            //yaxis_min=indicatorTop(0)+dim.indicator.height,    yaxis_max=indicatorTop(0)
              //軸位置の設定,軸の数値範囲の設定を行うヘルパー関数を定義している    //indicatorTop(0)=dim.indicator.top , 
            var n_axisScale = d3.scaleLinear().domain([min_val,max_val]).range([yaxis_min, yaxis_max]);

              //第2描写エリア 右軸の描写設定をしている。
            var n_AxisRight = d3.axisRight(n_axisScale).ticks(5);

              //第2描写エリア 左軸の描写設定をしている。
            var n_AxisLeft = d3.axisLeft(n_axisScale).ticks(5);
              //第2描写エリア 右軸の描写を行う。
            svg.select(dom1 + " .axis.right").call(n_AxisRight); 
              //第2描写エリア 左軸の描写を行う。
            svg.select(dom1 + " .axis.left").call(n_AxisLeft); 
              //yデータをプロットするy座標に変換する関数
            var y2 = d3.scaleLinear().domain([min_val, max_val]).range([yaxis_min, yaxis_max]);

            // average + i*sigma値 に該当するラインを引くためのデータを準備する
            var criteria_u=[       
                [{date: dats[0].date , board : average+sigma},{date: dats[dats.length-1].date , board : average+sigma}],
                [{date: dats[0].date , board : average+2*sigma},{date: dats[dats.length-1].date , board :  average+2*sigma}],
                [{date: dats[0].date , board : average+3*sigma},{date: dats[dats.length-1].date , board :  average+3*sigma}],
              ]

            // average - i*sigma値 に該当するラインを引くためのデータを準備する
            var criteria_d=[       
                [{date: dats[0].date , board : average-sigma},{date: dats[dats.length-1].date , board : average-sigma}],
                [{date: dats[0].date , board : average-2*sigma},{date: dats[dats.length-1].date , board :  average-2*sigma}],
                [{date: dats[0].date , board : average-3*sigma},{date: dats[dats.length-1].date , board :  average-3*sigma}],
              ]

            // ラインを生成するhtmlを生成するためのヘルパー関数を定義する。
            var criteria_line = d3.line()    
                    .x(function(d) { return x(d.date); })
                    .y(function(d) { return y2(d.board); });

            // average + i*sigma値 に該当するラインを描写する。
            criteria_u.forEach( criteria => {
                svg.select(dom1+" .indicator-plot").append("path")　
                    .datum(criteria)
                    .attr("class", "lineblack")
                    .attr("d",criteria_line)
              })

            // average - i*sigma値 に該当するラインを描写する。
            criteria_d.forEach( criteria => {
                svg.select(dom1+" .indicator-plot").append("path")　
                    .datum(criteria)
                    .attr("class", "lineblackdash")
                    .attr("d",criteria_line)
              })


            // 株価の前日との変化率時系列ラインを描写するためのヘルパー関数
            var variationline = d3.line()    
                    .x(function(d) { return x(d.date); })
                    .y(function(d) { return y2(d.val); });

            // 株価の前日との変化率時系列ラインを描写する
            svg.select(dom1+" .indicator-plot").append("path")　
                    .datum(dats)
                    .attr("class", "lineorange")
                    .attr("d",variationline)

            // 株価の前日との変化率値を黒丸で表現している。
            svg.select(dom1+" .indicator-plot").append("g")
                    .selectAll("circle")
                    .data(dats)
                    .enter()
                    .append("circle")
                    .attr("cx", function(d) { return x(d.date); })
                    .attr("cy", function(d) { return y2(d.val); })
                    .attr("fill", "black")
                    .attr("r", 1);

            // "ave + 3*sigma　の文字を描写する"
            svg.select(dom1+" .indicator-plot").append("g")
                  // .attr("transform", "translate(" + x1 + ",0)")
                    .append("text")
                    .style("font-size", 8)
                    .attr("x", x1-100)            
                    .attr("y", y2(criteria_u[2][1].board)-2)
                    .text("ave+" + 3 + "sigma");

            // "ave - 3*sigma　の文字を描写する"
            svg.select(dom1+" .indicator-plot").append("g")
                  // .attr("transform", "translate(" + x1 + ",0)")
                    .append("text")
                    .style("font-size", 8)
                    .attr("x", x1-100)            
                    .attr("y", y2(criteria_d[2][1].board)+7)
                    .text("ave-" + 3 + "sigma");

            svg.select(dom1+" .indicator-plot").append("g")
                  // .attr("transform", "translate(" + x1 + ",0)")
                    .append("text")
                    .attr("class", "symbol")
                    .attr("x", x0)            
                    .attr("y", yaxis_max)
                    .text(title);
          }


          //*********************************************************
          // (3-7)  PERの時系列を算出し、描写する関数(@第2,第3,第4,・・・に描写する関数)
          //*********************************************************

          //y軸の描写設定、実際のデータの描写を行う関数  
          //datsbox:データ
          //x0 : ｘデータ(日付データ)の描写開始座標値
          //x1 : xデータ(日付データ)の描写完了座標値
          // yaxis_min : yデータを描写する座標開始値 
          // yaxis_max : yデータを描写する座標終了値 
          //dom1 :  DOM名 x軸(右側)  描写エリアの指定名
          //title : グラフのタイトル
          getper_seriesline(datsbox,x0,x1,yaxis_min,yaxis_max,dom1,title){


            var dats = datsbox

            //min_val:描写するデータ系列の最小値 , max_val:描写するデータ系列の最大値
            var max_val=d3.max(dats, function(d) { return d.val; })
            var min_val=d3.min(dats, function(d) { return d.val; })


            //*** 第2描写エリア右軸の設定をしている。*******
            indicatorSelection.append("g")
                    .attr("class", "axis right")
                    .attr("transform", "translate(" + x1 + ",0)");//x(0)=0,  x(1)=dim.plot.width  x(1) -> x1
        
            //*** 第2描写エリア左軸の設定をしている。*******
            indicatorSelection.append("g")
                    .attr("class", "axis left")
                    .attr("transform", "translate(" + x0 + ",0)")   //x(0) ->x0

            //*** 第2描写エリアのデータを表示する場所を設定している。*******
            indicatorSelection.append("g")
                    .attr("class", "indicator-plot")
                    .attr("transform", "translate(0,0)");

            //yaxis_min=indicatorTop(0)+dim.indicator.height,    yaxis_max=indicatorTop(0)
              //軸位置の設定,軸の数値範囲の設定を行うヘルパー関数を定義している    //indicatorTop(0)=dim.indicator.top , 
            var n_axisScale = d3.scaleLinear().domain([min_val,max_val]).range([yaxis_min, yaxis_max]);

              //第2描写エリア 右軸の描写設定をしている。
            var n_AxisRight = d3.axisRight(n_axisScale).ticks(5);

              //第2描写エリア 左軸の描写設定をしている。
            var n_AxisLeft = d3.axisLeft(n_axisScale).ticks(5);
              //第2描写エリア 右軸の描写を行う。
            svg.select(dom1 + " .axis.right").call(n_AxisRight); 
              //第2描写エリア 左軸の描写を行う。
            svg.select(dom1 + " .axis.left").call(n_AxisLeft); 
              //yデータをプロットするy座標に変換する関数
            var y2 = d3.scaleLinear().domain([min_val, max_val]).range([yaxis_min, yaxis_max]);

            // PER(MIN)～PER(MAX)までを4分割した線を引くために、データを準備する

            var dw = (max_val-min_val)/4

            var criteria_u=[       
                [{date: dats[0].date , board : min_val},{date: dats[dats.length-1].date , board : min_val}],
                [{date: dats[0].date , board : min_val+dw},{date: dats[dats.length-1].date , board :  min_val+dw}],
                [{date: dats[0].date , board : min_val+2*dw},{date: dats[dats.length-1].date , board : min_val+2*dw}],
                [{date: dats[0].date , board : min_val+3*dw},{date: dats[dats.length-1].date , board : min_val+3*dw}],
                [{date: dats[0].date , board : max_val},{date: dats[dats.length-1].date , board : max_val}]       
              ]



            // ラインを生成するhtmlを生成するためのヘルパー関数を定義する。
            var criteria_line = d3.line()    
                    .x(function(d) { return x(d.date); })
                    .y(function(d) { return y2(d.board); });

            // average + i*sigma値 に該当するラインを描写する。
            criteria_u.forEach( criteria => {
                svg.select(dom1+" .indicator-plot").append("path")　
                    .datum(criteria)
                    .attr("class", "lineblackdash")
                    .attr("d",criteria_line)
              })

            // // average - i*sigma値 に該当するラインを描写する。
            // criteria_d.forEach( criteria => {
            //     svg.select(dom1+" .indicator-plot").append("path")　
            //         .datum(criteria)
            //         .attr("class", "lineblackdash")
            //         .attr("d",criteria_line)
            //    })


            // 株価の前日との変化率時系列ラインを描写するためのヘルパー関数
            var variationline = d3.line()    
                    .x(function(d) { return x(d.date); })
                    .y(function(d) { return y2(d.val); });

            // 株価の前日との変化率時系列ラインを描写する
            svg.select(dom1+" .indicator-plot").append("path")　
                    .datum(dats)
                    .attr("class", "lineorange")
                    .attr("d",variationline)

            // 株価の前日との変化率値を黒丸で表現している。
            svg.select(dom1+" .indicator-plot").append("g")
                    .selectAll("circle")
                    .data(dats)
                    .enter()
                    .append("circle")
                    .attr("cx", function(d) { return x(d.date); })
                    .attr("cy", function(d) { return y2(d.val); })
                    .attr("fill", "black")
                    .attr("r", 1);


            //グラフのタイトルを描写する関数
            svg.select(dom1+" .indicator-plot").append("g")
                  // .attr("transform", "translate(" + x1 + ",0)")
                    .append("text")
                    .attr("class", "symbol")
                    .attr("x", x0)            
                    .attr("y", yaxis_max)
                    .text(title);
          }

          //*********************************************************
          // (3-6)  棒グラフを表示する関数(@第2,第3,第4,・・・に描写する関数)
          //*********************************************************

          //y軸の描写設定、実際のデータの描写を行う関数  
          //min_val:描写するデータ系列の最小値 , max_val:描写するデータ系列の最大値
          //datsbox0:データ
          //x0 : ｘデータ(日付データ)の描写開始座標値
          //x1 : xデータ(日付データ)の描写完了座標値
          // yaxis_min : yデータを描写する座標開始値 
          // yaxis_max : yデータを描写する座標終了値 
          // barchart_property : 棒グラフのプロパティー
          // dom1 : DOM名 x軸(右側)  描写エリアの指定名
          // title : グラフのタイトル
          // period : 棒グラフ表示を開始する場所を指定する。

          get_barline_sma(datsbox0,x0,x1,yaxis_min, yaxis_max,barchart_property,dom1,title,period){



            var dats = datsbox0
            //var average = datsbox.average
            //var sigma = datsbox.sigma
            console.log("dats")
            console.log(dats)
            //console.log("barchart_property")
            //console.log(barchart_property)




            //min_val:描写するデータ系列の最小値 , max_val:描写するデータ系列の最大値
            var max_val=d3.max(dats, function(d) { return d.val; })
            var min_val=d3.min(dats, function(d) { return d.val; })


            //*** 描写エリア右軸の設定をしている。*******
            indicatorSelection.append("g")
                    .attr("class", "axis right")
                    .attr("transform", "translate(" + x1 + ",0)");//x(0)=0,  x(1)=dim.plot.width  x(1) -> x1
        
            //*** 描写エリア左軸の設定をしている。*******
            indicatorSelection.append("g")
                    .attr("class", "axis left")
                    .attr("transform", "translate(" + x0 + ",0)")   //x(0) ->x0

            //*** 描写エリアのデータを表示する場所を設定している。*******
            indicatorSelection.append("g")
                    .attr("class", "indicator-plot")
                    .attr("transform", "translate(0,0)");

            //yaxis_min=indicatorTop(0)+dim.indicator.height,    yaxis_max=indicatorTop(0)
              //軸位置の設定,軸の数値範囲の設定を行うヘルパー関数を定義している    //indicatorTop(0)=dim.indicator.top , 
              var n_axisScale = d3.scaleLinear().domain([min_val,max_val]).range([yaxis_min, yaxis_max]);

              //描写エリア 右軸の描写設定をしている。
              var n_AxisRight = d3.axisRight(n_axisScale).ticks(5);

              //描写エリア 左軸の描写設定をしている。
              var n_AxisLeft = d3.axisLeft(n_axisScale).ticks(5);
              //描写エリア 右軸の描写を行う。
              svg.select(dom1 + " .axis.right").call(n_AxisRight); 
              //描写エリア 左軸の描写を行う。
              svg.select(dom1 + " .axis.left").call(n_AxisLeft); 
              //yデータをプロットするy座標に変換する関数
              var y2 = d3.scaleLinear().domain([min_val, max_val]).range([yaxis_min, yaxis_max]);

              var delta0=barchart_property[0]
              var delta1=barchart_property[1]
              var dw=barchart_property[2]            


            //棒グラフ作成のためのデータを生成する関数。

              var datagenarate_bar=function(dats,delta0,delta1,dw){
              var bulk=[];
              dats.forEach(function(dat,i){

              var xp = function(i) { return delta0+i*(dw+delta1) }
              var yp = function(d) { if (y2(d.val) <= y2(0)) return y2(d.val) ; else if(y2(d.val) > y2(0)) return y2(0) }     


            //棒グラフを作成するパラメータを格納する配列
              bulk.push({
                x:xp(i+period-1), 
                y:yp(dat),
                width:dw,
                height:Math.abs(y2(dat.val)-y2(0))
              })

              })
                   //console.log("bulk")             
                  //console.log(bulk)
                  return bulk
              }



              //棒グラフ作成のためのデータを生成する。
              var datagenarate_barchart=datagenarate_bar(dats,delta0,delta1,dw)



            //棒グラフの表示
              indicatorSelection.append("g")
                .selectAll("rect")
                .data(datagenarate_barchart)
                .enter()
                .append("rect")
                .attr("x", function(d) { return d.x; })
                .attr("y", function(d) { return d.y; })
                .attr("width", function(d) { return d.width; })
                .attr("height", function(d) { return d.height; })
                .attr("fill", "gray");


              svg.select("g.third_area .indicator-plot").append("g")
                  // .attr("transform", "translate(" + x1 + ",0)")
                    .append("text")
                    .attr("class", "symbol")
                    .attr("x", x0)            
                    .attr("y", yaxis_max)
                    .text(title);



             var legendVals = ["もみあい"]
             var iro=['purple']
             let svgdom = svg;  // 描画svg作成  

            if(dats[dats.length-1].val==0){
               this.hanrei_writer_momiai(legendVals,iro,svgdom)
            }


          }


          //*********************************************************
          // (3-6)  棒グラフを表示する関数(@第2,第3,第4,・・・に描写する関数)
          //*********************************************************

          //y軸の描写設定、実際のデータの描写を行う関数  
          //min_val:描写するデータ系列の最小値 , max_val:描写するデータ系列の最大値
          //datsbox0:  close値-open値の移動平均値を計算している。
          //datsbox1:  close値(本日)-close値(昨日)の移動平均値を計算している。
          //x0 : ｘデータ(日付データ)の描写開始座標値
          //x1 : xデータ(日付データ)の描写完了座標値
          // yaxis_min : yデータを描写する座標開始値 
          // yaxis_max : yデータを描写する座標終了値 
          // barchart_property : 棒グラフのプロパティー
          // dom1 : DOM名 x軸(右側)  描写エリアの指定名
          // title : グラフのタイトル
          // period0 : datsbox0,棒グラフ表示を開始する場所を指定する。
          // period1 : datsbox1,棒グラフ表示を開始する場所を指定する。

          get_barline_smad(datsbox0,datsbox1,x0,x1,yaxis_min, yaxis_max,barchart_property,dom1,title,period0,period1){

            var dats0 = datsbox0
            var dats1 = datsbox1


            //console.log("barchart_property")
            //console.log(barchart_property)

            //min_val:描写するデータ系列の最小値 , max_val:描写するデータ系列の最大値
            var max_val0=d3.max(dats0, function(d) { return d.val; })
            var min_val0=d3.min(dats0, function(d) { return d.val; })
            var max_val1=d3.max(dats1, function(d) { return d.val; })
            var min_val1=d3.min(dats1, function(d) { return d.val; })
            var max_val=d3.max([max_val0,max_val1])
            var min_val=d3.min([min_val0,min_val1])



            //*** 描写エリア右軸の設定をしている。*******
            indicatorSelection.append("g")
                    .attr("class", "axis right")
                    .attr("transform", "translate(" + x1 + ",0)");//x(0)=0,  x(1)=dim.plot.width  x(1) -> x1
        
            //*** 描写エリア左軸の設定をしている。*******
            indicatorSelection.append("g")
                    .attr("class", "axis left")
                    .attr("transform", "translate(" + x0 + ",0)")   //x(0) ->x0

            //*** 描写エリアのデータを表示する場所を設定している。*******
            indicatorSelection.append("g")
                    .attr("class", "indicator-plot")
                    .attr("transform", "translate(0,0)");

            //yaxis_min=indicatorTop(0)+dim.indicator.height,    yaxis_max=indicatorTop(0)
              //軸位置の設定,軸の数値範囲の設定を行うヘルパー関数を定義している    //indicatorTop(0)=dim.indicator.top , 
              var n_axisScale = d3.scaleLinear().domain([min_val,max_val]).range([yaxis_min, yaxis_max]);

              //描写エリア 右軸の描写設定をしている。
              var n_AxisRight = d3.axisRight(n_axisScale).ticks(5);

              //描写エリア 左軸の描写設定をしている。
              var n_AxisLeft = d3.axisLeft(n_axisScale).ticks(5);
              //描写エリア 右軸の描写を行う。
              svg.select(dom1 + " .axis.right").call(n_AxisRight); 
              //描写エリア 左軸の描写を行う。
              svg.select(dom1 + " .axis.left").call(n_AxisLeft); 
              //yデータをプロットするy座標に変換する関数
              var y2 = d3.scaleLinear().domain([min_val, max_val]).range([yaxis_min, yaxis_max]);

              var delta0=barchart_property[0]
              var delta1=barchart_property[1]
              var dw=barchart_property[2]            


            //棒グラフ作成のためのデータを生成する関数。

              var datagenarate_bar=function(dats,delta0,delta1,dw,period){
              var bulk=[];
              dats.forEach(function(dat,i){

              var xp = function(i) { return delta0+i*(dw+delta1) }
              var yp = function(d) { if (y2(d.val) <= y2(0)) return y2(d.val) ; else if(y2(d.val) > y2(0)) return y2(0) }     

              bulk.push({
                x:xp(i+period-1), 
                y:yp(dat),
                width:dw,
                height:Math.abs(y2(dat.val)-y2(0))
              })

              })
                  return bulk
              }

              //棒グラフ作成のためのデータを生成する。
              var datagenarate_barchart0=datagenarate_bar(dats0,delta0,delta1,dw,period0)  //SMA 終値-始値 
              var datagenarate_barchart1=datagenarate_bar(dats1,delta0,delta1,dw,period1+1) //SMA 終値(本日)-始値(昨日)


            //棒グラフの表示 (SMA 終値-始値) 
              indicatorSelection.append("g")
                .selectAll("rect")
                .data(datagenarate_barchart0)
                .enter()
                .append("rect")
                .attr("x", function(d) { return d.x; })
                .attr("y", function(d) { return d.y; })
                .attr("width", function(d) { return d.width; })
                .attr("height", function(d) { return d.height; })
                .attr("fill", "gray")
                .attr("fill-opacity", 0.1);

            //棒グラフの表示 (SMA 終値(本日)-始値(昨日)) 
              indicatorSelection.append("g")
                .selectAll("rect")
                .data(datagenarate_barchart1)
                .enter()
                .append("rect")
                .attr("x", function(d) { return d.x; })
                .attr("y", function(d) { return d.y; })
                .attr("width", function(d) { return d.width; })
                .attr("height", function(d) { return d.height; })
                .attr("fill", "green")
                .attr("fill-opacity", 0.1);



            // y軸(左側)にタイトルを表示する
              svg.select(dom1+" .indicator-plot").append("g")
                    .append("text")
                    .attr("class", "symbol")
                    .style("font-size", 8)
                    .attr("x", x0)            
                    .attr("y", y2(max_val))
                    .text(title);




            var legendVals = ["終値-初値のSMA", "終値(前日)-終値(当日)のSMA"]
            var iro=['gray','green']
            var svgdom="g.third_area"
            this.hanrei_writer_second(legendVals,iro,svgdom)



              svg.select(dom1+" .indicator-plot").append("g")
                  // .attr("transform", "translate(" + x1 + ",0)")
                    .append("text")
                    .attr("class", "symbol")
                    .attr("x", x0)            
                    .attr("y", y2(max_val))
                    .text(title);







          }


          //第1領域に凡例を配置する
          hanrei_writer_first(legendVals,iro,svgdom){


            var legend = svg.selectAll('ohlc222').append("g")　// 凡例の領域作成    
                    .data(legendVals)
                    .enter()
                    .append('g')
                    .attr("class", "ohlc")
                    .attr("transform", function (d, i) {
                                {
                                    return "translate(100," + i * -15+ ")" // 各凡例をy方向に20px間隔で移動
                                }
              })                            //ohlcSelection
            legend.append('text')  // 凡例の文言
                  .attr("x", 20)
                  .attr("y", 10)
                  .text(function (d, i) {	return d ; })
                  .style("text-anchor", "start")
                  .style("font-size", 15)
                  .style("fill", function (d, i) { return iro[i]  });


          }

          //第2領域に凡例を配置する
          hanrei_writer_second(legendVals,iro,svgdom){

            var leg= svg.selectAll(svgdom+" .indicator-plot")
                  .data(legendVals)
                  .attr("class", "leg")
                  .append('text')
                  .attr("x", x1-500)
                  .attr("y", function (d, i){ return 530-15*i})
                  .text(function (d, i){ return d})
                  .style("font-size", 10)
                  .style("fill", function (d, i) { return iro[i]  });
          }

          //第1領域に「もみあい」文字を配置する
          hanrei_writer_momiai(legendVals,iro,svgdom){

            var legend = svg.selectAll('ohlc222').append("g")　// 凡例の領域作成    
                    .data(legendVals)
                    .enter()
                    .append('g')
                    .attr("class", "ohlc")
                    .attr("transform", function (d, i) {
                                {
                                    return "translate(900," + i * -15+ ")" // 各凡例をy方向に20px間隔で移動
                                }
              })                            //ohlcSelection
            legend.append('text')  // 凡例の文言
                  .attr("x", 20)
                  .attr("y", 10)
                  .text(function (d, i) {	return d ; })
                  .style("text-anchor", "start")
                  .style("font-size", 40)
                  .style("fill", function (d, i) { return iro[i]  });
          } 
 


 
          //(3)一目均衡表を描写する。ichimoku(data,consts.TENKAN_DELAY,consts.KIJYUN_DELAY,consts.CHIKOU_DELAY,consts.SENKOU1,consts.SENKOU2_P,consts.SENKOU2_F)

          ichimoku_put = function(data,tenkan_delay,kijyun_delay,chikou_delay,senkou1,senkou2_p,senkou2_f,tech){
              //(1)一目均衡表のデータを計算している。            
            var ichimoku_dat = tech.ichimoku(data,tenkan_delay,kijyun_delay,chikou_delay,senkou1,senkou2_p,senkou2_f)

                //[tenkan_box,kijyun_box,chikou_box,kumo_box,hanteibox]
              //(2)一目均衡表のデータを描写する。 


            var tenkanline = d3.line()    //転換線描写設定
                  .x(function(d) { return x(d.date); })
                  .y(function(d) { return y(d.tenkan); });

            ohlcSelection.append("path")   //htmlに転換線描写を追加する。
                  .datum(ichimoku_dat[0])
                  .attr("class", "line")
                  .attr("d",tenkanline)



            var kijyunline = d3.line()   //基準線
                  .x(function(d) { return x(d.date); })
                  .y(function(d) { return y(d.kijyun); });

            ohlcSelection.append("path")　//htmlに基準線描写を追加する。
                  .datum(ichimoku_dat[1])
                  .attr("class", "linepurple")
                  .attr("d",kijyunline)



            var chikouline = d3.line()   //遅行線
                  .x(function(d) { return x(d.date); })
                  .y(function(d) { return y(d.chikou); });

            ohlcSelection.append("path")　//htmlに遅行線描写を追加する。
                  .datum(ichimoku_dat[2])
                  .attr("class", "lineorange")
                  .attr("d",chikouline)



            var senkou1line = d3.line()   //先行スパン1
                  .x(function(d) { return x(d.date); })
                  .y(function(d) { return y(d.senkou1); });

            ohlcSelection.append("path")　//htmlに先行スパン1線描写
                  .datum(ichimoku_dat[3])
                  .attr("class", "linespan1")
                  .attr("d",senkou1line)


            var senkou2line = d3.line()   //先行スパン2
                    .x(function(d) { return x(d.date); })
                    .y(function(d) { return y(d.senkou2); });

            ohlcSelection.append("path")　//htmlに先行スパン2線描写
                  .datum(ichimoku_dat[3])
                  .attr("class", "linespan2")
                  .attr("d",senkou2line)


            var kumoArea = d3.area()  //雲を描く設定をしている。
                  .x(function(d) { return x(d.date); })
                  .y0(function(d) { return y(d.senkou1); })
                  .y1(function(d) { return y(d.senkou2); })
                  
            ohlcSelection.append("path")
                  .datum(ichimoku_dat[3])
                  .attr("class", "area bands")
                  .attr("d", kumoArea);


            var legendVals = ["転換線", "基準線", "遅行スパン","先行スパン1(実線)","先行スパン2(点線)"]
            var iro=['black','purple','orange','#3b0666','#3b0666']
            let svgdom = svg;  // 描画svg作成  

            this.hanrei_writer_first(legendVals,iro,svgdom) //凡例を描写する。



          }

        }


      //***** (4-2)ろうそく足の上にカーソルがoverしたときに日付とclose値を表示させる関数 ******//


        //(4-2-1)【ヘルパー関数】ろうそく足の上にカーソルがoverしたときに日付とclose値を表示させる
        function display_dayclose(n){
          var pathd0=document.getElementsByClassName('volume')[0].getElementsByClassName('data')[0].innerHTML
          var class_sep= splitString (pathd0,'down')  // path class="volume down"の前後で分割する。
          var class_sep_div0=splitString (class_sep[0],' ')   // path class="volume down"の前の要素をスペースで区切り配列に格納する
           //console.log("class_sep_div0")    
           //console.log(class_sep_div0)  
          var class_sep_div1=splitString (class_sep[1],' ')   // path class="volume down"の後の要素をスペースで区切り配列に格納する
           //console.log("class_sep_div1")   
           //console.log(class_sep_div1)

          var tmparray=[parseFloat(class_sep_div0[4]),parseFloat(class_sep_div0[16]),parseFloat(class_sep_div1[2]),parseFloat(class_sep_div1[14])]

          // console.log("tmparray0")   
          // console.log(tmparray)

            tmparray.sort(function(a, b){  //配列の要素を小さい順に並び替えを行う。
                if(a < b) return -1;
                else if(a > b) return 1;
                else return 0;
            });

          // console.log("tmparray1")   
          // console.log(tmparray)

          var delta0=parseFloat(tmparray[0])
          var second_sp=parseFloat(tmparray[1])
          var dw=parseFloat(class_sep_div1[8])
          //var first_ep = parseFloat(Math.min( Math.max(class_sep_div0[4],class_sep_div1[2]) ,  class_sep_div0[16] ))+dw
          //var second_sp = parseFloat(class_sep_div1[14]/2-dw)
          //var tmp=Math.max(class_sep_div1[14],class_sep_div0[16])
          
          //second_spの取得がうまくいかず、delta1の値が正しく求まらない場合はwidth=1160からdelta1を逆算している。
          var delta1=second_sp-delta0-dw<1? second_sp-delta0-dw : (1160-dw*n-2*delta0)/(n-1) //0.4461
          //var delta1=second_sp-delta0-dw
          var width=dw*n+delta1*(n-1)+2*delta0
          // console.log("delta0")
          // console.log(delta0)
           //console.log("dw")
           //console.log(dw)
           //console.log("delta1")
           //console.log(delta1)
          // console.log("second_sp")
          // console.log(second_sp)
          // console.log("n")
          // console.log(n)
          // console.log("width")
          // console.log(width)
          return [delta0,delta1,dw,n]
        }

          //(4-2-2)【ヘルパー関数】文字列を指定した文字で分割し、配列に格納する
        function splitString (stringToSplit,separator) {
          var arrayOfStrings = stringToSplit.split(separator);
          return arrayOfStrings;
        }


          //(4-2-3)【ヘルパー関数】マウスオーバーした場所が何番目のデータであるかを算出する
        var sol_get = function(n0,delta0,delta1,dw,nmax){

          if ( n0 < delta0 + dw + 0.5*delta1 ){
                var eq_n=1
          }else{
                eq_n = Math.floor((1/(dw+delta1))*(n0+delta1/2-delta0)+1)
          }

          if(eq_n>nmax)   eq_n = nmax
                return eq_n
          }


          //(4-2-4)ろうそく足にカーソルを重ねたときに、日にちと終値を表示させる。
          var dataput=function(data){        
          var positionLabel = svg.append("text")
          .attr("id",1)
          .attr("x",10)
          .attr("y",10) // positionLabelオブジェクト  <text x=posX, y=posY, id=1>(日にち,終値)</text>を生成する。
          .attr("font-weight","bold");
          var pos=svg.on("mousemove", function(){

                        var posX=d3.mouse(this)[0]
                        var posY=d3.mouse(this)[1]
                        var datlength=data.length
                        var val =display_dayclose(datlength)
                        var delta0=val[0]
                        var delta1=val[1]
                        var dw=val[2]
                        var nmax=val[3]
                        var num = sol_get(posX,delta0,delta1,dw,data.length)
                        //console.log("num")
                        //console.log(num)
                        positionLabel  
                        .attr("x",posX-100)
                        .attr("y",posY-10)
                        //console.log(timeForm(data[num-1].date))
                        //console.log(data[num-1].close)
                        positionLabel.text([timeForm(data[num-1].date),  "close:" + data[num-1].close])
                        //positionLabel.text(d3.mouse(this)); //座標を表示する。(for debug)
                        
                });
        }


    }

  }


}

</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
    body {
        font: 10px sans-serif;
    }

    text {
        fill: #000;
    }

    text.symbol {
        fill: #BBBBBB;
    }

    path {
        fill: none;
        stroke-width: 1;
    }

    path.candle {
        stroke: #000000;
    }

    path.candle.body {
        stroke-width: 0;
    }

    path.candle.up {
        fill: #00AA00;
        stroke: #00AA00;
    }

    path.candle.down {
        fill: #FF0000;
        stroke: #FF0000;
    }

    .close.annotation.up path {
        fill: #00AA00;
    }

    path.volume {
        fill: #DDDDDD;
    }

    .indicator-plot path.line {
        fill: none;
        stroke-width: 1;
    }

    .ma-0 path.line {
        stroke: #1f77b4;
    }

    .ma-1 path.line {
        stroke: #aec7e8;
    }

    .ma-2 path.line {
        stroke: #ff7f0e;
    }

    button {
        position: absolute;
        right: 110px;
        top: 25px;
    }

    path.macd {
        stroke: #0000AA;
    }

    path.signal {
        stroke: #FF9999;
    }

    path.zero {
        stroke: #BBBBBB;
        stroke-dasharray: 0;
        stroke-opacity: 0.5;
    }

    path.difference {
        fill: #BBBBBB;
        opacity: 0.5;
    }

    path.rsi {
        stroke: #000000;
    }

    path.overbought, path.oversold {
        stroke: #FF9999;
        stroke-dasharray: 5, 5;
    }

    path.middle, path.zero {
        stroke: #BBBBBB;
        stroke-dasharray: 5, 5;
    }

    .analysis path, .analysis circle {
        stroke: blue;
        stroke-width: 0.8;
    }

    .trendline circle {
        stroke-width: 0;
        display: none;
    }

    .mouseover .trendline path {
        stroke-width: 1.2;
    }

    .mouseover .trendline circle {
        stroke-width: 1;
        display: inline;
    }

    .dragging .trendline path, .dragging .trendline circle {
        stroke: darkblue;
    }

    .interaction path, .interaction circle {
        pointer-events: all;
    }

    .interaction .body {
        cursor: move;
    }

    .trendlines .interaction .start, .trendlines .interaction .end {
        cursor: nwse-resize;
    }

    .supstance path {
        stroke-dasharray: 2, 2;
    }

    .supstances .interaction path {
        pointer-events: all;
        cursor: ns-resize;
    }

    .mouseover .supstance path {
        stroke-width: 1.5;
    }

    .dragging .supstance path {
        stroke: darkblue;
    }

    .crosshair {
        cursor: crosshair;
    }

    .crosshair path.wire {
        stroke: #DDDDDD;
        stroke-dasharray: 1, 1;
    }

    .crosshair .axisannotation path {
        fill: #DDDDDD;
    }

    .tradearrow path.tradearrow {
        stroke: none;
    }

    .tradearrow path.buy {
        fill: #0000FF;
    }

    .tradearrow path.sell {
        fill: #9900FF;
    }

    .tradearrow path.highlight {
        fill: none;
        stroke-width: 2;
    }

    .tradearrow path.highlight.buy {
        stroke: #0000FF;
    }

    .tradearrow path.highlight.sell {
        stroke: #9900FF;
    }


/*********  移動平均 css **********/  

    .lineidou_s {
    fill: none;
    stroke: black;
    stroke-width: 0.7px;
   }

    .lineidou_m {
    fill: none;
    stroke: blue;
    stroke-width: 0.7px;
   }

    .lineidou_l {
    fill: none;
    stroke: purple;
    stroke-width: 0.7px;
   }



/******** ichimoku css ***********/


    .line {
    fill: none;
    stroke: black;
    stroke-width: 0.5px;
   }

    .linered {
    fill: none;
    stroke: red;
    stroke-width: 0.5px;
   }

    .linepurple {
    fill: none;
    stroke: purple;
    stroke-width: 1.2px;
   }

    .lineblack {
    fill: none;
    stroke: black;
    stroke-width: 0.5px;
   }

   .lineblackdash {
    fill: none;
    stroke: black;
    stroke-dasharray: 0.9;
   }



    .lineorange {
    fill: none;
    stroke: orange;
    stroke-width: 0.5px;
   }

  .linespan1 {
    stroke: #3b0666;
    stroke-opacity: 1.0;
    stroke-width: 0.5px;
  }

 .linespan2 {
    stroke: #3b0666;
    stroke-opacity: 1.0;
    stroke-dasharray: 0.9;
  }

  .area.bands {
    fill: #6c949f;
    fill-opacity: 0.3;
    stroke: none;
  }

/*****-- other css  *********/

  .line.bands {
    stroke: black;
    stroke-opacity: 1.0;
    stroke-dasharray: 0.9;
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

/***** waku css  *********/

.box2 {
    padding: 0.5em 1em;
    margin: 2em 0;
    font-weight: bold;
    color: #6091d3;/*文字色*/
    background: #FFF;
    border: solid 3px #6091d3;/*線*/
    border-radius: 10px;/*角の丸み*/
}
.box2 p {
    margin: 0; 
    padding: 0;
}


.float_test150 {
    height: 150px;              /* 高さ指定 */
    width: 150px;               /* 幅指定 */
    background-color: #FFF;     /* 背景色指定 */
    margin:  10px;              /* 周りの余白指定 */
    float:  right;   /* 回り込み指定 */
    border: solid 3px #6091d3;/*線*/
    border-radius: 10px;/*角の丸み*/
}

.float_test300 {
    height: 150px;              /* 高さ指定 */
    width: 300px;               /* 幅指定 */
    background-color: #FFF;     /* 背景色指定 */
    margin:  10px;              /* 周りの余白指定 */
    float:  right;   /* 回り込み指定 */
    border: solid 3px #6091d3;/*線*/
    border-radius: 10px;/*角の丸み*/
}

.float_test150r {
    height: 150px;              /* 高さ指定 */
    width: 150px;               /* 幅指定 */
    background-color: #FFF;     /* 背景色指定 */
    margin:  10px;              /* 周りの余白指定 */
    clear:  right;   /* 回り込み指定 */
    border: solid 3px #6091d3;/*線*/
    border-radius: 10px;/*角の丸み*/
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
