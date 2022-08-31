const { shell } = require("electron");
var vm = new Vue({
    el: "#gamesApp",
    data: {
        appName: "Detect and Track",
        author: "Catarina Freitas da Cruz",
        abstract: ["As part of the development of the master's dissertation, this program was developed with the objective of identifying the movement of a given object, in real time, in the environment of a game, using Machine Learning and Computer Vision techniques, more specifically methods of Object Detection and Tracking of Objects",
        "The practical environment was developed using the OpenCV python library, which has a diverse range of computer vision algorithms available and also allows the parallel use of CPU and GPU for the optimization of these same algorithm.","To start the program it is necessary to choose a window, an image and a threshold value and then click on start.The program will search for the provided image in screenshots constant to the window, highlighting only the objects found with equality equal to or greater than the given threshold."],
        // windows: [],
        windows: [],
        selectedwindow: "",
        filename: "",
        file:'',
        sense: 70,
        isRunning: false
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
            this.isRunning = !this.isRunning;
            //alert(this.file.name);
            //alert(this.file.webkitRelativePath);
            let formData = new FormData();
            formData.append('window', this.selectedwindow);
            formData.append('file', this.file);
            formData.append('threshold', this.sense / 100);
            
            axios.post('http://localhost:5000/run',
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }
            ).then(function () {
                console.log('SUCCESS!!');
            })
            .catch(function () {
                console.log("Failed");
            });
            // try{ 
            //     const requestOptions = {
            //         method: "POST",
            //         headers: { "Content-Type": "application/json" },
            //         body: JSON.stringify({
            //             window: this.selectedwindow,
            //             img: this.file,
            //             threshold: this.sense / 100,
            //         })
            //     };

            //     const response = fetch("http://localhost:5000/run", requestOptions);
            //     const data = response.json();
            // } catch(erros) {
            //     console.log(erros);
            // }
        },
        stop(event){
            this.isRunning = !this.isRunning;
            axios.post('http://localhost:5000/stop').then(function () {
                console.log('SUCCESS!!');
            })
            .catch(function () {
                console.log("Failed");
            });
        },
        processFile(event){
            var file = event.target.files;
            // alert(this.file);
        },
        handleFileUpload(event) {
            this.file = event.target.files[0];
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

