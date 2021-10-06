import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import io from 'socket.io-client'; 

const socket = io('192.168.0.20:12001'); 

Vue.config.productionTip = false;
Vue.prototype.$socket = socket;

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
