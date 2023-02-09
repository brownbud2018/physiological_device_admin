<template>
  <div id="main" ref="chinaRef" :style="{ height, width }"></div>
</template>
<script lang="ts">
  import { defineComponent, PropType, reactive, ref, toRefs, watch } from 'vue';
  import { useGo } from '/@/hooks/web/usePage';
  import * as echarts from 'echarts';
  import chinaMap from '/@/assets/china.json';
  //参数 数据类型配置
  interface DataProps {
    son: any;
    key: number;
  }
  /*interface DataItem {
    name: string;
    value: number;
  }*/
  export default defineComponent({
    name: 'EchartsChinaMap',
    props: {
      data1: {
        type: Object, //设置数据类型
        required: true, //是否必传
        // eslint-disable-next-line vue/require-valid-default-prop
        default: {},
      },
      width: {
        type: String as PropType<string>,
        default: '100%',
      },
      height: {
        type: String as PropType<string>,
        default: '750px',
      },
    },
    emits: ['nextStep'], //事件名称
    setup(props: any, context: any) {
      //  context子传递父的事件
      //需要展现到页面的变量
      const data2: DataProps = reactive({
        son: '子元素',
        key: 1,
        /**
         * 下一步点击
         */
        nextDown() {
          let index = data2.key++;
          context.emit('nextStep', index);
        },
      });
      const refData = toRefs(data2);
      watch(
        () => props.data1,
        (newValue, oldValue) => {
          console.log('newValue', newValue, 'oldValue', oldValue);
          console.log('data1', props.data1);
        },
      );


      const chinaRef = ref();
      setTimeout(() => {
        //console.log(props.data1);
        setData(props.data1);
      }, 30);

      const go = useGo();
      function innerClick() {
        go('/project/device');
      }
      /*function drawChinaDevice() {
        const data: DataItem[] = [
          { name: '金华', value: 157 },
          { name: '岳阳', value: 169 },
          { name: '长沙', value: 175 },
          { name: '衢州', value: 177 },
          { name: '廊坊', value: 193 },
          { name: '菏泽', value: 194 },
          { name: '合肥', value: 229 },
          { name: '武汉', value: 273 },
          { name: '大庆', value: 279 },
        ];
        const geoCoordMap: Record<string, number[]> = {
          金华: [119.64, 29.12],
          岳阳: [113.09, 29.37],
          长沙: [113, 28.21],
          衢州: [118.88, 28.97],
          廊坊: [116.7, 39.53],
          菏泽: [115.480656, 35.23375],
          合肥: [117.27, 31.86],
          武汉: [114.31, 30.52],
          大庆: [125.03, 46.58],
        };

        const convertData = function (data: DataItem[]) {
          var res = [];
          for (var i = 0; i < data.length; i++) {
            var geoCoord = geoCoordMap[data[i].name];
            if (geoCoord) {
              res.push({
                name: data[i].name,
                value: geoCoord.concat(data[i].value),
              });
            }
          }
          return res;
        };

        var option = {
          title: {
            text: '全国主要城市空气质量 - 百度地图',
            subtext: 'data from PM25.in',
            sublink: '',
            left: 'center',
          },
          tooltip: {
            trigger: 'item',
          },
          bmap: {
            center: [104.114129, 37.550339],
            zoom: 5,
            roam: true,
          },
          series: [
            {
              name: 'pm2.5',
              type: 'scatter',
              coordinateSystem: 'bmap',
              data: convertData(data),
              symbolSize: function (val) {
                return val[2] / 10;
              },
              encode: {
                value: 2,
              },
              label: {
                formatter: '{b}',
                position: 'right',
                show: false,
              },
              emphasis: {
                label: {
                  show: true,
                },
              },
            },
            {
              name: 'Top 5',
              type: 'effectScatter',
              coordinateSystem: 'bmap',
              data: convertData(
                data
                  .sort(function (a, b) {
                    return b.value - a.value;
                  })
                  .slice(0, 6),
              ),
              symbolSize: function (val) {
                return val[2] / 10;
              },
              encode: {
                value: 2,
              },
              showEffectOn: 'render',
              rippleEffect: {
                brushType: 'stroke',
              },
              label: {
                formatter: '{b}',
                position: 'right',
                show: true,
              },
              itemStyle: {
                shadowBlur: 10,
                shadowColor: '#333',
              },
              emphasis: {
                scale: true,
              },
              zlevel: 1,
            },
          ],
        };
        var myChart = echarts.init(chinaRef.value);
        echarts.registerMap('china', chinaMap); //注册可用的地图
        myChart.setOption(option);
      }

      function drawChina() {
        var myChart = echarts.init(chinaRef.value);
        echarts.registerMap('china', chinaMap); //注册可用的地图
        let regions = [
          {
            name: '新疆维吾尔自治区',
            itemStyle: {
              areaColor: '#374ba4',
              opacity: 1,
            },
          },
          {
            name: '四川省',
            itemStyle: {
              areaColor: '#fe9b45',
              opacity: 1,
            },
          },
          {
            name: '陕西省',
            itemStyle: {
              areaColor: '#fd691b',
              opacity: 1,
            },
          },
          {
            name: '黑龙江省',
            itemStyle: {
              areaColor: '#ffc556',
              opacity: 1,
            },
          },
        ];
        let scatter = [
          { name: '北京烤鸭', value: [116.46122, 39.97886, 9] },
          { name: '兰州拉面', value: [103.86615, 36.040129, 9] },
          { name: '新疆烤肉', value: [87.613228, 43.810394, 9] },
          { name: '长沙臭豆腐', value: [112.915204, 28.207735, 9] },
          { name: '西安肉夹馍', value: [108.953445, 34.288842, 9] },
          { name: '云南', value: [102.710002, 25.045806, 9] },
        ];
        var option = {
          geo: {
            map: 'china',
            roam: true, //是否允许缩放，拖拽
            zoom: 1, //初始化大小
            //缩放大小限制
            scaleLimit: {
              min: 1, //最小
              max: 2, //最大
            },
            //设置中心点
            center: [115.97, 29.71],
            //省份地图添加背景
            regions: regions,
            itemStyle: {
              areaColor: '#0b122e',
              color: 'red',
              borderColor: '#232652',
              borderWidth: 2,
            },
            //高亮状态
            emphasis: {
              itemStyle: {
                areaColor: '#1af9e5',
                color: '#fff',
              },
            },
          },
          //配置属性
          series: {
            type: 'effectScatter',
            coordinateSystem: 'geo',
            data: scatter,
            showEffectOn: 'render',
            rippleEffect: {
              //涟漪特效相关配置
              brushType: 'stroke', //波纹的绘制方式，可选 'stroke' 和 'fill'
            },
            emphasis: {
              scale: true,
            }, //是否开启鼠标 hover 的提示动画效果
            label: {
              //图形上的文本标签，可用于说明图形的一些数据信息，比如值，名称等，
              formatter: '{b}',
              position: 'right',
              show: true,
            },
            itemStyle: {
              //图形样式，是图形在默认状态下的样式；emphasis 是图形在高亮状态下的样式，比如在鼠标悬浮或者图例联动高亮时
              color: '#ffffff', //散点的颜色
              shadowBlur: 10,
              shadowColor: 20,
              fontSize: '12px',
            },
            zlevel: 1,
          },
        };
        myChart.setOption(option);
      }

      function drawChina1() {
        var myChart = echarts.init(chinaRef.value);
        echarts.registerMap('china', chinaMap); //注册可用的地图

        var optionMap = {
          tooltip: {
            trigger: 'item',
          },

          //左侧小导航图标

          visualMap: {
            show: false,

            x: 'left',

            y: 'center',

            //改变地图区域颜色

            splitList: [
              { start: 500, end: 600 },

              { start: 400, end: 500 },

              { start: 300, end: 400 },

              { start: 200, end: 300 },

              { start: 100, end: 200 },

              { start: 0, end: 100 },
            ],

            color: ['#ffff00', '#0e94eb', '#70bcf0', '#f0f26c', '#00cd00', '#eff26f'],
          },

          //配置属性

          series: [
            {
              name: '数据',

              type: 'map',

              mapType: 'china',

              roam: false,

              label: {
                show: false, //省份名称

                emphasis: {
                  show: false,
                },
              },

              data: [
                { name: '北京', value: '100' },

                { name: '天津', value: randomData() },

                { name: '上海', value: randomData() },

                { name: '重庆', value: randomData() },

                { name: '河北', value: randomData() },

                { name: '河南', value: randomData() },

                { name: '云南', value: randomData() },

                { name: '辽宁', value: randomData() },

                { name: '黑龙江', value: randomData() },

                { name: '湖南', value: randomData() },

                { name: '安徽', value: randomData() },

                { name: '山东', value: randomData() },

                { name: '新疆', value: randomData() },

                { name: '江苏', value: randomData() },

                { name: '浙江', value: randomData() },

                { name: '江西', value: randomData() },

                { name: '湖北', value: randomData() },

                { name: '广西', value: randomData() },

                { name: '甘肃', value: randomData() },

                { name: '山西', value: randomData() },

                { name: '内蒙古', value: randomData() },

                { name: '陕西', value: randomData() },

                { name: '吉林', value: randomData() },

                { name: '福建', value: randomData() },

                { name: '贵州', value: randomData() },

                { name: '广东', value: randomData() },

                { name: '青海', value: randomData() },

                { name: '西藏', value: randomData() },

                { name: '四川', value: randomData() },

                { name: '宁夏', value: randomData() },

                { name: '海南', value: randomData() },

                { name: '台湾', value: randomData() },

                { name: '香港', value: randomData() },

                { name: '澳门', value: randomData() },
              ], //数据
            },
          ],
        };
        myChart.setOption(optionMap);
      }
      function randomData() {
        return Math.round(Math.random() * 500);
      }
      var chinaGeoCoordMap: Object = {
        西安: [108.906866, 34.162109],
        柯桥区: [120.476075, 30.078038],
        拉萨: [91.140856, 29.645554],
        沈阳: [123.431474, 41.805698],
        新疆: [87.627704, 43.793026],
        台湾: [121.508903, 25.044319],
      };
      var chinaDatas = [
        [
          {
            name: '柯桥区',
            value: 0,
          },
        ],
        [
          {
            name: '拉萨',
            value: 2,
          },
        ],
        [
          {
            name: '沈阳',
            value: 1,
          },
        ],
        [
          {
            name: '新疆',
            value: 1,
          },
        ],
        [
          {
            name: '台湾',
            value: 1,
          },
        ],
      ];
      //设置投射点
      const scatterPos = [108.906866, 34.162109];

      var convertData = function (data: any) {
        var res = [];
        for (var i = 0; i < data.length; i++) {
          var dataItem = data[i];
          var fromCoord = chinaGeoCoordMap[dataItem[0].name];
          var toCoord = scatterPos;
          if (fromCoord && toCoord) {
            res.push([
              {
                coord: fromCoord,
                value: dataItem[0].value,
              },
              {
                coord: toCoord,
              },
            ]);
          }
        }
        return res;
      };
      var series: Array<any> = [];
      [['西安', chinaDatas]].forEach(function (item, i) {
        series.push(
          {
            //绘制一个新地图
            type: 'map',
            map: 'china',
            zoom: 1,
            center: [105.194115019531, 35.582111640625],
            z: -1,
            aspectScale: 0.75, //
            itemStyle: {
              areaColor: '#f00',
              borderColor: '#090438',
              borderWidth: '2',
              shadowColor: '#090438',
              shadowOffsetX: 0,
              shadowOffsetY: 15,
            },
          },
          //设置指向箭头信息
          {
            type: 'lines',
            zlevel: 2,
            effect: {
              show: true,
              period: 4, //箭头指向速度，值越小速度越快
              trailLength: 0.02, //特效尾迹长度[0,1]值越大，尾迹越长重
              symbol: 'arrow', //箭头图标
              symbolSize: 8, //图标大小
            },
            lineStyle: {
              color: '#adffd0',
              width: 1, //尾迹线条宽度
              opacity: 1, //尾迹线条透明度
              curveness: 0.3, //尾迹线条曲直度
            },
            data: convertData(item[1]),
          },
          // 发射点位置涟漪等效果
          {
            type: 'effectScatter',
            coordinateSystem: 'geo',
            zlevel: 2,
            rippleEffect: {
              //涟漪特效
              period: 4, //动画时间，值越小速度越快
              brushType: 'stroke', //波纹绘制方式 stroke, fill
              scale: 4, //波纹圆环最大限制，值越大波纹越大
            },
            label: {
              show: true,
              position: 'right', //显示位置
              offset: [5, 0], //偏移设置
              formatter: function (params) {
                //圆环显示文字
                return params.data.name;
              },
              fontSize: 13,
              emphasis: {
                itemStyle: {
                  show: true,
                },
              },
            },
            symbol: 'circle',
            symbolSize: function (val: Array<any>) {
              return 5 + val[2] * 5; //圆环大小
            },
            itemStyle: {
              show: false,
              color: '#f8f9f5',
            },
            data: item[1].map(function (dataItem: any) {
              return {
                name: dataItem[0].name,
                value: chinaGeoCoordMap[dataItem[0].name].concat([dataItem[0].value]),
              };
            }),
          },
          //被攻击点
          {
            type: 'effectScatter',
            coordinateSystem: 'geo',
            zlevel: 2,
            rippleEffect: {
              //涟漪相关
              period: 2,
              brushType: 'stroke',
              scale: 5,
            },
            label: {
              show: true,
              position: 'right',
              // offset:[5, 0],
              color: '#0f0',
              formatter: '{b}',
              textStyle: {
                color: '#fff',
                fontSize: 12,
              },
              emphasis: {
                itemStyle: {
                  show: true,
                  color: '#f60',
                },
              },
            },
            itemStyle: {
              color: '#f00',
            },
            symbol: 'circle',
            symbolSize: 10, //圆圈大小
            data: [
              {
                name: item[0],
                value: chinaGeoCoordMap[item[0]].concat([10]),
              },
            ],
          },
        );
      });
      function drawChina2() {
        var myChart = echarts.init(chinaRef.value);
        echarts.registerMap('china', chinaMap); //注册可用的地图
        var option = {
          tooltip: {
            trigger: 'item',
            backgroundColor: 'rgba(166, 200, 76, 0.82)',
            borderColor: '#FFFFCC',
            showDelay: 0,
            hideDelay: 0,
            enterable: true,
            transitionDuration: 0,
            extraCssText: 'z-index:100',
            formatter: function (params) {
              //根据业务自己拓展要显示的内容
              var res = '';
              var name = params.name;
              var value = params.value[params.seriesIndex + 1];
              res = "<span style='color:#fff;'>" + name + '</span> 数据：' + value;
              return res;
            },
          },
          geo: {
            show: true,
            center: [105.194115019531, 35.582111640625],
            map: 'china',
            roam: true, //是否允许缩放，拖拽
            zoom: 1, //初始化大小
            //缩放大小限制
            scaleLimit: {
              min: 0.1, //最小
              max: 12, //最大
            },
            //设置中心点
            //center: [95.97, 29.71],
            //省份地图添加背景
            //regions: regions,
            itemStyle: {
              areaColor: '#3352c7',
              color: 'red',
              borderColor: '#5e84fd',
              borderWidth: 2,
            },
            label: {
              color: 'rgba(255,255,255,0.5)',
              show: false,
            },
            //高亮状态
            emphasis: {
              itemStyle: {
                areaColor: '#ffc601',
              },
              label: {
                show: true,
                color: '#fff',
              },
            },
            z: 10,
          },
          //配置属性
          series: series,
        };
        myChart.setOption(option);
      }
      function drawChina3() {
        var myChart = echarts.init(chinaRef.value);
        echarts.registerMap('china', chinaMap); //注册可用的地图
        var seriesData = [
          { name: '北京市', value: 15477.48 },
          { name: '上海市', value: 31686.1 },
        ];
        var option = {
          // 标题
          title: {
            text: '中国地图',
            left: 'center',
            top: 20,
            // subtext: "下载链接",
            // sublink: "http://datav.aliyun.com/tools/atlas/#&lat=30.772340792178525&lng=103.94573258937584&zoom=9.5"
          },
          // 悬浮窗
          tooltip: {
            trigger: 'item',
            formatter: function (params: { name: string; value: unknown }) {
              return `${params.name}: ${params.value || '-'}`;
            },
          },
          // echarts大小位置
          grid: {
            left: '10px',
            right: '10px',
            top: '10px',
            bottom: '10px',
          },
          // 图例
          visualMap: {
            min: 800,
            max: 50000,
            text: ['High', 'Low'],
            realtime: false,
            calculable: true,
            inRange: {
              color: ['lightskyblue', 'yellow', 'orangered'],
            },
          },
          // 要显示的散点数据
          series: [
            {
              type: 'map',
              map: 'china',
              // 这是要显示的数据
              data: seriesData,
              // 自定义命名映射，不设置的话，label默认是使用 geoJson中的name名
              // nameMap: {
              //   '北京市': "北京重命名",
              //   "天津市": '天津重命名'
              // },
            },
          ],
        };
        myChart.setOption(option);
      }*/
      function setData(data1) {
        var myChart = echarts.init(chinaRef.value);
        echarts.registerMap('china1', chinaMap); //注册可用的地图
        var option = {
          backgroundColor: '#FFFFFF',
          title: {
            text: '全国设备大数据',
            subtext: '各省数据',
            x: 'center',
          },
          tooltip: {
            trigger: 'item',
          },

          //左侧小导航图标
          visualMap: {
            show: true,
            x: 'left',
            y: 'center',
            splitList: [
              { start: 50, end: 1000 },
              { start: 30, end: 50 },
              { start: 20, end: 30 },
              { start: 10, end: 20 },
              { start: 5, end: 10 },
              { start: 0, end: 5 },
            ],
            color: ['#5475f5', '#9feaa5', '#85daef', '#74e2ca', '#e6ac53', '#9fb5ea'],
            formatter: function (starvalue, endvalue) {
              //标签的格式化工具。
              return starvalue + '-' + endvalue + '台'; // 范围标签显示内容。
            },
          },

          //配置属性
          series: [
            {
              name: '数据',
              type: 'map',
              map: 'china1',
              roam: false,
              zoom: 1.25,
              label: {
                show: false, //省份名称
              },
              data: data1, //数据
            },
          ],
        };
        myChart.setOption(option);
      }

      /**
       * 抛出最终使用的参数+事件
       */
      return {
        chinaRef,
        ...refData,
        innerClick,
      };
    },
  });
</script>
