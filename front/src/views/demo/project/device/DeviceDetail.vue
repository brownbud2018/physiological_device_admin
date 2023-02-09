<template>
  <PageWrapper
    :title="`Device` + userId + `的资料`"
    content="这是Device详情页面。可以用来查看详情，和查看设备上传的相关log日志"
    contentBackground
    @back="goBack"
  >
    <template #extra>
      <a-button type="primary" @click="goChange()"> 修改密码 </a-button>
    </template>
    <template #footer>
      <a-tabs default-active-key="detail" v-model:activeKey="currentKey">
        <a-tab-pane key="detail" tab="Device资料" />
        <a-tab-pane key="logs" tab="相关操作日志" />
      </a-tabs>
    </template>
    <div class="pt-4 m-4 desc-wrap">
      <template v-if="currentKey == 'detail'">
        <div>DeviceID：{{ curData.id }}</div>
        <div>Device名称：{{ curData.name }}</div>
        <div>Device编号：{{ curData.device_code }}</div>
        <div>Device设备名称：{{ curData.prod_name }}</div>
        <div>Device版本：{{ curData.version }}</div>
        <div>Device地址：{{ curData.address }}</div>
        <div>Device图标：{{ curData.image }}
          <template v-if="curData.image != '' && curData.image != undefined">
            <img alt="example" :src="getimg(curData.image)" width="100" />
          </template>
        </div>
        <div>
          <p v-if="curData.is_active===0">Device是否激活：未激活</p>
          <p v-else-if="curData.is_active===1">Device是否激活：已激活</p>
          <p v-else>Device是否激活：未知激活</p>
          <p v-if="curData.device_level===0">Device等级权限：普通等级</p>
          <p v-else-if="curData.device_level===1">Device等级权限：授权等级</p>
          <p v-else-if="curData.device_level===2">Device等级权限：VIP等级</p>
          <p v-else>Device等级权限：未知等级</p>
          <p v-if="curData.device_auth_class_id===0">Device机器批次：测试样机</p>
          <p v-else-if="curData.device_auth_class_id===1">Device机器批次：客户样机</p>
          <p v-else-if="curData.device_auth_class_id===2">Device机器批次：第一批试产机器</p>
          <p v-else-if="curData.device_auth_class_id===3">Device机器批次：第二批试产机器</p>
          <p v-else-if="curData.device_auth_class_id===4">Device机器批次：第三批试产机器</p>
          <p v-else>Device机器批次：未知批次</p>
        </div>
      </template>
      <template v-if="currentKey == 'logs'">
        <BasicTable @register="registerTable" class="w-3/4 xl:w-4/5" :searchInfo="searchInfo">
          <template #action="{ record }">
            <TableAction
              :actions="[
                {
                  icon: 'clarity:info-standard-line',
                  tooltip: '查看日志详情',
                  onClick: handleView.bind(null, record),
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
  import { defineComponent, reactive, ref } from 'vue';
  import { useRoute } from 'vue-router';
  import { PageWrapper } from '/@/components/Page';
  import { useGo } from '/@/hooks/web/usePage';
  import { useTabs } from '/@/hooks/web/useTabs';
  import { Tabs } from 'ant-design-vue';
  import { getDeviceLogList, getDeviceDetail } from '/@/api/demo/device';
  import { useMessage } from '../../../../hooks/web/useMessage';
  import { BasicTable, TableAction, useTable } from '/@/components/Table';
  import { columns, searchFormSchema } from './devicedetail.data';

  export default defineComponent({
    name: 'DeviceDetail',
    components: { PageWrapper, ATabs: Tabs, ATabPane: Tabs.TabPane, BasicTable, TableAction },
    setup() {
      const searchInfo = reactive<Recordable>({});
      const [registerTable] = useTable({
        title: '日志列表',
        api: getDeviceLogList,
        rowKey: 'id',
        columns,
        formConfig: {
          labelWidth: 120,
          schemas: searchFormSchema,
          autoSubmitOnEnter: true,
        },
        useSearchForm: true,
        showTableSetting: false,
        bordered: true,
        beforeFetch(info) {
          info.deviceId = userId.value;
          return info;
        },
        actionColumn: {
          width: 120,
          title: '操作',
          dataIndex: 'action',
          slots: { customRender: 'action' },
        },
      });

      function handleView(record: Recordable) {
        //浏览
        const url = getfile(record.log_image);
        window.open(url, '_blank');
        //go(getfile(record.log_image));
      }
      const route = useRoute();
      const go = useGo();
      // 此处可以得到用户ID
      const userId = ref(route.params?.id);
      const currentKey = ref('detail');
      const { setTitle } = useTabs();
      const { createMessage } = useMessage();
      const curData = ref(0);
      const promise = new Promise((resolve, reject) => {
        const data = getDeviceDetail(userId.value)
          .then((res) => {
            curData.value = res.data[0];
            return res.data;
          })
          .catch(() => {
            createMessage.error('查询Device详情失败');
          });
        resolve(data);
      });
      // TODO
      // 本页代码仅作演示，实际应当通过userId从接口获得用户的相关资料
      // 设置Tab的标题（不会影响页面标题）
      setTitle('Device详情' + userId.value);

      // 页面左侧点击返回链接时的操作
      function goBack() {
        // 本例的效果时点击返回始终跳转到账号列表页，实际应用时可返回上一页
        go('/project/device');
      }

      // 修改密码
      function goChange() {
        // 修改密码
        go('/project/device_password/' + curData.value.id);
      }

      function getimg(url: string) {
        return import.meta.env.VITE_GLOB_API_URL_SIMPLE + '/' + url;
      }

      function getfile(url: string) {
        return import.meta.env.VITE_GLOB_API_URL_SIMPLE + '/' + url;
      }
      return {
        registerTable,
        userId,
        currentKey,
        curData,
        goBack,
        goChange,
        getimg,
        getfile,
        handleView,
        searchInfo,
      };
    },
  });
</script>

<style></style>
