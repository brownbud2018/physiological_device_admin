<template>
  <div :class="prefixCls">
    <a-row :class="`${prefixCls}-top`">
      <a-col :span="9" :class="`${prefixCls}-col`">
        <a-row>
          <a-col :span="8">
            <div :class="`${prefixCls}-top__avatar`">
              <img :alt="curData.name" :src="getimg(curData.headicon)" width="70" />
              <span>{{ curData.name }}</span>
              <div>设备：{{ curData.devicename }}{{ curData.deviceid }}</div>
            </div>
          </a-col>
          <a-col :span="16">
            <div :class="`${prefixCls}-top__detail`">
              <p>
                <Icon icon="ant-design:user-outlined" />
                姓名：{{ curData.name }}
              </p>
              <p>
                <Icon icon="ant-design:phone-filled" />
                电话：{{ curData.phone }}
              </p>
              <p>
                <Icon icon="ant-design:idcard-filled" />
                身份证：{{ curData.idcard }}
              </p>
              <p>
                <Icon icon="ant-design:book-filled" />
                建档时间：{{ curData.createtime }}
              </p>
            </div>
          </a-col>
        </a-row>
      </a-col>
      <a-col :span="7" :class="`${prefixCls}-col`">
        <CollapseContainer title="基本信息" :canExpan="false">
          <Tag class="mb-2">
            性别:
            <template v-if="curData.sex == 0">男</template>
            <template v-else>女</template>
          </Tag>
          <Tag class="mb-2"> 年龄:{{ curData.age }}岁 </Tag>
          <Tag class="mb-2"> 身高:{{ curData.height }}CM </Tag>
          <Tag class="mb-2"> 体重:{{ curData.weight }}公斤 </Tag>
          <Tag class="mb-2"> {{ curData.province }} </Tag>
          <Tag class="mb-2"> {{ curData.city }} </Tag>
        </CollapseContainer>
      </a-col>
      <a-col :span="8" :class="`${prefixCls}-col`">
        <CollapseContainer :class="`${prefixCls}-top__team`" title="健康信息" :canExpan="false">
          <div :class="`${prefixCls}-top__team-item`">
            <Icon icon="emojione-monotone:letter-a" color="#7c51b8" />
            <span>血型：{{ curData.bloodtypename }}</span>
          </div>
          <div :class="`${prefixCls}-top__team-item`">
            <Icon icon="emojione-monotone:letter-a" color="#7c51b8" />
            <span>药物过敏史：{{ curData.allergyname }}</span>
          </div>
          <div :class="`${prefixCls}-top__team-item`">
            <Icon icon="emojione-monotone:letter-a" color="#7c51b8" />
            <span>既往病史：{{ curData.medicalname }}</span>
          </div>
          <div :class="`${prefixCls}-top__team-item`">
            <Icon icon="emojione-monotone:letter-a" color="#7c51b8" />
            <span>遗传病史：{{ curData.geneticname }}</span>
          </div>
          <div :class="`${prefixCls}-top__team-item`">
            <Icon icon="emojione-monotone:letter-a" color="#7c51b8" />
            <span>健康问题：{{ curData.descr }}</span>
          </div>
        </CollapseContainer>
      </a-col>
    </a-row>
    <div :class="`${prefixCls}-bottom`">
      <Tabs>
        <template v-for="item in achieveList" :key="item.key">
          <template v-if="item.key == '1'">
            <TabPane :tab="item.name">
              <component :is="item.component" />
            </TabPane>
          </template>
          <template v-if="item.key == '2'">
            <TabPane :tab="item.name">
              <echartsBloodSugarBefor1 @nextStep="nextStep" :data="data1" />
              <echartsBloodSugarBack1 @nextStep="nextStep" :data="data1" />
              <BasicTable @register="registerTable" />
            </TabPane>
          </template>
          <template v-if="item.key == '3'">
            <TabPane :tab="item.name">
              <echartsBloodPressure1 @nextStep="nextStep" :data="data1" />
              <BasicTable @register="registerTable1" />
            </TabPane>
          </template>
          <template v-if="item.key == '4'">
            <TabPane :tab="item.name">
              <echartsHeartrate2 @nextStep="nextStep" :data="data1" />
              <echartsHeartrate3 @nextStep="nextStep" :data="data1" />
              <BasicTable @register="registerTable2">
                <template #action="{ record }">
                  <TableAction
                    :actions="[
                      {
                        icon: 'clarity:info-standard-line',
                        tooltip: '查看波形图',
                        onClick: handleView.bind(null, record),
                      },
                    ]"
                  />
                </template>
              </BasicTable>
            </TabPane>
          </template>
          <template v-if="item.key == '5'">
            <TabPane :tab="item.name">
              <echartsBloodoxygen2 @nextStep="nextStep" :data="data1" />
              <echartsBloodoxygen3 @nextStep="nextStep" :data="data1" />
              <BasicTable @register="registerTable3">
                <template #action="{ record }">
                  <TableAction
                    :actions="[
                      {
                        icon: 'clarity:info-standard-line',
                        tooltip: '查看波形图',
                        onClick: handleView1.bind(null, record),
                      },
                    ]"
                  />
                </template>
              </BasicTable>
            </TabPane>
          </template>
          <template v-if="item.key == '6'">
            <TabPane :tab="item.name">
              <echartsTemperature1 @nextStep="nextStep" :data="data1" />
              <BasicTable @register="registerTable4" />
            </TabPane>
          </template>
          <template v-if="item.key == '7'">
            <TabPane :tab="item.name">
              <medicalRecord1 @nextStep="nextStep" :data="data1" />
              <BasicTable @register="registerTable5">
                <template #action="{ record }">
                  <TableAction
                    :actions="[
                      {
                        icon: 'clarity:info-standard-line',
                        tooltip: '查看病历图',
                        onClick: handleView2.bind(null, record),
                      },
                    ]"
                  />
                </template>
              </BasicTable>
            </TabPane>
          </template>
          <template v-if="item.key == '8'">
            <TabPane :tab="item.name">
              <!--<questionShow @nextStep="nextStep" :data="data1" />-->
              <BasicTable @register="registerTable6">
                <template #action="{ record }">
                  <TableAction
                    :actions="[
                      {
                        icon: 'clarity:info-standard-line',
                        tooltip: '查看问卷',
                        onClick: handleView3.bind(null, record),
                      },
                    ]"
                  />
                </template>
              </BasicTable>
            </TabPane>
          </template>
          <template v-if="item.key == '9'">
            <TabPane :tab="item.name">
              <echartsPhysique @nextStep="nextStep" :data="data1" />
              <BasicTable @register="registerTable7">
                <template #action="{ record }">
                  <TableAction
                    :actions="[
                      {
                        icon: 'clarity:info-standard-line',
                        tooltip: '查看雷达图',
                        onClick: handleView4.bind(null, record),
                      },
                    ]"
                  />
                </template>
              </BasicTable>
            </TabPane>
          </template>
        </template>
      </Tabs>
    </div>
  </div>
</template>

<script lang="ts">
  import { Tag, Tabs, Row, Col } from 'ant-design-vue';
  import { defineComponent, reactive, toRefs, ref } from 'vue';
  import { useRoute } from 'vue-router';
  import { useTabs } from '/@/hooks/web/useTabs';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { CollapseContainer } from '/@/components/Container/index';
  import Icon from '/@/components/Icon/index';
  import UserDetailHead from './UserDetailHead.vue';
  import echartsBloodSugarBefor1 from './echartsBloodSugarBefor1.vue';
  import echartsBloodSugarBack1 from './echartsBloodSugarBack1.vue';
  import echartsBloodPressure1 from './echartsBloodPressure1.vue';
  import echartsHeartrate2 from './echartsHeartrate2.vue';
  import echartsHeartrate3 from './echartsHeartrate3.vue';
  import echartsBloodoxygen2 from './echartsBloodoxygen2.vue';
  import echartsBloodoxygen3 from './echartsBloodoxygen3.vue';
  import echartsTemperature1 from './echartsTemperature1.vue';
  import medicalRecord1 from './medicalrecord1.vue';
  import questionShow from './questionShow.vue';
  import echartsPhysique from './echartsPhysique.vue';

  import {
    achieveList,
    columns,
    columnsbloodoxygen,
    columnsheartrate,
    columnspressure,
    columnsmedicalrecord,
    columnstemperature,
    columnsquestion,
    columnsphysique,
  } from './data';
  import {
    getUserBloodpressureList1,
    getUserBloodsugarList1,
    getUserHeartrateList1,
    getUserBloodoxygenList1,
    getUserTemperatureList1,
    getUserMedicalRecordList1,
    getQuestionList1,
    getUserPhysiqueList1,
  } from '/@/api/demo/user';
  import { getUserconsultingUser } from '/@/api/demo/userconsulting';
  import { BasicTable, TableAction, useTable } from '/@/components/Table';
  //import { useUserStore } from '/@/store/modules/user';
  interface DataProps {
    data1: any;
  }
  export default defineComponent({
    name: 'UserconsultingDetail',
    components: {
      CollapseContainer,
      Icon,
      Tag,
      Tabs,
      TabPane: Tabs.TabPane,
      UserDetailHead,
      [Row.name]: Row,
      [Col.name]: Col,
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
      medicalRecord1,
      questionShow,
      echartsPhysique,
    },
    setup(props) {
      const searchInfo = reactive<Recordable>({});

      const route = useRoute();
      // 此处可以得到用户ID
      const userId = ref(route.params?.id);
      let user_id = 0;
      let userPromise = new Promise((resolve) => {
        const data1 = getUserconsultingUser(userId.value)
          .then((res) => {
            curData.value = res.data[0];
            user_id = curData.value.user_id;
            setTitle('咨询详情：' + curData.value.name);
            return curData.value;
          })
          .catch(() => {
            createMessage.error('查询咨询用户详情失败');
          });
        resolve(data1);
      });

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
        datasend['heart_data_id'] = data_id;
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
        datasend['oxy_data_id'] = data_id;
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
        /*let data_id = '0';
        let user_id = '0';
        let timestamp = String(Date.parse(new Date().toString()));
        let datasend = {};

        user_id = String(record.userid);
        data_id = String(record.id);
        datasend['question_data_id'] = data_id;
        datasend['user_id'] = user_id;
        datasend['time'] = timestamp;
        data.data1 = datasend;*/
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
        nextStep() {
          //data.data1 = $event;
          let data_id = '0';
          //let user_id = '0';
          let timestamp = String(Date.parse(new Date().toString()));
          let datasend = {};
          //console.log('user_id', user_id);
          //user_id = String(0);
          data_id = String(0);
          datasend['this_data_id'] = data_id;
          datasend['user_id'] = user_id;
          datasend['time'] = timestamp;
          data.data1 = datasend;
        },
      });

      const refData = toRefs(data);

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
          info.dmuserid = user_id;
          return info;
        },
        afterFetch(info) {
          let data_id = '0';
          //let user_id = '0';
          let timestamp = String(Date.parse(new Date().toString()));
          let datasend = {};
          if (info.length > 0) {
            //user_id = String(info[info.length - 1].dmuserid);
            data_id = String(info[info.length - 1].id);
            datasend['sug_data_id'] = data_id;
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
          info.dmuserid = user_id;
          return info;
        },
        afterFetch(info) {
          let data_id = '0';
          //let user_id = '0';
          let timestamp = String(Date.parse(new Date().toString()));
          let datasend = {};
          if (info.length > 0) {
            //user_id = String(info[info.length - 1].dmuserid);
            data_id = String(info[info.length - 1].id);
            datasend['pre_data_id'] = data_id;
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
          info.dmuserid = user_id;
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
            datasend['heart_data_id'] = data_id;
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
          info.dmuserid = user_id;
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
            datasend['oxy_data_id'] = data_id;
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
          info.dmuserid = user_id;
          return info;
        },
        afterFetch(info) {
          let data_id = '0';
          //let user_id = '0';
          let timestamp = String(Date.parse(new Date().toString()));
          let datasend = {};
          if (info.length > 0) {
            //user_id = String(info[info.length - 1].dmuserid);
            data_id = String(info[info.length - 1].id);
            datasend['temp_data_id'] = data_id;
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
          info.dmuserid = user_id;
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
          info.userid = user_id;
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
          info.dmuserid = user_id;
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
            datasend['phy_data_id'] = data_id;
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

      function getimg(url: string) {
        if (url !== '' && url != undefined && url != null) {
          return 'https://pic.luckystar.com.cn/' + url + '.jpg';
        } else {
          return '/resource/img/nohead.jpg';
        }
      }
      return {
        ...refData,
        prefixCls: 'account-center',
        achieveList,
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
        user_id,
        handleView,
        handleView1,
        handleView2,
        handleView3,
        handleView4,
        getimg,
        searchInfo,
      };
    },
  });
</script>
<style lang="less" scoped>
  .account-center {
    &-col:not(:last-child) {
      padding: 0 10px;

      &:not(:last-child) {
        border-right: 1px dashed rgb(206 206 206 / 50%);
      }
    }

    &-top {
      padding: 10px;
      margin: 16px 16px 12px;
      background-color: @component-background;
      border-radius: 3px;

      &__avatar {
        text-align: center;

        img {
          margin: auto;
          border-radius: 50%;
        }

        span {
          display: block;
          font-size: 20px;
          font-weight: 500;
        }

        div {
          margin-top: 3px;
          font-size: 12px;
        }
      }

      &__detail {
        padding-left: 20px;
        margin-top: 15px;
      }

      &__team {
        &-item {
          display: inline-block;
          padding: 4px 24px;
        }

        span {
          margin-left: 3px;
        }
      }
    }

    &-bottom {
      padding: 10px;
      margin: 0 16px 16px;
      background-color: @component-background;
      border-radius: 3px;
    }
  }
</style>
