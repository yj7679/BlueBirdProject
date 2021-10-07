<template>
    <div>
        <Header />
        <div class="container">
            <!--세로 중앙정렬이 안돼서 빈 container생성, 근데 px로 크기 지정해놔서 고치고 싶다..-->
            <div class="container" style="height:150px;"></div>
            <div class="d-flex align-items-center">
            <img @click="voiceRec" src="../assets/img/voice.png" style="margin:auto; width:170px;">
            </div>
            <div class="vc_text container">
                <h5 v-if="btnCheck">{{ voiceInput }}</h5>
                <h5 v-else>{{ voiceCheck }}</h5>
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
    name: 'VoiceRecognition',
    components: { Header, Footer },
    data() {
        return {
            btnCheck: true,
            voiceCheck: '음성 인식 중',
            voiceInput: '클릭 후 명령하기',
            roomList: ['세미나', '창고', '회의', '사무', '사장'],
            deviceList: ['에어컨', 'TV', '공기 청정기'],
            stuffList: ['상자', '물', '서류철'],
            findDepart: false,
            findStuff: false,
            sendErrandData: {
                'depart': null,
                'stuff': null,
                'arrival': 'blueman'
            },
            sendDeviceData: {
                'device_name': null,
                'room_name': '사무',
                'on_off': null
            },
            commandCheck: false,
            available: null,
        }
    },
    created() {
        this.$socket.on('bot_status_response_web', (data) => {
            this.available = data['available']
        })
    },
    methods: {
        voiceRec() {
            if (this.available != '사용가능') {
                alert('터틀봇이 다른 명령을 수행하고 있습니다')
                return
            }
            this.btnCheck = false
            var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

            // 인스턴스 생성
            const recognition = new SpeechRecognition();

            recognition.interimResults = true;

            recognition.lang = "ko-KR";

            recognition.continuous = true;

            recognition.maxAlternatives = 10000;

            recognition.addEventListener("result", (e) => {
                for (let i = e.resultIndex, len = e.results.length; i < len; i++) {
                    let transcript = e.results[i][0].transcript;
                    if (e.results[i].isFinal) {
                        recognition.stop()
                        this.voiceInput = transcript
                        this.btnCheck = true
                        this.voiceCheck = '음성 인식 중'
                    }
                }    
            })
            recognition.start();
        
        },
        deviceControl(device) {
            // 사물, 위치 찾기
            this.sendDeviceData['device_name'] = device

            for (const room of this.roomList) {
                const roomCheck = this.voiceInput.indexOf(room)
                if (roomCheck != -1) {
                    this.sendDeviceData['room_name'] = room
                }
            }
            if (device == '공기 청정기') {
                if (this.sendDeviceData['room_name'] != '세미나') {
                    this.sendDeviceData['device_name'] = null
                    this.sendDeviceData['room_name'] = '사무'
                    alert('해당 장소에 해당 기기가 없습니다')
                    return
                }
            }
            else if (device == 'TV') {
                if (this.sendDeviceData['room_name'] != '사장') {
                    this.sendDeviceData['device_name'] = null
                    this.sendDeviceData['room_name'] = '사무'
                    alert('해당 장소에 해당 기기가 없습니다')
                    return
                }
            }
            else {
                if ((this.sendDeviceData['room_name'] == '회의') || (this.sendDeviceData['room_name'] == '사무')) {
                    this.sendDeviceData
                }
                else {
                    this.sendDeviceData['device_name'] = null
                    this.sendDeviceData['room_name'] = '사무'
                    alert('해당 장소에 해당 기기가 없습니다')
                    return
                }
            }

            // 어떤 명령인지 파악하기
            // Device On
            if (this.voiceInput.indexOf('켜') != -1) {
                this.sendDeviceData['on_off'] = 'on'
                this.$socket.emit('deviceControl', (this.sendDeviceData))
            }
            else if (this.voiceInput.indexOf('꺼') != -1) {
                this.sendDeviceData['on_off'] = 'off'
                this.$socket.emit('deviceControl', (this.sendDeviceData))
            }
            else {
                alert('잘못된 명령입니다')
            }
            this.sendDeviceData['device_name'] = null
            this.sendDeviceData['room_name'] = '사무'
            this.sendDeviceData['on_off'] = null
        },
        errand() {
            const slicing = this.voiceInput.split('에')
            if (slicing.length != 2) {
                alert('잘못된 명령입니다')
                this.findDepart = false
                this.findStuff = false
                this.sendErrandData['depart'] = null
                this.sendErrandData['stuff'] = null
                this.sendErrandData['arrival'] = 'blueman'
                return
            }
            // depart 구하기
            for (const depart of this.roomList) {
                const departCheck = slicing[0].indexOf(depart)
                if (departCheck != -1) {
                    // console.log(depart);
                    this.sendErrandData['depart'] = depart
                    this.findDepart = true
                }
            }
            //  stuff 구하기
            for (const stuff of this.stuffList) {
                const stuffCheck = slicing[1].indexOf(stuff)
                if (stuffCheck != -1) {
                    // console.log(stuff);
                    this.sendErrandData['stuff'] = stuff
                    this.findStuff = true
                }
            }
            //  arrival 구하기
            for (const arrival of this.roomList) {
                const arrivalCheck = slicing[1].indexOf(arrival)
                if (arrivalCheck != -1) {
                    // console.log(arrival);
                }
            }
            if (!this.findDepart) {
                alert('회사에 없는 방입니다')
                this.findDepart = false
                this.findStuff = false
                this.sendErrandData['depart'] = null
                this.sendErrandData['stuff'] = null
                this.sendErrandData['arrival'] = 'blueman'
                return
            }
            else if (!this.findStuff) {
                alert('회사에 없는 물건입니다')
                this.findDepart = false
                this.findStuff = false
                this.sendErrandData['depart'] = null
                this.sendErrandData['stuff'] = null
                this.sendErrandData['arrival'] = 'blueman'
                return
            }
            this.$socket.emit('stuffBring', (this.sendErrandData))
            this.sendErrandData['depart'] = null
            this.sendErrandData['stuff'] = null
            this.sendErrandData['arrival'] = 'blueman'
        }
    },
    mounted() {
        setInterval(() => {
            if (this.voiceCheck == '음성 인식 중') {
                this.voiceCheck = '음성 인식 중.'
            } else if (this.voiceCheck == '음성 인식 중.') {
                this.voiceCheck = '음성 인식 중..'
            } else if (this.voiceCheck == '음성 인식 중..') {
                this.voiceCheck = '음성 인식 중...'
            } else {
                this.voiceCheck = '음성 인식 중'
            }
            
        }, 500);
    },
    watch: {
        voiceInput() {
            if (this.voiceInput.length == 0) {
                return
            }
            for(const device of this.deviceList) {
                const deviceCheck = this.voiceInput.indexOf(device)
                if (deviceCheck != -1) {
                    this.deviceControl(device)
                    this.commandCheck = true
                    return
                }
            }
            for (const stuff of this.stuffList) {
                const stuffCheck = this.voiceInput.indexOf(stuff)
                if (stuffCheck != -1) {
                    this.errand()
                    this.commandCheck = true
                    return
                }
            }
            if (!this.commandCheck) {
                alert('잘못된 명령입니다')
            }
            this.commandCheck = false
        }
    }
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
.footer{
    position: fixed;
    bottom: 0;
}
</style>