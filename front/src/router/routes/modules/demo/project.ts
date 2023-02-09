import type { AppRouteModule } from '/@/router/types';

import { LAYOUT } from '/@/router/constant';
import { t } from '/@/hooks/web/useI18n';

const project: AppRouteModule = {
  path: '/project',
  name: 'project',
  component: LAYOUT,
  redirect: '/project/projectlist',
  meta: {
    orderNo: 11,
    icon: 'ion:tv-outline',
    title: t('routes.demo.project.projectName'),
  },
  children: [
    {
      path: 'projectlist',
      name: 'ProjectManagement',
      meta: {
        title: t('routes.demo.project.projectlist'),
        ignoreKeepAlive: false,
      },
      component: () => import('/@/views/demo/project/projectlist/index.vue'),
    },
    {
      path: 'product',
      name: 'ProductManagement',
      meta: {
        title: t('routes.demo.project.product'),
        ignoreKeepAlive: true,
      },
      component: () => import('/@/views/demo/project/product/index.vue'),
    },
    {
      path: 'product_detail/:id',
      name: 'ProductDetail',
      meta: {
        hideMenu: true,
        title: t('routes.demo.project.product_detail'),
        ignoreKeepAlive: true,
        showMenu: false,
        currentActiveMenu: '/project/product',
      },
      component: () => import('/@/views/demo/project/product/ProductDetail.vue'),
    },
    {
      path: 'device',
      name: 'DeviceManagement',
      meta: {
        title: t('routes.demo.project.device'),
        ignoreKeepAlive: true,
      },
      component: () => import('/@/views/demo/project/device/index.vue'),
    },
    {
      path: 'device_detail/:id',
      name: 'DeviceDetail',
      meta: {
        hideMenu: true,
        title: t('routes.demo.project.device_detail'),
        ignoreKeepAlive: true,
        showMenu: false,
        currentActiveMenu: '/project/device',
      },
      component: () => import('/@/views/demo/project/device/DeviceDetail.vue'),
    },
    {
      path: 'device_password/:id',
      name: 'DevicePassword',
      meta: {
        hideMenu: true,
        title: t('routes.demo.project.device_password'),
        ignoreKeepAlive: true,
        showMenu: false,
        currentActiveMenu: '/project/device',
      },
      component: () => import('/@/views/demo/project/device/DevicePassword.vue'),
    },
    {
      path: 'productloglist',
      name: 'ProductloglistManagement',
      meta: {
        title: t('routes.demo.productlog.productloglist'),
        ignoreKeepAlive: false,
      },
      component: () => import('/@/views/demo/project/productloglist/index.vue'),
    },
    {
      path: 'productstatisticslist',
      name: 'ProductapplistManagement',
      meta: {
        title: t('routes.demo.productstatistics.productstatisticslist'),
        ignoreKeepAlive: false,
      },
      component: () => import('/@/views/demo/project/productstatisticslist/index.vue'),
    },
    {
      path: 'exceluploadlist',
      name: 'ExceluploadlistManagement',
      meta: {
        title: t('routes.demo.excelupload.exceluploadName'),
        ignoreKeepAlive: false,
      },
      component: () => import('/@/views/demo/project/exceluploadlist/index.vue'),
    },
    {
      path: 'excelupload_detail/:id',
      name: 'ExceluploadDetail',
      meta: {
        hideMenu: true,
        title: t('routes.demo.excelupload.excelupload_detail'),
        ignoreKeepAlive: true,
        showMenu: false,
        currentActiveMenu: '/project/exceluploadlist',
      },
      component: () => import('/@/views/demo/project/exceluploadlist/ExceluploadDetail.vue'),
    },
  ],
};

export default project;
