<template>
    <div class="mp_full container">
        <div class="mp_full container">
            <h4 class="mypage_text">마이페이지</h4>
        </div>
        <div class="card rounded-3 card_size">
            <div class="card-body">
                <h5 class="mp_full card-title">{{this.employee.name}}</h5>
                <ul class="mb-5 list-group list-group-flush">
                    <li class="list-group-item">사원번호 : {{this.employee.id}}</li>
                    <li class="list-group-item">직급 : {{this.employee.job}}</li>
                    <li class="list-group-item"></li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            employee:{
                id:"",
                name:"",
                job:"",
            }
        }
    },
    created() {
        this.$socket.on('employee',(data)=>{
            this.employee.id = data.id;
            this.employee.name = data.name;
            this.employee.job = data.job;
        })
    },
}
</script>

<style>
.mp_full{
    padding: 15px;
}
.mypage_text {
    color: white;
}
li {
    margin-top: 4px;
    height:45px;
}
.card_size{
    height:100%;
    margin:7px;
    padding:3px;
}
</style>