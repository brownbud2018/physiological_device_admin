<template>
  <div ref="chartRef" :style="{ height, width }"></div>
</template>
<script lang="ts">
  import { basicProps } from './props';
</script>
<script lang="ts" setup>
  import { onMounted, ref, Ref } from 'vue';
  import { useECharts } from '/@/hooks/web/useECharts';
  import { getUserBloodsugarList2 } from '/@/api/demo/user';
  import { useRoute } from 'vue-router';
  import { useMessage } from '../../../../hooks/web/useMessage';

  defineProps({
    ...basicProps,
  });
  const chartRef = ref<HTMLDivElement | null>(null);
  const { setOptions } = useECharts(chartRef as Ref<HTMLDivElement>);
  const route = useRoute();
  const userId = ref(route.params?.id);

  const { createMessage } = useMessage();
  const curData = ref(0);
  let dateData = [];
  //let pmbgData = [];
  let pbgData = [];
  let titleData = '餐后血糖：暂无数据';
  let subData = '';
  let topData = 'center';
  let leftData = 'center';
  let title;
  const promisedata = new Promise((resolve) => {
    const data = getUserBloodsugarList2(userId.value)
      .then((res) => {
        curData.value = res.data;
        let j = 0;
        for (let i = 0; i < res.data.length; i++) {
          if (res.data[i].pbg != undefined && res.data[i].pbg != '' && res.data[i].pbg != null) {
            if (
              res.data[i].createtime != undefined &&
              res.data[i].createtime != '' &&
              res.data[i].createtime != null
            ) {
              dateData[j] = res.data[i].createtime;
              //pmbgData[j] = res.data[i].pmbg;
              pbgData[j] = res.data[i].pbg;
              //pbgData[j] = String(Number(res.data[i].pbg) / 10);
              j = j + 1;
            }
          }
        }
        if (pbgData.length > 0) {
          titleData = '餐后血糖';
          subData = '正常范围：小于7.8mmol/.L';
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
        return res.data;
      })
      .catch(() => {
        createMessage.error('查询用户餐后血糖失败');
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
    resolve(data);
  });

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
          max: 40,
          splitNumber: 4,
          axisLabel: {
            //坐标文字
            color: '#151515',
            formatter: function (value) {
              return `${value} mmol/L`;
            },
          },
          axisTick: {
            show: false,
          },
          splitArea: {
            show: true,
            areaStyle: {
              color: ['rgba(226,226,226,0.2)'],
            },
          },
        },
      ],
      legend: {
        data: ['餐后血糖'],
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true,
      },
      series: [
        {
          name: '餐后血糖',
          smooth: true,
          data: pbgData,
          type: 'line',
          areaStyle: {},
          itemStyle: {
            color: '#019680',
          },
        },
      ],
    });
  }
</script>
