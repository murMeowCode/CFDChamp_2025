// composables/useApiGet.js
import { useQuery } from '@tanstack/vue-query'
import { apiClient } from '@/main'

export function useApiGet() {
  const useGet = (endpoint, params = {}, options = {}) => {
    const queryKey = ['api', endpoint, params]

    return useQuery({
      queryKey,
      queryFn: async () => {
        const startTime = Date.now()
        console.log(`🔄 GET ${endpoint}`, { params })

        try {
          const response = await apiClient.get(endpoint, { params })
          const duration = Date.now() - startTime

          console.log(`✅ Успех: GET ${endpoint}`, {
            duration: `${duration}ms`,
            data: response.data,
          })

          return response.data
        } catch (error) {
          const duration = Date.now() - startTime
          console.error(`❌ Ошибка: GET ${endpoint}`, {
            duration: `${duration}ms`,
            error: error.response?.data || error.message,
          })
          throw error
        }
      },
      ...options,
    })
  }

  return {
    useGet,
  }
}
