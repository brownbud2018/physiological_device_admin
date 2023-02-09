<template>
  <PageWrapper dense contentFullHeight contentClass="flex">
    <OtaTree class="w-1/4 xl:w-1/5" @select="handleSelect" />
    <BasicTable @register="registerTable" class="w-3/4 xl:w-4/5" :searchInfo="searchInfo">
      <template #toolbar>
        <a-button type="primary" @click="handleCreate">新增OTA版本</a-button>
      </template>
      <template #action="{ record }">
        <TableAction
          :actions="[
            {
              icon: 'ant-design:download',
              tooltip: '下载OTA版本文件',
              onClick: handleDownload.bind(null, record),
            },
            {
              icon: 'clarity:note-edit-line',
              tooltip: '编辑OTA版本',
              onClick: handleEdit.bind(null, record),
            },
            {
              icon: 'ant-design:delete-outlined',
              color: 'error',
              tooltip: '删除此OTA版本',
              popConfirm: {
                title: '是否确认删除',
                confirm: handleDelete.bind(null, record),
              },
            },
          ]"
        />
      </template>
    </BasicTable>
    <OtaversionModal @register="registerModal" @success="handleSuccess" />
  </PageWrapper>
</template>
<script lang="ts">
  import { defineComponent, reactive } from 'vue';

  import { BasicTable, useTable, TableAction } from '/@/components/Table';
  import { delOtaversion, getOtaversionList } from '/@/api/demo/otaversion';
  import { PageWrapper } from '/@/components/Page';
  import OtaTree from './OtaTree.vue';

  import { useModal } from '/@/components/Modal';
  import { useMessage } from '../../../../hooks/web/useMessage';
  import OtaversionModal from './OtaversionModal.vue';

  import { columns, searchFormSchema } from './otaversion.data';
  import { useGo } from '/@/hooks/web/usePage';

  export default defineComponent({
    name: 'OtaversionManagement',
    components: { BasicTable, PageWrapper, OtaTree, OtaversionModal, TableAction },
    setup() {
      const go = useGo();
      const [registerModal, { openModal }] = useModal();
      const searchInfo = reactive<Recordable>({});
      const [registerTable, { reload }] = useTable({
        title: 'OTA版本列表',
        api: getOtaversionList,
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
        handleSearchInfoFn(info) {
          //console.log('handleSearchInfoFn', info);
          return info;
        },
        actionColumn: {
          width: 120,
          title: '操作',
          dataIndex: 'action',
          slots: { customRender: 'action' },
        },
      });

      function handleCreate() {
        openModal(true, {
          isUpdate: false,
        });
      }

      function handleEdit(record: Recordable) {
        openModal(true, {
          record,
          isUpdate: true,
        });
      }

      function handleDelete(record: Recordable) {
        //console.log(record);
        const { createMessage } = useMessage();
        delOtaversion(record.id)
          .then((res) => {
            //console.log('res:' + res);
            createMessage.success('已成功删除OTA版本');
          })
          .catch(() => {
            createMessage.error('删除OTA版本失败');
          });
        reload();
        location.reload();
      }

      function handleSuccess({ isUpdate, values }) {
        reload();
      }

      function handleSelect(ota_main_id = '') {
        //左侧选择OTA钩子
        searchInfo.ota_main_id = ota_main_id;
        reload();
      }

      function getfile(url: string) {
        return import.meta.env.VITE_GLOB_API_URL_SIMPLE + '/' + url;
      }

      function handleDownload(record: Recordable) {
        //下载
        const url = getfile(record.ota_v_file);
        window.open(url, '_blank');
      }

      return {
        registerTable,
        registerModal,
        handleCreate,
        handleEdit,
        handleDelete,
        handleSuccess,
        handleSelect,
        getfile,
        handleDownload,
        searchInfo,
      };
    },
  });
</script>
