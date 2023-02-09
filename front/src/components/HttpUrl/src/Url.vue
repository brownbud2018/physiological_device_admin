<template>
  <a :href="geturl('')" :alt="getalt()">{{ getatext() }}</a>
</template>
<script lang="ts">
  import { defineComponent } from 'vue';
  import { propTypes } from '/@/utils/propTypes';

  export default defineComponent({
    name: 'HttpUrl',
    props: {
      // a url
      src: propTypes.string,
      // a text
      atext: propTypes.string,
      // a alt
      alttext: propTypes.string,
    },
    setup(props) {
      function geturl(url: string) {
        if (props.src != '') {
          return props.src;
        } else {
          return url;
        }
      }

      function getatext() {
        if (props.atext != '') {
          return props.atext;
        } else {
          return '';
        }
      }

      function getalt() {
        if (props.alttext != '') {
          return props.alttext;
        } else {
          return '';
        }
      }

      return { geturl, getalt, getatext };
    },
  });
</script>
