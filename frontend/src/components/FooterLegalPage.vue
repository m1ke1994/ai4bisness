<template>
  <div class="min-h-screen bg-white py-14 sm:py-16">
    <div class="mx-auto w-full max-w-4xl px-4 sm:px-6">
      <button
        type="button"
        class="mb-8 inline-flex items-center text-sm font-medium text-gray-500 transition hover:text-black"
        @click="goBack"
      >
        ← Назад
      </button>

      <article
        v-if="page"
        class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm sm:p-8"
      >
        <h1 class="text-3xl font-semibold leading-tight text-gray-900 sm:text-4xl">
          {{ page.title }}
        </h1>

        <div class="mt-6 whitespace-pre-line text-base leading-7 text-gray-700">
          {{ page.content }}
        </div>
      </article>

      <article
        v-else-if="!isLoading"
        class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm sm:p-8"
      >
        <h1 class="text-2xl font-semibold text-gray-900">Страница не найдена</h1>
        <p class="mt-3 text-gray-600">Попробуйте перейти на главную и открыть документ из футера.</p>
      </article>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { fetchFooterPageBySlug } from '~/data/api'

const props = defineProps({
  slug: {
    type: [String, Array],
    required: true,
  },
})

const router = useRouter()
const page = ref(null)
const isLoading = ref(false)

const normalizedSlugs = computed(() => {
  if (Array.isArray(props.slug)) {
    return props.slug
      .map((item) => String(item || '').trim())
      .filter(Boolean)
  }

  const singleSlug = String(props.slug || '').trim()
  return singleSlug ? [singleSlug] : []
})

const updateMeta = (loadedPage) => {
  const title = loadedPage?.title || 'Документ'
  const content = String(loadedPage?.content || '')
    .replace(/\s+/g, ' ')
    .trim()

  document.title = title

  let descriptionTag = document.head.querySelector('meta[name="description"]')
  if (!descriptionTag) {
    descriptionTag = document.createElement('meta')
    descriptionTag.setAttribute('name', 'description')
    document.head.appendChild(descriptionTag)
  }

  descriptionTag.setAttribute('content', content.slice(0, 160))
}

const loadPage = async () => {
  isLoading.value = true
  page.value = null

  try {
    for (const slug of normalizedSlugs.value) {
      const payload = await fetchFooterPageBySlug(slug)
      if (payload) {
        page.value = payload
        break
      }
    }
  } finally {
    isLoading.value = false
    updateMeta(page.value)
  }
}

const goBack = async () => {
  if (window.history.length > 1) {
    router.back()
    return
  }

  await router.push('/')
}

watch(normalizedSlugs, () => {
  void loadPage()
})

onMounted(() => {
  void loadPage()
})
</script>
