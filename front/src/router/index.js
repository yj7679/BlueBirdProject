import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import Header from "../views/Header.vue";
import Footer from "../views/Footer.vue";
import Voice from "../views/VoiceRecognition.vue";
import Mypage from "../views/Mypage.vue";
import Mainpage from "../views/Mainpage.vue";
import Delivery from "../views/Delivery.vue";
import Control from "../views/Control.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path:"/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/header",
    name: "header",
    component:Header,
  },
  {
    path: "/footer",
    name: "footer",
    component:Footer,
  },
  {
    path: "/voice",
    name: "voice",
    component:Voice,
  },
  {
    path: "/mypage",
    name: "mypage",
    component:Mypage,
  },
  {
    path: "/main",
    name: "main",
    component:Mainpage
  },
  {
    path: "/delivery",
    name: "delivery",
    component:Delivery,
  },
  {
    path: "/control",
    name: "control",
    component:Control,
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
