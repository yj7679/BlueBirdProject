import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import Header from "../views/Header.vue";
import Footer from "../views/Footer.vue";
import Voice from "../views/VoiceRecognition.vue";

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
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
