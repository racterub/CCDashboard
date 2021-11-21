import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "首頁",
    meta: {
      title: "CCDashboard | 首頁",
    },
    component: () =>
      import(/* webpackChunkName: "index" */ "../views/Index.vue"),
  },
  {
    path: "/settings",
    name: "設定",
    meta: {
      title: "CCDashboard | 設定",
    },
    component: () =>
      import(/* webpackChunkName: "settings" */ "../views/Settings.vue"),
  },
  {
    path: "/login",
    name: "登入",
    meta: {
      title: "CCDashboard | 登入",
    },
    component: () =>
      import(/* webpackChunkName: "login" */ "../views/Login.vue"),
  },
  {
    path: "/logout",
    name: "登出",
    meta: {
      title: "CCDashboard | 登出",
    },
    component: () =>
      import(/* webpackChunkName: "logout" */ "../views/Logout.vue"),
  },
  {
    path: "/spots/:coin",
    name: "列表",
    meta: {
      title: "CCDashboard | 列表",
    },
    component: () =>
      import(/* webpackChunkName: "spots" */ "../views/Spots.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
