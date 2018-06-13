<template>
  <ve-pie :data="chartData" :settings="chartSettings" :toolbox="toolbox" width="800px" height="400px">

  </ve-pie>
</template>

<script>
import 'echarts/lib/component/toolbox'
import Bus from '@/utils/bus'
export default {
  data () {
    this.toolbox = {
      left: 'left',
      feature: {
        restore: {},
        saveAsImage: {}
      }
    }
    this.chartSettings = {
      dimension: '污染',
      metrics: '天数'
    }
    return {
      chartData: {
        columns: ['污染', '天数'],
        rows: []
      }
    }
  },
  mounted: function () {
    Bus.$on('monitoring-curve-page-search', (message) => {
      let I = 0
      let II = 0
      let III = 0
      let IV = 0
      let V = 0
      let VI = 0
      for (let i = 0, len = message['aqi'].length; i < len; i++) {
        if (message['aqi'][i] !== '') {
          if (message['aqi'][i] >= 0 && message['aqi'][i] <= 50) {
            I = I + 1
          }
          if (message['aqi'][i] > 50 && message['aqi'][i] <= 100) {
            II = II + 1
          }
          if (message['aqi'][i] > 100 && message['aqi'][i] <= 150) {
            III = III + 1
          }
          if (message['aqi'][i] > 150 && message['aqi'][i] <= 200) {
            IV = IV + 1
          }
          if (message['aqi'][i] > 200 && message['aqi'][i] <= 300) {
            V = V + 1
          }
          if (message['aqi'][i] > 300) {
            VI = VI + 1
          }
        }
      }
      let columns = ['污染', '天数']
      let rows = [
        { '污染': '优 \n0-50', '天数': I },
        { '污染': '良 \n50-100', '天数': II },
        { '污染': '轻度污染 \n100-150', '天数': III },
        { '污染': '中度污染 \n150-200', '天数': IV },
        { '污染': '重度污染 \n200-300', '天数': V },
        { '污染': '严重污染 \n>300', '天数': VI }
      ]
      let chartData = { columns, rows }
      this.chartData = chartData
    })
  }
}
</script>
