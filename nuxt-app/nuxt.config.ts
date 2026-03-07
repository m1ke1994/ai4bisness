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
    public: {
      tracknodeApiKey: process.env.NUXT_PUBLIC_TRACKNODE_API_KEY || '',
      tracknodeTrackerSrc:
        process.env.NUXT_PUBLIC_TRACKNODE_TRACKER_SRC || 'https://tracknode.ru/tracker.js',
    },
  },
})
