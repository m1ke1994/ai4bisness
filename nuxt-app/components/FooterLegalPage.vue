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

      <article class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm sm:p-8">
        <h1 class="text-3xl font-semibold leading-tight text-gray-900 sm:text-4xl">
          {{ page.title }}
        </h1>

        <div class="mt-6 whitespace-pre-line text-base leading-7 text-gray-700">
          {{ page.content }}
        </div>
      </article>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { fetchFooterPageBySlug } from '~/data/api'

const props = defineProps({
  slug: {
    type: String,
    required: true,
  },
})

const router = useRouter()
<<<<<<< HEAD
const runtimeConfig = useRuntimeConfig()
const siteUrl = String(runtimeConfig.public.siteUrl || '').replace(/\/+$/, '')
=======
>>>>>>> 01c2954498212894780bf3e7930b723f73df20ad

const { data } = await useAsyncData(
  `footer-page-${props.slug}`,
  () => fetchFooterPageBySlug(props.slug),
)

if (!data.value) {
  throw createError({
    statusCode: 404,
    statusMessage: 'Страница не найдена',
    fatal: true,
  })
}

const page = computed(() => data.value)
const pageTitle = computed(() => page.value?.title || 'Страница подвала')
<<<<<<< HEAD
const pageDescription = computed(() => {
  const content = (page.value?.content || '').replace(/\s+/g, ' ').trim()
  return content.slice(0, 160)
})
const canonicalUrl = computed(() => (siteUrl ? `${siteUrl}/${props.slug}` : ''))

useSeoMeta({
  title: () => pageTitle.value,
  description: () => pageDescription.value,
  ogTitle: () => pageTitle.value,
  ogDescription: () => pageDescription.value,
  robots: 'index, follow',
})

useHead({
  link: canonicalUrl.value
    ? [
        {
          rel: 'canonical',
          href: canonicalUrl.value,
        },
      ]
    : [],
=======

useSeoMeta({
  title: () => pageTitle.value,
  ogTitle: () => pageTitle.value,
>>>>>>> 01c2954498212894780bf3e7930b723f73df20ad
})

const goBack = async () => {
  if (import.meta.client && window.history.length > 1) {
    router.back()
    return
  }

  await navigateTo('/')
}
</script>
<<<<<<< HEAD
=======

>>>>>>> 01c2954498212894780bf3e7930b723f73df20ad
