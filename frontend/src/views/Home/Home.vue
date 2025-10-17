<template>
  <div class="home" data-aos="zoom-out">
    <CardKarusel />
  </div>
</template>

<script setup>
import CardKarusel from '@/components/CardKarusel/CardKarusel.vue'
import MyNotifi from '@/components/Notyfi/MyNotifi.vue'
</script>

<style scoped>
.main {
  padding: 2rem;
  background: var(--color-bg-subtle);
  min-height: calc(100vh - 64px);
}
</style>
