<template>
  <PageWrapper dense contentFullHeight contentClass="flex">
    <ProductTree class="w-1/4 xl:w-1/5" @select="handleSelect" />
    <BasicTable @register="registerTable" class="w-3/4 xl:w-4/5" :searchInfo="searchInfo">
      <template #action="{ record }">
        <TableAction
          :actions="[
            {
              icon: 'clarity:info-standard-line',
              tooltip: '查看设备关联授权详情',
              onClick: handleView.bind(null, record),
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
  import { getProductauthList } from '/@/api/demo/productauth';
  import { PageWrapper } from '/@/components/Page';
  import ProductTree from './ProductTree.vue';

  import { useModal } from '/@/components/Modal';

  import { columns, searchFormSchema } from './productauth.data';
  import { useGo } from '/@/hooks/web/usePage';

  export default defineComponent({
    name: 'ProductauthManagement',
    components: { BasicTable, PageWrapper, ProductTree, TableAction },
    setup() {
      const go = useGo();
      const [registerModal] = useModal();
      const searchInfo = reactive<Recordable>({});
      const [registerTable, { reload }] = useTable({
        title: '设备关联授权列表',
        api: getProductauthList,
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

      function handleSelect(prod_id = '') {
        //左侧选择设备钩子
        searchInfo.prod_id = prod_id;
        reload();
      }

      function handleView(record: Recordable) {
        //浏览
        go('/auth/authclass_detail/' + record.id);
      }

      return {
        registerTable,
        registerModal,
        handleSelect,
        handleView,
        searchInfo,
      };
    },
  });
</script>
