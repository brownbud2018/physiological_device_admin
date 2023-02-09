<template>
  <List item-layout="vertical" :class="prefixCls">
    <ListItem>
      <ListItemMeta>
        <template #description>
          <template v-for="item in listData" :key="item.title">
            <template v-if="item.reply_type == 1">
            <div :class="`${prefixCls}__content`">
              <div class="flex items-center">
                <span class="mr-2 text-primary font-medium">
                  {{ item.username }}
                  <span>（{{ timestampToDate1(item.time) }}）</span>
                  :
                </span>
              </div>
              {{ item.content }}
            </div>
            </template>
            <template v-else>
            <div :class="`${prefixCls}__content`" style="text-align: right">
              <span class="mr-2 text-primary font-medium">
                {{ item.professor_name }}
                <span>（{{ timestampToDate1(item.time) }}）</span>
                :
              </span>
              <br />
              {{ item.content }}
            </div>
            </template>
          </template>
        </template>
      </ListItemMeta>
    </ListItem>
  </List>
  <div class="`${prefixCls}-bottom`">
      <template v-if="getIsOpen == false">
        <span style="color: red;">
          咨询状态:{{ close_type }}
        </span>
      </template>
      <textarea placeholder="请输入回复内容" v-model="contenttext" :disabled="!getIsOpen" style="resize: none; width: 100%; height: 100px" />
      <a-button type="primary" block class="mt-4" :disabled="!getIsOpen" @click="handlerSend(contenttext)"> 回复 </a-button>
  </div>
</template>
<script lang="ts">
  import { defineComponent, ref } from "vue";
  import { List, Input } from 'ant-design-vue';
  import { actions } from "./data";
  import { timestampToDate1 } from '/@/utils/dateUtil';
  import { useRoute } from 'vue-router';
  import {
    getUserconsultingDetail,
    getUserconsultingUser,
    updateUserconsultinglog
  } from "/@/api/demo/userconsulting";
  import { useTabs } from '/@/hooks/web/useTabs';
  import { getNewUserInfo } from '/@/api/sys/user';
  import { useMessage } from '/@/hooks/web/useMessage';

  interface listconsulting {
    title: string,
    description: string,
    content: string,
    reply_type: string,
    time: string,
    username: string,
    professor_name: string,
  }
  export default defineComponent({
    components: {
      List,
      ListItem: List.Item,
      ListItemMeta: List.Item.Meta,
      [Input.name]: Input,
      InputTextArea: Input.TextArea,
    },
    setup() {

      const listData = ref<listconsulting[]>([]);
      const route = useRoute();
      const getIsOpen = ref(true);
      const close_type = ref('未关闭');
      let mainid = parseInt(<string>ref(route.params?.id).value);
      let user_id = 0;
      let username = '';
      let contenttext = ref('');
      const { setTitle } = useTabs();
      let userPromisethis = new Promise((resolve) => {
        let userdeviceInfo = {};
        let vistitDeviceData = {};
        const data1 = getUserconsultingDetail(mainid)
          .then((res) => {
            vistitDeviceData = res['data'];
            for (const key in vistitDeviceData) {
              type KeyType = keyof typeof vistitDeviceData;
              const initialValue = vistitDeviceData[key as KeyType];
              username = initialValue['username'];
              user_id = initialValue['userid'];
              //console.log(user_id);
              setTitle('咨询详情：' + username);
              listData.value.push ({
                title: initialValue['username'],
                description: initialValue['content'],
                content: initialValue['content'],
                reply_type: initialValue['reply_type'],
                time: initialValue['add_time'],
                username: initialValue['username'],
                professor_name: initialValue['professor_name'],
              });
              if(parseInt(initialValue['close_type']) > 0){
                getIsOpen.value = false;
                if (parseInt(initialValue['close_type']) == 1){
                  close_type.value = '医生关闭';
                }
                if (parseInt(initialValue['close_type']) == 2){
                  close_type.value = '用户关闭';
                }
                if (parseInt(initialValue['close_type']) == 3){
                  close_type.value = '超过24小时自动关闭';
                }
                if (parseInt(initialValue['close_type']) == 4){
                  close_type.value = '20次回复后自动关闭';
                }
              }
            }
            return listData.value;
          })
          .catch(() => {
            console.log('查询咨询详情列表失败');
          });
        resolve(data1);
      });
      let userList = {};
      const userInfos = getNewUserInfo()
        .then((res) => {
          userList = res.data;
          return res.data;
        })
        .catch(() => {
          console.log('查询管理员详情失败');
        });

      function handlerSend(content) {
        const { createMessage } = useMessage();
        if (
          content.trim() === null ||
          content.trim() === '' ||
          content.trim() === undefined ||
          content.trim().length === 0
        ) {
          createMessage.error('没有输入内容');
          //console.log('没有输入内容');
        } else {
          try {
            if (user_id != 0){
              //把image的值，从数组，转成字符串，唉
              const datachange = {};
              datachange['id'] = 0;
              datachange['consulting_id'] = mainid;
              datachange['reply_type'] = 2;
              datachange['reply_uid'] = userList.professor_id;
              datachange['content_type'] = 'text';
              datachange['content'] = content;
              const dataUpdate = updateUserconsultinglog(datachange, 'none');
            }
          } catch(e) {
            createMessage.error('回复失败:' + e);
            //console.log('修改咨询详情子表失败e', e);
          }
          setTimeout(function(){
            location.reload();
          }, 1000);
        }
      }
      return {
        prefixCls: 'account-center-article',
        listData,
        username,
        timestampToDate1,
        actions,
        contenttext,
        getIsOpen,
        close_type,
        handlerSend,
      };
    },
  });
</script>
<style lang="less" scoped>
  .account-center-article {
    &__title {
      margin-bottom: 12px;
      font-size: 18px;
    }

    &__content {
      color: rgb(0 0 0 / 65%);
    }

    &__action {
      display: inline-block;
      padding: 0 16px;
      color: rgb(0 0 0 / 45%);

      &:nth-child(1),
      &:nth-child(2) {
        border-right: 1px solid rgb(206 206 206 / 40%);
      }

      &-icon {
        margin-right: 3px;
      }
    }

    &__time {
      position: absolute;
      right: 20px;
      color: rgb(0 0 0 / 45%);
    }
  }
</style>
