<template>
  <div class="columns">
      <div class="column is-3 is-offset-3">
        <form @submit.prevent="register">
          <h2 class="subtitle"> Kayıt Ol</h2>
          <p v-if="errors.length">
            <b>Please correct the following error(s):</b>
            <ul>
              <li v-for="error in errors" v-bind:key="error">{{ error }}</li>
            </ul>
          </p>
          <div class="field">
            <label class="label">Email</label>
            <div class="control"> 
              <input class="input" v-model="email" id="email" type="text">
            </div>
          </div>
          
          <div class="field">
            <label class="label">İsim</label>
            <div class="control"> 
              <input class="input" v-model="first_name" id="first_name" type="text">
            </div>
          </div>
          
          <div class="field">
            <label class="label">Soyisim</label>
             <div class="control"> 
              <input class="input" v-model="last_name" id="last_name" type="text">
            </div>
          </div>

          <div class="field">
            <label class="label">Parola</label>
             <div class="control"> 
              <input class="input" v-model="pass" id="password" type="password">
            </div>
          </div>
          
          <div class="field">
            <label class="label">Parola(Tekrar)</label>
             <div class="control"> 
              <input class="input" v-model="pass2" id="password2" type="password">
            </div>
          </div>

          <div class="field">
            <div class="control"> 
              <button class="button is-link" >Gönder</button>
            </div>
          </div>
        </form>
      </div>
    </div>
</template>



<script>
import axios from 'axios'
import router from '../router/index'
import Variables from '../controllers/helper'


export default {
  name: "Login",

  data () {
    return { 
      errors: [],
      email : '',
      first_name : '',
      last_name : '',
      pass : '',     
      pass2 : '',     
    }
  },
  
  methods: {
    register: function () {
          if(this.email && this.pass && this.pass2) {
            if(this.password === this.password2){
              const Formdata = new FormData();
              Formdata.append('email', this.email);
              Formdata.append('password', this.pass);
              Formdata.append('first_name', this.first_name);
              Formdata.append('last_name', this.last_name);
              Formdata.append('withCredentials', false);
              axios.post(
                Variables.BACKEND_URL+'/register/',
                Formdata,
                Variables.getDefaultConfig()
              ) 
              .then(response => {
                console.log(response.data)
                if (response.status == 200){
                    localStorage.token = response.data.token;
                    router.push('/login');
                  }
                })
              .catch(function (error) {
                if (error.response) {
                  if ( error.response.status != 200 ){
                    router.push('/register').catch(() => {
                      
                      localStorage.removeItem('token')
                      // localStorage.token = null;

                    });
                  }
                }
              })
            }else{
              console.log("Passwords didn't match");
            }
              
          } else {
              console.log("Please fill out of all fields");
          }
      
    }
  }
};
</script>


<style lang="scss">
  .select, select{
    width:100%;
  }

  .card{
    margin-bottom:20px;
  }

  .done{
    opacity : 0.3;
  }
</style>

