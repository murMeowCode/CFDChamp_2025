<template>
  <div class="home" data-aos="zoom-out">
    <CardKarusel />
    
    
    <div v-if="userData">
      <h2>Привет, {{ userData.name }}!</h2>
    </div>
  </div>
</template>

<script setup>
import CardKarusel from '@/components/CardKarusel/CardKarusel.vue'
import { computed, watch } from 'vue'
import { useApiGet } from '@/utils/api/useApiGet'
import { useAuthStore } from '@/stores/useAuthStore'
import { storeToRefs } from 'pinia'
import { api8001 } from '@/utils/apiUrl/urlApi'
import { useUserStore } from '@/stores/useUserStore'
const { getTokenAccsess } = storeToRefs(useAuthStore())
const { useGet } = useApiGet()
const useUser = useUserStore()
const { 
  data: userDataRaw,
  isPending,
  isSuccess 
} = useGet(`${api8001}/profiles/me`, {}, {
  headers: {
    'Authorization': `Bearer ${getTokenAccsess.value}`,
  },
  withCredentials: true
})
// Отслеживаем успешную загрузку
watch(isSuccess, (success) => {
  if (success && userData.value) {
    useUser.setUser(userData.value)
    console.log('Данные загружены:', userData.value)
  }
})
// Используем computed для удобства
const userData = computed(() => userDataRaw.value)

</script>