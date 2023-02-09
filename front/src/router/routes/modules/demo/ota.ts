import type { AppRouteModule } from '/@/router/types';

import { LAYOUT } from '/@/router/constant';
import { t } from '/@/hooks/web/useI18n';

const apppro: AppRouteModule = {
  path: '/ota',
  name: 'ota',
  component: LAYOUT,
  redirect: '/ota/otamain',
  meta: {
    orderNo: 14,
    icon: 'ant-design:cloud-filled',
    title: t('routes.demo.ota.otaName'),
  },
  children: [
    {
      path: 'otamain',
      name: 'OTAmainManagement',
      meta: {
        title: t('routes.demo.ota.otamainlist'),
        ignoreKeepAlive: true,
      },
      component: () => import('/@/views/demo/ota/otamain/index.vue'),
    },
    {
      path: 'otamain_detail/:id',
      name: 'OtamainDetail',
      meta: {
        hideMenu: true,
        title: t('routes.demo.ota.otamain_detail'),
        ignoreKeepAlive: true,
        showMenu: false,
        currentActiveMenu: '/ota/otamain',
      },
      component: () => import('/@/views/demo/ota/otamain/OtamainDetail.vue'),
    },
    {
      path: 'otaversion',
      name: 'OTAversionManagement',
      meta: {
        title: t('routes.demo.ota.otaversion'),
        ignoreKeepAlive: true,
      },
      component: () => import('/@/views/demo/ota/otaversion/index.vue'),
    },
    {
      path: 'productota',
      name: 'ProductotaManagement',
      meta: {
        title: t('routes.demo.ota.productota'),
        ignoreKeepAlive: true,
      },
      component: () => import('/@/views/demo/ota/productota/index.vue'),
    },
  ],
};

export default apppro;
