import type { AppRouteModule } from '/@/router/types';

import { LAYOUT } from '/@/router/constant';
import { t } from '/@/hooks/web/useI18n';

const admin: AppRouteModule = {
  path: '/admin',
  name: 'admin',
  component: LAYOUT,
  meta: {
    orderNo: 99,
    icon: 'ion:tv-outline',
    title: t('routes.demo.system.moduleName'),
  },
  children: [
    {
      path: 'role',
      name: 'RoleManagement',
      meta: {
        title: t('routes.demo.system.role'),
        ignoreKeepAlive: true,
      },
      component: () => import('/@/views/demo/admin/role/index.vue'),
    },
    {
      path: 'adminlist',
      name: 'AdminlistManagement',
      meta: {
        title: t('routes.demo.system.account'),
        ignoreKeepAlive: false,
      },
      component: () => import('/@/views/demo/admin/adminlist/index.vue'),
    },
    {
      path: 'admin_detail/:id',
      name: 'AdminDetail',
      meta: {
        hideMenu: true,
        title: t('routes.demo.system.account_detail'),
        ignoreKeepAlive: true,
        showMenu: false,
        currentActiveMenu: '/admin/adminlist',
      },
      component: () => import('/@/views/demo/admin/adminlist/AdminDetail.vue'),
    },
    {
      path: 'admin_password/:id',
      name: 'AdminPassword',
      meta: {
        hideMenu: true,
        title: t('routes.demo.system.account_password'),
        ignoreKeepAlive: true,
        showMenu: false,
        currentActiveMenu: '/admin/adminlist',
      },
      component: () => import('/@/views/demo/admin/adminlist/AdminPassword.vue'),
    },
    {
      path: 'access',
      name: 'AccessManagement',
      meta: {
        title: t('routes.demo.system.access'),
        ignoreKeepAlive: true,
      },
      component: () => import('/@/views/demo/admin/access/index.vue'),
    },
  ],
};

export default admin;
