<template>
    <div class="home-body">
        <div class="home-main-container">
            <div class="home-banner">
                <div class="dashboard-select">
                    <select name="hotels" id="properties" class="dashboard-combobox" @change="update">
                    </select>
                    <button class="btn light-btn dashboard-btn" @click="showAdd"><font-awesome-icon icon="fa-solid fa-plus" /></button>
                    <button class="btn light-btn dashboard-btn" @click="showEdit"><font-awesome-icon icon="fa-solid fa-pen" /></button>
                </div>
            </div>
            <hr style="width:90%; margin: 0 auto;">
            <div class="dashboard-main">
                <div class="dashboard-stat">
                    <div>
                        <font-awesome-icon icon="fa-solid fa-bed" class="dashboard-stat-icon" />
                        <p style="color:#1c1c1c; text-align: center;">Rooms</p>
                    </div>
                    <h1 style="font-size: 6rem; color: #1c1c1c;"><span id="drooms"  class="count"></span></h1>
                </div>
                <div class="dashboard-stat">
                    <div>
                        <font-awesome-icon icon="fa-solid fa-arrow-trend-up" class="dashboard-stat-icon" />
                        <p style="color:#1c1c1c; text-align: center;">Avg. ADR</p>
                    </div>
                    <h1 style="font-size: 6rem; color: #1c1c1c;" ><span id="dadr"></span></h1>
                </div>
                <div class="dashboard-stat">
                    <div>
                        <font-awesome-icon icon="fa-solid fa-location-pin" class="dashboard-stat-icon" />
                        <p style="color:#1c1c1c; text-align: center;">Location</p>
                    </div>
                    <h1 style="font-size: 6rem; color: #1c1c1c;">{{location}}</h1>
                </div>
                <div class="dashboard-stat">
                    <div>
                        <font-awesome-icon icon="fa-solid fa-percent" class="dashboard-stat-icon" />
                        <p style="color:#1c1c1c; text-align: center;">avg. Occ.</p>
                    </div>
                    <h1 style="font-size: 6rem; color: #1c1c1c;" ><span id="docc" ><!--{{avgocc}}--></span>%</h1>
                </div>
                <div v-show="store.formShow" >
                    <div class="login-overlay" @click="store.hideForm">
                        <div class="login-modal dashboard-add-prop-modal" v-show="store.propadd">
                            <form action="">
                                <input type="text" placeholder="Name" id="add-name" class="dashboard-add-prop-input">
                                <input type="number" placeholder="# Rooms" id="add-rooms" class="dashboard-add-prop-input">
                                <input type="text" placeholder="Location (city abv.)" id="add-location" class="dashboard-add-prop-input">
                                <input type="button" value="add" class="btn dark-green-btn" @click="addProp">
                            </form>
                        </div>
                        <div class="login-modal dashboard-add-prop-modal" v-show="!store.propadd">
                            <form action="">
                                <input type="text" placeholder="name" id="edit-name" class="dashboard-add-prop-input" value>
                                <input type="number" placeholder="# Rooms" id="edit-rooms" class="dashboard-add-prop-input">
                                <input type="text" placeholder="Location (city abv.)" id="edit-location" class="dashboard-add-prop-input">
                                <input type="button" value="Update" class="btn dark-green-btn" @click="editProp">
                                <input type="button" value="Delete" class="btn dark-green-btn" @click="deleteProp">
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref } from "@vue/runtime-core";
import { useStore } from "../stores/counter";

const store = useStore()

store.formShow = false;

const rooms = ref('')
const avgocc = ref('')
const avgadr = ref('')
const location = ref('')
var props_data = {}
var currName = ''

const getmyproperty = async function(){
    const data = await store.getResponse('getmyproperty', `username=${store.currentemail}`)
    const comboboxel = document.querySelector('#properties')
    comboboxel.innerHTML = '<option value="0" selected></option>'
    props_data = {}
    data.forEach((element, index) => {
        const prop_name = element.pname
        comboboxel.innerHTML += `<option value="${prop_name}">${prop_name}</option>`
        props_data[prop_name] = {ploc: element.plocation, pavgocc: element.pavgocc, pavgadr:element.pavgadr, prooms:element.prooms, pn:element.pn}
    });
}
const clear = function() {
    location.value = ''
    const occel = document.getElementById("docc")
    occel.style.setProperty('--num', '0')
    const adrel = document.getElementById("dadr")
    adrel.style.setProperty('--num', '0')
    const roomsel = document.getElementById("drooms")
    roomsel.style.setProperty('--num', '0')
}
const update = function(e) {
    const choice = e.target.value
    if (choice == '0'){
        clear()
        return
    }
    rooms.value = props_data[choice]['prooms']
    location.value = props_data[choice]['ploc']
    avgadr.value = (props_data[choice]['pavgadr'] / props_data[choice]['pn']).toFixed(0)
    avgocc.value = (props_data[choice]['pavgocc'] / props_data[choice]['pn']).toFixed(0)
    const occel = document.getElementById("docc")
    occel.style.setProperty('--num', `${avgocc.value}`)
    const adrel = document.getElementById("dadr")
    adrel.style.setProperty('--num', `${avgadr.value}`)
    const roomsel = document.getElementById("drooms")
    roomsel.style.setProperty('--num', `${rooms.value}`)
}

const showAdd = function () {
    console.log(typeof(store.showForm))
    store.showForm()
    store.propadd = true;
    const nameel = document.querySelector('#add-name')
    const roomsel = document.querySelector('#add-rooms')
    const locationel = document.querySelector('#add-location')
    nameel.value = ''
    roomsel.value = ''
    locationel.value = ''
}
const showEdit = function () {
    const choice = document.querySelector('#properties').value
    if (choice == '0'){
        return
    }
    let name = choice
    let rooms = props_data[choice]['prooms']
    let location = props_data[choice]['ploc']
    store.showForm()
    store.propadd = false;
    const nameel = document.querySelector('#edit-name')
    const roomsel = document.querySelector('#edit-rooms')
    const locationel = document.querySelector('#edit-location')
    nameel.value = name
    roomsel.value = rooms
    locationel.value = location
    currName = name
}
const addProp = async function () {
    const nameel = document.querySelector('#add-name')
    const roomsel = document.querySelector('#add-rooms')
    const locationel = document.querySelector('#add-location')
    const name = nameel.value
    const rooms = roomsel.value
    const location = locationel.value
    const data = await store.getResponse('addProp', `username=${store.currentemail}&name=${name}&rooms=${rooms}&location=${location}`)
    if (data.status) {
        store.showMessage(data.text)
    }else {
        store.showError(data.text)
    }
    getmyproperty()
    store.formShow = false;
}
const editProp = async function () {
    const nameel = document.querySelector('#edit-name')
    const roomsel = document.querySelector('#edit-rooms')
    const locationel = document.querySelector('#edit-location')
    const name = nameel.value
    const rooms = roomsel.value
    const location = locationel.value
    const data = await store.getResponse('editProp', `old=${currName}&username=${store.currentemail}&name=${name}&rooms=${rooms}&location=${location}`)
    if (data.status) {
        store.showMessage(data.text)
    }else {
        store.showError(data.text)
    }
    getmyproperty()
    store.formShow = false;
    clear()
}
const deleteProp = async function () {
    const data = await store.getResponse('deleteProp', `pname=${currName}&username=${store.currentemail}`)
    if (data.status) {
        store.showMessage(data.text)
    }else {
        store.showError(data.text)
    }
    getmyproperty()
    store.formShow = false;
    clear()
}

onMounted(()=>{
    getmyproperty()
    const navs = document.querySelectorAll('a')
    navs.forEach(e=>{
        if (e.id == 'dashboard') e.classList.add('active')
        else e.classList.remove('active')
    })

})

</script>

<style>
@property --num {
  syntax: "<integer>";
  initial-value: 0;
  inherits: false;
}
.dashboard-select{
    justify-content: center;
    align-items: center;
    gap: 10px;
}
.dashboard-btn {
    padding: 3px .5rem;
}
.dashboard-main{
    flex-grow: 1;
    align-self: center;
    justify-content: center;
    display: flex;
    padding: 1rem;
    flex-wrap: wrap;
}
.dashboard-stat{
    width: 460px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 15px;
}
#docc{
    transition: --num 1s;
    counter-reset: num1 var(--num);
}
#dadr{
    transition: --num 1s;
    counter-reset: num2 var(--num);
}#drooms{
    transition: --num 1s;
    counter-reset: num3 var(--num);
}
#docc::after{
    content: counter(num1);
}
#dadr::after{
    content: counter(num2);
}
#drooms::after{
    content: counter(num3);
}

.dashboard-stat-icon{
    font-size: 7rem;
    color: #305c69;
}
.dashboard-add-prop-input {
    /* width: 8rem; */
    text-align: center;
    border-radius: 5px;
    padding: .3rem .5rem;
    font-size: 1rem;
}

</style>