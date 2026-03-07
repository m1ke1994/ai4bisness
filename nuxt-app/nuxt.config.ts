export default defineNuxtConfig({
  ssr: true,
  modules: ['@nuxtjs/tailwindcss'],
  css: ['~/assets/main.css'],

  app: {
    head: {
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      ],
    },
  },

  runtimeConfig: {
    apiInternalBase: process.env.NUXT_INTERNAL_API_BASE || 'http://backend:8000',
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || '',
      tracknodeApiKey: process.env.NUXT_PUBLIC_TRACKNODE_API_KEY || '',
      tracknodeTrackerSrc:
        process.env.NUXT_PUBLIC_TRACKNODE_TRACKER_SRC || 'https://tracknode.ru/tracker.js',
    },
  },
})
