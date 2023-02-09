<template>
  <div>
    <BasicTable @register="registerTable">
      <template #toolbar>
        <a-button type="primary" @click="handleCreate"> 新增Excel导入 </a-button>
      </template>
      <template #action="{ record }">
        <TableAction
          :actions="[
            {
              icon: 'clarity:info-standard-line',
              tooltip: '查看导入详情',
              onClick: handleView.bind(null, record),
            },
            {
              icon: 'clarity:note-edit-line',
              tooltip: '编辑导入记录',
              onClick: handleEdit.bind(null, record),
            },
            {
              icon: 'ant-design:delete-outlined',
              color: 'error',
              tooltip: '删除此导入',
              popConfirm: {
                title: '是否确认删除',
                confirm: handleDelete.bind(null, record),
              },
            },
          ]"
        />
      </template>
    </BasicTable>
    <ExceluploadDrawer @register="registerDrawer" @success="handleSuccess" />
  </div>
</template>
<script lang="ts">
  import { defineComponent } from 'vue';

  import { BasicTable, useTable, TableAction } from '/@/components/Table';
  import { delExcelupload, getExceluploadList } from '/@/api/demo/excelupload';

  import { useDrawer } from '/@/components/Drawer';
  import ExceluploadDrawer from './ExceluploadDrawer.vue';

  import { columns, searchFormSchema } from './excelupload.data';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { useGo } from '/@/hooks/web/usePage';

  export default defineComponent({
    name: 'ExceluploadManagement',
    components: { BasicTable, ExceluploadDrawer, TableAction },
    setup() {
      const [registerDrawer, { openDrawer }] = useDrawer();
      const [registerTable, { reload }] = useTable({
        title: 'Excel导入列表',
        api: getExceluploadList,
        rowKey: 'id',
        columns,
        formConfig: {
          labelWidth: 120,
          schemas: searchFormSchema,
        },
        useSearchForm: true,
        showTableSetting: false,
        bordered: true,
        showIndexColumn: false,
        handleSearchInfoFn(info) {
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
        openDrawer(true, {
          isUpdate: false,
        });
      }

      function handleEdit(record: Recordable) {
        openDrawer(true, {
          record,
          isUpdate: true,
        });
      }

      function handleDelete(record: Recordable) {
        //console.log(record);
        const { createMessage } = useMessage();
        delExcelupload(record.id)
          .then((res) => {
            createMessage.success('已成功删除Excel');
          })
          .catch(() => {
            createMessage.error('删除Excel失败');
          });
        //reload();
        location.reload();
      }

      function handleSuccess() {
        reload();
      }

      const go = useGo();
      function handleView(record: Recordable) {
        //浏览
        go('/project/excelupload_detail/' + record.id);
      }

      function handleDownload(record: Recordable) {
        //浏览
        const url = getfile(record.excel_address);
        window.open(url, '_blank');
      }

      function getfile(url: string) {
        return import.meta.env.VITE_GLOB_API_URL_SIMPLE + '/' + url;
      }

      return {
        registerTable,
        registerDrawer,
        handleCreate,
        handleEdit,
        handleSuccess,
        handleDelete,
        handleView,
        handleDownload,
      };
    },
  });
</script>
