<script setup>
import MainHead from './components/Header/MainHead.vue'
</script>

<template>
  <div class="app">
    <MainHead />
    <div class="page-container">
      <RouterView />
    </div>
  </div>
</template>

<style>
/* УБРАТЬ SCOPED - стили будут глобальными */
.app {
  min-height: 100vh;
  background-color: var(--color-bg);
}

.page-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}
</style>
