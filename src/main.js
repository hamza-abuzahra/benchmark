import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faBed, faPercent, faLocationPin, faCalendar, faArrowTrendUp, faArrowRightToBracket, faUpload, faChartColumn, faPlus, faPen, faDownload, faCircleUser} from '@fortawesome/free-solid-svg-icons'

library.add(faBed, faPercent,  faLocationPin, faCalendar, faArrowTrendUp, faArrowRightToBracket, faUpload, faChartColumn, faPlus, faPen, faDownload, faCircleUser)

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.component('font-awesome-icon', FontAwesomeIcon)
app.mount('#app')
