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
  let pmbgData = [];
  //let pbgData = [];
  let titleData = '餐前血糖：暂无数据';
  let subData = '';
  let title;
  let topData = 'center';
  let leftData = 'center';
  const promisedata = new Promise((resolve) => {
    const data = getUserBloodsugarList2(userId.value)
      .then((res) => {
        curData.value = res.data;
        let j = 0;
        for (let i = 0; i < res.data.length; i++) {
          if (res.data[i].pmbg != undefined && res.data[i].pmbg != '' && res.data[i].pmbg != null) {
            if (
              res.data[i].createtime != undefined &&
              res.data[i].createtime != '' &&
              res.data[i].createtime != null
            ) {
              dateData[j] = res.data[i].createtime;
              pmbgData[j] = res.data[i].pmbg;
              //pmbgData[j] = String(Number(res.data[i].pmbg) / 10);
              j = j + 1;
            }
          }
          //pbgData[i] = res.data[i].pbg;
        }
        if (pmbgData.length > 0) {
          titleData = '餐前血糖';
          subData = '正常范围：3.9~6.1mmol/L';
          topData = 'top';
          leftData = 'left';
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
        createMessage.error('查询用户餐前血糖失败');
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
              color: ['rgba(255,255,255,0.2)'],
            },
          },
        },
      ],
      legend: {
        data: ['餐前血糖'],
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true,
      },
      series: [
        {
          name: '餐前血糖',
          smooth: true,
          data: pmbgData,
          type: 'line',
          areaStyle: {},
          itemStyle: {
            color: '#5ab1ef',
          },
        },
      ],
    });
  }
</script>
