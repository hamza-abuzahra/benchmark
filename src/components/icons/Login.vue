<template>
    <div class="login-overlay" @click="store.hideForm">
        <div class="login-modal">
            <form action="">
                <h1 style="align-self:center; font-weight: 600;margin-bottom: 30px;">Login</h1>
                <input type="text" placeholder="Email" class="login-input" id="un">
                <input type="password" placeholder="Password" class="login-input" id="pass">
                <input type="button" class="btn dark-green-btn" value="Submit" @click="login">
                <p style="text-align:center;">Don't have an account? <a href="#" @click="store.showSignup">Sign up</a></p>
            </form>
        </div>
    </div>
</template>

<script setup>
import router from '../../router';
import { useStore } from '../../stores/counter';

const store = useStore()
const login = async function(){
    const unel = document.querySelector('#un')
    const un = unel.value
    const passel = document.querySelector('#pass')
    const pass = passel.value
    const data = await store.getResponse('login', `username=${un}&password=${pass}`)
    if (data.status) {
        store.loggedin = true
        router.push("/home")
        unel.value = ''
        passel.value = ''
        store.formShow = false
        store.showMessage(data.text)
        store.currentUser = data.username
        store.currentemail = un
    } else {
        store.showError(data.text)
    }
}

</script>

<style>
.login-overlay{
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: rgba(0, 0, 0, 0.75);
    display: flex;
    justify-content: center;
    align-items: center;
}
.login-modal{
    height: 60%;
    width: 22%;
    min-width: 20rem;
    min-height: 20rem;
    background: #f5f5f5;
    border-radius: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
}
.login-modal > form {
    display: flex;
    height: 100%;
    justify-content: center;
    align-items: stretch;
    flex-direction: column;
    gap: 15px;
}
.login-input {
    font-size: 1rem;
    border-radius: 3px;
    padding: .5rem;
    border: solid 1px; 
}

</style>