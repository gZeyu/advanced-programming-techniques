module.exports = [
  {
    name: '历史数据',
    id: 'HistoryData',
    icon: 'history',
    sub: [
      {
        name: '检测曲线',
        componentName: 'MonitoringCurvePage'
      },
      {
        name: '城市对比',
        componentName: 'CityComparisonPage'
      }
    ]
  },
  {
    name: '实时数据',
    id: 'RealTimeData',
    icon: 'th-large',
    sub: []
  }
]
