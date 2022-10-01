import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useStore = defineStore('store', {
  state: () => ({ 
    loginShow: true, 
    formShow: false, 
    loggedin: true, 
    propadd: true,
    url: "http://127.0.0.1:5000/",
    currentUser: 'hamza.abuzahra@bilgiedu.net', 
    currentemail: 'hamza.abuzahra@bilgiedu.net', 
    records: [],
    lastsdate: '', 
    lastedate: ''
   }),
  getters: {

  },
  actions: {
    loginSwitch(e) {
      console.log(e)
      this.loginShow = !this.loginShow
    }, 
    showForm(e){
      this.formShow = true;
    }, 
    showLogin(e){
      this.showForm()
      this.loginShow = true;
    }, 
    showSignup(e){
      this.showForm()
      this.loginShow = false;
    },
    hideForm(e){
      const a = e.target.classList.value
      if (a.includes('login-overlay')) this.formShow = false;
    }, 
    async getResponse(method, args, httpmethod='get'){
      const requestedUrl = `${this.url}${method}?${args}`
      const res = await fetch(requestedUrl)
      const data = await res.json()
      return data
    }, 
    showError(msg){
      alert(msg)
    },
    showMessage(msg){
      alert(msg)
    }
  },
})