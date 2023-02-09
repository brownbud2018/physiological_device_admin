<template>
  <div ref="chartRef" :style="{ height, width }"></div>
</template>
<script lang="ts">
  import { basicProps } from './props';
</script>
<script lang="ts" setup>
  import { ref, Ref } from 'vue';
  import { useECharts } from '/@/hooks/web/useECharts';
  import { getUserHeartrateList2 } from '/@/api/demo/user';
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
  let heartrateData = [];
  let titleData = '心率：暂无数据';
  let leftData = 'center';
  let topData = 'center';
  let title;
  let subData = '';
  const promisedata = new Promise((resolve) => {
    const data = getUserHeartrateList2(userId.value)
      .then((res) => {
        curData.value = res.data;
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
        return res.data;
      })
      .catch(() => {
        createMessage.error('查询用户心率失败');
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

  /*chartRef.value.on('click', function (params) {
    // 控制台打印数据的名称
    console.log(params.name);
  });*/

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
</script>
