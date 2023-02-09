<template>
  <PageWrapper dense contentFullHeight contentClass="flex">
    <AuthclassTree class="w-1/4 xl:w-1/5" @select="handleSelect" />
    <BasicTable @register="registerTable" class="w-3/4 xl:w-4/5" :searchInfo="searchInfo">
      <template #toolbar>
        <a-button type="primary" @click="handleCreate">新增权限</a-button>
      </template>
      <template #action="{ record }">
        <TableAction
          :actions="[
            {
              icon: 'clarity:note-edit-line',
              tooltip: '编辑权限',
              onClick: handleEdit.bind(null, record),
            },
            {
              icon: 'ant-design:delete-outlined',
              color: 'error',
              tooltip: '删除此权限',
              popConfirm: {
                title: '是否确认删除',
                confirm: handleDelete.bind(null, record),
              },
            },
          ]"
        />
      </template>
    </BasicTable>
    <AuthdetailModal @register="registerModal" @success="handleSuccess" />
  </PageWrapper>
</template>
<script lang="ts">
  import { defineComponent, reactive } from 'vue';

  import { BasicTable, useTable, TableAction } from '/@/components/Table';
  import { delAuthdetail, getAuthdetailList } from '/@/api/demo/authdetail';
  import { PageWrapper } from '/@/components/Page';
  import AuthclassTree from './AuthclassTree.vue';

  import { useModal } from '/@/components/Modal';
  import { useMessage } from '/@/hooks/web/useMessage';
  import AuthdetailModal from './AuthdetailModal.vue';

  import { columns, searchFormSchema } from './authdetail.data';

  export default defineComponent({
    name: 'AuthdetailManagement',
    components: { BasicTable, PageWrapper, AuthclassTree, AuthdetailModal, TableAction },
    setup() {
      const [registerModal, { openModal }] = useModal();
      const searchInfo = reactive<Recordable>({});
      const [registerTable, { reload }] = useTable({
        title: '权限列表',
        api: getAuthdetailList,
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
        delAuthdetail(record.id)
          .then((res) => {
            //console.log('res:' + res);
            createMessage.success('已成功删除权限');
          })
          .catch(() => {
            createMessage.error('删除权限失败');
          });
        reload();
        location.reload();
      }

      function handleSuccess({ isUpdate, values }) {
        reload();
      }

      function handleSelect(class_id = '') {
        //左侧选择OTA钩子
        searchInfo.class_id = class_id;
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
