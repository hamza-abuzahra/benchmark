<script setup>
import Login from '../components/icons/Login.vue';
import Signup from '../components/icons/Signup.vue';
import router from '../router';
import { useStore } from '../stores/counter';

const store = useStore();
if (store.loggedin == true){
  router.push('/home')
}
const navs = document.querySelectorAll('a')
navs.forEach(e=>{
    if (e.id == 'landing') e.classList.add('active')
    else e.classList.remove('active')
})
</script>

<template>
  <div class="landing-body">
    <div class="landing-main-container">
      <div class="landing-left">
        <div class="landing-big-text">
          <h1>Welcome</h1>
          <p style="margin-top:2.5rem; font-size: 1.5rem;">Take your Hotel to the next level at the age of big data, use it to your advantage </p>
        </div>
        <div class="landing-action-call">
          <button class="dark-green-btn btn" @click="store.showSignup">Get Started</button>
          <button class="light-btn btn" @click="store.showLogin">Sign in</button>

        </div>
      </div>
      <div class="landing-right">
      </div>
      <div v-show="store.formShow">
        <Login v-show="store.loginShow"/> 
        <Signup v-show="!store.loginShow" />
      </div>
    </div>
  </div>
</template>

<style>
.landing-body{
  display: flex;
  justify-content: center;
  background: #f5f5f5;
}
.landing-main-container{
  display: flex;
  flex-grow: 1;
  max-width: 1400px;
  min-height: 100vh;
}
.landing-left, .landing-right{
  width: 50%; 
  display: flex;
  justify-content: center;
  align-items: center;
}
.landing-right{
  background: url(../assets/hotel.png) center;
}
.landing-left{
  flex-direction: column;
}
.landing-big-text{
  padding: 2.5rem 3rem;
  margin: 1.5rem;
  color: #1c1c1c;
}
.landing-big-text h1 {
  color: #305c69;
  font-size: 4rem;
  font-weight: 600  ;
}
.landing-action-call{
  display: flex;
  gap: 25px;
  margin: 2rem 0;
  justify-self: flex-end;
}
.btn{
  padding: .5rem 1.8rem;
  font-size: 1.2rem;
  font-weight: 500;
  border: 0;
  border-radius: 5px;
  transition: all 0.25s ease-out;
  cursor: pointer;
}
.dark-green-btn, .light-btn:hover{
  color: #f5f5f5;
  background-color: #305c69;
}
.light-green-btn{
  background-color: #305c69;
  color: #f5f5f5;
}

.light-btn, .dark-green-btn:hover, .light-green-btn:hover, .active-light-btn{
  color: #8ab3b5;
  background-color: #1c1c1c;
}


</style>