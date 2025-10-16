<script setup>
import MainHead from './components/Header/MainHead.vue'
</script>

<template>
  <div class="app">
    <MainHead />
    <RouterView />
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  background-color: var(--color-bg);
}
</style>
