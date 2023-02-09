<template>
  <div>
    <BasicTable @register="registerTable">
      <template #toolbar>
        <a-button type="primary" @click="handleCreate"> 新增授权分类 </a-button>
      </template>
      <template #action="{ record }">
        <TableAction
          :actions="[
            {
              icon: 'clarity:info-standard-line',
              tooltip: '查看授权详情',
              onClick: handleView.bind(null, record),
            },
            {
              icon: 'clarity:note-edit-line',
              onClick: handleEdit.bind(null, record),
            },
            {
              icon: 'ant-design:delete-outlined',
              color: 'error',
              popConfirm: {
                title: '是否确认删除',
                confirm: handleDelete.bind(null, record),
              },
            },
          ]"
        />
      </template>
    </BasicTable>
    <AuthclassDrawer @register="registerDrawer" @success="handleSuccess" />
  </div>
</template>
<script lang="ts">
  import { defineComponent } from 'vue';

  import { BasicTable, useTable, TableAction } from '/@/components/Table';
  import { delAuthclass, getAuthclassList } from '/@/api/demo/authclass';

  import { useDrawer } from '/@/components/Drawer';
  import AuthclassDrawer from './AuthclassDrawer.vue';

  import { columns, searchFormSchema } from './authclass.data';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { useGo } from '/@/hooks/web/usePage';

  export default defineComponent({
    name: 'AuthclassManagement',
    components: { BasicTable, AuthclassDrawer, TableAction },
    setup() {
      const go = useGo();
      const [registerDrawer, { openDrawer }] = useDrawer();
      const [registerTable, { reload }] = useTable({
        title: '授权列表',
        api: getAuthclassList,
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
        delAuthclass(record.id)
          .then((res) => {
            //console.log('res:' + res);
            createMessage.success('已成功删除授权');
          })
          .catch(() => {
            createMessage.error('删除授权失败');
          });
        reload();
      }

      function handleSuccess() {
        reload();
      }

      function handleView(record: Recordable) {
        //浏览
        go('/auth/authclass_detail/' + record.id);
      }

      return {
        registerTable,
        registerDrawer,
        handleCreate,
        handleEdit,
        handleDelete,
        handleSuccess,
        handleView,
      };
    },
  });
</script>
