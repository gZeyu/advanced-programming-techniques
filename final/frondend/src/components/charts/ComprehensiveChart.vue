<template>
  <ve-line :data="chartData" :data-zoom="dataZoom" :toolbox="toolbox" width="800px" height="400px">
  </ve-line>
</template>

<script>
import 'echarts/lib/component/dataZoom'
import 'echarts/lib/component/toolbox'
import Bus from '@/utils/bus'
export default {
  data () {
    this.toolbox = {
      left: 'left',
      feature: {
        dataZoom: {
          yAxisIndex: 'none'
        },
        restore: {},
        saveAsImage: {}
      }
    }
    this.dataZoom = [{
      startValue: 0
    }, {
      type: 'inside'
    }]
    return {
      chartData: {
        columns: ['日期', 'AQI', 'PM2.5', 'PM10', 'CO', 'NO2', 'O3', 'SO2'],
        rows: []
      }
    }
  },
  mounted: function () {
    Bus.$on('monitoring-curve-page-search', (message) => {
      let columns = ['日期', 'AQI', 'PM2.5', 'PM10', 'CO', 'NO2', 'O3', 'SO2']
      let rows = []
      for (let i = 0, len = message['date'].length; i < len; i++) {
        rows.push(
          {
            '日期': message['date'][i],
            'AQI': message['aqi'][i],
            'PM2.5': message['pm2_5'][i],
            'PM10': message['pm10'][i],
            'CO': message['co'][i],
            'NO2': message['no2'][i],
            'O3': message['o3'][i],
            'SO2': message['so2'][i]
          }
        )
      }
      let chartData = { columns, rows }
      this.chartData = chartData
    })
  }
}
</script>
