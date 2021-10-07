<template>
  <div class="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "app",
  data() {
    return {
      
    };
  },
  mounted() {
    //배달 success,fail값을 받아오기
    this.$socket.on('stuffBringCheck',(data)=>{
      //백엔드에서 답변이 오면 localStorage에 set하기
    var existingEntries = JSON.parse(localStorage.getItem('notifications'));
    var today= new Date();
    var h = today.getHours();
    var m = today.getMinutes();

    //현재시간도 같이 넣으면 좋을 듯
    if(data.result == "SUCCESS"){
        existingEntries.push(h+":"+m+"\n"+"배달에 성공하였습니다.");
    }else if(data.result == "FAIL"){
        existingEntries.push(h+":"+m+"\n"+"물건을 찾지 못하였습니다.");
    }else{
        existingEntries.push("알 수 없는 오류가 발생하였습니다.");
    }
    localStorage.setItem('notifications',JSON.stringify(existingEntries));
    //새로운 알림 badge추가용 data
    localStorage.setItem('update','true');
    })
  },
};
</script>

<style>
body {
  background: url("assets/img/background.png") no-repeat center center fixed;
  -webkit-background-size: cover;
  -moz-background-size: cover;
  -o-background-size: cover;
  background-size: cover;
  font-family: "Do Hyeon", sans-serif;
}
</style>
