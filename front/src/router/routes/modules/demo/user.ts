import type { AppRouteModule } from '/@/router/types';

import { LAYOUT } from '/@/router/constant';
import { t } from '/@/hooks/web/useI18n';

const apppro: AppRouteModule = {
  path: '/user',
  name: 'user',
  component: LAYOUT,
  redirect: '/user/usermain',
  meta: {
    orderNo: 14,
    icon: 'ant-design:user-outlined',
    title: t('routes.demo.user.userName'),
  },
  children: [
    {
      path: 'usermain',
      name: 'UsermainManagement',
      meta: {
        title: t('routes.demo.user.userlist'),
        ignoreKeepAlive: true,
      },
      component: () => import('/@/views/demo/user/usermain/index.vue'),
    },
    {
      path: 'user_detail/:id',
      name: 'UserDetail',
      meta: {
        hideMenu: true,
        title: t('routes.demo.user.usermain_detail'),
        ignoreKeepAlive: true,
        showMenu: false,
        currentActiveMenu: '/user/usermain',
      },
      component: () => import('/@/views/demo/user/usermain/UserDetail.vue'),
    },
    {
      path: 'userconsulting',
      name: 'UserconsultingManagement',
      meta: {
        title: t('routes.demo.user.userconsultinglist'),
        ignoreKeepAlive: true,
      },
      component: () => import('/@/views/demo/user/userconsulting/index.vue'),
    },
    {
      path: 'userconsulting_detail/:id',
      name: 'UserconsultingDetail',
      meta: {
        hideMenu: true,
        title: t('routes.demo.user.userconsulting_detail'),
        ignoreKeepAlive: true,
        showMenu: false,
        currentActiveMenu: '/user/userconsulting',
      },
      component: () => import('/@/views/demo/user/userconsulting/UserconsultingDetail.vue'),
    },
    {
      path: 'professors',
      name: 'ProfessorsManagement',
      meta: {
        title: t('routes.demo.system.professors'),
        ignoreKeepAlive: true,
      },
      component: () => import('/@/views/demo/admin/professors/index.vue'),
    },
  ],
};

export default apppro;
