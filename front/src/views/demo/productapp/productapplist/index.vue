<template>
  <PageWrapper dense contentFullHeight contentClass="flex">
    <ProductTree class="w-1/4 xl:w-1/5" @select="handleSelect" />
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
    <ProductappModal @register="registerModal" @success="handleSuccess" />
  </PageWrapper>
</template>
<script lang="ts">
  import { defineComponent, reactive } from 'vue';

  import { BasicTable, useTable, TableAction } from '/@/components/Table';
  import { delProductapp, getProductappList } from '/@/api/demo/productapp';
  import { PageWrapper } from '/@/components/Page';
  import ProductTree from './ProductTree.vue';

  import { useModal } from '/@/components/Modal';
  import { useMessage } from '../../../../hooks/web/useMessage';
  import ProductappModal from './ProductappModal.vue';

  import { columns, searchFormSchema } from './productapp.data';
  import { useGo } from '/@/hooks/web/usePage';

  export default defineComponent({
    name: 'productapplistManagement',
    components: { BasicTable, PageWrapper, ProductTree, ProductappModal, TableAction },
    setup() {
      const go = useGo();
      const [registerModal, { openModal }] = useModal();
      const searchInfo = reactive<Recordable>({});
      const [registerTable, { reload, updateTableDataRecord }] = useTable({
        title: '关联列表',
        api: getProductappList,
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
        delProductapp(record.id)
          .then((res) => {
            //console.log('res:' + res);
            createMessage.success('已成功删除关联');
          })
          .catch(() => {
            createMessage.error('删除关联失败');
          });
        reload();
      }

      function handleSuccess({ isUpdate, values }) {
        if (isUpdate) {
          reload();
        } else {
          reload();
        }
      }

      function handleSelect(prod_id = '') {
        //左侧选择项目钩子
        searchInfo.prod_id = prod_id;
        reload();
      }

      function handleView(record: Recordable) {
        //浏览
        go('/productapp/productapp_detail/' + record.id);
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
