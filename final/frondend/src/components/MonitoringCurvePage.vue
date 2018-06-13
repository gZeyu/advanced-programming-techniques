<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="2.5">
        <el-select v-model="cityName" filterable placeholder="请选择城市">
          <el-option v-for="item in cityNameOption" :key="item.value" :label="item.label" :value="item.value">
          </el-option>
        </el-select>
      </el-col>
      <el-col :span="4.5">
        <el-date-picker v-model="dateRange" type="daterange" start-placeholder="开始日期" end-placeholder="结束日期" value-format="yyyy-MM-dd" unlink-panels>
        </el-date-picker>
      </el-col>
      <el-col :span="2">
        <el-button @click="search" type="primary" icon="el-icon-search" round></el-button>
      </el-col>
    </el-row>
    <el-row>
      <el-tabs type="border-card">
        <el-tab-pane label="AQI">
          <div class="aqi-charts-box">
            <div class="charts">
              <aqichart></aqichart>
              <aqipie></aqipie>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="综合">
          <div class="charts-box">
            <div class="charts">
              <comprehensivechart></comprehensivechart>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="PM2.5">
          <div class="charts-box">
            <div class="charts">
              <pm25chart></pm25chart>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="PM10">
          <div class="charts-box">
            <div class="charts">
              <pm10chart></pm10chart>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="CO">
          <div class="charts-box">
            <div class="charts">
              <cochart></cochart>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="NO2">
          <div class="charts-box">
            <div class="charts">
              <no2chart></no2chart>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="O3">
          <div class="charts-box">
            <div class="charts">
              <o3chart></o3chart>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="SO2">
          <div class="charts-box">
            <div class="charts">
              <so2chart></so2chart>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-row>
    <!-- {{message}} -->
    <!-- <button v-on:click="search">search</button> -->
  </div>
</template>

<script>
import axios from 'axios'
import AQIChart from '@/components/charts/AQIChart'
import AQIPie from '@/components/charts/AQIPie'
import ComprehensiveChart from '@/components/charts/ComprehensiveChart'
import PM25Chart from '@/components/charts/PM2_5Chart'
import PM10Chart from '@/components/charts/PM10Chart'
import COChart from '@/components/charts/COChart'
import NO2Chart from '@/components/charts/NO2Chart'
import O3Chart from '@/components/charts/O3Chart'
import SO2chart from '@/components/charts/SO2chart'
import Bus from '@/utils/bus'
axios.defaults.withCredentials = true
export default {
  // name: 'monitoringcurvepage',
  components: {
    'aqichart': AQIChart,
    'aqipie': AQIPie,
    'comprehensivechart': ComprehensiveChart,
    'pm25chart': PM25Chart,
    'pm10chart': PM10Chart,
    'cochart': COChart,
    'no2chart': NO2Chart,
    'o3chart': O3Chart,
    'so2chart': SO2chart
  },
  data () {
    return {
      baseURL: 'http://10.0.0.28:8000',
      dateRange: ['2017-12-01', '2017-12-31'],
      cityNameOption: [],
      cityName: '北京',
      message: ''
    }
  },
  methods: {
    search () {
      var url = '/air/?city_name=' + this.cityName + '&begin_date=' + this.dateRange[0] + '&end_date=' + this.dateRange[1]
      var instance = axios.create({
        baseURL: this.baseURL,
        withCredentials: true
      })
      instance.get(url)
        .then(response => {
          this.message = response.data
          Bus.$emit('monitoring-curve-page-search', this.message)
          // console.log(response.data)
          // console.log(response.status)
          // console.log(response.statusText)
          // console.log(response.headers)
          // console.log(response.config)
        })
    }
  },
  mounted: function () {
    this.search()
    this.$nextTick(function () {
      var instance = axios.create({
        baseURL: this.baseURL,
        withCredentials: true
      })
      instance.get('/air/?city_name_list')
        .then(response => {
          for (var cityName of response.data['city_name_list']) {
            this.cityNameOption.push({
              value: cityName,
              label: cityName
            })
          }
        })
    })
  }
}
</script>
<style>
.el-row {
  margin-bottom: 20px;
}
.el-col {
  border-radius: 4px;
}
.aqi-charts-box {
  position: relative;
  width: 800px;
  height: 800px;
  margin: 20px auto;
}
.charts-box {
  position: relative;
  width: 800px;
  height: 400px;
  margin: 20px auto;
}
.charts {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  top: 0;
  margin: auto;
  width: 800px;
  height: auto;
  /* background-color: rgba(245, 248, 245, 0.925); */
}
</style>
