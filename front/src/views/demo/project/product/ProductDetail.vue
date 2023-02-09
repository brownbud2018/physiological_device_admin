<template>
  <PageWrapper
    :title="`设备类型` + userId + `的资料`"
    content="这是设备类型详情页面。可以用来查看详情，和查看设备上传的相关log日志"
    contentBackground
    @back="goBack"
  >
    <template #footer>
      <a-tabs default-active-key="detail" v-model:activeKey="currentKey">
        <a-tab-pane key="detail" tab="设备类型资料" />
        <a-tab-pane key="logs" tab="相关操作日志" />
      </a-tabs>
    </template>
    <div class="pt-4 m-4 desc-wrap">
      <template v-if="currentKey == 'detail'">
        <div>设备类型ID：{{ curData.id }}</div>
        <div>设备类型名称：{{ curData.prod_name }}</div>
        <div>设备类型编号：{{ curData.prod_code }}</div>
        <div>设备类型项目名称：{{ curData.pro_name }}</div>
        <div
          >设备类型图标：{{ curData.prod_image }}
          <template v-if="curData.prod_image != '' && curData.prod_image != undefined">
            <img alt="example" :src="getimg(curData.prod_image)" width="100" />
          </template>
        </div>
        <div>设备类型备注：{{ curData.prod_remark }}</div>
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
  import { getLogList, getProductDetail } from '../../../../api/demo/product';
  import { useMessage } from '../../../../hooks/web/useMessage';
  import { BasicTable, TableAction, useTable } from '../../../../components/Table';
  import { columns, searchFormSchema } from './productdetail.data';

  export default defineComponent({
    name: 'ProductDetail',
    components: { PageWrapper, ATabs: Tabs, ATabPane: Tabs.TabPane, BasicTable, TableAction },
    setup() {
      const searchInfo = reactive<Recordable>({});
      const [registerTable] = useTable({
        title: '日志列表',
        api: getLogList,
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
          info.prod_id = userId.value;
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
        const data = getProductDetail(userId.value)
          .then((res) => {
            curData.value = res.data[0];
            return res.data;
          })
          .catch(() => {
            createMessage.error('查询设备类型详情失败');
          });
        resolve(data);
      });
      // TODO
      // 本页代码仅作演示，实际应当通过userId从接口获得用户的相关资料
      // 设置Tab的标题（不会影响页面标题）
      setTitle('设备类详情' + userId.value);

      // 页面左侧点击返回链接时的操作
      function goBack() {
        // 本例的效果时点击返回始终跳转到账号列表页，实际应用时可返回上一页
        go('/project/product');
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
        getimg,
        getfile,
        handleView,
        searchInfo,
      };
    },
  });
</script>

<style></style>
