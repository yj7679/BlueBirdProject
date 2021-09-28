<template>
    <div class="back">     
        <b-container fluid class="back">
            <div>
                <b-form-group
                id="fieldset-horizontal"
                label-cols-sm="4"
                label-cols-lg="3"
                content-cols-sm
                content-cols-lg="7"
                label="아이디"
                label-for="input-horizontal"
                >
                <b-form-input id="input-horizontal"></b-form-input>

                </b-form-group>
                <b-form-group
                id="fieldset-horizontal"
                label-cols-sm="4"
                label-cols-lg="3"
                content-cols-sm
                content-cols-lg="7"
                label="비밀번호"
                label-for="input-horizontal"
                >
                <b-form-input id="input-horizontal"></b-form-input>
                </b-form-group>

                <div>
                <b-button block variant="primary">Block Level Button</b-button>
                </div>
            </div>
        </b-container>
    </div>
</template>

<script>
export default {
    name: 'login',
    data() {
        return {
            src : "../assets/img/background.png",
        }
    },
}
</script>

<style>
.back{
    background-image: url("../assets/img/background.png");
}
</style>