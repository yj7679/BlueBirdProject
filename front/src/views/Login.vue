<template>
    <div class="container">
        <div class="container pt-5">
            <img src="../assets/img/peace.png" 
            class="main_img mx-auto d-block m-5" alt="Cinque Terre">
        </div>
        <div class="container">
            <div class="row m-5 p-2"></div>
        </div>
        <div class="container">
            <form action="/action_page.php">
                <div class="form-group">
                    <label for="number">사원번호:</label>
                    <input v-model="employee.id" type="number" class="form-control" placeholder="사원번호를 입력하세요" id="email">
                </div>
                <div class="form-group pt-2">
                    <label for="pwd">비밀번호:</label>
                    <input v-model="employee.password" type="password" class="form-control" placeholder="비밀번호를 입력하세요" id="pwd">
                </div>
                <!-- <div class="form-group form-check pt-2">
                    <label class="form-check-label">
                    <input class="form-check-input" type="checkbox"> 사원번호 저장하기
                    </label>
                </div> -->
                <div class="d-grid">
                    <button @click="login" type="button" class="btn btn-primary btn-block mt-3">로그인</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
export default {
    name: 'login',
    data() {
        return {
            employee:{
                id:"",
                password:"",
            }
        }
    },
    methods: {
        login(){
            this.$socket.emit('join',this.employee);
        }
    },
}
</script>

<style>
.main_img {
    width:100px;
}
</style>