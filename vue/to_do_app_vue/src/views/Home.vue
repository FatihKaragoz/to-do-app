<template>
  <div class="home">
    <h1 class="title"> Yeni Görev Ekle </h1>
    <hr>
    <div class="columns">
      <div class="column is-4 " style="background-color:#7dc6c7;">
        <form v-on:submit.prevent="addTask">
          <h2 class="subtitle"> Task ekle</h2>

          <div class="field">
            <label class="label">Başlık</label>
            <div class="control"> 
              <input class="input" v-model="title" id="title" type="text">
            </div>
          </div>
          
          <div class="field">
            <label class="label">Açıklama</label>
            <div class="control"> 
              <textarea class="input" v-model="description" id="description" type="text"></textarea>
            </div>
          </div>
          
          <!-- <div class="field">
            <label class="label">Durum</label>
            <div class="control"> 
              <div class="select"> 
                <select>
                  <option value="todo">Yapılacak</option>
                  <option value="done">Tamamlandı</option>
                </select>
              </div>
            </div>
          </div> -->
          <div class="field">
            <label class="label">Atanmış Kişi</label>
            <div class="control"> 
              <div class="select"> 
                <select v-model='assigned_user_id'>
                <!-- eslint-disable -->
                  <option v-for="user in users" :value="user.id">{{ user.get_full_name }}</option>
                <!-- eslint-enable -->
                </select>
              </div>
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
    
      <h1 class="title"> Görevlerim </h1>
    <div class="columns">
      <div class="column is-6"  style="background-color:#7dc6c7;">
        <h2 class="subtitle">Yapılacaklar</h2>
        <div class="to_do">
          <!-- eslint-disable -->
          <div class="card" v-for="task in tasks" :value="task.id" v-if="task.status == 'to_do'" v-bind:key="task.id">
            <!-- eslint-enable -->
            <div class="card-content">
              <div class="is-row">
                <div class="columns">
                  <div class="column is-10"  style="background-color:#7dc6c7;">
                    <div class="is-row">
                      <h3>{{ task.title }} {{ task.created_at }} Tarihinde {{ task.created_by }} tarafından.  </h3>
                    </div>
                    <div class="is-row">
                      {{ task.description }} 
                    </div>

                  </div>
                  <div class="column is-2"  style="background-color:#7dc6c7;">
                    <a class="button is-link" v-on:click="setStatus(task.id,'done')">Yapıldı</a>
                  </div>
                </div>

              </div>
            </div>

          </div>
          <footer class="card-footer">
          </footer>
        </div>
      </div>
      
      <div class="column is-6"  style="background-color:#abfcff;">
        <h2 class="subtitle">Yapılanlar</h2>
        <div class="done">
          <!-- eslint-disable -->
          <div class="card" v-for="task in tasks" :value="task.id" v-if="task.status === 'done'" v-bind:key="task.id">
            <!-- eslint-enable -->
            <div class="card-content">
              <div class="is-row">
                <div class="columns">
                  <div class="column is-12"  style="background-color:#7dc6c7;">
                    <div class="is-row">
                      <h3>{{ task.title }} {{ task.created_at }} Tarihinde {{ task.completed_by }} tarafından atandı.  </h3>
                    </div>
                    
                    <div class="is-row">
                      <h3>{{ task.completed_at }} Tarihinde tamamlandı.  </h3>
                    </div>
                    <div class="is-row">
                      {{ task.description }} 
                    </div>

                  </div>
                  
                </div>

              </div>
            </div>
          </div>
          
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import router from '../router/index'
import Variables from '../controllers/helper'

export default {
  tasks : '',
  name: "Home",
  data () {
    return {
      tasks: [],
      users: [],
      description: '',
      title: '',
      status: 'to_do',
      assigned_user_id : ''
    }
  },
  mounted (){
    this.getInfos()
  },
  methods: {
    getInfos(){
      // TASKLERİ GETİR
      axios.post(
        Variables.BACKEND_URL+'/tasks/',
        {},
        Variables.getDefaultConfig()
      )
      .then(response => {
        console.log(response.status)
        this.tasks = response.data;
        
        console.log(response.data);
        })
      .catch(function (error) {
        if (error.response) {
          // console.log();
          if ( error.response.status == 401 ){
            // window.location.href = '/about'
            localStorage.token = '';
            router.push('/login');

          }
        }
      })
      // USERLARI GETİR
      axios.post(
        Variables.BACKEND_URL+'/users/',
        {},
        Variables.getDefaultConfig()
      )
      .then(response => {
        console.log(response.status)
        this.users = response.data;
        
        console.log(response.data); 
        })
      .catch(function (error) {
        if (error.response) {
          // console.log();
          if ( error.response.status == 401 ){
            // window.location.href = '/about'
            localStorage.token = '';
            router.push('/login');

          }
        }
      })
        
    },
    addTask(){
      if(this.description){
        axios.post(
          Variables.BACKEND_URL+'/tasks/',
          {
            process : 'new', 
            description : this.description,
            status : this.status,
            assigned_user_id : this.assigned_user_id,
          },
          Variables.getDefaultConfig()
        )
        .then((response) => {
            let newTask = {
              'id' : response.data.id,
              'description' : this.description,
              'status' : this.status,
            }
            this.tasks.push(newTask)
            this.description = ''
            this.status = 'to_do'
            console.log('Yeni Task Eklendi');
            
          }).catch((error) => {
            console.log('ERROR',error)
          })

      }
    },
    setStatus(task_id,status){
      console.log('STATUS SET',task_id,status)
      axios.post(
        Variables.BACKEND_URL + '/tasks/',
        {
          process : 'change',
          status : status,
          id : task_id
        },
        Variables.getDefaultConfig()
      ).then((response) => {
        console.log(response)
            let changedTask = {
              'id' : response.data.id,
              'description' : response.data.description,
              'status' : response.data.status,
            }
            // this.tasks.splice(, 1);
            this.tasks.splice(this.tasks.findIndex(f => f.id === response.data.id),1, changedTask)

            // this.$delete(this.tasks, response.data.id);
            // this.$forceUpdate();
            // this.tasks.splice(response.data.id,1);
            // this.tasks.push(changedTask)
            

            
          }).catch((error) => {
            console.log('ERROR',error)
          })
    }
    
  }

};
</script>


<style lang="scss">
  .select, select{
    width:100%;
  }
  .home{
    margin:50px;
  }
  .card{
    margin-bottom:20px;
  }

  .done{
    opacity : 0.7;
  }
</style>

