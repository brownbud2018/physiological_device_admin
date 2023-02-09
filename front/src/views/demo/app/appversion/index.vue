<template>
  <PageWrapper dense contentFullHeight contentClass="flex">
    <AppTree class="w-1/4 xl:w-1/5" @select="handleSelect" />
    <BasicTable @register="registerTable" class="w-3/4 xl:w-4/5" :searchInfo="searchInfo">
      <template #toolbar>
        <a-button type="primary" @click="handleCreate">新增app版本</a-button>
      </template>
      <template #action="{ record }">
        <TableAction
          :actions="[
            {
              icon: 'ant-design:download',
              tooltip: '下载app版本文件',
              onClick: handleDownload.bind(null, record),
            },
            {
              icon: 'clarity:note-edit-line',
              tooltip: '编辑app版本',
              onClick: handleEdit.bind(null, record),
            },
            {
              icon: 'ant-design:delete-outlined',
              color: 'error',
              tooltip: '删除此app版本',
              popConfirm: {
                title: '是否确认删除',
                confirm: handleDelete.bind(null, record),
              },
            },
          ]"
        />
      </template>
    </BasicTable>
    <AppversionModal @register="registerModal" @success="handleSuccess" />
  </PageWrapper>
</template>
<script lang="ts">
  import { defineComponent, reactive } from 'vue';

  import { BasicTable, useTable, TableAction } from '/@/components/Table';
  import { delAppversionType, getAppversionList } from '/@/api/demo/appversion';
  import { PageWrapper } from '/@/components/Page';
  import AppTree from './AppTree.vue';

  import { useModal } from '/@/components/Modal';
  import { useMessage } from '../../../../hooks/web/useMessage';
  import AppversionModal from './AppversionModal.vue';

  import { columns, searchFormSchema } from './appversion.data';
  import { useGo } from '/@/hooks/web/usePage';

  export default defineComponent({
    name: 'AppversionManagement',
    components: { BasicTable, PageWrapper, AppTree, AppversionModal, TableAction },
    setup() {
      const go = useGo();
      const [registerModal, { openModal }] = useModal();
      const searchInfo = reactive<Recordable>({});
      const [registerTable, { reload }] = useTable({
        title: 'app版本列表',
        api: getAppversionList,
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
        delAppversionType(record.id)
          .then((res) => {
            //console.log('res:' + res);
            createMessage.success('已成功删除app版本');
          })
          .catch(() => {
            createMessage.error('删除app版本失败');
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

      function handleSelect(app_pro_id = '') {
        //左侧选择app钩子
        searchInfo.app_pro_id = app_pro_id;
        reload();
      }

      function handleView(record: Recordable) {
        //浏览
        go('/app/appversion_detail/' + record.id);
      }

      function getfile(url: string) {
        return import.meta.env.VITE_GLOB_API_URL_SIMPLE + '/' + url;
      }

      function handleDownload(record: Recordable) {
        //下载
        const url = getfile(record.app_v_file);
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
        handleView,
        getfile,
        handleDownload,
        searchInfo,
      };
    },
  });
</script>
