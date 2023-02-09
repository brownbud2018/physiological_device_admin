<template>
  <PageWrapper dense contentFullHeight contentClass="flex">
    <ProductTree class="w-1/4 xl:w-1/5" @select="handleSelect" />
    <BasicTable @register="registerTable" class="w-3/4 xl:w-4/5" :searchInfo="searchInfo">
      <template #toolbar>
        <a-button type="primary" @click="handleCreate">新增用户</a-button>
        <a-button type="primary" @click="getSelectRowKeyList"> 导出Excel </a-button>
      </template>
      <template #action="{ record }">
        <TableAction
          :actions="[
            {
              icon: 'clarity:info-standard-line',
              tooltip: '查看用户详情',
              onClick: handleView.bind(null, record),
            },
            {
              icon: 'clarity:note-edit-line',
              tooltip: '编辑用户',
              onClick: handleEdit.bind(null, record),
            },
            {
              icon: 'ant-design:delete-outlined',
              color: 'error',
              tooltip: '删除此用户',
              popConfirm: {
                title: '是否确认删除',
                confirm: handleDelete.bind(null, record),
              },
            },
          ]"
        />
      </template>
    </BasicTable>
    <UserModal @register="registerModal" @success="handleSuccess" />
  </PageWrapper>
</template>
<script lang="ts">
  import { defineComponent, reactive } from 'vue';

  import { BasicTable, useTable, TableAction } from '/@/components/Table';
  import { delUserType, getUserList, outExcelUser } from '/@/api/demo/user';
  import { PageWrapper } from '/@/components/Page';
  import ProductTree from './ProductTree.vue';

  import { useModal } from '/@/components/Modal';
  import { useMessage } from '/@/hooks/web/useMessage';
  import UserModal from './UserModal.vue';

  import { columns, searchFormSchema } from './user.data';
  import { useGo } from '/@/hooks/web/usePage';
  import { UserIDParams } from '/@/api/demo/model/userModel';

  export const downloadFile = (url) => {
    const iframe = document.createElement('iframe');
    iframe.style.display = 'none'; // 防止影响页面
    iframe.style.height = String(0); // 防止影响页面
    iframe.src = url;
    document.body.appendChild(iframe); // 这一行必须，iframe挂在到dom树上才会发请求
    // 5分钟之后删除（onload方法对于下载链接不起作用）
    setTimeout(() => {
      iframe.remove();
    }, 30 * 1000);
  };
  export default defineComponent({
    name: 'UsermainManagement',
    components: { BasicTable, PageWrapper, ProductTree, UserModal, TableAction },
    setup() {
      const go = useGo();
      const [registerModal, { openModal }] = useModal();
      const searchInfo = reactive<Recordable>({});
      const [registerTable, { reload, getSelectRowKeys }] = useTable({
        title: 'user列表',
        api: getUserList,
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
        afterFetch(info) {
          return info;
        },
        rowSelection: {
          type: 'checkbox',
        },
        actionColumn: {
          width: 120,
          title: '操作',
          dataIndex: 'action',
          slots: { customRender: 'action' },
        },
      });
      const { createMessage } = useMessage();

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
        const { createMessage } = useMessage();
        delUserType(record.id)
          .then((res) => {
            createMessage.success('已成功删除用户');
          })
          .catch(() => {
            createMessage.error('删除用户失败');
          });
        //reload();
        location.reload();
      }

      function handleSuccess({ isUpdate, values }) {
        if (isUpdate) {
          // 演示不刷新表格直接更新内部数据。
          // 注意：updateTableDataRecord要求表格的rowKey属性为string并且存在于每一行的record的keys中
          //const result = updateTableDataRecord(values.id, values);
          reload();
        } else {
          reload();
        }
      }

      function handleSelect(productId = '') {
        //左侧选择项目钩子
        searchInfo.productId = productId;
        reload();
      }

      function handleView(record: Recordable) {
        //浏览
        go('/user/user_detail/' + record.id);
      }

      async function getSelectRowKeyList() {
        if (getSelectRowKeys().length > 0) {
          let str1: string = getSelectRowKeys().map(String).join(',');
          let idary: UserIDParams = { idstr: str1 };
          const dataOutExcel = await outExcelUser(idary, 'none')
            .then((res) => {
              for (let i = 0; i < res.data.length; i++) {
                const url = getfile(res.data[i]);
                downloadFile(url);
                /*window.open(url, '_self');
                setTimeout(() => {
                  createMessage.success('开始批量下载Excel');
                }, 1000);*/
              }
            })
            .catch(() => {
              createMessage.error('导出Excel失败');
            });
        } else {
          createMessage.error('至少选择一条记录');
        }
      }

      function getfile(url: string) {
        return import.meta.env.VITE_GLOB_API_URL_SIMPLE + '/' + url;
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
        getSelectRowKeyList,
      };
    },
  });
</script>
