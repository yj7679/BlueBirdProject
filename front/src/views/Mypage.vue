<template>
    <div class="mp_full container">
        <div class="mp_full container">
            <h4 class="mypage_text">마이페이지</h4>
        </div>
        <div class="card rounded-3 card_size">
            <div class="card-body">
                <h5 class="mp_full card-title">{{this.employee.name}}님</h5>
                <ul class="mb-5 list-group list-group-flush">
                    <li class="list-group-item">사원번호 : {{this.employee.number}}</li>
                    <li class="list-group-item">회사명 : {{this.employee.company}}</li>
                    <li class="list-group-item">부서 : {{this.employee.department}}</li>
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
                number:"",
                name:"",
                company:"",
                department:"",
                job:"",
            }
        }
    },
    created() {
        var employee_number = JSON.parse(localStorage.getItem('employee_number'));

        this.$socket.emit('employee',employee_number,(data)=>{
            this.employee.id = data.employee_number;
            this.employee.name = data.name;
            this.employee.company = data.company;
            this.employee.department = data.department;
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