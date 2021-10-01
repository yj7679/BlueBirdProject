<template>
    <div class="container">
        <div class="row">
            <div class="col">
                <a @click="goMain">
                    <img class="hd_img" src="../assets/img/peace_white.png" alt="Logo"> 
                </a>
            </div>
            <div class="col">
            </div>
            <div class="col">
            </div>
            <div class="col">
            </div>
            <div class="col">
                <a @click="goNotify" class="notification">
                    <img class="hd_img2" src="../assets/img/bell_simple_white.png" alt="Logo"> 
                    <span class="badge">1</span>
                </a>
                
            </div>
        </div>
    </div>
</template>

<script>
export default {
    methods: {
        goNotify(){
            this.$router.push('/notify');
        },
        goMain(){
            this.$router.push('/main')
        }
    },
}
</script>

<style>
.hd_img {
    margin-top: 10px;
    margin-left: 5px;
    padding: 5px;
    width:50px;
}
.hd_img2 {
    margin-top : 10px;
    margin-right:5px;
    padding : 5px;
    width:50px;
}
.notification {
  color: white;
  text-decoration: none;
  /* padding: 15px 26px; */
  position: relative;
  /* display: inline-block; */
  /* border-radius: 2px; */
}

.notification:hover {
  background: red;
}

.notification .badge {
  position: absolute;
  top: -12px;
  right: -0px;
  /* padding: 5px 10px; */
  border-radius: 50%;
  background:red;
  color: white;
}
</style>