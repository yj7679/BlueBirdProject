<template>
    <div class="mp_full container">
        <div class="mp_full container">
            <h4 class="mypage_text">알림</h4>
        </div>
        <div class="card rounded-3 card_size">
            <div class="card-body">
                <ul 
                v-for="(item,i) in notifications" :key={i} 
                class="mb-5 list-group list-group-flush">
                    <li class="list-group-item">{{item}}</li>
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
        //알림 받아오기
    },
}
</script>