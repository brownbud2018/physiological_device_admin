<template>
  <Card
    :tab-list="tabListTitle"
    v-bind="$attrs"
    :active-tab-key="activeKey"
    @tab-change="onTabChange"
  >
    <p v-if="activeKey === 'tab1'" @nextStep="nextStep" :data1="data1">
      <VisitAnalysis @nextStep="nextStep" :data1="data1" />
    </p>
  </Card>
</template>
<script lang="ts">
  import { defineComponent, reactive, ref, toRefs } from 'vue';
  import { Card } from 'ant-design-vue';
  import VisitAnalysis from './EchartsChinaMap.vue';

  import { GetDeviceDataCnInfo, GetDeviceDataInfo } from "/@/api/sys/user";
  import { useRouter } from 'vue-router';
  interface DataProps {
    data1: any;
  }
  export default defineComponent({
    name: 'ChinaMap',
    components: {
      Card,
      VisitAnalysis,
    },
    setup(props) {
      const route = useRouter();
      let DeviceData = {};
      let getDeviceInfo = {};
      let pdata = [];
      const openPages = async () => {
        if (JSON.stringify(route.query) !== '{}') {
          getDeviceInfo = await GetDeviceDataCnInfo();
          DeviceData = getDeviceInfo['data']['all_count_data'];
          //X轴检测日期，Y轴检测人数，折线1：检测正常,折线2：检测异常.
          for (const key in DeviceData) {
            type KeyType = keyof typeof DeviceData;
            const initialValue = DeviceData[key as KeyType];
            pdata.push({ name: initialValue['province'], value: initialValue['countid'] });
          }
        }
      };
      openPages();

      //需要展现到页面的变量
      const data: DataProps = reactive({
        data1: pdata, //父给子的参数
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
          tab: '全国设备分布图',
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
      };
    },
  });
</script>
