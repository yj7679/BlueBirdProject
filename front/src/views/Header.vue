<template>
    <div class="container">
        <div class="row">
            <div class="col">
                <a @click="goMain">
                    <img class="hd_img" src="../assets/img/logo_white.png" alt="Logo"> 
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
                    <img class="hd_img2" src="../assets/img/bell_white.png" alt="Logo"> 
                    <span v-if="badgeshow == true" class="badge">1</span>
                </a>
                
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            badgeshow:false,
        }
    },
    methods: {
        goNotify(){
            this.$router.push('/notify');
        },
        goMain(){
            this.$router.push('/')
        }
    },
    created() {
        const isLogin = localStorage.getItem('employee_number') || ''
        if (isLogin == '') {
            this.$router.push('/login')
        }
        var check = localStorage.getItem('update');
        if(check == 'true'){
            //badge show
            this.badgeshow = true;
        }else {
            this.badgeshow = false;
        }
    },
    mounted() {
        setInterval(() => {
        var check = localStorage.getItem('update');

        if(check == 'true'){
            //badge show
            this.badgeshow = true;
        }else {
            this.badgeshow = false;
        }
        }, 500);
    },
}
</script>

<style>
.hd_img {
    margin-top: 10px;
    margin-left: 5px;
    padding: 4px;
    width:45px;
}
.hd_img2 {
    margin-top : 10px;
    margin-right:5px;
    padding : 8px;
    width:100%;
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
  color: red;
  width:5px;
  height: 15px;
}
</style>