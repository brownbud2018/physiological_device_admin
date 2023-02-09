<template>
  <div class="md:flex">
    <template v-for="(item, index) in growCardList" :key="item.title">
      <Card
        size="small"
        :loading="loading"
        :title="item.title"
        class="md:w-1/4 w-full !md:mt-0"
        :class="{ '!md:mr-4': index + 1 < 4, '!mt-4': index > 0 }"
      >
        <template #extra>
          <Tag :color="item.color">{{ item.action }}</Tag>
        </template>

        <div class="py-4 px-4 flex justify-between items-center">
          <CountTo prefix="" :startVal="1" :endVal="item.value" class="text-2xl" />
          <img :src="item.img" class="iconimg" />
          <!--<Icon :icon="item.icon" :size="40" />-->
        </div>

        <div class="p-2 px-4 flex justify-between">
          <span>总{{ item.title }}</span>
          <CountTo prefix="" :startVal="1" :endVal="item.total" />
        </div>
      </Card>
    </template>
  </div>
</template>
<script lang="ts" setup>
  import { CountTo } from '/@/components/CountTo/index';
  //import { Icon } from '/@/components/Icon';
  import { Tag, Card } from 'ant-design-vue';
  import { growCardList } from '../data';
  import { GetUserDataInfo } from '/@/api/sys/user';
  import { useRouter } from 'vue-router';

  const route = useRouter();
  let userdataInfo = {};
  let device_count = '';
  let device_active_count = '';
  let dm_user_count = '';
  let bloodoxygen_count = '';
  let bloodoxygen_out_count = '';
  let bloodpressure_count = '';
  let bloodpressure_out_count = '';
  let bloodsugar_count = '';
  let bloodsugarpmbg_out_count = '';
  let bloodsugarpbg_out_count = '';
  let heartrate_count = '';
  let heartrate_out_count = '';
  let temperature_count = '';
  let temperature_out_count = '';
  let count_all = 0;
  let count_out_all = 0;
  const openPages = async () => {
    if (JSON.stringify(route.query) !== '{}') {
      userdataInfo = await GetUserDataInfo();
      device_count = userdataInfo['data']['device_count'];
      device_active_count = userdataInfo['data']['device_active_count'];
      dm_user_count = userdataInfo['data']['dm_user_count'];
      bloodoxygen_count = userdataInfo['data']['bloodoxygen_count'];
      bloodoxygen_out_count = userdataInfo['data']['bloodoxygen_out_count'];
      bloodpressure_count = userdataInfo['data']['bloodpressure_count'];
      bloodpressure_out_count = userdataInfo['data']['bloodpressure_out_count'];
      bloodsugar_count = userdataInfo['data']['bloodsugar_count'];
      bloodsugarpmbg_out_count = userdataInfo['data']['bloodsugarpmbg_out_count'];
      bloodsugarpbg_out_count = userdataInfo['data']['bloodsugarpbg_out_count'];
      heartrate_count = userdataInfo['data']['heartrate_count'];
      heartrate_out_count = userdataInfo['data']['heartrate_out_count'];
      temperature_count = userdataInfo['data']['temperature_count'];
      temperature_out_count = userdataInfo['data']['temperature_out_count'];
      count_all =
        parseInt(bloodoxygen_count) +
        parseInt(bloodpressure_count) +
        parseInt(bloodsugar_count) +
        parseInt(heartrate_count) +
        parseInt(temperature_count);
      count_out_all =
        parseInt(bloodoxygen_out_count) +
        parseInt(bloodpressure_out_count) +
        parseInt(bloodsugarpmbg_out_count) +
        parseInt(bloodsugarpbg_out_count) +
        parseInt(heartrate_out_count) +
        parseInt(temperature_out_count);
      for (const key in growCardList) {
        type KeyType = keyof typeof growCardList;
        const initialValue = growCardList[key as KeyType];
        if (initialValue['title'] == '设备数') {
          initialValue['value'] = device_active_count;
          initialValue['total'] = device_count;
          initialValue['img'] = '/resource/img/device.png';
        }
        if (initialValue['title'] == '用户数') {
          initialValue['value'] = dm_user_count;
          initialValue['total'] = dm_user_count;
          initialValue['img'] = '/resource/img/nohead.jpg';
        }
        if (initialValue['title'] == '检测数') {
          initialValue['value'] = count_all;
          initialValue['total'] = count_all;
          initialValue['img'] = '/resource/img/check.jpg';
        }
        if (initialValue['title'] == '超标数') {
          initialValue['value'] = count_out_all;
          initialValue['total'] = count_out_all;
          initialValue['img'] = '/resource/img/kaiguanred.png';
        }
      }
    }
  };
  openPages();
  defineProps({
    loading: {
      type: Boolean,
    },
  });
</script>
