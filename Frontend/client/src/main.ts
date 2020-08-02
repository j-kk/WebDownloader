import 'bootstrap/dist/css/bootstrap.css';
import 'material-design-icons-iconfont/dist/material-design-icons.css';
import BootstrapVue from 'bootstrap-vue';
import Notifications from 'vue-notification';
import Vue from 'vue';
import AxiosPlugin from 'vue-axios-cors';
import Vuetify from 'vuetify';
import App from './App.vue';
import router from './router';

Vue.use(BootstrapVue);
Vue.use(AxiosPlugin);
Vue.use(Vuetify, {
  iconfont: 'mdi',
});

Vue.use(Notifications);

Vue.config.productionTip = false;

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
