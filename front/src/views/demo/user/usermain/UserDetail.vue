<template>
  <PageWrapper
    :title="`用户` + curData.name + `的资料`"
    content="这是用户详情页面。包括用户资料，用户相关测量数据。"
    contentBackground
    @back="goBack"
  >
    <!--<template #extra>
      <a-button type="primary" @click="outExcel()"> 导出Excel </a-button>
    </template>-->
    <Description
      size="middle"
      title="用户信息"
      :bordered="false"
      :column="3"
      :data="personDataOut"
      :schema="personSchema"
    />
    <template #footer>
      <a-tabs default-active-key="detail" v-model:activeKey="currentKey">
        <a-tab-pane key="detail" tab="用户资料" />
        <a-tab-pane key="sugar" tab="用户血糖" @nextStep="nextStep" :data="data1" />
        <a-tab-pane key="pressure" tab="用户血压" @nextStep="nextStep" :data="data1" />
        <a-tab-pane key="heartrate" tab="用户心率" @nextStep="nextStep" :data="data1" />
        <a-tab-pane key="oxygen" tab="用户血氧" @nextStep="nextStep" :data="data1" />
        <a-tab-pane key="temperature" tab="用户体温" @nextStep="nextStep" :data="data1" />
        <a-tab-pane key="medicalrecord" tab="用户病历" @nextStep="nextStep" :data="data1" />
        <a-tab-pane key="question" tab="用户问卷" @nextStep="nextStep" :data="data1" />
        <a-tab-pane key="physique" tab="体质辨识" @nextStep="nextStep" :data="data1" />
      </a-tabs>
    </template>
    <div class="pt-4 m-4 desc-wrap">
      <template v-if="currentKey == 'detail'">
        <div>
          用户头像：<img alt="example" :src="getimg(curData.headicon)" height="100" width="100" />
        </div>
        <Description
          size="middle"
          title="用户详情"
          :bordered="false"
          :column="3"
          :data="userDetailDataOut"
          :schema="userDetailSchema"
        />
      </template>
      <template v-if="currentKey == 'sugar'">
        <echartsBloodSugarBefor1 @nextStep="nextStep" :data="data1" />
        <echartsBloodSugarBack1 @nextStep="nextStep" :data="data1" />
        <BasicTable @register="registerTable" />
      </template>
      <template v-if="currentKey == 'pressure'">
        <echartsBloodPressure1 @nextStep="nextStep" :data="data1" />
        <BasicTable @register="registerTable1" />
      </template>
      <template v-if="currentKey == 'heartrate'">
        <echartsHeartrate2 @nextStep="nextStep" :data="data1" />
        <echartsHeartrate3 @nextStep="nextStep" :data="data1" />
        <BasicTable @register="registerTable2">
          <template #action="{ record }">
            <TableAction
              :actions="[
                {
                  icon: 'clarity:info-standard-line',
                  tooltip: '查看波形图',
                  onClick: handleView.bind(null, record), //openModalLoading.bind(null, record),
                },
              ]"
            />
          </template>
        </BasicTable>
      </template>
      <template v-if="currentKey == 'oxygen'">
        <echartsBloodoxygen2 @nextStep="nextStep" :data="data1" />
        <echartsBloodoxygen3 @nextStep="nextStep" :data="data1" />
        <BasicTable @register="registerTable3">
          <template #action="{ record }">
            <TableAction
              :actions="[
                {
                  icon: 'clarity:info-standard-line',
                  tooltip: '查看波形图',
                  onClick: handleView1.bind(null, record), //openModalLoading.bind(null, record),
                },
              ]"
            />
          </template>
        </BasicTable>
      </template>
      <template v-if="currentKey == 'temperature'">
        <echartsTemperature1 @nextStep="nextStep" :data="data1" />
        <BasicTable @register="registerTable4" />
      </template>
      <template v-if="currentKey == 'medicalrecord'">
        <MedicalRecord1 @nextStep="nextStep" :data="data1" />
        <BasicTable @register="registerTable5">
          <template #action="{ record }">
            <TableAction
              :actions="[
                {
                  icon: 'clarity:info-standard-line',
                  tooltip: '查看波形图',
                  onClick: handleView2.bind(null, record), //openModalLoading.bind(null, record),
                },
              ]"
            />
          </template>
        </BasicTable>
      </template>
      <template v-if="currentKey == 'question'">
        <BasicTable @register="registerTable6">
          <template #action="{ record }">
            <TableAction
              :actions="[
                {
                  icon: 'clarity:info-standard-line',
                  tooltip: '查看问卷',
                  onClick: handleView3.bind(null, record), //openModalLoading.bind(null, record),
                },
              ]"
            />
          </template>
        </BasicTable>
      </template>
      <template v-if="currentKey == 'physique'">
        <echartsPhysique @nextStep="nextStep" :data="data1" />
        <BasicTable @register="registerTable7">
          <template #action="{ record }">
            <TableAction
              :actions="[
                {
                  icon: 'clarity:info-standard-line',
                  tooltip: '查看雷达图',
                  onClick: handleView4.bind(null, record), //openModalLoading.bind(null, record),
                },
              ]"
            />
          </template>
        </BasicTable>
      </template>
    </div>
  </PageWrapper>
</template>

<script lang="ts">
  import { defineComponent, reactive, ref, toRefs } from 'vue';
  import { Description } from '/@/components/Description/index';
  import { useRoute } from 'vue-router';
  import { PageWrapper } from '/@/components/Page';
  import { useGo } from '/@/hooks/web/usePage';
  import { useTabs } from '/@/hooks/web/useTabs';
  import { Tabs } from 'ant-design-vue';
  import {
    getUserBloodpressureList1,
    getUserBloodsugarList1,
    getUserDetail,
    getUserHeartrateList1,
    getUserBloodoxygenList1,
    getUserTemperatureList1,
    getUserMedicalRecordList1,
    getQuestionList1,
    getUserPhysiqueList1,
  } from '/@/api/demo/user';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { BasicTable, TableAction, useTable } from '/@/components/Table';
  import {
    columns,
    columnsbloodoxygen,
    columnsheartrate,
    columnspressure,
    columnstemperature,
    columnsmedicalrecord,
    personSchema,
    personData,
    userDetailSchema,
    userDetailData,
    columnsquestion,
    columnsphysique,
  } from './userdetail.data';
  import echartsBloodSugarBefor1 from './echartsBloodSugarBefor1.vue';
  import echartsBloodSugarBack1 from './echartsBloodSugarBack1.vue';
  import echartsBloodPressure1 from './echartsBloodPressure1.vue';
  import echartsHeartrate2 from './echartsHeartrate2.vue';
  import echartsHeartrate3 from './echartsHeartrate3.vue';
  import echartsBloodoxygen2 from './echartsBloodoxygen2.vue';
  import echartsBloodoxygen3 from './echartsBloodoxygen3.vue';
  import echartsTemperature1 from './echartsTemperature1.vue';
  import MedicalRecord1 from './medicalrecord1.vue';
  import echartsPhysique from './echartsPhysique.vue';
  interface DataProps {
    data1: any;
  }
  export default defineComponent({
    name: 'UserDetail',
    components: {
      Description,
      PageWrapper,
      ATabs: Tabs,
      ATabPane: Tabs.TabPane,
      TableAction,
      BasicTable,
      echartsBloodSugarBefor1,
      echartsBloodSugarBack1,
      echartsBloodPressure1,
      echartsHeartrate2,
      echartsHeartrate3,
      echartsBloodoxygen2,
      echartsBloodoxygen3,
      echartsTemperature1,
      MedicalRecord1,
      echartsPhysique,
    },
    setup() {
      const searchInfo = reactive<Recordable>({});
      //let user_id = 0;
      const [registerTable] = useTable({
        title: '血糖列表',
        api: getUserBloodsugarList1,
        rowKey: 'id',
        columns,
        useSearchForm: false,
        showTableSetting: false,
        bordered: true,
        canResize: false,
        beforeFetch(info) {
          info.dmuserid = userId.value;
          return info;
        },
        afterFetch(info) {
          let data_id = '0';
          let user_id = '0';
          let timestamp = String(Date.parse(new Date().toString()));
          let datasend = {};
          if (info.length > 0) {
            user_id = String(info[info.length - 1].dmuserid);
            data_id = String(info[info.length - 1].id);
            datasend['this_data_id'] = data_id;
            datasend['user_id'] = user_id;
            datasend['time'] = timestamp;
            data.data1 = datasend;
          }
          return info;
        },
      });
      const [registerTable1] = useTable({
        title: '血压列表',
        api: getUserBloodpressureList1,
        rowKey: 'id',
        columns: columnspressure,
        useSearchForm: false,
        showTableSetting: false,
        bordered: true,
        canResize: false,
        beforeFetch(info) {
          info.dmuserid = userId.value;
          return info;
        },
        afterFetch(info) {
          let data_id = '0';
          let user_id = '0';
          let timestamp = String(Date.parse(new Date().toString()));
          let datasend = {};
          if (info.length > 0) {
            user_id = String(info[info.length - 1].dmuserid);
            data_id = String(info[info.length - 1].id);
            datasend['this_data_id'] = data_id;
            datasend['user_id'] = user_id;
            datasend['time'] = timestamp;
            data.data1 = datasend;
          }
          return info;
        },
      });
      const [registerTable2] = useTable({
        title: '心率列表',
        api: getUserHeartrateList1,
        rowKey: 'id',
        columns: columnsheartrate,
        useSearchForm: false,
        showTableSetting: false,
        bordered: true,
        canResize: false,
        beforeFetch(info) {
          info.dmuserid = userId.value;
          return info;
        },
        afterFetch(info) {
          let data_id = '0';
          let user_id = '0';
          let timestamp = String(Date.parse(new Date().toString()));
          let datasend = {};
          if (info.length > 0) {
            user_id = String(info[0].dmuserid);
            data_id = String(info[0].id);
            datasend['this_data_id'] = data_id;
            datasend['user_id'] = user_id;
            datasend['time'] = timestamp;
            data.data1 = datasend;
          }
          return info;
        },
        actionColumn: {
          width: 120,
          title: '操作',
          dataIndex: 'action',
          slots: { customRender: 'action' },
        },
      });
      const [registerTable3] = useTable({
        title: '血氧列表',
        api: getUserBloodoxygenList1,
        rowKey: 'id',
        columns: columnsbloodoxygen,
        useSearchForm: false,
        showTableSetting: false,
        bordered: true,
        canResize: false,
        beforeFetch(info) {
          info.dmuserid = userId.value;
          return info;
        },
        afterFetch(info) {
          let data_id = '0';
          let user_id = '0';
          let timestamp = String(Date.parse(new Date().toString()));
          let datasend = {};
          if (info.length > 0) {
            user_id = String(info[0].dmuserid);
            data_id = String(info[0].id);
            datasend['this_data_id'] = data_id;
            datasend['user_id'] = user_id;
            datasend['time'] = timestamp;
            data.data1 = datasend;
          }
          return info;
        },
        actionColumn: {
          width: 120,
          title: '操作',
          dataIndex: 'action',
          slots: { customRender: 'action' },
        },
      });
      const [registerTable4] = useTable({
        title: '体温列表',
        api: getUserTemperatureList1,
        rowKey: 'id',
        columns: columnstemperature,
        useSearchForm: false,
        showTableSetting: false,
        bordered: true,
        canResize: false,
        beforeFetch(info) {
          info.dmuserid = userId.value;
          return info;
        },
        afterFetch(info) {
          let data_id = '0';
          let user_id = '0';
          let timestamp = String(Date.parse(new Date().toString()));
          let datasend = {};
          if (info.length > 0) {
            user_id = String(info[info.length - 1].dmuserid);
            data_id = String(info[info.length - 1].id);
            datasend['this_data_id'] = data_id;
            datasend['user_id'] = user_id;
            datasend['time'] = timestamp;
            data.data1 = datasend;
          }
          return info;
        },
      });
      const [registerTable5] = useTable({
        title: '病历列表',
        api: getUserMedicalRecordList1,
        rowKey: 'id',
        columns: columnsmedicalrecord,
        useSearchForm: false,
        showTableSetting: false,
        bordered: true,
        canResize: false,
        beforeFetch(info) {
          info.dmuserid = userId.value;
          return info;
        },
        afterFetch(info) {
          let data_id = '0';
          let user_id = '0';
          let timestamp = String(Date.parse(new Date().toString()));
          let datasend = {};
          if (info.length > 0) {
            user_id = String(info[0].dmuserid);
            data_id = String(info[0].id);
            datasend['med_data_id'] = data_id;
            datasend['user_id'] = user_id;
            datasend['time'] = timestamp;
            data.data1 = datasend;
          }
          return info;
        },
        actionColumn: {
          width: 120,
          title: '操作',
          dataIndex: 'action',
          slots: { customRender: 'action' },
        },
      });
      const [registerTable6] = useTable({
        title: '问卷列表',
        api: getQuestionList1,
        rowKey: 'id',
        columns: columnsquestion,
        useSearchForm: false,
        showTableSetting: false,
        bordered: true,
        canResize: false,
        beforeFetch(info) {
          info.userid = userId.value;
          return info;
        },
        afterFetch(info) {
          let data_id = '0';
          //let user_id = '0';
          let timestamp = String(Date.parse(new Date().toString()));
          let datasend = {};
          if (info.length > 0) {
            //user_id = String(info[info.length - 1].dmuserid);
            data_id = String(info[0].id);
            datasend['question_data_id'] = data_id;
            datasend['user_id'] = userId.value;
            datasend['time'] = timestamp;
            data.data1 = datasend;
          }
          return info;
        },
        actionColumn: {
          width: 120,
          title: '操作',
          dataIndex: 'action',
          slots: { customRender: 'action' },
        },
      });
      const [registerTable7] = useTable({
        title: '体质辨识',
        api: getUserPhysiqueList1,
        rowKey: 'id',
        columns: columnsphysique,
        useSearchForm: false,
        showTableSetting: false,
        bordered: true,
        canResize: false,
        beforeFetch(info) {
          info.dmuserid = userId.value;
          return info;
        },
        afterFetch(info) {
          let data_id = '0';
          //let user_id = '0';
          let timestamp = String(Date.parse(new Date().toString()));
          let datasend = {};
          if (info.length > 0) {
            //user_id = String(info[0].dmuserid);
            data_id = String(info[0].id);
            datasend['phy_data_id'] = data_id;
            datasend['user_id'] = userId.value;
            datasend['time'] = timestamp;
            data.data1 = datasend;
          }
          return info;
        },
        actionColumn: {
          width: 120,
          title: '操作',
          dataIndex: 'action',
          slots: { customRender: 'action' },
        },
      });

      const route = useRoute();
      const go = useGo();
      // 此处可以得到用户ID
      const userId = ref(route.params?.id);
      const currentKey = ref('detail');
      const { setTitle } = useTabs();
      const { createMessage } = useMessage();
      const curData = ref(0);
      //const curId = ref(1);
      function handleView(record: Recordable) {
        let data_id = '0';
        let user_id = '0';
        let timestamp = String(Date.parse(new Date().toString()));
        let datasend = {};

        user_id = String(record.dmuserid);
        data_id = String(record.id);
        datasend['this_data_id'] = data_id;
        datasend['user_id'] = user_id;
        datasend['time'] = timestamp;
        data.data1 = datasend;
        //传递给心电图子页面的id信息
        //data.data1 = String(record.id);
      }
      function handleView1(record: Recordable) {
        let data_id = '0';
        let user_id = '0';
        let timestamp = String(Date.parse(new Date().toString()));
        let datasend = {};

        user_id = String(record.dmuserid);
        data_id = String(record.id);
        datasend['this_data_id'] = data_id;
        datasend['user_id'] = user_id;
        datasend['time'] = timestamp;
        data.data1 = datasend;
        //传递给血氧图子页面的id信息
        //data.data1 = String(record.id);
      }
      function handleView2(record: Recordable) {
        let data_id = '0';
        let user_id = '0';
        let timestamp = String(Date.parse(new Date().toString()));
        let datasend = {};

        user_id = String(record.dmuserid);
        data_id = String(record.id);
        datasend['med_data_id'] = data_id;
        datasend['user_id'] = user_id;
        datasend['time'] = timestamp;
        data.data1 = datasend;
        //传递给病历图子页面的id信息
        //data.data1 = String(record.id);
      }
      function handleView3(record: Recordable) {
        //弹出健康问卷页面
        window.open(
          'http://175.178.200.243:9600/device/reQuestion/' +
            String(record.id) +
            '/1/' +
            String(record.userid),
          '_blank',
        );
      }
      function handleView4(record: Recordable) {
        let data_id = '0';
        let user_id = '0';
        let timestamp = String(Date.parse(new Date().toString()));
        let datasend = {};

        user_id = String(record.dmuserid);
        data_id = String(record.id);
        datasend['phy_data_id'] = data_id;
        datasend['user_id'] = user_id;
        datasend['time'] = timestamp;
        data.data1 = datasend;
      }
      //需要展现到页面的变量
      const data: DataProps = reactive({
        data1: {}, //父给子的参数
        /**
         * 下一步
         * 点击反馈
         */
        nextStep($event: any) {
          //data.data1 = $event;
          let data_id = '0';
          let user_id = '0';
          let timestamp = String(Date.parse(new Date().toString()));
          let datasend = {};

          user_id = String(0);
          data_id = String(0);
          datasend['this_data_id'] = data_id;
          datasend['user_id'] = user_id;
          datasend['time'] = timestamp;
          data.data1 = datasend;
        },
      });

      const refData = toRefs(data);

      let personDataOut = ref(personData);
      let userDetailDataOut = ref(userDetailData);
      let userPromise = new Promise((resolve) => {
        const data1 = getUserDetail(userId.value)
          .then((res) => {
            curData.value = res.data[0];
            setTitle('用户详情：' + curData.value.name);
            let personDatauser1: userDetailData = {
              b1: curData.value.id,
              b2: curData.value.name,
              b3: curData.value.phone,
              b4: curData.value.age + '岁',
              b5: curData.value.sex == 0 ? '男' : '女',
              b6: curData.value.height + 'cm',
              b7: curData.value.weight + 'Kg',
              b8: curData.value.deviceid,
              b9: curData.value.devicename,
              b10: curData.value.idcard,
              b11: curData.value.cityid,
              b12: curData.value.cityname,
              b13: curData.value.bloodtypename,
              b14: curData.value.allergyname,
              b15: curData.value.medicalname,
              b16: curData.value.geneticname,
              b17: curData.value.descr,
              b18: curData.value.createtime,
            };
            userDetailDataOut.value = personDatauser1;
            let personDatauser2: personData;
            personDatauser2 = {
              b1: curData.value.name,
              b2: curData.value.phone,
              b3: curData.value.age + '岁',
              b4: curData.value.sex == 0 ? '男' : '女',
              b5: curData.value.height + 'cm',
              b6: curData.value.weight + 'Kg',
            };
            personDataOut.value = personDatauser2;
            return curData.value;
          })
          .catch(() => {
            createMessage.error('查询用户详情失败');
          });
        resolve(data1);
      });
      // TODO
      // 导出Excel
      function outExcel() {
        go('/user/usermain');
      }

      // 页面左侧点击返回链接时的操作
      function goBack() {
        // 本例的效果时点击返回始终跳转到账号列表页，实际应用时可返回上一页
        go('/user/usermain');
      }

      function getimg(url: string) {
        if (url !== '' && url != undefined && url != null) {
          return 'https://pic.luckystar.com.cn/' + url + '.jpg';
        } else {
          return '/resource/img/nohead.jpg';
        }
      }

      return {
        ...refData,
        registerTable,
        registerTable1,
        registerTable2,
        registerTable3,
        registerTable4,
        registerTable5,
        registerTable6,
        registerTable7,
        userId,
        currentKey,
        curData,
        handleView,
        handleView1,
        handleView2,
        handleView3,
        handleView4,
        goBack,
        getimg,
        outExcel,
        searchInfo,
        personSchema,
        personData,
        personDataOut,
        userDetailSchema,
        userDetailData,
        userDetailDataOut,
      };
    },
  });
</script>

<style></style>
