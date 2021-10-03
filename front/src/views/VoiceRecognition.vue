<template>
    <div class="container">
        <!--세로 중앙정렬이 안돼서 빈 container생성, 근데 px로 크기 지정해놔서 고치고 싶다..-->
        <div class="container" style="height:220px;"></div>
        <div class="d-flex align-items-center">
        <img @click="testRecode" src="../assets/img/voice.png" style="margin:auto; width:170px;">
        </div>
        <div class="vc_text container">
            <h5 v-if="btnCheck">{{ voiceInput }}</h5>
            <h5 v-else>{{ voiceCheck }}</h5>
        </div>
    </div>
</template>

<script>
export default {
    name: 'VoiceRecognition',
    data() {
        return {
            btnCheck: true,
            voiceCheck: '음성 인식 중',
            voiceInput: '클릭 후 명령하기',
            roomList: ['세미나', '창고', '회의', '사무', '사장'],
            deviceList: ['에어컨', 'TV', '전등', '블라인드', '공기청정기'],
            stuffList: ['가위', '물', '서류'],
            findDepart: false,
            findStuff: false,
            sendErrandData: {
                'depart': null,
                'stuff': null,
                'arrival': 'blueman'
            }
        }
    },
    methods: {
        testRecode() {
            // this.voiceInput = '에어컨 켜줘'
            this.voiceInput = '사무실에서 가위 좀 회의실에 갖다 놔'
        },
        voiceRecognition() {
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
        deviceControl(event) {
            console.log(event);
        },
        errand() {
            const slicing = this.voiceInput.split('에서')
            if (slicing.length != 2) {
                alert('잘못된 입력값입니다')
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
            if (!this.findDepart || !this.findStuff) {
                alert('회사에 없는 데이터입니다')
                this.findDepart = false
                this.findStuff = false
                return
            }
            console.log(this.sendErrandData);
            this.$socket.emit('stuffBring', (this.sendErrandData))
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
            for(const device of this.deviceList) {
                const deviceCheck = this.voiceInput.indexOf(device)
                if (deviceCheck != -1) {
                    this.deviceControl(this.voiceInput)
                    return
                }
            }
            this.errand(this.voiceInput)
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
</style>