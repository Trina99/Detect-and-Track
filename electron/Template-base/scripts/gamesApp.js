const { shell } = require("electron");
var vm = new Vue({
    el: "#gamesApp",
    data: {
        appName: "Detect and Track",
        author: "Catarina Freitas da Cruz",
        abstract: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent luctus ex id lacus rutrum, in aliquam mauris rutrum. Suspendisse justo sapien, finibus vel convallis id, elementum ac magna. Aliquam consectetur nisi at tortor tincidunt vestibulum. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nullam tincidunt augue id tortor tristique, vel suscipit magna sodales. Duis sed luctus ex. Pellentesque nec purus non quam ornare euismod. Donec in nulla sit amet ex consequat varius id quis arcu. Ut felis erat, consequat ac pulvinar in, luctus non velit. Sed varius non massa in dictum. Quisque auctor, lorem eget sodales consectetur, libero tellus ultrices nunc, eget commodo neque eros eget nisl. Quisque varius diam mi, non sollicitudin eros iaculis non.Ut et nibh placerat, semper purus at, gravida nisl.Sed eu sem ut sapien venenatis iaculis vitae eu risus.",
        // windows: [],
        windows: [],
        selectedwindow: "",
        filename: "",
        sense: 70
    },
    methods: {
        windos: async function () {
            w_list = [];
            try{
                const response = await fetch("http://localhost:5000/getWindows");
                win = await response.json();
                //console.log(win);
                for(w of win.windows){
                    //console.log(w + typeof(w));
                    w_list.push(w);
                }

                //console.log("windows capture" + typeof(win.windows));
            } catch (erros){
                console.log(erros);
            }
            console.log(typeof(w_list));
            this.windows = w_list;
            return w_list;
        },
    // methods: {
        start(event){
            alert(this.filename);
            try{ 
                const requestOptions = {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        window: this.selectedwindow,
                        img: '',
                        threshold: this.sense / 100,
                    })
                };

                const response = fetch("http://localhost:5000/run", requestOptions);
                const data = response.json();
            } catch(erros) {
                console.log(erros);
            }
        },
        processFile(event){
            var file = event.target.files;
            // alert(this.file);
        }
    },
    created(){
        this.windos();
    }
})


Vue.component('link-button', {
    props: {
        link: String,
        img: String,
        width: String,
        height: String,
        padding: {
            type: String,
            default: "0px"
        },
        download: {
            type: Boolean,
            default: false
        }
    },
    methods:{
        openLink(){
            if (!this.download) {
                console.log(this.link);
                shell.openExternal(this.link);
            }
        }
    },
    computed:{
        fileName(){
            return (this.download) ? this.link : this.download;
        },
        linkName(){
            return (this.download) ? this.link : "#";
        }
    },
    template: `
            <a v-bind:href="linkName" @click="openLink" v-bind:download="fileName">
                <img v-bind:style="{ width: width , height: height, padding: padding }" v-bind:src="img">
            </a>
    `
})


Vue.component ('links-url', {
    data: function () {
        return{
            thesis_url: 'a84011_pre_dissertation.pdf',
            github_url: "https://github.com/Trina99/Detect-and-Track",
            linkdIn_url: "https://www.linkedin.com/in/catarinafreitascruz/",
            anybrain_url: "https://anybrain.gg/",
        }
    },
    template:`
        <div class="buttons">

            <link-button v-bind:link="thesis_url" img="icons/download.png" height="40px" width="40px" padding="5px" download/>
            
            <link-button v-bind:link="github_url" img="icons/github.png" height="45px" width="45px"/>

            <link-button v-bind:link="linkdIn_url" img="icons/linkdIn.png" height="48px" width="50px"/>

            <div style="width:100%; height:1px;"></div>

            <link-button v-bind:link="anybrain_url" img="icons/anybrain.png" height="68px" width="96px"/>
        </div>
    `
})

