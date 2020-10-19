// eslint-disable-next-line
/* eslint-disable */ 

import * as d3 from 'd3'  //有効にする
const consts = require('./components/const')
const INITIAL_AF=0.02
const MAX_AF=0.2

var RATING=consts.RATING
var DURING=consts.MOMIAI

class TECH{

    constructor(n){
    this.n=n
    }

    //本日の株価と前日との差分を取得する。


    get_newdata(data){

          var today_data      = data[data.length-1].close
          var yesterday_data  = data[data.length-2].close
          return {today:today_data, dif:today_data-yesterday_data,}

      }

    //前日との変化率2乗の移動平均線
    sma_val2get(data, period) {   
      let bands = []; //{ ma: 0, low: 0, high: 0 }
      for (var i = 0, len = data.length; i < len-period+1; i++) {
          var slice = data.slice(i, i+period);
          var mean = d3.mean(slice, function(d) { return d.val});
          bands.push({ date: data[i+period-1].date,
                        val: mean
                        });
        }
        return bands;
  }



    //SMA close値の移動平均線
    sma_close(data, period) {  //n:対象とする日数, k: k*σのkを表す, data:対象とするデータを表す。 
        let bands = []; //{ ma: 0, low: 0, high: 0 }
        for (var i = 0, len = data.length; i < len-period+1; i++) {
            var slice = data.slice(i, i+period);
            var mean = d3.mean(slice, function(d) { return d.close});
            bands.push({ date: data[i+period-1].date,
                          val: mean
                          });
          }
          return bands;
    }

    //SMA close(本日) - close(昨日)
    sma_ct_cy(data, period) {  //n:対象とする日数, k: k*σのkを表す, data:対象とするデータを表す。 
          var bands = []; //{ ma: 0, low: 0, high: 0 }
          var temp = [];
  
          for (var i = 0, len = data.length; i < len-1; i++) {

              temp.push({ date: data[i+1].date,
                          val: data[i+1].close-data[i].close
                          });
          }
          for (var i = 0, len = temp.length; i < len-period+1; i++) {
              var slice = temp.slice(i, i+period);
              var mean = d3.mean(slice, function(d) { return d.val});
              bands.push({ date: temp[i+period-1].date,
                            val: mean
                            });
          }
            //console.log("bands")
            //console.log(bands)
          return bands;
    }

    //SMA open->close差値の移動平均線
    sma_close_open(data, period) {  //n:対象とする日数, k: k*σのkを表す, data:対象とするデータを表す。 
          let bands = []; //{ ma: 0, low: 0, high: 0 }
          for (var i = 0, len = data.length; i < len-period+1; i++) {
              var slice = data.slice(i, i+period);
              var mean = d3.mean(slice, function(d) { return d.close - d.open});
              bands.push({ date: data[i+period-1].date,
                          val: mean
                          });
          }
          return bands;
    }

    //SMA(中期)と株価の乖離率
    sma_kairi(data,period){

    let sma_middle = []
    let bulk=[]
    sma_middle = this.sma_close(data, period)
    sma_middle.forEach(function(sma_mid,i){

    bulk.push({ date: data[i+period-1].date,
                val: 100*(data[i+period-1].close-sma_mid.val)/sma_mid.val
                          });

    })

    return bulk

    }


    //************ variationの計算 *******************//f=0の場合closeを取り出し
    val_get(data,f,rate_th){
      var bands=[];
      var bands2=[];
        for (var i=0 ; i<data.length-1; i++ ){
        var temp=data.slice(i,i+2)
        var change_rate
        if (f==0){
               change_rate=(temp[1].close/temp[0].close -1)*100
               bands.push({ date: data[i+1].date,
                  val: change_rate,
                        });
               bands2.push({ date: data[i+1].date,
                              val:change_rate*change_rate
                        });                      
            }
      //もみ合い判定に使用する      
         else if (f==1) { change_rate=Math.pow((temp[1].kijyun/temp[0].kijyun -1),2) }
         bands.push({ date: data[i+1].date,
                             val: change_rate
                                                 });
           }

      let sig=d3.deviation(bands,function(d){ return d.val})
      let ave=d3.mean(bands,function(d){ return d.val})

 

      let val_get_box= {variation:bands,
                          average:ave,
                          sigma:sig}

      //当日と前日株価との変化率2乗したものを算出している。
      let val2_get_box= bands2
      
      //当日と前日株価との変化率2乗の移動平均をかけている。
      let sma_val2box=this.sma_val2get(val2_get_box,consts.VAL2_SMA)

      console.log("val2_get_box")
      console.log(val2_get_box)
      console.log("sma_val2box")
      console.log(sma_val2box)

      return [val_get_box,sma_val2box]
    } 


    //************ PERの計算 *******************// 
    get_per(data,hitokabueki){
      var bands=[];
        for (var i=0; i<data.length; i++){
        bands.push({date: data[i].date,
                    val: data[i].close/hitokabueki
                  })
        }
      return bands
    }


    //************ もみ合い判定関数 *******************// 
    momiai(data,delay_kijyun){
      //var tenkan_box=[];
      var kijyun_box=[];
      //var chikou_box=[];
      //var senkou1_box=[];
      //var senkou2_box=[];
      var momiai_box=[];

      //最新日付後に25日ダミーデータを追加する。(計算の都合) 
      var dataself=data
      data=this.dateadd(data,consts.SENKOU1,data[data.length-1].date)


      //tenkan_box=this.tenkan(data,delay_tenkan)
      //console.log(tenkan_box)
      //console.log("tenkan_box")
      kijyun_box=this.kijyun(data,delay_kijyun)
      //console.log(kijyun_box)
      //console.log("kijyun_box")         
      //chikou_box=this.chikou(data,delay_chikou)
      //senkou1_box=this.senkou1(data,tenkan_box,kijyun_box,delay_senkou1,delay_tenkan,delay_kijyun)
      //console.log("senkou1_box")
      //console.log(senkou1_box)          
      //senkou2_box=this.senkou2(data,delay_senkou2,future_senkou2)
      //console.log("senkou2_box")
      //console.log(senkou2_box)          

      momiai_box=this.det_momiai(kijyun_box,RATING,DURING)

      //console.log("momiai_box")
      //console.log(momiai_box)  



      data=dataself

      return momiai_box


  }





    //***** (4-4)一目均衡表 **************************//  GO 561
    ichimoku(data,delay_tenkan,delay_kijyun,delay_chikou,delay_senkou1,delay_senkou2,future_senkou2){
          var tenkan_box=[];
          var kijyun_box=[];
          var chikou_box=[];
          var senkou1_box=[];
          var senkou2_box=[];
   

          tenkan_box=this.tenkan(data,delay_tenkan)
          //console.log(tenkan_box)
          //console.log("tenkan_box")
          kijyun_box=this.kijyun(data,delay_kijyun)
          //console.log(kijyun_box)
          //console.log("kijyun_box")         
          chikou_box=this.chikou(data,delay_chikou)
          senkou1_box=this.senkou1(data,tenkan_box,kijyun_box,delay_senkou1,delay_tenkan,delay_kijyun)
          //console.log("senkou1_box")
          //console.log(senkou1_box)          
          senkou2_box=this.senkou2(data,delay_senkou2,future_senkou2)
          //console.log("senkou2_box")
          //console.log(senkou2_box)          


          var kumo_box=[];

          for (var i = 0, len = data.length-(delay_senkou2+future_senkou2); i < len+2; i++){
          kumo_box.push({ 
                  date: data[i+delay_senkou2+future_senkou2-2].date,
                  senkou1:senkou1_box[i+delay_senkou2+future_senkou2-delay_kijyun-delay_senkou1].senkou1,
                  senkou2:senkou2_box[i].senkou2
          })

          }


      return [tenkan_box,kijyun_box,chikou_box,kumo_box]


    }


    tenkan(data,delay){  //転換線の算出関数    
          let val_box=[];
          let datah=[]; //dateとhigh値のみの株価配列を準備する
          let datal=[]; //dateとlow値のみの株価配列を準備する
          data.forEach( element =>  datah.push({date:element.date, high:element.high})  ) //dateとhigh値のみを取り出す
          data.forEach( element =>  datal.push({date:element.date, low:element.low})  )  //dataとlow値のみを取り出す
          for(let i=delay ; i<=data.length-25 ; i++) {
          var pickuph=datah.slice(i-delay,i)
          var pickupl=datal.slice(i-delay,i)
          //let pickupl=data.slice(i-delay,i)              
          let get_min=d3.min(pickupl,function(d){return d.low})
          let get_max=d3.max(pickuph,function(d){return d.high})
          let get_val=(get_min+get_max)/2
          val_box.push({
                  date: data[i-1].date,
                  tenkan:get_val
          })
          }       
          return val_box
    }

    kijyun(data,delay){  //基準線の算出関数
          let val_box=[];
          let datah=[]; //dateとhigh値のみの株価配列を準備する
          let datal=[]; //dateとlow値のみの株価配列を準備する
          data.forEach( element =>  datah.push({date:element.date, high:element.high})  ) //dateとhigh値のみを取り出す
          data.forEach( element =>  datal.push({date:element.date, low:element.low})  )  //dataとlow値のみを取り出す
          for(let i=delay ; i<=data.length-25 ; i++) {
          let pickuph=datah.slice(i-delay,i)
          let pickupl=datal.slice(i-delay,i)
          let get_min=d3.min(pickupl,function(d){return d.low})
          let get_max=d3.max(pickuph,function(d){return d.high})
          let get_val=(get_min+get_max)/2
          val_box.push({
                  date: data[i-1].date,
                  kijyun:get_val
          })
          }
          return val_box
    }


    chikou(data,delay){  //遅行スパンの算出関数
          let val_box=[];
          //data = data.slice(0, datlength).map(function(d) {return d.close});
          for(let i=delay ; i<=data.length-25 ; i++) {
          val_box.push({
                  date: data[i-delay].date,
                  chikou:data[i-1].close
          })
          }
          return val_box
    }

    //株式データにd日先の日付を追加で付加する関数
    dateadd(data,d,latestdate){
      for(let i=1;i<d;i++){
 
            var newdate = new Date(latestdate.getFullYear(), latestdate.getMonth(), latestdate.getDate(), 20, 30)
            var dummy=data[data.length-1].close
            data.push({
                  date: new Date(newdate.setDate(newdate.getDate()+i)),                
                  close: dummy,
                  open: dummy,
                  high: dummy,
                  low: dummy,
                  volume: 0             
            })
 
      }
      

      return data
    }



    senkou1(data,tenkan_box,kijyun_box,s_delay,t_delay,k_delay){  //先行スパン1の算出関数
      
          var val_box_t=[];
          var val_box_k=[];
          val_box_t=tenkan_box; //転換線データ収容
          val_box_k=kijyun_box; //基準線データ収容
          let val_box=[]; //先行スパン1データ収容       
          for(let i=k_delay ; i<data.length-k_delay-23+25 ; i++) {           
          val_box.push({
                  date: data[i+s_delay-2].date,
                  senkou1:(val_box_t[i-t_delay].tenkan+val_box_k[i-k_delay].kijyun)/2
          })
      
          }          
          return val_box
    }


    senkou2(data,delay,future){  //先行スパン2の算出関数
          let val_box=[];
          let datah=[]; //dateとhigh値のみの株価配列を準備する
          let datal=[]; //dateとlow値のみの株価配列を準備する
          data.forEach( element =>  datah.push({date:element.date, high:element.high})  ) //dateとhigh値のみを取り出す
          data.forEach( element =>  datal.push({date:element.date, low:element.low})  )  //dataとlow値のみを取り出す
          for(let i=delay ; i<data.length-future+2 ; i++) {
            let pickuph=datah.slice(i-delay,i)
            let pickupl=datal.slice(i-delay,i)
            let get_min=d3.min(pickupl,function(d){return d.low})
            let get_max=d3.max(pickuph,function(d){return d.high})
            let get_val=(get_min+get_max)/2
            val_box.push({
                  date: data[i+future-2].date,
                  senkou2:get_val
            })
  
          }
          return val_box
    }

      //銘柄の状態がもみ合いかを判定する関数
    det_momiai(data,rating,during){ 
      //console.log("det_momiai")    
      //console.log(data)    
      var variation_kijyun=this.val_get(data,1)[0]
      //console.log("variation_kijyun")     
      //console.log(variation_kijyun.variation)
      var var_kijyun_vari=variation_kijyun.variation

      var bunds=[]
      var tmp=[]
      var hanteibox=[]
      var cont=0
      var_kijyun_vari.forEach(function(element,k){         
             tmp.push({ 
                   date: element.date,
                   th:element.val>Math.pow(rating,2)? 1:0
           })
            return tmp
                })
                //console.log("tmp")
                //console.log(tmp)
                //console.log(tmp.slice(0,during))
            
            for(let i=0 ; i<=tmp.length-during-consts.KIJYUN_DELAY+1 ; i++) {
                  cont=0
                  bunds=tmp.slice(i,i+during)
                  //console.log("checkbunds")
                  //console.log(bunds)
                  bunds.forEach(element => cont=cont+element.th )

                 
                  hanteibox.push({
                          date: bunds[during-1].date,
                          val:cont==0?0:1
                  })
             
                  }

                  //console.log("hanteibox")
                  //console.log(hanteibox)

          return hanteibox

    }


    //***********************************************// 
    //***** (4-3)ボリンジャーバンドを計算する関数 ******//
    //***********************************************//

    getBollingerBands(n, k, data) {  //n:対象とする日数, k: k*σのkを表す, data:対象とするデータを表す。 
          var bands = []; //{ ma: 0, low: 0, high: 0 }
          for (var i = n - 1, len = data.length; i < len; i++) {
              var slice = data.slice(i + 1 - n , i);
              var mean = d3.mean(slice, function(d) { return d.close; });
              var stdDev = Math.sqrt(d3.mean(slice.map(function(d) {
                  return Math.pow(d.close - mean, 2);
              })));
              bands.push({ date: data[i].date,
                          ma: mean,
                          low: mean - (k * stdDev),
                          high: mean + (k * stdDev) });
          }
          return bands;
    }


    //***********************************************// 
    //***** パラボリック解析を行う ******//
    //***********************************************//

    paraboric(data){
      let candles=data
      //console.log('candles')
      //console.log(candles)
      var acceleration_factor = INITIAL_AF
      let bull = true
      let extreme_price = candles[0].high
      let temp_sar_array =  [{date:candles[0].date, sar:candles[0].low}]
      let temp_sar 
      //console.log('extreme_price:',extreme_price)

      candles.forEach(function(ele,k){

            var current_high = ele.high
            var current_low =  ele.low
            var last_sar = temp_sar_array[temp_sar_array.length-1].sar
            var current_date = ele.date

            if((bull==true  &&  last_sar > current_low) || (bull==false  &&  last_sar < current_high)){
                  //console.log("touch:",k)
                  temp_sar = extreme_price
                  acceleration_factor = INITIAL_AF
                  if(bull==true){
                        bull = false
                        extreme_price = current_low
                  } else {
                        bull = true
                        extreme_price = current_high
                  }     

            }else{
                  temp_sar = last_sar + acceleration_factor * (extreme_price - last_sar )
                  //console.log("nontouch:",k)  
                  //console.log("acceleration_factor:",acceleration_factor)                    
                  //console.log("extreme_price:",extreme_price)  
                  //console.log("last_sar:",last_sar) 
                   
      




                  if((bull==true  &&  extreme_price  < current_high) || (bull==false  && extreme_price  > current_low)){
                        //console.log("acceleration_factor_tmp:",acceleration_factor)
                        acceleration_factor = Math.min(acceleration_factor + INITIAL_AF, MAX_AF)

                        //console.log("acceleration_factor revise:",k)  
                        //console.log("acceleration_factor:",acceleration_factor) 
                  }
                  if(k>1){
                        if(bull==true){
                              //console.log("TRUE",k)                             
                              temp_sar =  Math.min(temp_sar, candles[k-1].low, candles[k-2].low)
                              extreme_price = Math.max(extreme_price, current_high)
                        }else{
                              //console.log("FALSE",k)
                              temp_sar =  Math.max(temp_sar, candles[k-1].high, candles[k-2].high)
                              extreme_price = Math.min(extreme_price, current_low)

                        }
                  }      
                  

            }

            if(k==0){
                  temp_sar_array[temp_sar_array.length-1] = ({date:ele.date, sar:temp_sar})
            }else{
                  temp_sar_array.push({date:ele.date, sar:temp_sar})
            }
      });

      console.log('temp_sar_array:',temp_sar_array)
      return temp_sar_array

    }



  }


export default TECH