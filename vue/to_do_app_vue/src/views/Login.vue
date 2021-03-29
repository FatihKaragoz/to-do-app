<template>
  <div class="columns">
      <div class="column is-3 is-offset-3">
        <form @submit.prevent="login">
          <h2 class="subtitle"> Giriş Yap</h2>

          <div class="field">
            <label class="label">Email</label>
            <div class="control"> 
              <input class="input" v-model="email" id="email" type="text">
            </div>
          </div>
          
          <div class="field">
            <label class="label">Parola</label>
             <div class="control"> 
              <input class="input" v-model="pass" id="pass" type="password">
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
    // console.log("CHECK :" + Variables.checkLoggedStatus());
    
    return { 
      email : '',
      pass : '',
    }
  },
  
  methods: {
    login: function () {
      if(this.email != "" && this.pass != "") {
          if(this.email && this.pass) {
              const Formdata = new FormData();
              Formdata.append('email', this.email);
              Formdata.append('password', this.pass);
              Formdata.append('withCredentials', false);

              axios.post(
                Variables.BACKEND_URL+'/login/',
                Formdata,
                Variables.getDefaultConfig()
              )
              .then(response => {
                console.log(response.data)
                if (response.status == 200){
                    localStorage.token = response.data.token;
                    router.push('/');
                  }
                })
              .catch(function (error) {
                if (error.response) {
                  if ( error.response.status != 200 ){
                    router.push('/login').catch(() => {
                      console.log('HATA HALİNDE')
                      
                      localStorage.removeItem('token')
                    });
                  }
                }
              })
          } else {
              console.log("The username and / or password is incorrect");
          }
      } else {
          console.log("A username and password must be present");
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

