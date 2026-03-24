import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/main.css'
import { initTracknodeTracker } from './plugins/tracknode-tracker'
import { initB24U } from './plugins/b24u'

const app = createApp(App)
app.use(router)
app.mount('#app')

initTracknodeTracker()
initB24U()
