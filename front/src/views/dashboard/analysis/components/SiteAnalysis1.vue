<template>
  <Card
    :tab-list="tabListTitle"
    v-bind="$attrs"
    :active-tab-key="activeKey"
    @tab-change="onTabChange"
  >
    <p v-if="activeKey === 'tab1'" @nextStep="nextStep" :data1="data1">
      <VisitAnalysisBar @nextStep="nextStep" :data1="data1" :data2="data2" :data3="data3" />
    </p>
    <p v-if="activeKey === 'tab2'" @nextStep="nextStep" :data1="data1">
      <VisitAnalysisBar @nextStep="nextStep" :data1="data1" :data2="data4" :data3="data5" />
    </p>
    <p v-if="activeKey === 'tab3'" @nextStep="nextStep" :data1="data1">
      <VisitAnalysisBar @nextStep="nextStep" :data1="data1" :data2="data6" :data3="data7" />
    </p>
    <p v-if="activeKey === 'tab4'" @nextStep="nextStep" :data1="data1">
      <VisitAnalysisBar @nextStep="nextStep" :data1="data1" :data2="data8" :data3="data9" :data4="data10" />
    </p>
    <p v-if="activeKey === 'tab5'" @nextStep="nextStep" :data1="data1">
      <VisitAnalysisBar @nextStep="nextStep" :data1="data1" :data2="data11" :data3="data12" />
    </p>
    <p v-if="activeKey === 'tab6'" @nextStep="nextStep" :data1="data1">
      <VisitAnalysisBar @nextStep="nextStep" :data1="data1" :data2="data13" :data3="data14" />
    </p>
  </Card>
</template>
<script lang="ts">
  import { defineComponent, reactive, ref, toRefs } from 'vue';
  import { Card } from 'ant-design-vue';
  import VisitAnalysisBar from './VisitAnalysisBar.vue';

  import { GetDeviceDataInfo1 } from '/@/api/sys/user';
  import { useRouter } from 'vue-router';
  interface DataProps {
    data1: any;
  }
  export default defineComponent({
    name: 'SiteAnalysis',
    components: {
      Card,
      VisitAnalysisBar,
    },
    setup(props) {
      const route = useRouter();
      let vistitDeviceData = {};
      let userdeviceInfo = {};
      let dataA1 = []; //日期
      let dataA2 = []; //总检测次数
      let dataA3 = []; //检测超标次数
      let dataA4 = []; //血氧总检测次数
      let dataA5 = []; //血氧检测超标次数
      let dataA6 = []; //血压检测次数
      let dataA7 = []; //血压检测超标次数
      let dataA8 = []; //血糖总检测次数
      let dataA9 = []; //餐前血糖检测超标次数
      let dataA10 = []; //餐后血糖检测超标次数
      let dataA11 = []; //心率总检测次数
      let dataA12 = []; //心率检测超标次数
      let dataA13 = []; //体温总检测次数
      let dataA14 = []; //体温检测超标次数
      const openPages = async () => {
        if (JSON.stringify(route.query) !== '{}') {
          userdeviceInfo = await GetDeviceDataInfo1();
          vistitDeviceData = userdeviceInfo['data']['all_count_data'];
          //X轴检测日期，Y轴检测人数，折线1：检测正常,折线2：检测异常.
          for (const key in vistitDeviceData) {
            type KeyType = keyof typeof vistitDeviceData;
            const initialValue = vistitDeviceData[key as KeyType];
            dataA1.push(initialValue['device_code']);
            dataA2.push(initialValue['ALLCount']);
            dataA3.push(initialValue['ExceedanceCount']);
            dataA4.push(initialValue['OxygenCount0']);
            dataA5.push(initialValue['OxygenExceedanceCount']);
            dataA6.push(initialValue['PressureCount0']);
            dataA7.push(initialValue['PressureExceedanceCount']);
            dataA8.push(initialValue['SugarCount0']);
            dataA9.push(
              initialValue['SugarExceedanceCount'] + initialValue['SugarExceedanceCount1'],
            );
            dataA10.push(initialValue['SugarExceedanceCount1']);
            dataA11.push(initialValue['HeartrateCount0']);
            dataA12.push(initialValue['HeartrateExceedanceCount']);
            dataA13.push(initialValue['TemperatureCount0']);
            dataA14.push(initialValue['TemperatureExceedanceCount']);
          }
        }
      };
      openPages();

      //需要展现到页面的变量
      const data: DataProps = reactive({
        data1: dataA1, //父给子的参数
        data2: dataA2, //父给子的参数
        data3: dataA3, //父给子的参数
        data4: dataA4, //父给子的参数
        data5: dataA5, //父给子的参数
        data6: dataA6, //父给子的参数
        data7: dataA7, //父给子的参数
        data8: dataA8, //父给子的参数
        data9: dataA9, //父给子的参数
        data10: dataA10, //父给子的参数
        data11: dataA11, //父给子的参数
        data12: dataA12, //父给子的参数
        data13: dataA13, //父给子的参数
        data14: dataA14, //父给子的参数
        /**
         * 下一步
         * 点击反馈
         */
        nextStep($event: any) {
          console.log('$event', $event);
          let datasend = [1, 2, 3, 4];
          console.log(datasend);
          data.data1 = datasend;
        },
      });
      const refsData = toRefs(data);

      const activeKey = ref('tab1');
      const tabListTitle = [
        {
          key: 'tab1',
          tab: '【设备】总检测次数',
        },
        {
          key: 'tab2',
          tab: '血氧',
        },
        {
          key: 'tab3',
          tab: '血压',
        },
        {
          key: 'tab4',
          tab: '血糖',
        },
        {
          key: 'tab5',
          tab: '心率',
        },
        {
          key: 'tab6',
          tab: '体温',
        },
      ];

      function onTabChange(key) {
        activeKey.value = key;
      }
      return {
        ...refsData,
        tabListTitle,
        activeKey,
        onTabChange,
        dataA1,
        dataA2,
        dataA3,
      };
    },
  });
</script>
