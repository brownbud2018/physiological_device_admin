import type { AppRouteRecordRaw, Menu } from '/@/router/types';

import { defineStore } from 'pinia';
import { store } from '/@/store';
import { useI18n } from '/@/hooks/web/useI18n';
import { useUserStore } from './user';
import { useAppStoreWithOut } from './app';
import { toRaw } from 'vue';
import { transformObjToRoute, flatMultiLevelRoutes } from '/@/router/helper/routeHelper';
import { transformRouteToMenu } from '/@/router/helper/menuHelper';

import projectSetting from '/@/settings/projectSetting';

import { PermissionModeEnum } from '/@/enums/appEnum';

import { asyncRoutes } from '/@/router/routes';
import { ERROR_LOG_ROUTE, PAGE_NOT_FOUND_ROUTE } from '/@/router/routes/basic';

import { filter } from '/@/utils/helper/treeHelper';

import { getMenuList } from '/@/api/sys/menu';
import { getNewUserInfo, getPermCode } from '/@/api/sys/user';

import { useMessage } from '/@/hooks/web/useMessage';
import { PageEnum } from '/@/enums/pageEnum';
import { isArray } from '/@/utils/is';
import { RoleEnum } from '/@/enums/roleEnum';
import { AppRouteModule } from '/@/router/types';

interface PermissionState {
  // Permission code list
  permCodeList: string[] | number[];
  // Whether the route has been dynamically added
  isDynamicAddedRoute: boolean;
  // To trigger a menu update
  lastBuildMenuTime: number;
  // Backstage menu list
  backMenuList: Menu[];
  frontMenuList: Menu[];
}
export const usePermissionStore = defineStore({
  id: 'app-permission',
  state: (): PermissionState => ({
    permCodeList: [],
    // Whether the route has been dynamically added
    isDynamicAddedRoute: false,
    // To trigger a menu update
    lastBuildMenuTime: 0,
    // Backstage menu list
    backMenuList: [],
    // menu List
    frontMenuList: [],
  }),
  getters: {
    getPermCodeList(): string[] | number[] {
      return this.permCodeList;
    },
    getBackMenuList(): Menu[] {
      return this.backMenuList;
    },
    getFrontMenuList(): Menu[] {
      return this.frontMenuList;
    },
    getLastBuildMenuTime(): number {
      return this.lastBuildMenuTime;
    },
    getIsDynamicAddedRoute(): boolean {
      return this.isDynamicAddedRoute;
    },
  },
  actions: {
    setPermCodeList(codeList: string[]) {
      this.permCodeList = codeList;
    },

    setBackMenuList(list: Menu[]) {
      this.backMenuList = list;
      list?.length > 0 && this.setLastBuildMenuTime();
    },

    setFrontMenuList(list: Menu[]) {
      this.frontMenuList = list;
    },

    setLastBuildMenuTime() {
      this.lastBuildMenuTime = new Date().getTime();
    },

    setDynamicAddedRoute(added: boolean) {
      this.isDynamicAddedRoute = added;
    },
    resetState(): void {
      this.isDynamicAddedRoute = false;
      this.permCodeList = [];
      this.backMenuList = [];
      this.lastBuildMenuTime = 0;
    },
    async changePermissionCode() {
      const codeList = await getPermCode();
      this.setPermCodeList(codeList);
    },
    async buildRoutesAction(): Promise<AppRouteRecordRaw[]> {
      const { t } = useI18n();
      const userStore = useUserStore();
      const appStore = useAppStoreWithOut();

      let routes: AppRouteRecordRaw[] = [];
      const roleList = toRaw(userStore.getRoleList) || [];
      const { permissionMode = projectSetting.permissionMode } = appStore.getProjectConfig;

      const routeFilter = (route: AppRouteRecordRaw) => {
        const { meta } = route;
        const { roles } = meta || {};
        if (!roles) return true;
        return roleList.some((role) => roles.includes(role));
      };

      const routeRemoveIgnoreFilter = (route: AppRouteRecordRaw) => {
        const { meta } = route;
        const { ignoreRoute } = meta || {};
        return !ignoreRoute;
      };

      /**
       * @description 根据设置的首页path，修正routes中的affix标记（固定首页）
       * */
      const patchHomeAffix = (routes: AppRouteRecordRaw[]) => {
        if (!routes || routes.length === 0) return;
        let homePath: string = userStore.getUserInfo.homePath || PageEnum.BASE_HOME;
        function patcher(routes: AppRouteRecordRaw[], parentPath = '') {
          if (parentPath) parentPath = parentPath + '/';
          routes.forEach((route: AppRouteRecordRaw) => {
            const { path, children, redirect } = route;
            const currentPath = path.startsWith('/') ? path : parentPath + path;
            if (currentPath === homePath) {
              if (redirect) {
                homePath = route.redirect! as string;
              } else {
                route.meta = Object.assign({}, route.meta, { affix: true });
                throw new Error('end');
              }
            }
            children && children.length > 0 && patcher(children, currentPath);
          });
        }
        try {
          patcher(routes);
        } catch (e) {
          // 已处理完毕跳出循环
        }
        return;
      };

      switch (permissionMode) {
        case PermissionModeEnum.ROLE:
          routes = filter(asyncRoutes, routeFilter);
          routes = routes.filter(routeFilter);
          // Convert multi-level routing to level 2 routing
          routes = flatMultiLevelRoutes(routes);
          break;

        case PermissionModeEnum.ROUTE_MAPPING:
          //let scores : string[] = ['PageNotFound', 'Dashboard', 'About'];
          let boolin = false;
          const userInfo = await getNewUserInfo();
          const data = userInfo.data;
          const back_user_type = data.user_type;
          const roles = data.roles;
          let myRouteModuleList: AppRouteModule[] = [];
          myRouteModuleList = getMenu(roles);
          //console.log('myRouteModuleList', myRouteModuleList);
          //const myAsyncRoutes = [PAGE_NOT_FOUND_ROUTE, ...myRouteModuleList];
          //console.log('asyncRoutes', asyncRoutes);
          routes = filter(asyncRoutes, routeFilter);
          //console.log('asyncRoutes', routes);
          if (back_user_type == true) {
            //超级管理员
          } else {
            routes = checkMenu(routes, roles);
          }
          //console.log('routes', routes);
          routes = routes.filter(routeFilter);
          const menuList = transformRouteToMenu(routes, true);
          routes = filter(routes, routeRemoveIgnoreFilter);
          routes = routes.filter(routeRemoveIgnoreFilter);
          menuList.sort((a, b) => {
            return (a.meta?.orderNo || 0) - (b.meta?.orderNo || 0);
          });

          //console.log('menuList', menuList);
          this.setFrontMenuList(menuList);
          // Convert multi-level routing to level 2 routing
          routes = flatMultiLevelRoutes(routes);
          //console.log('routes', routes);
          break;

        //  If you are sure that you do not need to do background dynamic permissions, please comment the entire judgment below
        case PermissionModeEnum.BACK:
          const { createMessage } = useMessage();

          createMessage.loading({
            content: t('sys.app.menuLoading'),
            duration: 1,
          });

          // !Simulate to obtain permission codes from the background,
          // this function may only need to be executed once, and the actual project can be put at the right time by itself
          let routeList: AppRouteRecordRaw[] = [];
          try {
            this.changePermissionCode();
            routeList = (await getMenuList()) as AppRouteRecordRaw[];
          } catch (error) {
            console.error(error);
          }

          // Dynamically introduce components
          routeList = transformObjToRoute(routeList);

          //  Background routing to menu structure
          const backMenuList = transformRouteToMenu(routeList);
          this.setBackMenuList(backMenuList);

          // remove meta.ignoreRoute item
          routeList = filter(routeList, routeRemoveIgnoreFilter);
          routeList = routeList.filter(routeRemoveIgnoreFilter);

          routeList = flatMultiLevelRoutes(routeList);
          routes = [PAGE_NOT_FOUND_ROUTE, ...routeList];
          break;
      }

      routes.push(ERROR_LOG_ROUTE);
      patchHomeAffix(routes);
      //console.log('routesEND：：：：', routes);
      return routes;
    },
  },
});

// Need to be used outside the setup
export function usePermissionStoreWithOut() {
  return usePermissionStore(store);
}

// Need to be used outside the setup
export function getMenu(roles) {
  //const myRouteModuleList: AppRouteModule[] = [];
  const returnmenu = [];
  let newRoute = {};
  let newmeta = {};
  let childrendata = [];
  let children = [];
  for (let i = 0; i < roles.length; i++) {
    childrendata = [];
    children = [];
    childrendata = roles[i].children;
    if (childrendata != undefined && childrendata.length > 0) {
      //console.log('childrendata', childrendata);
      children = getMenu(childrendata);
      // @ts-ignore
      //children.push(getchildren);
    } else {
      children = undefined;
    }
    newmeta = {
      orderNo: roles[i].sort_order,
      icon: roles[i].menu_icon,
      title: roles[i].access_name,
    };
    newRoute = {
      name: roles[i].access_code,
      path: roles[i].access_path,
      redirect: roles[i].access_redirect,
      component: roles[i].access_component,
      meta: newmeta,
      children: children,
    };
    // @ts-ignore
    returnmenu.push(newRoute);
  }
  return returnmenu;
}
export function checkMenu(rolesall, rolesback) {
  let boolin = false;
  let boolchildin = false;
  //console.log('rolesall', rolesall);
  //console.log('rolesback', rolesback);
  for (let i = rolesall.length - 1; i >= 0; i--) {
    boolin = false;
    for (let j = rolesback.length - 1; j >= 0; j--) {
      if (rolesall[i].name == rolesback[j].access_code) {
        rolesall[i].meta.hideMenu = rolesback[j].is_menu != 1;
        rolesall[i].meta.icon = rolesback[j].menu_icon;
        rolesall[i].meta.title = rolesback[j].access_name;
        rolesall[i].meta.orderNo = rolesback[j].sort_order;
        boolin = true;
        let nowchildren = rolesall[i].children;
        for (let k = nowchildren.length - 1; k >= 0; k--) {
          boolchildin = false;
          for (let l = rolesback[j].children.length - 1; l >= 0; l--) {
            if (nowchildren[k].name == rolesback[j].children[l].access_code) {
              boolchildin = true;
              nowchildren[k].meta.hideMenu = rolesback[j].children[l].is_menu != 1;
              nowchildren[k].meta.icon = rolesback[j].children[l].menu_icon;
              nowchildren[k].meta.title = rolesback[j].children[l].access_name;
              nowchildren[k].meta.orderNo = rolesback[j].children[l].sort_order;
            }
          }
          if (boolchildin == false) {
            nowchildren.splice(k, 1);
          }
        }
      }
    }
    if (boolin == false) {
      // splice(N,M,[element1])意思是删除数组中：下标为N（3）开始计算的M（1）个元素，可选：使用element1元素替换掉删除的元素
      // routes.splice(3, 1);
      rolesall.splice(i, 1);
    }
  }
  return rolesall;
}
