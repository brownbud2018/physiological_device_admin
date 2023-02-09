<template>
  <PageWrapper dense contentFullHeight contentClass="flex">
    <AdminTree class="w-1/4 xl:w-1/5" @select="handleSelect" />
    <BasicTable @register="registerTable" class="w-3/4 xl:w-4/5" :searchInfo="searchInfo">
      <template #toolbar>
        <a-button type="primary" @click="handleCreate">新增关联</a-button>
      </template>
      <template #action="{ record }">
        <TableAction
          :actions="[
            {
              icon: 'clarity:note-edit-line',
              tooltip: '编辑关联',
              onClick: handleEdit.bind(null, record),
            },
            {
              icon: 'ant-design:delete-outlined',
              color: 'error',
              tooltip: '删除此关联',
              popConfirm: {
                title: '是否确认删除',
                confirm: handleDelete.bind(null, record),
              },
            },
          ]"
        />
      </template>
    </BasicTable>
    <AdminauthModal @register="registerModal" @success="handleSuccess" />
  </PageWrapper>
</template>
<script lang="ts">
  import { defineComponent, reactive } from 'vue';

  import { BasicTable, useTable, TableAction } from '/@/components/Table';
  import { delAdminauth, getAdminauthList } from '/@/api/demo/adminauth';
  import { PageWrapper } from '/@/components/Page';
  import AdminTree from './AdminTree.vue';

  import { useModal } from '/@/components/Modal';
  import { useMessage } from '../../../../hooks/web/useMessage';
  import AdminauthModal from './AdminauthModal.vue';

  import { columns, searchFormSchema } from './adminauth.data';

  export default defineComponent({
    name: 'AdminauthManagement',
    components: { BasicTable, PageWrapper, AdminTree, AdminauthModal, TableAction },
    setup() {
      const [registerModal, { openModal }] = useModal();
      const searchInfo = reactive<Recordable>({});
      const [registerTable, { reload, updateTableDataRecord }] = useTable({
        title: '关联列表',
        api: getAdminauthList,
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
        delAdminauth(record.id)
          .then((res) => {
            //console.log('res:' + res);
            createMessage.success('已成功删除关联');
          })
          .catch(() => {
            createMessage.error('删除关联失败');
          });
        reload();
        location.reload();
      }

      function handleSuccess({ isUpdate, values }) {
        if (isUpdate) {
          reload();
        } else {
          reload();
        }
      }

      function handleSelect(admin_id = '') {
        //左侧选择项目钩子
        searchInfo.admin_id = admin_id;
        reload();
      }

      return {
        registerTable,
        registerModal,
        handleCreate,
        handleEdit,
        handleDelete,
        handleSuccess,
        handleSelect,
        searchInfo,
      };
    },
  });
</script>
