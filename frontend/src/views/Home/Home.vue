<template>
  <div class="home" data-aos="zoom-out">
    <CardKarusel />
  </div>
</template>

<script setup>
import CardKarusel from '@/components/CardKarusel/CardKarusel.vue'
import { onMounted } from 'vue'
import { useApiGet } from '@/utils/api/useApiGet'
import { apiUsersMe } from '@/main'
import { useAuthStore } from '@/stores/useAuthStore'
import { storeToRefs } from 'pinia'
const { getTokenAccsess} = storeToRefs(useAuthStore())
const {useGet} = useApiGet()
onMounted(()=>{

  const dat = useGet(apiUsersMe,{},{
     headers: {
    'Authorization': `Bearer ${getTokenAccsess.value}`,
  }
  })
     console.log(dat,'dataUser')
})
</script>

<style scoped>
.main {
  padding: 2rem;
  background: var(--color-bg-subtle);
  min-height: calc(100vh - 64px);
}
</style>
