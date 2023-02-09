<template>
  <div :class="prefixCls">
    <CollapseContainer :class="`${prefixCls}-top__team`" :title="`${userData.username}-${userData.questionname}:${userData.createtime}`" :canExpan="false">
      <template v-for="item in dataList" :key="item.key">
        <a-row>
          <a-col :class="`${prefixCls}-col`">
            <div :class="`${prefixCls}-top__team-item`">
              <Icon icon="emojione-monotone:letter-a" color="#7c51b8" />
              <span>
                {{ item.questioninfoname }}：
                <template v-if="item.type == 'S'">
                  {{ item.selectname }}
                </template>
                <template v-if="item.type == 'A'">
                  {{ item.answer }}
                </template>
              </span>
            </div>
          </a-col>
        </a-row>
      </template>
    </CollapseContainer>
  </div>
</template>
<script lang="ts">
  import { Row, Col } from 'ant-design-vue';
  import { defineComponent, PropType, reactive, ref, watch } from 'vue';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { getUserQuestionList2 } from '/@/api/demo/user';
  import { CollapseContainer } from '/@/components/Container/index';
  import Icon from '/@/components/Icon/index';
  //参数 数据类型配置
  interface DataProps {
    son: any;
    key: number;
  }
  export default defineComponent({
    name: 'QuestionShow',
    props: {
      data: {
        type: Object, //设置数据类型
        required: true, //是否必传
        // eslint-disable-next-line vue/require-valid-default-prop
        default: {},
      },
      width: {
        type: String as PropType<string>,
        default: '100%',
      },
      height: {
        type: String as PropType<string>,
        default: '350px',
      },
    },
    emits: ['nextStep'], //事件名称
    components: {
      CollapseContainer,
      Icon,
      [Row.name]: Row,
      [Col.name]: Col,
    },
    setup(props: any, context: any) {
      //  context子传递父的事件
      //需要展现到页面的变量
      const data2: DataProps = reactive({
        son: '子元素',
        key: 1,
        /**
         * 下一步点击
         */
        nextDown() {
          let index = data2.key++;
          context.emit('nextStep', index);
        },
      });

      const { createMessage } = useMessage();

      let dataList = ref(0);
      let userData = ref({});
      watch(
        () => props.data,
        () => {
          let user_id = props.data.user_id;
          let this_data_id = props.data.question_data_id;
          if (this_data_id === 0 || this_data_id != undefined || this_data_id === '') {
            const promisedata = new Promise((resolve) => {
              const data1 = getUserQuestionList2(this_data_id)
                .then((res) => {
                  userData.value['questionname'] = res.data[0].questionname;
                  userData.value['createtime'] = res.data[0].createtime;
                  userData.value['username'] = res.data[0].username;
                  dataList.value = res.data[0].child;
                  //console.log(dataList);
                })
                .catch(() => {
                  createMessage.error('查询用户问卷失败');
                });
              resolve(data1);
            });
          }
        },
      );
      return {
        dataList,
        userData,
        prefixCls: 'account-center',
      };
    },
  });
</script>
