<template>
<div>
    <Header />
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
            <div class="logout_bt container d-flex flex-row-reverse">
                <button @click="logout" type="button" class="btn btn-danger">Logout</button>
            </div>
        </div>
    </div>
    <div class="footer">
            <Footer />
        </div>
</div>
</template>

<script>
import Header from "./Header.vue";
import Footer from "./Footer.vue";

export default {
    name:'MyPage',
    components:{ Header, Footer },
    data() {
        return {
            employee:{
                number:"",
                name:"",
                company:"",
                department:"",
                job:"",
            },
            data:{
                employee_number:null,
            }
        }
    },
    created() {
        localStorage.setItem('employee_number',1);
        this.data["employee_number"] = localStorage.getItem('employee_number');

        this.$socket.emit('employee',this.data)
        this.$socket.on('putEmployee',(data)=>{
            this.employee.number = data[0].employee_number;
            this.employee.name = data[0].name;
            this.employee.company = data[0].company;
            this.employee.department = data[0].department;
            this.employee.job = data[0].job;
        })
            console.log(this.employee)
    },
    methods: {
        logout(){
            //clear해도 되나,,?
            //localStorage.clear();

            //remove
            localStorage.removeItem('employee_number');
            this.$router.push('/login');
        }
    },
}
</script>

<style>
.mp_full{
    padding-left: 15px;
    padding-right: 15px;
    padding-top : 8px;
    padding-block: 8px;
}
.mypage_text {
    color: white;
}
li {
    margin-top: 4px;
    height:40px;
}
.card_size{
    height:100%;
    margin-top:7px;
    margin-left:7px;
    margin-right:7px;
    padding:3px;
}
.logout_bt{
    margin-top: 0px;
    padding-top: 0px;
    margin-bottom: 20px;
}
</style>