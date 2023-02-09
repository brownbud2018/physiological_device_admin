//子组件
<!--<template>
  <div>
    <p>父级传递来的值=>{{ data }}</p>
    <p>{{ son }}</p>
    <p><button @click="nextDown">子按钮</button></p>
  </div>
</template>-->
<template>
  <div ref="chartRef" :style="{ height, width }"></div>
</template>
<script lang="ts">
  import { defineComponent, PropType, reactive, Ref, ref, toRefs, watch } from 'vue';
  import { useECharts } from '/@/hooks/web/useECharts';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { getUserHeartrateList3 } from '/@/api/demo/user'; //
  //参数 数据类型配置
  interface DataProps {
    son: any;
    key: number;
  }
  export default defineComponent({
    name: 'EchartsHeartrate3',
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

      const { createMessage } = useMessage();

      let title;
      let titleData = '心电图：暂无数据';
      let leftData = 'center';
      let topData = 'center';
      let subData = '';
      let endDate = '';
      let endData = '';
      watch(
        () => props.data,
        (newValue, oldValue) => {
          //console.log('echartsHeartrate3', props.data);
          let user_id = props.data.user_id;
          let this_data_id = props.data.heart_data_id;
          if (this_data_id != undefined) {
            const promisedata = new Promise((resolve) => {
              const data1 = getUserHeartrateList3(this_data_id)
                .then((res) => {
                  if (res.data.id > 0) {
                    endData = res.data.heartrateurl;
                    endDate = res.data.createtime;
                    titleData = '心电图';
                    subData =
                      res.data.dmusername +
                      '的心率值：' +
                      res.data.heartrate +
                      '，测量时间：' +
                      res.data.createtime;
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
                  setHData(title, endData, endDate);
                })
                .catch(() => {
                  //createMessage.error('查询用户心率失败');
                  title = {
                    text: titleData,
                    left: leftData,
                    top: topData,
                    textStyle: {
                      align: 'center',
                    },
                  };
                  setHData(title, '', '');
                });
              resolve(data1);
            });
          }
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
      setHData(title, '', '');
      function setHData(title, ydata, xdate) {
        let str1 = ydata.replace('[', '').replace(']', '');
        let data0 = str1.split(',');
        let datax = [];
        let miny = 0;
        let maxy = 0;
        for (var j = 0; j < data0.length; j++) {
          datax.push(j);
          if (parseInt(data0[j]) > maxy) {
            maxy = parseInt(data0[j]);
          }
          if (parseInt(data0[j]) < miny) {
            miny = parseInt(data0[j]);
          }
        }
        maxy = maxy + 100;
        miny = miny - 100;
        setOptions({
          title,
          animationDuration: 3000,
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
            data: datax,
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
              min: miny,
              max: maxy,
              splitNumber: 4,
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
            data: ['心电图'],
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true,
          },
          series: [
            {
              name: '心电图',
              data: data0,
              type: 'line',
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
