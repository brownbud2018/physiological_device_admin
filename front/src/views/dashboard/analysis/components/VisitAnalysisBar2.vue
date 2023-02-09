<template>
  <div ref="chartRef" :style="{ height, width }" @click="innerClick"></div>
</template>
<script lang="ts">
  import { defineComponent, PropType, reactive, Ref, ref, toRefs, watch } from 'vue';
  import { useECharts } from '/@/hooks/web/useECharts';
  import { useGo } from '/@/hooks/web/usePage';
  //参数 数据类型配置
  interface DataProps {
    son: any;
    key: number;
  }
  export default defineComponent({
    name: 'VisitAnalysisBar2',
    props: {
      data1: {
        type: Object, //设置数据类型
        required: true, //是否必传
        // eslint-disable-next-line vue/require-valid-default-prop
        default: {},
      },
      data2: {
        type: Object, //设置数据类型
        required: true, //是否必传
        // eslint-disable-next-line vue/require-valid-default-prop
        default: {},
      },
      data3: {
        type: Object, //设置数据类型
        required: true, //是否必传
        // eslint-disable-next-line vue/require-valid-default-prop
        default: {},
      },
      data4: {
        type: Object, //设置数据类型
        required: false, //是否必传
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
      watch(
        () => props.data1,
        (newValue, oldValue) => {
          console.log('newValue', newValue, 'oldValue', oldValue);
          console.log('data1', props.data1);
        },
      );
      setData(props.data1, props.data2, props.data3);

      function setData(data1, data2, data3) {
        //let maxnumber = Math.max.apply(null, data1);
        let maxnumber1 = Math.max.apply(null, data2);
        let maxnumber2 = Math.max.apply(null, data3);
        let maxnum = 0;
        /*if (maxnumber != '-Infinity' && maxnumber != 'NaN') {
          if (maxnumber > maxnum) {
            maxnum = maxnumber;
          }
        }*/
        if (maxnumber1 != '-Infinity' && maxnumber1 != 'NaN') {
          if (maxnumber1 > maxnum) {
            maxnum = maxnumber1;
          }
        }
        if (maxnumber2 != '-Infinity' && maxnumber2 != 'NaN') {
          if (maxnumber2 > maxnum) {
            maxnum = maxnumber2;
          }
        }
        maxnum = maxnum + 0;

        setOptions({
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              lineStyle: {
                width: 1,
                color: '#019680',
              },
            },
          },
          legend: {
            data: ['总检测次数', '超标次数'],
          },
          grid: { left: '1%', right: '1%', top: '10%', bottom: 0, containLabel: true },
          xAxis: {
            type: 'category',
            data: data1,
          },
          yAxis: {
            type: 'value',
            max: maxnum,
            splitNumber: 4,
          },
          series: [
            {
              name: '总检测次数',
              data: data2,
              type: 'bar',
              barMaxWidth: 80,
              itemStyle: {
                color: '#008080',
              },
            },
            {
              name: '超标次数',
              data: data3,
              type: 'bar',
              itemStyle: {
                color: '#FF0000',
              },
              barMaxWidth: 80,
            },
          ],
        });
      }
      const go = useGo();
      function innerClick() {
        go('/user/usermain');
      }
      /**
       * 抛出最终使用的参数+事件
       */
      return {
        chartRef,
        ...refData,
        innerClick,
      };
    },
  });
</script>
