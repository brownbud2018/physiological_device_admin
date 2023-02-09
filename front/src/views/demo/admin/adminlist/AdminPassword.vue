<template>
  <PageWrapper title="修改管理员密码" content="修改成功后会自动生效！" @back="goBack">
    <div class="py-8 bg-white flex flex-col justify-center items-center">
      <BasicForm @register="register" />
      <div class="flex justify-center">
        <a-button @click="resetFields"> 重置 </a-button>
        <a-button class="!ml-4" type="primary" @click="handleSubmit"> 确认 </a-button>
      </div>
    </div>
  </PageWrapper>
</template>
<script lang="ts">
  import { defineComponent, ref } from 'vue';
  import { PageWrapper } from '/@/components/Page';
  import { BasicForm, useForm } from '/@/components/Form';

  import { formSchema } from './pwd.data';
  import { useRoute } from 'vue-router';
  import { useTabs } from '../../../../hooks/web/useTabs';
  import { setAdminPwd } from '../../../../api/demo/admin';
  import { useMessage } from '../../../../hooks/web/useMessage';
  import { useGo } from '../../../../hooks/web/usePage';
  export default defineComponent({
    name: 'AdminPassword',
    components: { BasicForm, PageWrapper },
    setup() {
      const { setTitle } = useTabs();
      const route = useRoute();
      const go = useGo();
      // 此处可以得到用户ID
      const userId = ref(route.params?.id);
      setTitle('管理员改密码' + userId.value);
      const [register, { validate, resetFields }] = useForm({
        size: 'large',
        labelWidth: 100,
        showActionButtonGroup: false,
        schemas: formSchema,
      });

      async function handleSubmit() {
        try {
          const values = await validate();
          const { passwordNew } = values;

          // TODO custom api
          const { createMessage } = useMessage();
          const dataChangePwd = await setAdminPwd(Number(userId.value), passwordNew)
            .then((res) => {
              //console.log('res:' + res);
              createMessage.success('更新密码成功');
            })
            .catch(() => {
              createMessage.error('更新密码失败');
            });
          // const { router } = useRouter();
          // router.push(pageEnum.BASE_LOGIN);
        } catch (error) {}
      }

      // 页面左侧点击返回链接时的操作
      function goBack() {
        // 本例的效果时点击返回始终跳转到账号列表页，实际应用时可返回上一页
        go('/admin/adminlist');
      }
      return { register, resetFields, userId, goBack, handleSubmit };
    },
  });
</script>
