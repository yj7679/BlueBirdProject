<template>
  <div class="aa container">
    <!--header-->
      <div>
          <a href="#">
          <img src="../assets/img/peace.png" alt="Logo" style="width:20%;"> 
          </a>
      </div>
    <!--main-->
    <div style="height:500px; display:flex;">
      <img src="../assets/img/stone.png" style="margin:auto; width:170px;">
    </div>
    <!--footer-->
    <div class="abc">
          <img src="../assets/img/whitehome.png" width="20%" alt="no home">
          <img src="../assets/img/deliver_white.png" width="20%" alt="no deli">
          <img src="../assets/img/mic_white.png" width="20%" alt="no mic">
          <img src="../assets/img/turn-off_white.png" width="20%" alt="no cont">
          <img src="../assets/img/user_white.png" width="20%" alt="no mypage">
      </div>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: "Home"
};
</script>

<style>
img {
    display: inline-block;
    padding: 10px;
}
.aa {
  background-image: url('../assets/img/background.png');
  background-size: 100%;
}
</style>