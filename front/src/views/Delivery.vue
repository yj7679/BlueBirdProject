<template>
    <div>
        <Header />
        <div class="mp_full container">
            <div class="mp_full container">
                <h4 class="del_text">물건 배달</h4>
            </div>
            <div class="card rounded-3 card_size">
                <div class="card-body">
                    <h5 class="card-title">장소</h5>
                    <select v-model="value.depart" class="form-select" aria-label="Default select example">
                        <option disabled value="">물건을 가져올 장소를 선택해주세요.</option>
                        <option value="나에게서">나에게서(from me)</option>
                        <option value="창고">창고</option>
                        <option value="회의">회의실</option>
                        <option value="사무">사무실</option>
                        <option value="세미나">세미나실</option>
                        <option value="사장">사장실</option>
                    </select>
                </div>
                <div class="card-body">
                    <h5 class="card-title">물건</h5>
                    <select v-model="value.stuff" class="form-select" aria-label="Default select example">
                        <option disabled value="">배달할 물건을 선택해주세요.</option>
                        <option value="물">물</option>
                        <option value="서류철">서류철</option>
                        <option value="상자">상자</option>
                    </select>
                </div>
                <div class="card-body">
                    <h5 class="card-title">목적지</h5>
                    <select v-model="value.arrival" class="form-select" aria-label="Default select example">
                        <option disabled value="">목적지를 선택해주세요.</option>
                        <option value="나에게">나에게(to me)</option>
                        <option value="창고">창고</option>
                        <option value="회의">회의실</option>
                        <option value="사무">사무실</option>
                        <option value="세미나">세미나실</option>
                        <option value="사장">사장실</option>
                    </select>
                </div>
                <div class="container d-grid mb-3">
                    <button @click="goDelivery" type="button" class="btn_color btn btn-block mt-3">배달가기</button>
                </div>
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
    name: 'Delivery',
    components: { Header, Footer },
    data() {
        return {
            // res : "SUCCESS", //임시 response
            value:{
                depart : "",
                stuff:"",
                arrival:"",
            }
        }
    },
    methods: {
        goDelivery(){
            //백엔드에 배달 요청
            this.$socket.emit('stuffBring',this.value);
        }
    },
}
</script>

<style>
.btn_color{
    border-color: #2980B9;
    /* background-color: #6DD5FA; */
    color: #2980B9;
}
.placeholder{
    color:gray;
}
.del_text{
    color:white;
}
</style>