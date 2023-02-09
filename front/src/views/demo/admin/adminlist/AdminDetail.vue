<template>
  <PageWrapper
    :title="`管理员` + userId + `的资料`"
    content="这是管理员详情页面。可以用来查看详情，和查看设备上传的相关log日志"
    contentBackground
    @back="goBack"
  >
    <template #extra>
      <a-button type="primary" @click="goChange()"> 修改密码 </a-button>
    </template>
    <template #footer>
      <a-tabs default-active-key="detail" v-model:activeKey="currentKey">
        <a-tab-pane key="detail" tab="管理员资料" />
        <a-tab-pane key="logs" tab="相关授权" />
      </a-tabs>
    </template>
    <div class="pt-4 m-4 desc-wrap">
      <template v-if="currentKey == 'detail'">
        <div>管理员ID：{{ curData.id }}</div>
        <div>管理员用户名：{{ curData.name }}</div>
        <div>管理员角色名称：{{ curData.role_name }}</div>
        <div>管理员地址：{{ curData.address }}</div>
        <div
          >管理员图标：{{ curData.image }}
          <template v-if="curData.image != '' && curData.image != undefined">
            <img alt="example" :src="getimg(curData.image)" width="100" />
          </template>
        </div>
        <div>
          <p v-if="curData.is_active === 0">管理员是否启用：已禁用</p>
          <p v-else-if="curData.is_active === 1">管理员是否激活：已启用</p>
          <p v-else>是否超级管理员：否</p>
          <p v-if="curData.user_type === 0">否</p>
          <p v-else-if="curData.user_type === 1">是</p>
        </div>
      </template>
      <template v-if="currentKey == 'logs'">
        <!--<BasicTable @register="registerTable" class="w-3/4 xl:w-4/5" :searchInfo="searchInfo">
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
        </BasicTable>-->
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
  import { getAdminDetail } from '/@/api/demo/admin';
  import { useMessage } from '../../../../hooks/web/useMessage';
  //import { BasicTable, TableAction, useTable } from '/@/components/Table';
  //import { columns, searchFormSchema } from './admindetail.data';

  export default defineComponent({
    name: 'AdminDetail',
    components: { PageWrapper, ATabs: Tabs, ATabPane: Tabs.TabPane }, //, BasicTable, TableAction
    setup() {
      const searchInfo = reactive<Recordable>({});
      /*const [registerTable] = useTable({
        title: '日志列表',
        api: getAdminLogList,
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
          info.adminId = userId.value;
          return info;
        },
        actionColumn: {
          width: 120,
          title: '操作',
          dataIndex: 'action',
          slots: { customRender: 'action' },
        },
      });*/

      function handleView(record: Recordable) {
        //浏览
        const url = getfile(record.image);
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
        const data = getAdminDetail(userId.value)
          .then((res) => {
            curData.value = res.data[0];
            return res.data;
          })
          .catch(() => {
            createMessage.error('查询管理员详情失败');
          });
        resolve(data);
      });
      // TODO
      // 本页代码仅作演示，实际应当通过userId从接口获得用户的相关资料
      // 设置Tab的标题（不会影响页面标题）
      setTitle('管理员详情' + userId.value);

      // 页面左侧点击返回链接时的操作
      function goBack() {
        // 本例的效果时点击返回始终跳转到账号列表页，实际应用时可返回上一页
        go('/admin/adminlist');
      }

      // 修改密码
      function goChange() {
        // 修改密码
        go('/admin/admin_password/' + curData.value.id);
      }

      function getimg(url: string) {
        return import.meta.env.VITE_GLOB_API_URL_SIMPLE + '/' + url;
      }

      function getfile(url: string) {
        return import.meta.env.VITE_GLOB_API_URL_SIMPLE + '/' + url;
      }
      return {
        //registerTable,
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
