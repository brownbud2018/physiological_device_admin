<template>
  <PageWrapper
    :title="`导入` + userId + `的资料`"
    content="这是导入Device详情页面。可以用来查看导入详情，和Excel浏览.<br />导入规则：已经导入的，进行修改，未导入的，新增。"
    contentBackground
    @back="goBack"
  >
    <template v-if="curData.is_import">
      <div class="py-8 bg-white flex flex-col justify-center items-center">
        <div class="flex justify-center"> 已导入 </div>
        <div class="flex justify-center">
          <a-button class="!ml-4" type="primary" @click="handleSubmit"> 再次导入 </a-button>
        </div>
      </div>
    </template>
    <template v-else>
      <div class="py-8 bg-white flex flex-col justify-center items-center">
        <div class="flex justify-center">
          <a-button class="!ml-4" type="primary" @click="handleSubmit"> 点击导入 </a-button>
        </div>
      </div>
    </template>
    <template #footer>
      <a-tabs default-active-key="detail" v-model:activeKey="currentKey">
        <a-tab-pane key="detail" tab="导入资料" />
        <a-tab-pane key="logs" tab="Excel浏览" />
      </a-tabs>
    </template>
    <div class="pt-4 m-4 desc-wrap">
      <template v-if="currentKey == 'detail'">
        <div>导入ID：{{ curData.id }}</div>
        <div>导入编号：{{ curData.excel_code }}</div>
        <div>导入名称：{{ curData.excel_name }}</div>
        <div>导入地址：{{ curData.excel_address }}</div>
        <div>
          <p v-if="curData.is_import === 0">是否导入：未导入</p>
          <p v-else-if="curData.is_import === 1">是否导入：已导入</p>
          <p v-else>是否导入：未知</p>
        </div>
        <div>导入备注：{{ curData.excel_remark }}</div>
        <div>Device名称：{{ curData.name }}</div>
        <div>
          Device图标：{{ curData.image }}
          <template v-if="curData.image != '' && curData.image != undefined">
            <img alt="example" :src="getimg(curData.image)" width="100" />
          </template>
        </div>
        <div>所属项目类型：{{ curData.prod_name }}</div>
        <div>所属Ota名称：{{ curData.ota_name }}</div>
        <div>所属授权名称：{{ curData.class_name }}</div>
        <div>
          <p v-if="curData.is_active === 0">是否激活：未激活</p>
          <p v-else-if="curData.is_active === 1">是否激活：已激活</p>
          <p v-else>是否激活：未知</p>
        </div>
        <div>
          <p v-if="curData.device_level === 0">等级权限：普通等级</p>
          <p v-else-if="curData.device_level === 1">等级权限：授权等级</p>
          <p v-else-if="curData.device_level === 2">等级权限：VIP等级</p>
          <p v-else>等级权限：未知</p>
        </div>
        <div>Device版本：{{ curData.version }}</div>
        <div>Device地址：{{ curData.address }}</div>
        <div>Device密码：{{ curData.hashed_password }}</div>
      </template>
      <template v-if="currentKey == 'logs'">
        <!--<BasicTable @register="registerExcelTable" />-->
        <BasicTable
          v-for="(table, index) in tableListRef"
          :key="index"
          :title="table.title"
          :columns="table.columns"
          :dataSource="table.dataSource"
        />
      </template>
    </div>
  </PageWrapper>
</template>

<script lang="ts">
  import { defineComponent, h, ref } from 'vue';
  import { useRoute } from 'vue-router';
  import { PageWrapper } from '/@/components/Page';
  import { useGo } from '/@/hooks/web/usePage';
  import { useTabs } from '/@/hooks/web/useTabs';
  import { Tabs } from 'ant-design-vue';
  import { getExceluploadDetail, setExcelImport } from '/@/api/demo/excelupload';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { BasicTable, BasicColumn } from '/@/components/Table';
  import { useI18n } from '../../../../hooks/web/useI18n';

  export default defineComponent({
    name: 'ExceluploadDetail',
    components: { PageWrapper, ATabs: Tabs, ATabPane: Tabs.TabPane, BasicTable },
    setup() {
      const route = useRoute();
      const go = useGo();
      // 此处可以得到用户ID
      const userId = ref(route.params?.id);
      const currentKey = ref('detail');
      const { setTitle } = useTabs();
      const { createMessage } = useMessage();
      const curData = ref(0);
      const curData1 = ref(1);
      let tableListRef = ref<
        {
          title: string;
          columns?: any[];
          dataSource?: any[];
        }[]
      >([]);

      /*const [registerExcelTable] = useTable({
        title: 'Device列表',
        columns: tableFormExcel,
        dataSource: tableListRef,
      });*/

      const promise = new Promise((resolve, reject) => {
        const data = getExceluploadDetail(userId.value)
          .then((res) => {
            curData.value = res.data.data[0];
            curData1.value = res.data.table;
            const dataSo = [];
            tableListRef.value = [];
            for (const excelData of res.data.table) {
              dataSo.push({ device_code: excelData });
            }
            const columns: BasicColumn[] = [];
            columns.push({
              title: 'Device编号',
              dataIndex: 'device_code',
              width: 120,
            });
            tableListRef.value.push({ title: '导入的Excel文件浏览', columns, dataSource: dataSo });
            return res.data;
          })
          .catch(() => {
            createMessage.error('查询导入详情失败');
          });
        resolve(data);
      });
      // TODO
      // 本页代码仅作演示，实际应当通过userId从接口获得用户的相关资料
      // 设置Tab的标题（不会影响页面标题）
      setTitle('导入详情' + userId.value);

      // 页面左侧点击返回链接时的操作
      function goBack() {
        // 返回列表页
        go('/project/exceluploadlist');
      }

      function getimg(url: string) {
        return import.meta.env.VITE_GLOB_API_URL_SIMPLE + '/' + url;
      }

      async function handleSubmit() {
        try {
          const { createConfirm } = useMessage();
          const { t } = useI18n();
          createConfirm({
            iconType: 'warning',
            title: () => h('span', t('温馨提醒')),
            content: () => h('span', t('是否确定导入？')),
            onOk: async () => {
              await setExcelImport(Number(userId.value));
              location.reload();
            },
          });
          /*// TODO custom api
          const { createMessage } = useMessage();
          const dataExcelImport = await setExcelImport(Number(userId.value))
            .then((res) => {
              console.log('res:' + res);
              location.reload();
            })
            .catch(() => {
              createMessage.error('导入失败');
            });*/
        } catch (error) {}
      }

      return {
        userId,
        currentKey,
        curData,
        curData1,
        goBack,
        getimg,
        tableListRef,
        handleSubmit,
      };
    },
  });
</script>

<style></style>
