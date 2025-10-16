<template>
    <div class="home" data-aos="zoom-out">
      <MyNotifi/>
      <h1>Добро</h1>
    </div>
  
</template>

<script setup>

import MyNotifi from '@/components/Notyfi/MyNotifi.vue';
</script>

<style scoped>
.main {
  padding: 2rem;
  background: var(--color-bg-subtle);
  min-height: calc(100vh - 64px);
}
</style>
