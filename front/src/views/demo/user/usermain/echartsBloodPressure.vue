<template>
  <div ref="chartRef" :style="{ height, width }"></div>
</template>
<script lang="ts">
  import { basicProps } from './props';
</script>
<script lang="ts" setup>
  import { onMounted, ref, Ref } from 'vue';
  import { useECharts } from '/@/hooks/web/useECharts';
  import { getUserBloodpressureList2 } from '/@/api/demo/user';
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
  let dbpData = [];
  let sbpData = [];
  let titleData = '血压：暂无数据';
  let leftData = 'center';
  let topData = 'center';
  let title;
  let subData = '';
  const promisedata = new Promise((resolve) => {
    const data = getUserBloodpressureList2(userId.value)
      .then((res) => {
        curData.value = res.data;
        let j = 0;
        for (let i = 0; i < res.data.length; i++) {
          if (res.data[i].dbp != undefined && res.data[i].dbp != '' && res.data[i].dbp != null) {
            if (
              res.data[i].createtime != undefined &&
              res.data[i].createtime != '' &&
              res.data[i].createtime != null
            ) {
              dateData[j] = res.data[i].createtime;
              dbpData[j] = res.data[i].dbp;
              sbpData[i] = res.data[i].sbp;
              j = j + 1;
            }
          }
        }
        /*if (dbpData.length > 0) {
          titleData = '血压';
          subData = '舒张压正常范围：60~90mmHg，收缩压正常范围：90~140mmHg';
          leftData = 'left';
          topData = 'top';
          setData();
        }*/
        if (dbpData.length > 0) {
          titleData = '血压';
          subData = '收缩压正常范围：90~140mmHg，舒张压正常范围：60~90mmHg';
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
        createMessage.error('查询用户血压失败');
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
          max: 200,
          splitNumber: 4,
          axisLabel: {
            color: '#151515',
            formatter: function (value) {
              return `${value} mmHg`;
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
        data: ['收缩压', '舒张压'],
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true,
      },
      series: [
        {
          name: '收缩压',
          data: sbpData,
          type: 'line',
          markLine: {
            data: [
              {
                // yAxis:(yearCountValue/yearCountValue)*100
                yAxis: 90,
              },
            ],
          },
        },
        {
          name: '舒张压',
          data: dbpData,
          type: 'line',
        },
      ],
    });
  }
  /*
          markLine: {
            silent: true,
            lineStyle: {
              color: '#333',
            },
            data: [
              {
                yAxis: 60,
              },
              {
                yAxis: 90,
              },
              {
                yAxis: 91,
              },
              {
                yAxis: 140,
              },
            ],
          },
  */
</script>
