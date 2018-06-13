<template>
  <ve-line :data="chartData" :data-zoom="dataZoom" :mark-line="markLine" :mark-point="markPoint" :toolbox="toolbox" width="800px" height="400px">
  </ve-line>
</template>

<script>
import 'echarts/lib/component/dataZoom'
import 'echarts/lib/component/markLine'
import 'echarts/lib/component/markPoint'
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
    this.markLine = {
      silent: true,
      data: [
        {
          name: 'average',
          type: 'average',
          label: { show: true, position: 'middle' },
          lineStyle: { color: 'red' }
        }
      ]
    }
    this.markPoint = {
      data: [
        {
          name: 'max',
          type: 'max',
          symbolSize: 60
        },
        {
          name: 'min',
          type: 'min',
          symbolRotate: 180
        }
      ]
    }
    return {
      chartData: {
        columns: ['日期', 'SO2'],
        rows: []
      }
    }
  },
  mounted: function () {
    Bus.$on('monitoring-curve-page-search', (message) => {
      let columns = ['日期', 'SO2']
      let rows = []
      for (let i = 0, len = message['date'].length; i < len; i++) {
        rows.push(
          {
            '日期': message['date'][i],
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
