// eslint-disable-next-line
/* eslint-disable */ 
module.exports={
    DATLENGTH:500, //描写する対象の日数を設定する 
    MEIGARA_NAME:"NIKKEI225", //銘柄名を設定する。
    S_PERIOD:5, //移動平均短期
    M_PERIOD:25, //移動平均中期
    L_PERIOD:75, //移動平均長期
    RSI_PERIOD:14, //RSI算出期間
    BOL_N:20, //ボリンジャーバンド算出対象日数
    TENKAN_DELAY:9,  //一目均衡表 転換線パラメータ
    KIJYUN_DELAY:26, //一目均衡表 基準線パラメータ
    CHIKOU_DELAY:26,  //一目均衡表 遅行スパンパラメータ
    SENKOU1:26,  //一目均衡表 先行スパン1パラメータ過去
    SENKOU2_P:52,  //一目均衡表 先行スパン2パラメータ過去
    SENKOU2_F:26,  //一目均衡表 遅行スパン2パラメータ未来
    HITOKABUEKI:2000, //一株益
    CLOSE_OPEN_PERIOD:3, //終値-始値の移動平均線算出期間
    CLOSE_T_Y:3, //終値(本日) - 終値(昨日)の移動平均算出期間
    CSVPath:'/home/stock/stockdata.csv', //株価データを格納しているファイル
    KEYS:['STOCK_NUM','TODAY','DIF'],
    MOMIAI:10, //一目均衡表もみ合い判定データを棒グラフで表示を開始する位置を指定している。
    RATING:0.005, //一目均衡表もみ合い判定データ RATING以上の基準線の変化が発生した時に変動相場になったとする。
    VAL2_SMA:10, //当日と前日との変化率2乗値の移動平均設定値
    HOME:'/home/fdfpy/docshare/',   // アプリのHomeディレクトリ HOME:'/home/'   or    '/home/fdfpy/docshare/'   C:/Users/fdfpy/docshare/  C:\Users\fdfpy\docshare
    url:'25.32.185.252' ,    
}
