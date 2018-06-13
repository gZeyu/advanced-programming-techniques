## 大作业: 基于 Vue 与 django 的空气质量查询单页应用

##项目

- github : https://github.com/gZeyu/advanced-programming-techniques

```
advanced-programming-techniques
├── final //空气质量查询单页应用
│   ├── air-data //从http://beijingair.sinaapp.com/下载的空气质量数据
│   ├── backend //后端工程项目
│   ├── frondend //前端工程项目
│   └── script //数据处理脚本
├── hw01
├── hw02
├── hw03
└── hw04
```

## 项目建构简单介绍

### 数据库设计

```
sql = '''CREATE TABLE IF NOT EXISTS `%s` (
                        `meas_time` DATE NOT NULL,
                        `meas_hour` TINYINT NOT NULL,
                        `aqi` FLOAT NOT NULL,
                        `pm2_5` FLOAT NOT NULL,
                        `pm2_5_24h` FLOAT NOT NULL,
                        `pm10` FLOAT NOT NULL,
                        `pm10_24h` FLOAT NOT NULL,
                        `so2` FLOAT NOT NULL,
                        `so2_24h` FLOAT NOT NULL,
                        `no2` FLOAT NOT NULL,
                        `no2_24h` FLOAT NOT NULL,
                        `o3` FLOAT NOT NULL,
                        `o3_24h` FLOAT NOT NULL,
                        `o3_8h` FLOAT NOT NULL,
                        `o3_8h_24h` FLOAT NOT NULL,
                        `co` FLOAT NOT NULL,
                        `co_24h` FLOAT NOT NULL,
                        UNIQUE KEY (`meas_time`, `meas_hour`)
                        );''' % (city_name + table_suffix)
```

## 后端设计

- **django**+**mysql**

### api

#### 获取城市列表

- 简要描述：获取城市列表接口
- 请求 URL：http://xx.com/air
- 请求方式：GET
- 参数：

| 参数名         | 必选 | 类型 | 说明     |
| -------------- | ---- | ---- | -------- |
| city_name_list | 是   | 无   | 城市列表 |

- 使用实例

```
http://xx.com/air/?city_name_list
```

- 返回示例

```
{
	"city_name_list": ["七台河", "三亚", "三明", ...... , "齐齐哈尔", "龙岩"]
}
```

#### 获取天气质量数据

- 简要描述：获取天气质量数据
- 请求 URL：http://xx.com/air
- 请求方式：GET
- 参数：

| 参数名     | 必选 | 类型   | 说明     |
| ---------- | ---- | ------ | -------- |
| city_name  | 是   | 字符串 | 城市名   |
| begin_date | 是   | 字符串 | 起始日期 |
| end_date   | 是   | 字符串 | 结束日期 |

- 使用实例

```
http://xx.com/air/?city_name=北京&begin_date=2017-01-01&end_date=2017-01-02
```

- 返回示例

```
{
	"aqi": [454.211, 220.9],
	"pm2_5": [430.211, 161.65],
	"pm2_5_24h": [362.105, 309.5],
	"pm10": [501.684, 274.278],
	"pm10_24h": [417.947, 468.45],
	"so2": [8.053, 12.65],
	"so2_24h": [15.368, 10.25],
	"no2": [131.211, 92.45],
	"no2_24h": [130.421, 119.05],
	"o3": [4.105, 24.4],
	"o3_24h": [11.158, 40.55],
	"o3_8h": [3.895, 23.9],
	"o3_8h_24h": [4.526, 26.9],
	"co": [6.432, 3.139],
	"co_24h": [5.345, 5.085],
	"date": ["2017-01-01", "2017-01-02"],
	"city_name": "北京",
	"begin_date": "2017-01-01",
	"end_date": "2017-01-2"
}
```

## 前端设计

- **vue.js**+**element-ui**+**axios.js**+**v-charts**

### 工程目录结构

```
frondend
├── build
├── config
├── index.html
├── node_modules
├── package.json
├── package-lock.json
├── README.md
├── src
├── static
└── test
```

```
frondend/src
├── App.vue
├── components
│   ├── charts
│   │   ├── AQIChart.vue
│   │   ├── AQIPie.vue
│   │   ├── COChart.vue
│   │   ├── ComprehensiveChart.vue
│   │   ├── NO2Chart.vue
│   │   ├── O3Chart.vue
│   │   ├── PM10Chart.vue
│   │   ├── PM2_5Chart.vue
│   │   └── SO2chart.vue
│   ├── CityComparisonPage.vue
│   ├── Header.vue
│   ├── MonitoringCurvePage.vue
│   └── NavMenu.vue
├── config
│   └── menu-config.js
├── main.js
├── router
│   └── index.js
└── utils
    └── bus.js
```

#### 模仿的网站

- 中国空气质量在线分析平台 : [https://www.aqistudy.cn/](https://note.youdao.com/)

#### 前端界面

![image](https://note.youdao.com/yws/api/personal/file/WEBd1bacff58dd34c06d62bf295eb4a04d3?method=download&shareKey=cb968b66334f4ba5a11998afc0998469)
