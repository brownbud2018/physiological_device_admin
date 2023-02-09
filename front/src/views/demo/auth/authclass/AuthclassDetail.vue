<template>
  <PageWrapper
    :title="`授权` + userId + `的资料`"
    content="这是授权详情页面。可以用来查看详情，和查看相关权限"
    contentBackground
    @back="goBack"
  >
    <template #footer>
      <a-tabs default-active-key="detail" v-model:activeKey="currentKey">
        <a-tab-pane key="detail" tab="授权资料" />
        <a-tab-pane key="logs" tab="相关权限" />
      </a-tabs>
    </template>
    <div class="pt-4 m-4 desc-wrap">
      <template v-if="currentKey == 'detail'">
        <div>授权ID：{{ curData.id }}</div>
        <div>授权名称：{{ curData.class_name }}</div>
        <div>授权编号：{{ curData.class_code }}</div>
        <div>授权描述：{{ curData.class_desc }}</div>
        <div
          >授权图标：{{ curData.class_image }}
          <template v-if="curData.class_image != '' && curData.class_image != undefined">
            <img alt="example" :src="getimg(curData.class_image)" width="100" />
          </template>
        </div>
        <div>授权备注：{{ curData.class_remark }}</div>
      </template>
      <template v-if="currentKey == 'logs'">
        <BasicTable @register="registerTable" class="w-3/4 xl:w-4/5" :searchInfo="searchInfo">
          <template #action="{ record }">
            <TableAction />
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
  import { getAuthclassDetail, getAuthdetailList } from '/@/api/demo/authclass';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { BasicTable, TableAction, useTable } from '/@/components/Table';
  import { columns, searchFormSchema } from './authclassdetail.data';

  export default defineComponent({
    name: '授权Detail',
    components: { PageWrapper, ATabs: Tabs, ATabPane: Tabs.TabPane, BasicTable, TableAction },
    setup() {
      const searchInfo = reactive<Recordable>({});
      const [registerTable] = useTable({
        title: 'ota权限列表',
        api: getAuthdetailList,
        rowKey: 'id',
        columns,
        formConfig: {
          labelWidth: 120,
          schemas: searchFormSchema,
          autoSubmitOnEnter: true,
        },
        useSearchForm: false,
        showTableSetting: false,
        bordered: true,
        beforeFetch(info) {
          info.class_id = userId.value;
          return info;
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
      const promise = new Promise((resolve, reject) => {
        const data = getAuthclassDetail(userId.value)
          .then((res) => {
            curData.value = res.data[0];
            return res.data;
          })
          .catch(() => {
            createMessage.error('查询授权详情失败');
          });
        resolve(data);
      });
      // TODO
      // 本页代码仅作演示，实际应当通过userId从接口获得用户的相关资料
      // 设置Tab的标题（不会影响页面标题）
      setTitle('授权详情' + userId.value);

      // 页面左侧点击返回链接时的操作
      function goBack() {
        // 本例的效果时点击返回始终跳转到账号列表页，实际应用时可返回上一页
        go('/auth/authclass');
      }

      function getimg(url: string) {
        return import.meta.env.VITE_GLOB_API_URL_SIMPLE + '/' + url;
      }

      function getfile(url: string) {
        return import.meta.env.VITE_GLOB_API_URL_SIMPLE + '/' + url;
      }

      function handleView(record: Recordable) {
        //浏览
        const url = getfile(record.detail_file);
        window.open(url, '_blank');
        //go(getfile(record.log_image));
      }
      return {
        registerTable,
        userId,
        currentKey,
        curData,
        goBack,
        getimg,
        getfile,
        handleView,
        searchInfo,
      };
    },
  });
</script>

<style></style>
