<script setup>
import { isFunctionType } from '@vue/compiler-core';
import { RouterLink, RouterView } from 'vue-router'
import router from './router';
import { useStore } from './stores/counter'

const store = useStore()

const signout = function () {
  if (confirm("Are you sure you want to log out?")){
    store.loggedin = false;
    store.currentUser = ''
    store.currentemail = ''
    router.push('/')
  }
} 

</script>

<template> 
  <nav>
    <div class="inner-nav">
      <div class="left-nav">
        <h2>Logo</h2>
        <RouterLink to="/" id="landing" class="active" v-show="!store.loggedin">landing</RouterLink>
        <RouterLink to="/" id="about" v-show="!store.loggedin">About</RouterLink>
        <RouterLink to="/" id="contact" v-show="!store.loggedin">Contact</RouterLink>

        <RouterLink to="/home" id="home" v-show="store.loggedin">home</RouterLink>
        <RouterLink to="/dashboard"  id="dashboard" v-show="store.loggedin">dashboard</RouterLink>
        <RouterLink to="/report"  id="report" v-show="store.loggedin">report</RouterLink>
      </div>
      <div class="right-nav" @click="store.showLogin" v-show="!store.loggedin">
        Sign in 
        <span><font-awesome-icon icon="fa-solid fa-arrow-right-to-bracket" /></span>
      </div>
      <div class="right-nav" v-show="store.loggedin" @click="signout">
        {{store.currentUser}} 
        <span><font-awesome-icon icon="fa-solid fa-circle-user" /></span>
      </div>
    </div>
  </nav>
  <RouterView />

</template>

<style>
* {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
nav{
  position: absolute;
  z-index: 1;
  width: 100%;
  background-color: #1c1c1c;
  padding: .35rem 3rem;
  display: flex;
  justify-content: center;
  font-size: 1.2rem;
  user-select: none;
}
.inner-nav{
  max-width: 1400px;
  flex-grow: 1;
  display: flex;
  justify-content: space-between;
}
.left-nav, .right-nav{
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
}
.left-nav > *{
  text-decoration: none;
  color: #f5f5f5;
  font-weight: 400;
  /* padding-bottom: 10px; */
}
.right-nav {
  color: #8ab3b5;
  font-weight: 500;
  gap: 10px;
  padding: .5rem;
  transition: all .2s ease-out;
}
.right-nav:hover {
  background-color: #8ab3b5;
  color: #f5f5f5;
  border-radius: 5px;
  cursor: pointer;
}
.active{
  border-bottom: 3px solid #8ab3b5;
  padding-bottom: 5px;
}
</style>
