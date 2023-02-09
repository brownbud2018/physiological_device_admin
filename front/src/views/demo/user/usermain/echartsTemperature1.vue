<template>
  <div ref="chartRef" :style="{ height, width }"></div>
</template>
<script lang="ts">
  import { defineComponent, PropType, reactive, Ref, ref, toRefs, watch } from 'vue';
  import { useECharts } from '/@/hooks/web/useECharts';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { getUserTemperatureList2 } from '/@/api/demo/user';
  import { useRoute } from 'vue-router'; //
  //参数 数据类型配置
  interface DataProps {
    son: any;
    key: number;
  }
  export default defineComponent({
    name: 'EchartsTemperature1',
    props: {
      data: {
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
        default: '350px',
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

      const chartRef = ref<HTMLDivElement | null>(null);
      const { setOptions } = useECharts(chartRef as Ref<HTMLDivElement>);
      const route = useRoute();
      const userId = ref(route.params?.id);

      const { createMessage } = useMessage();

      let dateData = [];
      let temperatureData = [];
      let titleData = '体温：暂无数据';
      let subData = '';
      let topData = 'center';
      let leftData = 'center';
      let title;
      watch(
        () => props.data,
        (newValue, oldValue) => {
          ///console.log('newValue', newValue, 'oldValue', oldValue);
          //console.log('echartsBloodSugarBack1', props.data);
          let user_id = props.data.user_id;
          const promisedata = new Promise((resolve) => {
            const data1 = getUserTemperatureList2(user_id)
              .then((res) => {
                let j = 0;
                for (let i = 0; i < res.data.length; i++) {
                  if (
                    res.data[i].temperature != undefined &&
                    res.data[i].temperature != '' &&
                    res.data[i].temperature != null
                  ) {
                    if (
                      res.data[i].createtime != undefined &&
                      res.data[i].createtime != '' &&
                      res.data[i].createtime != null
                    ) {
                      dateData[j] = res.data[i].createtime;
                      temperatureData[j] = res.data[i].temperature;
                      //temperatureData[j] = String(Number(res.data[i].pmbg) / 10);
                      j = j + 1;
                    }
                  }
                  //pbgData[i] = res.data[i].pbg;
                }
                if (temperatureData.length > 0) {
                  titleData = '体温';
                  subData = '正常范围：36.0~37.5度';
                  leftData = 'left';
                  topData = 'top';
                  title = {
                    text: titleData,
                    subtext: subData,
                    left: leftData,
                    top: topData,
                    textStyle: {
                      align: 'center',
                    },
                  };
                } else {
                  title = {
                    text: titleData,
                    left: leftData,
                    top: topData,
                    textStyle: {
                      align: 'center',
                    },
                  };
                }
                setData(title);
              })
              .catch(() => {
                createMessage.error('查询用户体温失败');
                title = {
                  text: titleData,
                  left: leftData,
                  top: topData,
                  textStyle: {
                    align: 'center',
                  },
                };
                setData(title);
              });
            resolve(data1);
          });
        },
      );
      title = {
        text: titleData,
        left: leftData,
        top: topData,
        textStyle: {
          align: 'center',
        },
      };
      setData(title);

      function setData(title) {
        setOptions({
          title,
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              lineStyle: {
                width: 1,
                color: '#019680',
              },
            },
          },
          xAxis: {
            type: 'category',
            max: null,
            boundaryGap: false,
            data: dateData, //[...new Array(18)].map((_item, index) => `${index + 6}:00`),
            splitLine: {
              show: true,
              lineStyle: {
                width: 1,
                type: 'solid',
                color: 'rgba(226,226,226,0.5)',
              },
            },
            axisTick: {
              show: false,
            },
          },
          yAxis: [
            {
              type: 'value',
              max: 45,
              min: 30,
              splitNumber: 4,
              axisLabel: {
                //坐标文字
                color: '#151515',
                formatter: function (value) {
                  return `${value} ℃`;
                },
              },
              axisTick: {
                show: false,
              },
              splitArea: {
                show: true,
                areaStyle: {
                  color: ['rgba(255,255,255,0.2)'],
                },
              },
            },
          ],
          legend: {
            data: ['体温'],
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true,
          },
          series: [
            {
              name: '体温',
              smooth: true,
              data: temperatureData,
              type: 'line',
              areaStyle: {},
              itemStyle: {
                color: '#5ab1ef',
              },
            },
          ],
        });
      }
      /**
       * 抛出最终使用的参数+事件
       */
      return {
        chartRef,
        ...refData,
      };
    },
  });
</script>
