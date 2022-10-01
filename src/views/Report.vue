<template>
  <div class="home-body">
    <div class="home-main-container">
        <div class="report-btns">
            <div class="report-btns-left" @click="changeDate">
                <button name="quick-btns" class="btn light-green-btn medium active-light-btn" value="w">Last Week</button>
                <button name="quick-btns" class="btn light-green-btn medium" value="m">This Month</button>
                <button name="quick-btns" class="btn light-green-btn medium" value="y">Last Year</button>
                <button name="quick-btns" class="btn light-disabled-btn medium" id="custom-btn">Custom</button>
            </div>
            <div class="report-btns-right">
                <button class="btn medium dark-disabled-btn" id="show-btn" @click="filter">Show</button>
                <button class="btn light-green-btn medium">Export <font-awesome-icon icon="fa-solid fa-download" /></button>
            </div>
        </div>
        <div class="report-filters">
            <select name="hotels" id="reprot-myprops" class="home-combobox" @change="customDate"></select>
            <div class="report-filters-start">
                <label for="">Starting Date</label>
                <input type="date" id="start-date" @change="customDate">
            </div>
            <div class="report-filters-end">
                <label for="">Ending Date</label>
                <input type="date" id="end-date" @change="customDate">
            </div>
            <div class="report-filters-radio">
                <form action="">
                    <input type="radio" name="view" id="daily" checked> 
                    <label for="daily">Daily</label>
                    <!-- <input type="radio" name="view" id="weekly" disabled> 
                    <label for="weekly">Weekly</label>
                    <input type="radio" name="view" id="monthly" disabled> 
                    <label for="monthly">Monthly</label> -->
                </form>
                <form action="">
                    <input type="checkbox" name="" id="occ" value="2" checked @change="hideCol"> 
                    <label for="occ">Occupancy</label>
                    <input type="checkbox" name="" id="adr" value="3" checked @change="hideCol"> 
                    <label for="adr">ADR</label>
                    <input type="checkbox" name="" id="revpar" value="4" checked @change="hideCol"> 
                    <label for="revpar">RevPAR</label>
                </form>
            </div>
        </div>
        <hr style="width:90%; margin: 0 auto;">
        <table class="report-table">
            <colgroup>
                <col span="1" id="col1">
                <col span="1" id="col2">
                <col span="1" id="col3">
                <col span="1" id="col4">
            </colgroup>
            <tr>
                <th>Date</th>
                <th>Occupancy</th>
                <th>ADR</th>
                <th>RevPAR</th>
            </tr>
            <tbody>
                <tr v-for="data in reportRecords" :key="data.date">
                    <td>{{data.rdate}}</td>
                    <td>{{data.occupancy}}%</td>
                    <td>{{data.adr}}</td>
                    <td>{{data.revpar}}</td>
                </tr>
            </tbody>
        </table>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, watch } from "@vue/runtime-core"
import router from "../router"
import { useStore } from "../stores/counter"

const store = useStore()
if (store.loggedin == false){
  router.push('/')
}
let mypropsdata = {}

const filter = function (e) {
    if (e.target.classList.contains('dark-disabled-btn')) return
    e.target.classList.add('dark-disabled-btn')
    e.target.classList.remove('light-green-btn')
    const startdateel = document.querySelector('#start-date')
    const enddateel = document.querySelector('#end-date')
    if (startdateel.value == store.lastsdate && enddateel.value == store.lastedate) return
    loadReports()
}

const customDate = function (e) {
    const btns = document.getElementsByName('quick-btns')
    btns.forEach((btn)=> btn.classList.remove('active-light-btn'))
    document.querySelector('#custom-btn').classList.add('active-light-btn')
    document.querySelector('#custom-btn').classList.remove('light-disabled-btn')
    const sbtn = document.getElementById('show-btn')
    sbtn.classList.remove('dark-disabled-btn')
    sbtn.classList.add('light-green-btn')
}

const changeDate = function (e) {
    if (!e.target.value) return
    const btns = document.getElementsByName('quick-btns')
    btns.forEach((btn)=> btn.classList.remove('active-light-btn'))
    document.querySelector('#custom-btn').classList.add('light-disabled-btn')
    e.target.classList.add('active-light-btn')
    const timeframe = e.target.value
    const edel = document.getElementById("end-date")
    const sdel = document.getElementById("start-date")
    var date = new Date()
    var day = date.getDate();
    var month = date.getMonth() + 1;
    var year = date.getFullYear();
    if (month < 10) month = "0" + month;
    if (day < 10) day = "0" + day;

    var today = year + "-" + month + "-" + day;       
    edel.value = today;

    var week = new Date(Date.now())
    if (timeframe == "w") var week = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
    if (timeframe == "m") week.setDate(1)
    var wday = week.getDate();
    var wmonth = week.getMonth() + 1;
    var wyear = week.getFullYear();
    if (timeframe == "y") wyear -= 1
    if (wmonth < 10) wmonth = "0" + wmonth;
    if (wday < 10) wday = "0" + wday;
    var wtoday = wyear + "-" + wmonth + "-" + wday;     
    sdel.value = wtoday;

    const sbtn = document.getElementById('show-btn')
    sbtn.classList.remove('dark-disabled-btn')
    sbtn.classList.add('light-green-btn')
}


const reportRecords = computed(()=>store.records)

const hideCol = function (e) {
    const id = `col${e.target.value}`
    const colel = document.getElementById(id)
    colel.classList.toggle('hide-col')
}

const loadReports = async function() {
    const startdateel = document.querySelector('#start-date')
    const enddateel = document.querySelector('#end-date')
    const choiceel = document.querySelector('#reprot-myprops')
    const pname = choiceel.value
    const data = await store.getResponse('loadRecords', `uemail=${store.currentemail}&pname=${pname}&sd=${startdateel.value}&ed=${enddateel.value}`)
    data.data.forEach((record, index)=>{
        var datestr = record.rdate
        var date = new Date(datestr)
        var day = date.getDate()
        var month = date.getMonth() + 1
        var year = date.getFullYear()
        if (month < 10) month = "0" + month;
        if (day < 10) day = "0" + day;
        var rdate = year + "-" + month + "-" + day; 
        record.rdate = rdate
        record['occupancy'] = ((parseInt(record.rrooms)  / mypropsdata[pname].prooms) * 100).toFixed(2)
        record['adr'] = (parseFloat(record.rrevenue) / parseInt(record.rrooms)).toFixed(2)
        record['revpar'] = (parseFloat(record.rrevenue) / mypropsdata[pname].prooms).toFixed(2)
    })
    store.lastedate = enddateel.value
    store.lastsdate = startdateel.value
    store.records = data.data
}

const getmyproperty = async function(){
    const data = await store.getResponse('getmyproperty', `username=${store.currentemail}`)
    const comboboxel = document.querySelector('#reprot-myprops')
    mypropsdata = {}
    data.forEach((element, index) => {
        const prop_name = element.pname
        mypropsdata[prop_name] = {ploc: element.plocation, pavgocc: element.pavgocc, pavgadr:element.pavgadr, prooms:element.prooms}
        if (index == 0) comboboxel.innerHTML += `<option value="${prop_name}" selected>${prop_name}</option>`
        else comboboxel.innerHTML += `<option value="${prop_name}">${prop_name}</option>`
        
    });
}
onMounted(async () => {
    const navs = document.querySelectorAll('a')
    navs.forEach(e=>{
        if (e.id == 'report') e.classList.add('active')
        else e.classList.remove('active')
    })
    await getmyproperty()
    var date = new Date()
    var day = date.getDate();
    var month = date.getMonth() + 1;
    var year = date.getFullYear();
    if (month < 10) month = "0" + month;
    if (day < 10) day = "0" + day;

    var today = year + "-" + month + "-" + day;       
    document.getElementById("end-date").value = today;

    var week = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
    var wday = week.getDate();
    var wmonth = week.getMonth() + 1;
    var wyear = week.getFullYear();
    if (wmonth < 10) wmonth = "0" + wmonth;
    if (wday < 10) wday = "0" + wday;

    var wtoday = wyear + "-" + wmonth + "-" + wday;     
    document.getElementById("start-date").value = wtoday;
    await loadReports()

})


</script>

<style>
.report-btns {
    margin-top: 4rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 4rem 3rem 0 3rem;
}
.report-btns-left{
    display: flex;
    align-items: center;
    gap: 20px;
}
.report-btns-right{
    display: flex;
    gap: 20px;
    flex-direction: row;
}
.dark-disabled-btn{
    background-color: #8ab3b5;
    color: #1c1c1c;
    cursor: default;
}
.light-disabled-btn{
    background-color: #305c69;
    color: #f5f5f5;
    cursor: default;
}
.medium{
    font-size: 1rem;
    padding: .3rem 1rem;
}
.report-filters{
    margin: .5rem 3rem;
    display: flex;
    align-items: center;
    gap: 3rem;
    color: #1c1c1c;
}
.report-filters-start, .report-filters-end{
    display: flex;
    flex-direction: column;
    gap: .5rem;
    align-items: center;
}
.report-filters-radio{
    display: flex;
    flex-direction: column;
    gap: .5rem;
}
.report-filters-radio > form {
    display: flex;
    gap: .8rem;
}
.report-table{
    margin: 1rem 3rem;
    color: #f5f5ff;
    border-collapse: collapse;
    font-size: 1.2rem;
    border-radius: 5px;
    overflow: hidden;
}
.report-table tr th{
    background-color: #305c69;
    color: #f5f5f5;
    padding: .1rem;
}
.report-table td{
    padding: .5rem 2rem;
}
.report-table tbody tr{
    border-bottom: 1px solid #f5f5ff;
    background-color: #f5f5f5;
    color: #1c1c1c;
    text-align: center;
}
.report-table tbody tr:nth-of-type(even) {
    background-color: #e6e4e4;
}
.report-table tbody tr:last-of-type {
    border-bottom: 3px solid #305c69;
}
.hide-col {
    visibility: collapse;
}
</style>