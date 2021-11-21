import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

// Element Plus
import ElementPlus from "element-plus";
import "element-plus/lib/theme-chalk/index.css";

// ApexChart
import VueApexCharts from "vue3-apexcharts";

router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = to.meta.title;
  }
  next();
});

createApp(App)
  .use(ElementPlus)
  .use(VueApexCharts)
  .use(store)
  .use(router)
  .mount("#app");
