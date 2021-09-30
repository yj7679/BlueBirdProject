<template>
    <div class="app">
      <router-view></router-view>
    </div>
</template>

<script>

export default {
  name : 'app',
  data() {
    return {

    }
  },
}
</script>

<style>
body{
    background: url("assets/img/background.png") no-repeat center center
    fixed;
  -webkit-background-size: cover;
  -moz-background-size: cover;
  -o-background-size: cover;
  background-size: cover;
  font-family: 'Gamja Flower', sans-serif;
}
</style>

