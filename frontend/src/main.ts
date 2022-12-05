import App from "@/components/App.vue";
import router from "@/router";
import "bootstrap-icons/font/bootstrap-icons.css";
import "bootstrap/dist/css/bootstrap.css";
import { createPinia } from "pinia";
import { createApp } from "vue";

const app = createApp(App);
app.use(router);
app.use(createPinia());

app.component("App", App);

app.mount("#app");
