<template>
  <div class="home" data-aos="zoom-out">
    <CardKarusel />
  </div>
</template>

<script setup>
import CardKarusel from '@/components/CardKarusel/CardKarusel.vue'
import { onMounted } from 'vue'
import { useApiGet } from '@/utils/api/useApiGet'
import { useAuthStore } from '@/stores/useAuthStore'
import { storeToRefs } from 'pinia'
import { apiProfilesMe } from '@/utils/apiUrl/urlApi'
const { getTokenAccsess} = storeToRefs(useAuthStore())
const {useGet} = useApiGet()
onMounted(()=>{

  const dat = useGet(`${apiProfilesMe}/profiles/me`,{},{
     headers: {
    'Authorization': `Bearer ${getTokenAccsess.value}`,
  },witchCredentials:true
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
