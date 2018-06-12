<template>
  <div>
    <p>{{ message }}</p>
    <button v-on:click="search">search</button>
  </div>
</template>
<script>
import axios from 'axios'
axios.defaults.withCredentials = true
export default {
  name: 'monitoringcurvepage',
  data () {
    return {
      baseURL: 'http://10.0.0.28:8000',
      message: 'aaaaaaaaaaaaaaaaaa'
    }
  },
  methods: {
    search () {
      var instance = axios.create({
        baseURL: this.baseURL,
        withCredentials: true
      })
      instance.get('/air/?city_name=北京&begin_date=2017-01-01&end_date=2017-12-31')
        .then(response => {
          this.message = response.data
          console.log(response.data)
          console.log(response.status)
          console.log(response.statusText)
          console.log(response.headers)
          console.log(response.config)
        })
    }
  }
}
</script>
