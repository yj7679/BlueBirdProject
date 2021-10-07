<template>
    <div>
        <Header />
        <div class="mp_full container">
            <div class="mp_full container">
                <h4 class="mypage_text">알림</h4>
            </div>
            <div class="card rounded-3 card_size">
                <div class="scroll_set card-body">
                    <h2 class="text-center my-5">
                        {{ notification }}
                    </h2>
                    <div class="container" style="text-align : center;">
                        <img src="../assets/img/bird.png" class="w-50 mt-5">
                    </div>
                </div>
            </div>
        </div>
        <div class="footer">
            <Footer />
        </div>
    </div>
</template>

<script>
import Header from "./Header.vue"
import Footer from "./Footer.vue"

export default {
    name: 'Notification',
    components: { Header, Footer },
    data() {
        return {
            notification: null,
        }
    },
    created() {
        //local storage 에 알림 받아오기
        this.notification = localStorage.getItem('notifications')
        //내림차순 설정
        localStorage.setItem('update', false)
    },
}
</script>

<style>
.scroll_set {
    /*여기서는 height를 %로 주면 scroll이 적용이 안 됨 ㅠ */
    height: 400px;
    overflow-y: scroll;
}
</style>