<template>
  <ve-line :data="chartData" :data-zoom="dataZoom" :mark-area="markArea" :mark-line="markLine" :mark-point="markPoint" :yAxis="yAxis" :toolbox="toolbox" :visual-map="visualMap" width="800px" height="400px">
  </ve-line>
</template>

<script>
import 'echarts/lib/component/dataZoom'
import 'echarts/lib/component/markArea'
import 'echarts/lib/component/markLine'
import 'echarts/lib/component/markPoint'
import 'echarts/lib/component/toolbox'
import 'echarts/lib/component/visualMap'
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

    this.yAxis =
      {
        max: 500
      }

    this.dataZoom = [{
      startValue: 0
    }, {
      type: 'inside'
    }]

    this.visualMap = {
      top: 10,
      right: 10,
      pieces: [{
        gt: 0,
        lte: 50,
        color: '#096'
      }, {
        gt: 50,
        lte: 100,
        color: '#ffde33'
      }, {
        gt: 100,
        lte: 150,
        color: '#ff9933'
      }, {
        gt: 150,
        lte: 200,
        color: '#cc0033'
      }, {
        gt: 200,
        lte: 300,
        color: '#660099'
      }, {
        gt: 300,
        color: '#7e0023'
      }],
      outOfRange: {
        color: '#999'
      }
    }

    this.markLine = {
      silent: true,
      data: [
        {
          yAxis: 50,
          label: { show: false }
        },
        {
          yAxis: 100,
          label: { show: false }
        },
        {
          yAxis: 150,
          label: { show: false }
        },
        {
          yAxis: 200,
          label: { show: false }
        },
        {
          yAxis: 300,
          label: { show: false }
        },
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
          type: 'min'
        }
      ]
    }
    // this.markArea = {
    //   label: { show: true, position: 'insideTopLeft' },
    //   data: [
    //     [
    //       { name: '优', yAxis: '0' },
    //       { yAxis: '50' }
    //     ],
    //     [
    //       { name: '良', yAxis: '50' },
    //       { yAxis: '100' }
    //     ],
    //     [
    //       { name: '轻度污染', yAxis: '100' },
    //       { yAxis: '150' }
    //     ],
    //     [
    //       { name: '中度污染', yAxis: '150' },
    //       { yAxis: '200' }
    //     ],
    //     [
    //       { name: '重度污染', yAxis: '200' },
    //       { yAxis: '300' }
    //     ],
    //     [
    //       { name: '严重污染', yAxis: '300' },
    //       { yAxis: '500' }
    //     ]
    //   ]
    // }
    return {
      chartData: {
        columns: ['日期', 'AQI'],
        rows: []
      }
    }
  },
  mounted: function () {
    Bus.$on('monitoring-curve-page-search', (message) => {
      let columns = ['日期', 'AQI']
      let rows = []
      for (let i = 0, len = message['date'].length; i < len; i++) {
        rows.push({ '日期': message['date'][i], 'AQI': message['aqi'][i] })
      }
      let chartData = { columns, rows }
      this.chartData = chartData
    })
  }
}
</script>
