module.exports = {
    devServer: {
      proxy: {
        "/api/": {
          target: "http://192.168.0.4:3000",
        }
      }
    }
  };