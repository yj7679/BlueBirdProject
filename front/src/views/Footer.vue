<template>
    <div class="ft_set container">
        <div class="row">
            <div class="col" @click="goMain">
                <img class="ft_img" src="../assets/img/whitehome_shadow.png" alt="no home">
            </div>
            <div class="col" @click="goDelivery">
                <img class="ft_img" src="../assets/img/box_white_shadow.png" width="20%" alt="no home">
            </div>
            <div class="col" @click="goVoice">
                <img class="ft_img" src="../assets/img/mic_white_shadow.png" width="20%" alt="no home">
            </div>
            <div class="col" @click="goControl">
                <img class="ft_img" src="../assets/img/settings_white.png" width="20%" alt="no home">
            </div>
            <div class="col" @click="goMypage">
                <img class="ft_img" src="../assets/img/user_white_shadow.png" width="20%" alt="no home">
            </div>
        </div>
    </div>
</template>

<script>
export default {
    methods: {
        goMain(){
            this.$router.push('/');
        },
        goDelivery(){
            this.$router.push('/delivery');
        },
        goVoice(){
            this.$router.push('/voice');
        },
        goControl(){
            this.$router.push('/control');
        },
        goMypage(){
            this.$router.push('/mypage');
        }
    },
}
</script>


<style>
.ft_img {
    width: 100%;
    margin: 0px;
    padding: 10px;
}
.ft_set{
    /* background-color: hsl(0, 0%, 50%,0.1); */
    background-color: hsl(0, 0%, 0%, 0.1);
}
</style>