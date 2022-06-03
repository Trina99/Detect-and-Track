const { VueElement } = require("vue");

console.log("ola");

var vm = new VueElement({
    el:"#gameApp",
    data: {
        appName: "Detect and Track",
        username: "Trina",
        games: []
    }
})