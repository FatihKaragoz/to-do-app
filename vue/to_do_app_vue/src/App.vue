
<template>
  <div id="app">
    <div id="nav" v-if="showMenu">
      <router-link to="/" >Görevlerim | </router-link> 
      <router-link to="/logout">Çıkış Yap</router-link> 
    </div>
    
    <div id="nav" v-else>
      <router-link to="/login">Giriş Yap |</router-link> 
      <router-link to="/register" >Kayıt Ol |</router-link>

    </div>
    <router-view />
  </div>
</template>



<style lang="scss">
@import '../node_modules/bulma';
</style>

<script>
export default {
  name: "App",
  data () {
    return {
      menu: false,
    }
  },
  computed: {
    showMenu: function () {
      if (localStorage.getItem('token') && localStorage.getItem('token') != null) {
        return true
      } else {
        return false
      }
    }
  },
  
}

</script>


