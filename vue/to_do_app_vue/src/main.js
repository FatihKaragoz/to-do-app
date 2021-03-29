import Vue from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./store";
import axios from 'axios';

import { MdButton, MdContent, MdTabs } from 'vue-material/dist/components'
import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default.css'

Vue.use(MdButton)
Vue.use(MdContent)
Vue.use(MdTabs)


axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://127.0.0.1/login/';

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  // data: {
  //   menu: false
  // },
  // computed: {
  //   showMenu: function () {
  //     if (localStorage.token && localStorage.token != null) {
  //       this.menu = true
  //     } else {
  //       this.menu = false
  //     }

  //     return this.menu
  //   }
  // },
  render: (h) => h(App),
}).$mount("#app");
