<template>
    <div class="mp_full container">
        <div class="mp_full container">
            <h4 class="mypage_text">알림</h4>
        </div>
        <div class="card rounded-3 card_size">
            <div class="scroll_set card-body">
                <ul class="mb-5 list-group list-group-flush">
                    <li
                    v-for="(item,i) in notifications"
                    :key={i} 
                    class="list-group-item">{{item}}</li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            notifications :[],
        }
    },
    created() {
        //local storage 에 알림 받아오기
        var tmp = JSON.parse(localStorage.getItem('notifications'));
        //내림차순 설정
        this.notifications = tmp.slice().reverse();
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