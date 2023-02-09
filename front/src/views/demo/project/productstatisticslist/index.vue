<template>
  <PageWrapper dense contentFullHeight contentClass="flex">
    <ProductTree class="w-1/4 xl:w-1/5" @select="handleSelect" />
    <BasicTable @register="registerTable" class="w-3/4 xl:w-4/5" :searchInfo="searchInfo">
      <template #action="{ record }">
        <TableAction
          :actions="[
            {
              icon: 'ant-design:delete-outlined',
              color: 'error',
              tooltip: '删除此统计',
              popConfirm: {
                title: '是否确认删除',
                confirm: handleDelete.bind(null, record),
              },
            },
          ]"
        />
      </template>
    </BasicTable>
  </PageWrapper>
</template>
<script lang="ts">
  import { defineComponent, reactive } from 'vue';

  import { BasicTable, useTable, TableAction } from '/@/components/Table';
  import { delProductstatistics, getProductstatisticsList } from '/@/api/demo/productstatistics';
  import { PageWrapper } from '/@/components/Page';
  import ProductTree from './ProductTree.vue';

  import { useModal } from '/@/components/Modal';
  import { useMessage } from '../../../../hooks/web/useMessage';

  import { columns, searchFormSchema } from './productstatistics.data';

  export default defineComponent({
    name: 'ProductstatisticsManagement',
    components: { BasicTable, PageWrapper, ProductTree, TableAction },
    setup() {
      const [registerModal, { openModal }] = useModal();
      const searchInfo = reactive<Recordable>({});
      const [registerTable, { reload, updateTableDataRecord }] = useTable({
        title: '关联列表',
        api: getProductstatisticsList,
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
        delProductstatistics(record.id)
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
