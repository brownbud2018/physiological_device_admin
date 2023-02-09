<template>
  <PageWrapper dense contentFullHeight contentClass="flex">
    <RoleTree class="w-1/4 xl:w-1/5" @select="handleSelect" />
    <BasicTable @register="registerTable" class="w-3/4 xl:w-4/5" :searchInfo="searchInfo">
      <template #toolbar>
        <a-button type="primary" @click="handleCreate">新增管理员</a-button>
      </template>
      <template #action="{ record }">
        <TableAction
          :actions="[
            {
              icon: 'clarity:info-standard-line',
              tooltip: '查看管理员详情',
              onClick: handleView.bind(null, record),
            },
            {
              icon: 'clarity:note-edit-line',
              tooltip: '编辑管理员',
              onClick: handleEdit.bind(null, record),
            },
            {
              icon: 'ant-design:delete-outlined',
              color: 'error',
              tooltip: '删除此管理员',
              popConfirm: {
                title: '是否确认删除',
                confirm: handleDelete.bind(null, record),
              },
            },
          ]"
        />
      </template>
    </BasicTable>
    <AdminModal @register="registerModal" @success="handleSuccess" />
  </PageWrapper>
</template>
<script lang="ts">
  import { defineComponent, reactive } from 'vue';

  import { BasicTable, useTable, TableAction } from '/@/components/Table';
  import { delAdminType, getAdminList } from '/@/api/demo/admin';
  import { PageWrapper } from '/@/components/Page';
  import RoleTree from './RoleTree.vue';

  import { useModal } from '/@/components/Modal';
  import { useMessage } from '/@/hooks/web/useMessage';
  import AdminModal from './AdminModal.vue';

  import { columns, searchFormSchema } from './admin.data';
  import { useGo } from '/@/hooks/web/usePage';

  export default defineComponent({
    name: 'AdminManagement',
    components: { BasicTable, PageWrapper, RoleTree, AdminModal, TableAction },
    setup() {
      const go = useGo();
      const [registerModal, { openModal }] = useModal();
      const searchInfo = reactive<Recordable>({});
      const [registerTable, { reload }] = useTable({
        title: '管理员列表',
        api: getAdminList,
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
        delAdminType(record.id)
          .then((res) => {
            //console.log('res:' + res);
            createMessage.success('已成功删除管理员');
          })
          .catch(() => {
            createMessage.error('删除管理员失败');
          });
        reload();
      }

      function handleSuccess({ isUpdate, values }) {
        if (isUpdate) {
          // 演示不刷新表格直接更新内部数据。
          // 注意：updateTableDataRecord要求表格的rowKey属性为string并且存在于每一行的record的keys中
          //const result = updateTableDataRecord(values.id, values);
          reload();
          //console.log(result);
        } else {
          reload();
        }
      }

      function handleSelect(roleId = '') {
        //左侧选择项目钩子
        searchInfo.roleId = roleId;
        reload();
      }

      function handleView(record: Recordable) {
        //浏览
        go('/admin/admin_detail/' + record.id);
      }

      return {
        registerTable,
        registerModal,
        handleCreate,
        handleEdit,
        handleDelete,
        handleSuccess,
        handleSelect,
        handleView,
        searchInfo,
      };
    },
  });
</script>
