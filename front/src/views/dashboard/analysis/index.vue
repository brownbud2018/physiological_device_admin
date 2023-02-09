<template>
  <div class="p-4">
    <GrowCard :loading="loading" class="enter-y" />
    <ChinaMap class="!my-4 enter-y" :loading="loading" />
    <SiteAnalysis class="!my-4 enter-y" :loading="loading" />
    <SiteAnalysis1 class="!my-4 enter-y" :loading="loading" />
    <SiteAnalysis2 class="!my-4 enter-y" :loading="loading" />
    <!--<div class="md:flex enter-y">
      <VisitRadar class="md:w-1/3 w-full" :loading="loading" />
      <VisitSource class="md:w-1/3 !md:mx-4 !md:my-0 !my-4 w-full" :loading="loading" />
      <SalesProductPie class="md:w-1/3 w-full" :loading="loading" />
    </div>-->
  </div>
</template>
<script lang="ts" setup>
  import { ref } from 'vue';
  import GrowCard from './components/GrowCard.vue';
  import ChinaMap from './components/ChinaMap.vue';
  import SiteAnalysis from './components/SiteAnalysis.vue';
  import SiteAnalysis1 from './components/SiteAnalysis1.vue';
  import SiteAnalysis2 from './components/SiteAnalysis2.vue';
  //import VisitSource from './components/VisitSource.vue';
  //import VisitRadar from './components/VisitRadar.vue';
  //import SalesProductPie from './components/SalesProductPie.vue';

  const loading = ref(true);

  setTimeout(() => {
    loading.value = false;
  }, 1500);
</script>
