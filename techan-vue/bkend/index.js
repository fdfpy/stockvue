const express = require('express')
const bodyParser = require('body-parser')
const fs = require('fs')
const JSONFILEPATH="/home/stock/stockdata.json"
const JSONDELPATH="/home/stock/stockdel.json"
const PYPATH="/home/stock/sqltest.py"
const PYDELPATH="/home/stock/sqldel.py"
const CSVPATH="/home/stock/stockdata.csv"
const MEIGARA_PATH="/home/stock/read.csv"
const CSV_KAKUSYUPATH='/home/stock/kakusyudat.csv'

const app = express()
app.use(bodyParser.json())

//CORSポリシーを無効にしている。
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});


//【R-1】銘柄登録を行う。
app.get('/reg', function(req, res) {

  var {PythonShell} = require('python-shell');
  var pyshell = new PythonShell(PYPATH, { mode: 'text'});  

  //データの形式チェックを実施している。NGデータの場合フロントエンドにNGメッセージを送り返す
  //★★★ 銘柄パラメータを増やすときに追記する箇所★★★   
  if (req.query.stock_num==0 || req.query.stock_num==''){
    let csvobj_reg=fs.readFileSync(CSVPATH,'utf-8') //エラー時処理のためcsvobj_regを取得している。
    res.send({      
      message:          
      {
        "mes":"(銘柄番号) 銘柄番号が0、もしくは空白",
        "stockdata":[
          csvobj_reg
                    ]
      }   
    })
  }
  else if(req.query.c_name==''){
    let csvobj_reg=fs.readFileSync(CSVPATH,'utf-8')  
    res.send({

      message:          
      {
        "mes":"(会社名) 会社名が空白",
        "stockdata":[
          csvobj_reg
                    ]
      } 


    })
  }
  else if(req.query.eps=='' || isNaN(req.query.eps)==true){
    let csvobj_reg=fs.readFileSync(CSVPATH,'utf-8')  

    res.send({

      message:          
      {
        "mes":"(一株益) 入力値が空白、もしくは数値型ではない",
        "stockdata":[
          csvobj_reg
                    ]
      } 
 
    })
  }

  else if(req.query.kessan==''){
    let csvobj_reg=fs.readFileSync(CSVPATH,'utf-8')  
    res.send({


      message:          
      {
        "mes":"(決算日)入力値が空白",
        "stockdata":[
          csvobj_reg
                    ]
      } 
    })
  }

  else if(req.query.url==''){
    let csvobj_reg=fs.readFileSync(CSVPATH,'utf-8')  
    res.send({
      message:          
      {
        "mes":"(会社URL)入力値が空白",
        "stockdata":[
          csvobj_reg
                    ]
      } 
    })
  }

  else if(req.query.haitoub=='' || isNaN(req.query.haitoub)==true){
    let csvobj_reg=fs.readFileSync(CSVPATH,'utf-8')  
    res.send({
      message:          
      {
        "mes":"(配当)入力値が空白もしくは数値型ではない",
        "stockdata":[
          csvobj_reg
                    ]
      } 
    })
  }  

  else if(req.query.kaisya==''){
    let csvobj_reg=fs.readFileSync(CSVPATH,'utf-8')  
    res.send({
      message:          
      {
        "mes":"(会社概要)入力値が空白",
        "stockdata":[
          csvobj_reg
                    ]
      } 
    })
  }  


  //★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★  

  //これから下は実際に行う処理が書かれている。
  else{

  //登録する銘柄データを辞書型配列に格納する。
  //★★★ 銘柄パラメータを増やすときに追記する箇所★★★ 
   obj={
    stock_num: req.query.stock_num,
    c_name:req.query.c_name,
    eps:req.query.eps,
    kessan:req.query.kessan,
    url:req.query.url,
    kaisya:req.query.kaisya,
    haitoub:req.query.haitoub,
    hold:req.query.hold
  }
  //★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★  

  
  //辞書型配列をJSON形式に変換している。
  var jsondat = JSON.stringify( obj );
  //console.log(obj)

  if (fs.existsSync(JSONFILEPATH)) fs.unlinkSync(JSONFILEPATH)  //上記jsondatを書き込むファイルがすでに存在する場合は当該ファイルを一度削除する。
  fs.writeFileSync(JSONFILEPATH,jsondat) //jsondatをJSONFILEPATHに存在するファイルに書き込む


  pyshell.send(""); //jsからpythonコードに空データを送る。pythonコードを起動させるため

    //pythonコード実施後にpythonからjsにデータが引き渡される。
    //pythonから返されたデータは「data」に格納される。
    pyshell.on('message',  function (data) {
          let csvobj_reg=fs.readFileSync(CSVPATH,'utf-8')
          res.send({
          message:          
          {
            "mes":"success",
            "stockdata":[
                csvobj_reg
                        ]
          }          
             //pythonで実施した演算結果をフロントエンドに返している。
        })
      })
  }
})


//登録全銘柄の株価を取得する
app.get('/apiall', function(req, res) {

  var {PythonShell} = require('python-shell');
  var pyshell = new PythonShell('/home/stock/stockgetall.py');  
  
  console.log("receiving data from FE")

  pyshell.send(""); //jsからpythonコードstockgetall.pyを呼び出す。
  console.log("pass0")
    //pythonコード実施後にpythonからjsにデータが引き渡される。
    //pythonに引き渡されるデータは「data」に格納される。
  pyshell.on('message',  function (data) {
      let csvobj=fs.readFileSync(CSVPATH,'utf-8') 
      let csvkakusyuobj=fs.readFileSync(CSV_KAKUSYUPATH,'utf-8') //原油、米国10年金利等のデータ
      console.log("pass1")
      res.send({
        message:          
        {
          "mes":"success",
          "stockdata":[
              csvobj,
              csvkakusyuobj //原油、米国10年金利等のデータ
                      ]
        }          
           //pythonで実施した演算結果をフロントエンドに返している。
      })
      })
  
})


//指定した銘柄の情報を取得する
app.get('/meigarainfo', function(req, res) {

  var {PythonShell} = require('python-shell');
  var pyshell = new PythonShell('/home/stock/sqlread.py', { mode: 'text'});  
    console.log("req.query.dat")  
    console.log(req.query.dat)
    pyshell.send(req.query.dat); //jsからpythonコードに'req.query.dat'を入力データとして提供する 

    //pythonコード実施後にpythonからjsにデータが引き渡される。
    //pythonに引き渡されるデータは「data」に格納される。
    pyshell.on('message',  function (data) {   
      console.log("meigarainfo test")
      let csvobj=fs.readFileSync(MEIGARA_PATH,'utf-8')
      let csvkakusyuobj=fs.readFileSync(CSV_KAKUSYUPATH,'utf-8')     
      res.send({
        message:          
        {
          "mes":"success",
          "stockdata":[
                csvobj,
                csvkakusyuobj
                      ]
        }          
           //pythonで実施した演算結果をフロントエンドに返している。
      })
      })
  }
)


//指定した銘柄の株価取得を行う。
app.get('/api', function(req, res) {

  var {PythonShell} = require('python-shell');
  var pyshell = new PythonShell('/home/stock/stockget.py');  
  //var pyshell = new PythonShell('sample.py');    
  //console.log("receiving data from FE")
  //console.log(req.query.dat) //フロントエンドから受け取ったデータをconsole.logしている。
  //console.log(isNaN(req.query.dat)) //フロントエンドから受け取ったデータをconsole.logしている。

  if (req.query.dat==''){
    res.send({
      message: "入力値が空白"
    })
  }else{

    pyshell.send(req.query.dat); //jsからpythonコードに'req.query.dat'を入力データとして提供する 

    //pythonコード実施後にpythonからjsにデータが引き渡される。
    //pythonに引き渡されるデータは「data」に格納される。
    pyshell.on('message',  function (data) {   
      let csvobj=fs.readFileSync(CSVPATH,'utf-8')
      let csvkakusyuobj=fs.readFileSync(CSV_KAKUSYUPATH,'utf-8')  //原油、米国10年金利等のデータ
      res.send({
        message:          
        {
          "mes":"success",
          "stockdata":[
              csvobj,
              csvkakusyuobj //原油、米国10年金利等のデータ
                      ]
        }          
           //pythonで実施した演算結果をフロントエンドに返している。
      })
      })
  }
})




//銘柄削除を行う。
app.get('/del', function(req, res) {

  var {PythonShell} = require('python-shell');
  var pyshell = new PythonShell(PYDELPATH, { mode: 'text'});  

  //データの形式チェックを実施している。NGデータの場合フロントエンドにNGメッセージを送り返す
  if (req.query.stock_num=='' ){
    res.send({
      message: "銘柄番号:入力値が空白、もしくは数値型ではない"
    })}
    //これから下は実際に行う処理が書かれている。
  else{

  //登録する銘柄データを辞書型配列に格納する。
  var obj={
    stock_num: req.query.stock_num,
  }

  //辞書型配列をJSON形式に変換している。
  var jsondat = JSON.stringify( obj );

  if (fs.existsSync(JSONDELPATH)) fs.unlinkSync(JSONDELPATH)  //上記jsondatを書き込むファイルがすでに存在する場合は当該ファイルを一度削除する。
  fs.writeFileSync(JSONDELPATH,jsondat) //jsondatをJSONFILEPATHに存在するファイルに書き込む

  pyshell.send(""); //jsからpythonコードに空データを送る。pythonコードを起動させるため

    //pythonコード実施後にpythonからjsにデータが引き渡される。
    //pythonから返されたデータは「data」に格納される。
    pyshell.on('message',  function (data) {
      let csvobj=fs.readFileSync(CSVPATH,'utf-8')
      let csvkakusyuobj=fs.readFileSync(CSV_KAKUSYUPATH,'utf-8') //原油、米国10年金利等のデータ
      console.log("del")
      console.log(csvobj)     
      res.send({
        message:          
        {
          "mes":"success",
          "stockdata":[
              csvobj,
              csvkakusyuobj //原油、米国10年金利等のデータ
                      ]
        }          
           //pythonで実施した演算結果をフロントエンドに返している。
      })
      })
  }
})








app.listen(3000)





