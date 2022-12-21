import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

Vue.config.productionTip = false


// axios的配置
import axios from 'axios'
Vue.prototype.$axios=axios

// elementui的配置
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
Vue.use(ElementUI);

//vue-cookies
import cookies from 'vue-cookies'
Vue.prototype.$cookies=cookies

//安装bootstrap和jquery
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
// 配置全局样式
import '@/assets/css/global.css'
// 配置全局自定义设置
import settings from "@/assets/js/settings";
Vue.prototype.$settings=settings;

// 视频播放器的使用vue-video播放器

import 'video.js/dist/video-js.css'
import 'vue-video-player/src/custom-theme.css'
import VideoPlayer from 'vue-video-player'
Vue.use(VideoPlayer);

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
