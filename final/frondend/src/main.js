import Vue from 'vue'
import ElementUI from 'element-ui'
import VeLine from 'v-charts/lib/line'
import VePie from 'v-charts/lib/pie'
import 'element-ui/lib/theme-chalk/index.css'
import 'normalize.css'
import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon'

import App from './App'
import router from './router'

Vue.config.productionTip = false

Vue.use(ElementUI)
Vue.component(VeLine.name, VeLine)
Vue.component(VePie.name, VePie)
Vue.component('icon', Icon)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})
