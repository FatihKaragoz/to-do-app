// import { config } from "vue/types/umd";

class Variables{
    BACKEND_URL = 'http://127.0.0.1:8004';
    flag = false;
    // eslint-disable
    // authenticated =  false;
    config = {  withCredentials : false, headers : {} }
    checkLoggedStatus = () => {
        console.log('CHECK ICINDE TOKEN : ' + localStorage.token)
        if(localStorage.token && localStorage.token != null){
            return true;
        }else{
            return false;
        }
    }
    getDefaultConfig = () => {
        this.config.headers =  {}
        if(localStorage.token){
            this.config.headers.Authorization = 'Bearer ' + localStorage.token;
        } 
        return this.config
    }
}

export default new Variables();
