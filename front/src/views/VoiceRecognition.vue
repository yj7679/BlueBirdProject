<template>
    <div class="container">
        <!--세로 중앙정렬이 안돼서 빈 container생성, 근데 px로 크기 지정해놔서 고치고 싶다..-->
        <div class="container" style="height:220px;"></div>
        <div class="d-flex align-items-center">
        <img @click="voiceRecognition" src="../assets/img/voice.png" style="margin:auto; width:170px;">
        </div>
        <div class="vc_text container">
            <h5>클릭 후 명령하기</h5>
        </div>
    </div>
</template>

<script>
export default {
    methods: {
        voiceRecognition(){

        }
    },
}
</script>

<style>
.vc_img{
    min-height: 100%;  /* Fallback for browsers do NOT support vh unit */
    min-height: 100vh; /* These two lines are counted as one :-)       */
    vertical-align: middle;
    align-items: center;
    justify-content: center;
}
.vc_text{
    margin-top: 10px;
    text-align: center;
    color: white;
    font-weight: bold;
}
</style>