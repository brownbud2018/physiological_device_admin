<template>
  <div>
    <BasicTable @register="registerTable">
      <template #toolbar>
        <a-button type="primary" @click="handleCreate"> 新增项目 </a-button>
      </template>
      <template #action="{ record }">
        <TableAction
          :actions="[
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
    <ProjectDrawer @register="registerDrawer" @success="handleSuccess" />
  </div>
</template>
<script lang="ts">
  import { defineComponent } from 'vue';

  import { BasicTable, useTable, TableAction } from '/@/components/Table';
  import { delProjectType, getProjectList } from '/@/api/demo/project';

  import { useDrawer } from '/@/components/Drawer';
  import ProjectDrawer from './ProjectDrawer.vue';

  import { columns, searchFormSchema } from './project.data';
  import { useMessage } from '../../../../hooks/web/useMessage';

  export default defineComponent({
    name: 'ProjectManagement',
    components: { BasicTable, ProjectDrawer, TableAction },
    setup() {
      const [registerDrawer, { openDrawer }] = useDrawer();
      const [registerTable, { reload }] = useTable({
        title: '项目列表',
        api: getProjectList,
        columns,
        formConfig: {
          labelWidth: 120,
          schemas: searchFormSchema,
        },
        useSearchForm: true,
        showTableSetting: false,
        bordered: true,
        showIndexColumn: false,
        actionColumn: {
          width: 80,
          title: '操作',
          dataIndex: 'action',
          slots: { customRender: 'action' },
          fixed: undefined,
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
        delProjectType(record.id)
          .then((res) => {
            //console.log('res:' + res);
            createMessage.success('已成功删除项目');
          })
          .catch(() => {
            createMessage.error('删除项目失败');
          });
        reload();
      }

      function handleSuccess() {
        reload();
      }

      return {
        registerTable,
        registerDrawer,
        handleCreate,
        handleEdit,
        handleSuccess,
        handleDelete,
      };
    },
  });
</script>
