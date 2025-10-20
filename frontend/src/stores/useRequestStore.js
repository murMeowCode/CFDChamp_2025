import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useRequestsStore = defineStore('user', () => {
  const requests = ref(null)
  function setRequests(newR) {
    requests.value = newR
    console.log(requests.value, 'USERVALUE')
  }
  const getRequests = computed(() => requests.value)

  return {
    setRequests,
    getRequests,
  }
})
