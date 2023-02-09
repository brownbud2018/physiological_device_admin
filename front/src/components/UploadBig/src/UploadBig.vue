<template>
  <div>
    <template v-if="fileName">
      <input alt="文件地址" :value="fileName" style="width: 250px" disabled />
    </template>
    <template v-else>
      <input alt="文件地址" style="width: 250px" disabled />
    </template>
    <br />
    <br />
    <input type="file" v-show="true" @change="handleInputClick" />
    <div @click="handleUpload">
      <slot></slot>
    </div>
    <br />
    <a-button @click="handleStartUpload" :disabled="getIsSelectFile">
      <span>上传</span>
    </a-button>
  </div>
</template>
<script lang="ts">
  import { computed, defineComponent, ref, watch } from 'vue';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { isEmpty } from '/@/utils/is';
  import {
    delBigUploadFile,
    uploadBigFile,
    uploadBigMergeFile,
  } from '/@/components/UploadBig/src/useUploadBig';
  export default defineComponent({
    name: 'UploadBig',
    props: {
      value: {
        type: String,
        default: '',
      },
    },
    emits: ['change', 'update:value'],
    setup(props, { emit }) {
      const fileName = ref<string>('');
      const selectfileName = ref<string>('');
      let filesthis: FileList | null = null;

      const { createMessage } = useMessage();

      watch(
        () => props.value,
        (value = '') => {
          if (isEmpty(value)) {
            fileName.value = '';
          } else {
            if (value.indexOf('fakepath') != -1) {
              //fileName.value = '';
            } else {
              fileName.value = value;
            }
          }
        },
        { immediate: true },
      );

      async function upload(file: File) {
        const timestamp: number = Date.parse(new Date().toString());
        const filenamemerge = file.name;
        try {
          let blobSlice = File.prototype.slice;
          let currentChunk = 0; // 当前第几片
          const chunkSize = 6 * 1024 * 1024; // 每片的大小，这里是10M
          let chunks = Math.ceil(file.size / chunkSize); // 总片数
          for (let i = 0; i < chunks; i++) {
            currentChunk = i;
            let start = currentChunk * chunkSize;
            let end = start + chunkSize >= file.size ? file.size : start + chunkSize;
            let chunkFile = blobSlice.call(file, start, end);
            chunkFile.name = file.name;
            const formData = new FormData();
            formData.append('file', chunkFile); //文件【分片文件】
            formData.append('chunknumber', i.toString()); // 属于第几片
            formData.append('identifier', timestamp.toString()); //唯一标志符
            // TODO uploadBig api
            const dataUpload = await uploadBigFile(formData, 'none'); // 请求分片文件上传接口
            createMessage.success('分片上传：第' + i.toString() + '个分片上传成功');
          }
          const formMergeData = new FormData();
          formMergeData.append('identifier', timestamp.toString()); //唯一标志符
          formMergeData.append('filename', filenamemerge); // 文件名
          formMergeData.append('chunkstar', '0'); // 属于第几片
          // TODO Merge uploadBig api
          const dataUpload1 = await uploadBigMergeFile(formMergeData, 'none'); // 请求合并分片文件接口
          fileName.value = '';
          fileName.value = dataUpload1.data.filename;
          emit('update:value', fileName.value);
          emit('change', fileName.value);
          return createMessage.success('上传成功');
        } catch (e) {
          //出错就访问删除接口，删除掉已经上传的分片文件
          const formDelData = new FormData();
          formDelData.append('identifier', timestamp.toString()); //唯一标志符
          formDelData.append('chunkstar', '0'); // 第几片开始删除
          const dataUpload2 = await delBigUploadFile(formDelData, 'none');
          createMessage.warning('上传失败');
          throw e;
        }
      }

      /**
       * @description: 触发选择文件管理器
       */
      function handleInputClick(e: Event) {
        const files = e && (e.target as HTMLInputElement).files;
        filesthis = files;
        if (files) {
          selectfileName.value = files[0].name;
        }
      }

      /**
       * @description 手动请求上传服务
       * @author YXM
       */
      async function handleUpload() {
        //
      }

      // 点击开始上传
      async function handleStartUpload() {
        try {
          createMessage.warning('开始上传文件，请稍后');
          selectfileName.value = '';
          upload(filesthis[0]);
        } catch (e) {
          //isUploadingRef.value = false;
          throw e;
        }
      }

      const getIsSelectFile = computed(() => {
        return !(selectfileName.value.length > 0);
      });
      return {
        handleUpload,
        handleInputClick,
        handleStartUpload,
        fileName,
        getIsSelectFile,
      };
    },
  });
</script>
