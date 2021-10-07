<template>
  <div class="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "app",
  data() {
    return {
      
    };
  },
  mounted() {
    //배달 success,fail값을 받아오기
    setInterval(() => {
      this.$socket.on('stuffBringCheck', (data) => {
        var today= new Date();
        var h = today.getHours();
        var m = today.getMinutes();
        localStorage.setItem('notifications', h+":"+m+"\n"+"배달에 성공하였습니다.")
        localStorage.setItem('update', true)
      })
    }, 1500);
  },
};
</script>

<style>
body {
  background: url("assets/img/background.png") no-repeat center center fixed;
  -webkit-background-size: cover;
  -moz-background-size: cover;
  -o-background-size: cover;
  background-size: cover;
  font-family: "Do Hyeon", sans-serif;
}
</style>
