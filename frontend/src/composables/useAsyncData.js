import { ref, onMounted } from 'vue'

export const useAsyncData = (key, handler, options = {}) => {
  const initialData = typeof options.default === 'function' ? options.default() : null
  const data = ref(initialData)
  const pending = ref(false)
  const error = ref(null)

  const execute = async () => {
    pending.value = true
    error.value = null

    try {
      data.value = await handler()
    } catch (err) {
      error.value = err
      if (typeof options.default === 'function') {
        data.value = options.default()
      } else {
        data.value = null
      }
    } finally {
      pending.value = false
    }

    return data.value
  }

  onMounted(() => {
    void execute()
  })

  return {
    data,
    pending,
    error,
    refresh: execute,
  }
}
