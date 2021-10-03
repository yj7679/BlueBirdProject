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
            roomList: ['세미나', '창고', '회의', '사무'],
            deviceList: ['에어컨', 'TV', '전등', '블라인드', '공기청정기'],
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
        errand(event) {
            console.log(event);
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