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
  import { getUserPhysiqueList2 } from '/@/api/demo/user'; //
  //参数 数据类型配置
  interface DataProps {
    son: any;
    key: number;
  }
  export default defineComponent({
    name: 'EchartsPhysique',
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
      let titleData = '体质辨识图：暂无数据';
      let leftData = 'center';
      let topData = 'center';
      let subData = '';
      let endDate = '';
      let endData = '';
      watch(
        () => props.data,
        (newValue, oldValue) => {
          //console.log('echartsPhysique3', props.data);
          let user_id = props.data.user_id;
          let this_data_id = props.data.phy_data_id;
          if (this_data_id != undefined) {
            const promisedata = new Promise((resolve) => {
              const data1 = getUserPhysiqueList2(this_data_id)
                .then((res) => {
                  if (res.data.id > 0) {
                    endData = res.data.physique;
                    endDate = res.data.createtime;
                    titleData = '体质辨识雷达图'; //res.data.dmusername +
                    subData =
                      res.data.hint.replace('。', '\n') + '\n时间：' + res.data.createtime;
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
        const color = ['#22ff00', '#f9d559', '#aafc87', '#cdc8f7', '#e3fddb'];
        //const data = '[' + ydata + ']';
        let str1 = ydata.replace('[', '').replace(']', '');
        let data0 = str1.split(',');
        //0.平和质，1.气虚质，2.阳虚质，3.阴虚质，4.痰湿质，5.湿热质，6.血瘀质，7.气郁质，8.特禀质
        setOptions({
          title,
          radar: {
            //中心（圆心）坐标，数组的第一项是横坐标，第二项是纵坐标。
            center: ['50%', '55%'],
            axisLine: {//轴线颜色以及字体颜色
              show: true,
              lineStyle: {
                color: "#000000",
                type: "solid",
              },
            },
            splitLine: {
              lineStyle: {
                // 使用黑色的间隔色
                color: ['#000'],
              },
            },
            indicator: [//轴设置
              {
                name: '平和质',
                max: 100,
                axisLabel: {
                  show: true,
                  fontsize: 12,
                  lineStyle: {
                    color: "#000000",
                    type: "solid",
                  },
                },
              },
              { name: '气虚质', max: 100 },
              { name: '阳虚质', max: 100 },
              { name: '阴虚质', max: 100 },
              { name: '痰湿质', max: 100 },
              { name: '湿热质', max: 100 },
              { name: '血瘀质', max: 100 },
              { name: '气郁质', max: 100 },
              { name: '特禀质', max: 100 },
            ],
            splitArea: {
              areaStyle: {
                color: color,
                shadowColor: 'rgba(0, 0, 0, 0.2)',
                shadowBlur: 20
              }
            },
          },
          series: [
            {
              name: '数值',
              type: 'radar',
              data: [
                {
                  value: data0,
                  name: 'Allocated Budget',
                },
              ],
              areaStyle: {
                color: '#0000ff',
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
