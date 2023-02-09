<template>
  <img :src="getimg('')" :width="getwidth()" alt="" />
</template>
<script lang="ts">
  import { defineComponent } from 'vue';
  import { propTypes } from '/@/utils/propTypes';

  export default defineComponent({
    name: 'Httpimg',
    //components: { SvgImg },
    props: {
      // img name
      src: propTypes.string,
      // img width
      imgwidth: propTypes.string,
    },
    setup(props) {
      function getimg(url: string) {
        if (props.src != '') {
          return props.src;
        } else {
          return url;
        }
      }

      function getwidth() {
        if (props.imgwidth != '') {
          return props.imgwidth;
        } else {
          return '10';
        }
      }

      return { getimg, getwidth };
    },
  });
</script>
