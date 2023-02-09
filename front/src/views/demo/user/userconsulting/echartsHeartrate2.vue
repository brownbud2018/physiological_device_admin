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
  import { getUserHeartrateList2 } from '/@/api/demo/user';
  import { useRoute } from 'vue-router'; //
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
      const route = useRoute();
      const userId = ref(route.params?.id);

      const { createMessage } = useMessage();

      let dateData = [];
      let heartrateData = [];
      let titleData = '心率：暂无数据';
      let leftData = 'center';
      let topData = 'center';
      let title;
      let subData = '';
      watch(
        () => props.data,
        (newValue, oldValue) => {
          let user_id = props.data.user_id;
          let this_data_id = props.data.heart_data_id;
          if (this_data_id != undefined) {
            const promisedata = new Promise((resolve) => {
              const data1 = getUserHeartrateList2(user_id)
                .then((res) => {
                  let j = 0;
                  for (let i = 0; i < res.data.length; i++) {
                    if (
                      res.data[i].heartrate != undefined &&
                      res.data[i].heartrate != '' &&
                      res.data[i].heartrate != null
                    ) {
                      if (
                        res.data[i].createtime != undefined &&
                        res.data[i].createtime != '' &&
                        res.data[i].createtime != null
                      ) {
                        dateData[j] = res.data[i].createtime;
                        heartrateData[j] = res.data[i].heartrate;
                        j = j + 1;
                      }
                    }
                  }
                  if (heartrateData.length > 0) {
                    titleData = '心率';
                    subData = '心率值正常范围：50~120bpm';
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
                  //createMessage.error('查询用户心率失败');
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
      setData(title);
      function setData(title) {
        /*
          tooltip: {
            show: true,
            enterable: true,
            triggerOn: 'click', // item 图形触发， axis 坐标轴触发， none 不触发
            trigger: 'item',
            // 浮层隐藏的延迟
            hideDelay: 800,
            formatter: function (params) {
              console.log(params);
              //let name = that.getTooltipName(params); //进行显示提示框添加事件
              var html = `<div class='specialLook' οnclick="${console.log('查看画像')}">查看画像</div>
                       <div class='addSearch' οnclick="${console.log('添加搜索')}">添加搜索</div>`;
              return html;
            },
          },
          */
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
              max: 200,
              splitNumber: 4,
              axisLabel: {
                color: '#151515',
                formatter: function (value) {
                  return `${value} bpm`;
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
            data: ['心率值'],
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true,
          },
          series: [
            {
              name: '心率值',
              data: heartrateData,
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
