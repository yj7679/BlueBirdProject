<template>
    <div class="mp_full container">
        <div class="mp_full container">
            <h5 class="main_text">000님 안녕하세요</h5>
        </div>
        <div class="card main_card rounded-3" style="margin-bottom:8px;">
            <!--미니맵-->
        </div>
        <div class="row">
            <div class="col container" style="padding-right:3px;">
                <div class="card rounded-3">
                    <!--요일-->
                    <div class="mt-2">
                        <img class="calendar_size" src="../assets/img/calendar.png" alt="no home">
                        {{ date }}
                        <span v-if="this.day == '토'" class="text-primary">({{ day }})</span>
                        <span v-else-if="this.day == '일'" class="text-danger">({{ day }})</span>
                        <span v-else class="text-dark">({{ day }})</span>
                    </div>
                    <div class="text-center fs-2 mb-2">
                        {{ time }}
                    </div>
                </div>
            </div>
            <div class="col" style="padding-left:3px;">
                <div class="card sub_card rounded-3 container px-0">
                    <!--날씨-->
                    <img :src="require(`@/assets/img/${weather}.png`)" class="mx-auto mt-1 p-0 img-size" v-if="weather != null" />
                    <h4 class="text-center mb-0 mt-2">{{ temperature }}°C</h4>
                </div>
            </div>
        </div>
        <div class="card sub2_card rounded-3" style="margin-top:8px;">
            <!--로봇의 상태-->
        </div>
    </div>
</template>

<script>
export default {
    name: "Mainpage",
    data() {
        return {
            date: null,
            time: null,
            day: null,
            weather: null,
            temperature: null
        }
    },
    created() {
        var today= new Date();
        var date= today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
        var hour = today.getHours()
        var minute = today.getMinutes()
        if (hour < 10) {
            hour = "0" + hour
        }
        if ( minute < 10) {
            minute = "0" + minute
        }
        var time= hour + " : " + minute
        var day = ['일', '월', '화', '수', '목', '금', '토']
        this.date = date
        this.time = time
        this.day = day[today.getDay()]
        this.$socket.emit('env_msg_request_web', 'go')
        this.$socket.on('env_msg_response_web', (data) => {
            this.weather = data.weather
            this.temperature = data.temperature
        })
    },
    mounted() {
        setInterval(() => {
            var today= new Date();
            var date= today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
            var hour = today.getHours()
            var minute = today.getMinutes()
            if (hour < 10) {
                hour = "0" + hour
            }
            if ( minute < 10) {
                minute = "0" + minute
            }
            var time= hour + " : " + minute
            var day = ['일', '월', '화', '수', '목', '금', '토']
            this.date = date
            this.time = time
            this.day = day[today.getDay()]

            this.$socket.emit('env_msg_request_web', 'go')
        }, 1000);
    },
}
</script>

<style>
.main_text{
    color: white;
    margin-bottom: 0px;
}
.main_card{
    height: 220px;
}
.sub_card{
    height: 100px;
    padding-left: 0px;
}
.sub2_card{
    height: 120px;
}
.calendar_size{
    width: 30%;
}
.img-size{
    width: 35%;
}
</style>