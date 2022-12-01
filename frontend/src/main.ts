import App from "@/components/App.vue";
import router from "@/router";
import "bootstrap-icons/font/bootstrap-icons.css";
import "bootstrap/dist/css/bootstrap.css";
import moment from "moment";
import "moment-timezone";
import { createPinia } from "pinia";
import { createApp } from "vue";

const app = createApp(App);
app.use(router);
app.use(createPinia());

app.component("App", App);

app.config.globalProperties.$filters = {
  datetime(value: string): string {
    return moment(value)
      .tz(moment.tz.guess())
      .locale(navigator.language)
      .format("LLLL");
  },
  seconds(value: number): string {
    return moment
      .utc(moment.duration(value, "seconds").asMilliseconds())
      .format("HH:mm:ss");
  },
  prettyBytes(bytes: number, kib: boolean = false): string {
    if (bytes === 0) return "0 Bytes";
    const base = kib ? 1024 : 1000;
    const sizes = kib ? ["Bytes", "KiB", "MiB"] : ["Bytes", "KB", "MB"];
    const exp = Math.floor(Math.log(bytes) / Math.log(base));
    return (bytes / Math.pow(base, exp)).toFixed(1) + " " + sizes[exp];
  },
};
app.mount("#app");
