<template>
  <PageWrapper title="病历图片">
    <ImagePreview :imageList="imgList" />
    <p>上传时间：{{ curData.createtime }}</p>
    <p>检测项目：{{ curData.recordname }}</p>
    <p>说明：{{ curData.descr }}</p>
  </PageWrapper>
</template>
<script lang="ts">
  import { defineComponent, PropType, reactive, ref, watch } from 'vue';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { getUserMedicalRecordList2 } from '/@/api/demo/user';
  import { useRoute } from 'vue-router'; //
  import { ImagePreview } from '/@/components/Preview/index';
  import { PageWrapper } from '/@/components/Page';
  //参数 数据类型配置
  interface DataProps {
    son: any;
    key: number;
  }
  export default defineComponent({
    name: 'MedicalRecord1',
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
    components: { PageWrapper, ImagePreview },
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

      const route = useRoute();
      const userId = ref(route.params?.id);
      const { createMessage } = useMessage();

      let url = '';
      let imgList = ref([]);
      let curData = ref(0);
      watch(
        () => props.data,
        (newValue, oldValue) => {
          let user_id = props.data.user_id;
          let this_data_id = props.data.med_data_id;
          if (this_data_id === 0 || this_data_id != undefined || this_data_id === '') {
            const promisedata = new Promise((resolve) => {
              const data1 = getUserMedicalRecordList2(this_data_id)
                .then((res) => {
                  url = res.data.url;
                  //console.log(url);
                  curData.value = res.data;
                  imgList.value = [];
                  if (url === 0 || url === undefined || url === '') {
                    imgList.value.push('/resource/img/nodata.png');
                  } else {
                    let data = url.split(',');
                    let i = 0;
                    for (i = 0; i < data.length; i++) {
                      imgList.value.push('https://pic.luckystar.com.cn/' + data[i] + '.jpg');
                    }
                  }
                })
                .catch(() => {
                  createMessage.error('查询用户病历失败');
                });
              resolve(data1);
            });
          }
        },
      );
      return {
        imgList,
        curData,
      };
    },
  });
</script>
