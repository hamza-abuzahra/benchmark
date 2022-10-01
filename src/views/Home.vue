<template>
  <div class="home-body">
    <div class="home-main-container">
        <div class="home-banner">
            <h1 style="color: #1c1c1c">Enter Daily Data</h1>
        </div>
        <hr style="width:90%; margin: 0 auto;">
        <div class="home-select">
            <select name="hotels" id="myprops" class="home-combobox">
            </select>
        </div>
        <div class="home-data-entry">
            <div class="home-data-entry-manual">
                <h1 style="margin: 1rem 2rem 0 2rem; color: #305c69; font-weight: 500;">Manually</h1>
                <form action="" class="home-data-entry-form">
                    <label for="">
                        Date   
                        <input type="date" id="date">
                    </label>
                    <label for="">
                        Revenue   
                        <input type="number" id="rev">
                    </label>
                    <label for="">
                        Currency   
                        <select name="" id="curr" >
                            <option value="TL">TL</option>
                            <option value="USD">USD</option>
                            <option value="EURO">EURO</option>
                        </select>
                    </label>
                    <label for="">
                        Rooms   
                        <input type="number" id="rooms">
                    </label>
                    <input type="button" class="btn home-data-entry-btn light-btn" value="Submit" @click="addRecord">
                </form>
            </div>
            <hr style="height:25rem; background-color: #305c69; align-self: center; margin: 2rem 0 0 0;">
            <div class="home-data-entry-upload">
                <h1 style="margin-top:1rem; color:#305c69; font-weight: 500; align-self: flex-start;">or Upload PDF</h1>
                <div  style="position: relative;">
                    <button type="submit" class="btn home-data-entry-btn light-btn">
                        <input type="file" class="home-file-input" id="finput" accept="application/pdf" @change="upload">
                        <font-awesome-icon icon="fa-solid fa-upload" />
                    </button>
                </div>
                <h3 style="color:#1c1c1c; font-weight:400;">PDF example</h3>
                <img src="" alt="" width="400" height="200">
            </div>
            
        </div>
        <div class="home-report-btn">
            <RouterLink to="/report">
            <button class="btn dark-green-btn"><font-awesome-icon icon="fa-solid fa-chart-column" /></button></RouterLink>
            <h3 style="color:#1c1c1c; font-weight:400; text-align: center;">Reports</h3>
            </div>
        </div>
  </div>
</template>

<script setup>
import { onMounted } from '@vue/runtime-core'
import { RouterLink, RouterView } from 'vue-router'
import router from '../router'
import { useStore } from '../stores/counter'

const store = useStore()

if (store.loggedin == false){
  router.push('/')
}
const upload = async function () {
    const data = document.querySelector('#finput').files[0]
    console.log(data)
    const comboboxel = document.querySelector('#myprops')
    const choice = comboboxel.value
    const res = await fetch(`${store.url}upload?uemail=${store.currentemail}&pname=${choice}`, {
        method: 'POST',
        body: data, 
    })
    const result = await res.json()
    if (result.stats){
        store.showMessage(result.text)
    } else store.showError(result.text)
}
const addRecord = async function() {
    const dateel = document.querySelector('#date')
    const revel = document.querySelector('#rev')
    const currel = document.querySelector('#curr')
    const roomsel = document.querySelector('#rooms')
    const comboboxel = document.querySelector('#myprops')
    const choice = comboboxel.value
    const date = dateel.value
    const curr = currel.value
    const rooms = roomsel.value
    const rev = revel.value
    const data = await store.getResponse("addRecord", `uemail=${store.currentemail}&pname=${choice}&date=${date}&rev=${rev}&rooms=${rooms}&curr=${curr}`)
    if (data.status) {
        store.showMessage(data.text)
        dateel.value = ''
        revel.value = ''
        currel.value = 'TL'
        roomsel.value = ''
    } else {
        store.showError(data.text)
    }
}

const getmyproperty = async function(){
    const data = await store.getResponse('getmyproperty', `username=${store.currentemail}`)
    const comboboxel = document.querySelector('#myprops')
    comboboxel.innerHTML = ''
    let mypropsdata = {}
    data.forEach((element, index) => {
        const prop_name = element.pname
        if (index == 0) comboboxel.innerHTML += `<option value="${prop_name}" selected>${prop_name}</option>`
        else comboboxel.innerHTML += `<option value="${prop_name}">${prop_name}</option>`
        mypropsdata[prop_name] = {ploc: element.plocation, pavgocc: element.pavgocc, pavgadr:element.pavgadr, prooms:element.prooms}
    });
}
onMounted(()=>{
    getmyproperty()
    const navs = document.querySelectorAll('a')
    navs.forEach(e=>{
        if (e.id == 'home') e.classList.add('active')
        else e.classList.remove('active')
    })

    console.log(navs)
})
</script>

<style>
.home-body{
    background: url('../assets/hotel.png');
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center ;
}
.home-main-container{
    max-width: 1400px;
    background-color: #f5f5f5;
    min-height: 100vh;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    align-items: stretch;
}
.home-banner{
    margin-top: 4rem;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-grow: 1;
    max-height: 50px;
}
.home-select, .dashboard-select{
    display: flex;
    width: 90%;
    margin: 10px auto;
}
.home-combobox, .dashboard-combobox{
    padding: 2px 20px;
    font-size: 1.1rem;
    border-radius: 5px;
    background-color: #f5f5f5;
    color: #305c69  ;
}
.home-data-entry{
    width: 90%;
    margin: 0 auto;
    display: flex;
    justify-content: center;
    /* align-items: center; */
    padding: 3px;
    max-width: 1400px;
}
.home-data-entry-manual, .home-data-entry-upload{
    width: 50%;
    /* border: 1px solid yellow; */
    flex-grow: 1;
    display: flex;
    align-items: flex-start;
    flex-direction: column;
    align-items: stretch;
    min-height: 90%;
    gap: 2rem;
}
.home-data-entry-form{
    display: flex;
    flex-direction: column;
    margin: 2rem;
    gap: 20px;
    color: #1c1c1c;
    font-size: 1.5rem;
    
}
.home-data-entry-form > label{
    display: flex;
    justify-content: space-between;
    flex-grow: 1;
}
.home-data-entry-form > label > *{
    width: 8rem;
    text-align: center;
    border-radius: 10px;
    padding: .3rem .5rem;
    margin-right: 2.5rem;
}
.home-data-entry-btn{
    align-self: center;
}
.home-data-entry-upload{
    gap: 2rem;
    padding-left: 2rem;
    align-items: center;
}
.home-data-entry-upload > button{
    display: inline-block;
}
.home-report-btn{
    align-self: flex-end;
    margin-right: 3rem;
    margin-top: -3rem;
}
.home-report-btn .btn{
    border-radius: 50%;
    width: 65px;
    height: 65px;
    display: flex;
    justify-content: center;
    align-items: center;
}
.home-file-input{
    opacity: 0;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}
</style>
