<template>
<h1 class="title" style="display:block;"> LOGOUT </h1>
</template>



<script>
import router from '../router/index'
export default {
  name: "Logout",

  data () {
    return {

    }
  },
  mounted (){
    this.logout()
  },
  methods: {
    logout(){
        localStorage.removeItem('token');
        router.push('/login');
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

