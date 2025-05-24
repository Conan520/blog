import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import navie from 'naive-ui'
import {createDiscreteApi} from 'naive-ui'
import {router} from './common/router'
import {createPinia} from "pinia";
import axios from 'axios'
import {AdminStore} from "@/stores/AdminStore.js";

axios.defaults.baseURL = 'http://127.0.0.1:8000'
const {message, notification, dialog} =  createDiscreteApi(["message", "notification", "dialog"])

const app = createApp(App)

app.provide("axios", axios)
app.provide("message", message)
app.provide("notification", notification)
app.provide("dialog", dialog)
app.provide("server_url", axios.defaults.baseURL)

app.use(navie)
app.use(createPinia())
app.use(router)
const adminStore = AdminStore()
axios.interceptors.request.use((config) => {
    config.headers.token = adminStore.token
    return config
})
app.mount('#app')
