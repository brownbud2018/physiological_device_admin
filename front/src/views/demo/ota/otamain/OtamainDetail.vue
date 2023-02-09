<template>
  <PageWrapper
    :title="`OTA` + userId + `的资料`"
    content="这是OTA详情页面。可以用来查看详情，和查看相关版本"
    contentBackground
    @back="goBack"
  >
    <template #footer>
      <a-tabs default-active-key="detail" v-model:activeKey="currentKey">
        <a-tab-pane key="detail" tab="OTA资料" />
        <a-tab-pane key="logs" tab="相关版本" />
      </a-tabs>
    </template>
    <div class="pt-4 m-4 desc-wrap">
      <template v-if="currentKey == 'detail'">
        <div>OTAID：{{ curData.id }}</div>
        <div>OTA名称：{{ curData.ota_name }}</div>
        <div>OTA编号：{{ curData.ota_code }}</div>
        <div>OTA分类名称：{{ curData.class_name }}</div>
        <div>OTA包名：{{ curData.ota_package }}</div>
        <div>
          <p v-if="curData.ota_type === 0">OTA属性：应用市场</p>
          <p v-else-if="curData.ota_type === 1">OTA属性：内置应用</p>
          <p v-else>OTA属性：未知</p>
          <p v-if="curData.ota_update_type === 0">OTA更新属性：非强制更新</p>
          <p v-else-if="curData.ota_update_type === 1">OTA更新属性：强制更新</p>
          <p v-else>OTA更新属性：未知</p>
        </div>
        <div>OTA简介：{{ curData.ota_info }}</div>
        <div>OTA评分：{{ curData.ota_score }}</div>
        <div>OTA下载次数：{{ curData.ota_download_amount }}</div>
        <div>OTA公司：{{ curData.ota_company }}</div>
        <div>OTA描述：{{ curData.ota_desc }}</div>
        <div
          >OTA图标：{{ curData.ota_image }}
          <template v-if="curData.ota_image != '' && curData.ota_image != undefined">
            <img alt="example" :src="getimg(curData.ota_image)" width="100" />
          </template>
        </div>
        <div>OTA备注：{{ curData.ota_remark }}</div>
      </template>
      <template v-if="currentKey == 'logs'">
        <BasicTable @register="registerTable" class="w-3/4 xl:w-4/5" :searchInfo="searchInfo">
          <template #action="{ record }">
            <TableAction
              :actions="[
                {
                  icon: 'ant-design:download',
                  tooltip: '下载此软件',
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
  import { getOtamainDetail, getOtaversionList } from '/@/api/demo/otamain';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { BasicTable, TableAction, useTable } from '/@/components/Table';
  import { columns, searchFormSchema } from './otamaindetail.data';

  export default defineComponent({
    name: 'OTADetail',
    components: { PageWrapper, ATabs: Tabs, ATabPane: Tabs.TabPane, BasicTable, TableAction },
    setup() {
      const searchInfo = reactive<Recordable>({});
      const [registerTable] = useTable({
        title: 'ota版本列表',
        api: getOtaversionList,
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
          info.ota_main_id = userId.value;
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
      const promise = new Promise((resolve, reject) => {
        const data = getOtamainDetail(userId.value)
          .then((res) => {
            curData.value = res.data[0];
            return res.data;
          })
          .catch(() => {
            createMessage.error('查询OTA详情失败');
          });
        resolve(data);
      });
      // TODO
      // 本页代码仅作演示，实际应当通过userId从接口获得用户的相关资料
      // 设置Tab的标题（不会影响页面标题）
      setTitle('OTA详情' + userId.value);

      // 页面左侧点击返回链接时的操作
      function goBack() {
        // 本例的效果时点击返回始终跳转到账号列表页，实际应用时可返回上一页
        go('/ota/otamain');
      }

      function getimg(url: string) {
        return import.meta.env.VITE_GLOB_API_URL_SIMPLE + '/' + url;
      }

      function getfile(url: string) {
        return import.meta.env.VITE_GLOB_API_URL_SIMPLE + '/' + url;
      }

      function handleView(record: Recordable) {
        //浏览
        const url = getfile(record.ota_v_file);
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
