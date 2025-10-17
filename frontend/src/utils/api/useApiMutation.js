// composables/useApiMutations.js
import { useMutation } from '@tanstack/vue-query'
import { apiClient } from '@/main'

const createMutation = (method) => (endpoint, options = {}) => {
  return useMutation({
    mutationFn: (data) => apiClient[method](endpoint, data).then(res => res.data),
    onSuccess: (data, variables, context) => {
      console.log(`✅ ${method.toUpperCase()} Success: ${endpoint}`, data)
      options.onSuccess?.(data, variables, context)
    },
    onError: (error, variables, context) => {
      console.error(`❌ ${method.toUpperCase()} Error: ${endpoint}`, error.response?.data)
      options.onError?.(error, variables, context)
    },
    ...options
  })
}

export function useApiMutations() {
  return {
    usePost: createMutation('post'),
    usePut: createMutation('put'),
    usePatch: createMutation('patch'),
    useDelete: createMutation('delete')
  }
}