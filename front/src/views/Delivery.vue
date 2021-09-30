<template>
    <div class="mp_full container">
        <div class="mp_full container">
            <h4 class="del_text">물건 배달</h4>
        </div>
        <div class="card rounded-3 card_size">
            <div class="card-body">
                <h5 class="card-title">장소</h5>
                <select class="form-select" aria-label="Default select example">
                    <option selected class="placeholder">물건을 가져올 장소를 선택해주세요.</option>
                    <option value="1">세미나실</option>
                    <option value="2">비품실</option>
                    <option value="3">회의실</option>
                    <option value="4">사무실</option>
                </select>
            </div>
            <div class="card-body">
                <h5 class="card-title">물건</h5>
                <select class="form-select" aria-label="Default select example">
                    <option selected>배달할 물건을 선택해주세요.</option>
                    <!--1번 선택지에 따라서 결과가 다르게 출력되도록 해야함-->
                    <option value="1">물</option>
                    <option value="2">서류철</option>
                    <option value="3">박스</option>
                </select>
            </div>
            <div class="card-body">
                <h5 class="card-title">목적지</h5>
                <select class="form-select" aria-label="Default select example">
                    <option selected>목적지를 선택해주세요.</option>
                    <option value="1">One</option>
                    <option value="2">Two</option>
                    <option value="3">Three</option>
                </select>
            </div>
            <div class="container d-grid mb-3">
                <button @click="goDelivery" type="button" class="btn_color btn btn-block mt-3">배달가기</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    methods: {
        goDelivery(){

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