<template>
    <div class="mp_full container">
        <div class="mp_full container">
            <h4 class="del_text">디바이스</h4>
        </div>
        <div class="card rounded-3 card_size">
            <div class="card-body">
                <h5 class="card-title">장소</h5>
                <select 
                class="form-select" 
                aria-label="Default select example"
                @change="onChange($event)">
                    <option selected class="placeholder">장소를 선택해주세요.</option>
                    <option value="1">세미나실</option>
                    <option value="2">비품실</option>
                    <option value="3">회의실</option>
                    <option value="4">사무실</option>
                </select>
            </div>
            <div class="container">
                <div class="row">
                    <div class="ct_text col" style="text-align:center;">
                        <p class="print_text">{{this.printvalue}}</p>
                    </div>
                    <div class="switch_pad col" v-show="showtext">
                    <div class="d-flex justify-content-center col form-check form-switch">
                        <input class="form-check-input" type="checkbox" id="flexSwitchCheckChecked" checked>
                    </div>    
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            selectvalue:"",
            printvalue:"",
            showtext:false,
        }
    },
    methods: {
        onChange(event){
            console.log(event.target.value)
            this.selectvalue = event.target.value;

            if(this.selectvalue == 1){
                this.printvalue = "공기청정기";
                this.showtext = true;
            }else if(this.selectvalue == 2){
                this.printvalue = "해당 장소에 제어할 수 있는 기기가 없습니다.";
                this.showtext = false;
            }else if(this.selectvalue == 3){
                this.printvalue = "에어컨";
                this.showtext = true;
            }else if(this.selectvalue == 4){
                this.printvalue = "TV";
                this.showtext = true;
            }else{
                this.printvalue = "해당 장소에 제어할 수 있는 기기가 없습니다.";
                this.showtext = false;
            }
        }
    },
}
</script>

<style>
.switch_pad{
    margin: 10px;
    padding:10px;
}
.ct_text{
    text-align: center;
}
.print_text{
    padding-top:20px;
    /* padding: 10px;
    margin-left:30px;
    margin-top: 9px;
    margin-right: 9px;
    margin-bottom: 9px; */
}
</style>