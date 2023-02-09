import type { AppRouteModule } from '/@/router/types';

import { LAYOUT } from '/@/router/constant';
import { t } from '/@/hooks/web/useI18n';

const apppro: AppRouteModule = {
  path: '/auth',
  name: 'auth',
  component: LAYOUT,
  redirect: '/auth/authclass',
  meta: {
    orderNo: 15,
    icon: 'ant-design:apartment-outlined',
    title: t('routes.demo.auth.authName'),
  },
  children: [
    {
      path: 'authclass',
      name: 'AuthclassManagement',
      meta: {
        title: t('routes.demo.auth.authclasslist'),
        ignoreKeepAlive: true,
      },
      component: () => import('/@/views/demo/auth/authclass/index.vue'),
    },
    {
      path: 'authclass_detail/:id',
      name: 'AuthclassDetail',
      meta: {
        hideMenu: true,
        title: t('routes.demo.auth.authclass_detail'),
        ignoreKeepAlive: true,
        showMenu: false,
        currentActiveMenu: '/auth/authclass_detail',
      },
      component: () => import('/@/views/demo/auth/authclass/AuthclassDetail.vue'),
    },
    {
      path: 'authdetail',
      name: 'AuthdetailManagement',
      meta: {
        title: t('routes.demo.auth.authdetaillist'),
        ignoreKeepAlive: true,
      },
      component: () => import('/@/views/demo/auth/authdetail/index.vue'),
    },
    {
      path: 'authabout',
      name: 'AuthaboutManagement',
      meta: {
        title: t('routes.demo.auth.authabout'),
        ignoreKeepAlive: true,
      },
      component: () => import('/@/views/demo/auth/authabout/index.vue'),
    },
    {
      path: 'productauth',
      name: 'ProductauthManagement',
      meta: {
        title: t('routes.demo.auth.authproductauth'),
        ignoreKeepAlive: true,
      },
      component: () => import('/@/views/demo/auth/productauth/index.vue'),
    },
    {
      path: 'adminauth',
      name: 'AdminauthManagement',
      meta: {
        title: t('routes.demo.system.adminauth'),
        ignoreKeepAlive: true,
      },
      component: () => import('/@/views/demo/admin/adminauth/index.vue'),
    },
  ],
};

export default apppro;
