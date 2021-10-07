import Vue from "vue";
import VueRouter from "vue-router";
import Login from "../views/Login.vue";
import Header from "../views/Header.vue";
import Footer from "../views/Footer.vue";
import Voice from "../views/VoiceRecognition.vue";
import Mypage from "../views/Mypage.vue";
import Mainpage from "../views/Mainpage.vue";
import Delivery from "../views/Delivery.vue";
import Control from "../views/Control.vue";
import Notify from "../views/Notification.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Mainpage",
    component:Mainpage
  },
  {
    path:"/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/header",
    name: "Header",
    component:Header,
  },
  {
    path: "/footer",
    name: "Footer",
    component:Footer,
  },
  {
    path: "/voice",
    name: "Voice",
    component:Voice,
  },
  {
    path: "/mypage",
    name: "Mypage",
    component:Mypage,
  },
  {
    path: "/delivery",
    name: "Delivery",
    component:Delivery,
  },
  {
    path: "/control",
    name: "Control",
    component:Control,
  },
  {
    path: "/notify",
    name: "Notify",
    component : Notify,
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
