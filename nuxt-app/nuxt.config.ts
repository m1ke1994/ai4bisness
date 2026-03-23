export default defineNuxtConfig({
  ssr: true,
  modules: ['@nuxtjs/tailwindcss'],
  css: ['~/assets/main.css'],
  nitro: {
    compressPublicAssets: true,
  },

  app: {
    head: {
      htmlAttrs: {
        lang: 'ru',
      },
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      ],
    },
  },

  routeRules: {
    '/': { swr: 300 },
    '/privacy-policy': { swr: 3600 },
    '/public-offer': { swr: 3600 },
    '/user-agreement': { swr: 3600 },
    '/robots.txt': {
      swr: 3600,
      headers: {
        'cache-control': 'public, max-age=0, s-maxage=3600, stale-while-revalidate=86400',
      },
    },
    '/sitemap.xml': {
      swr: 3600,
      headers: {
        'cache-control': 'public, max-age=0, s-maxage=3600, stale-while-revalidate=86400',
      },
    },
    '/favicon.ico': {
      headers: {
        'cache-control': 'public, max-age=604800, stale-while-revalidate=86400',
      },
    },
    '/images/**': {
      headers: {
        'cache-control': 'public, max-age=604800, stale-while-revalidate=86400',
      },
    },
    '/_nuxt/**': {
      headers: {
        'cache-control': 'public, max-age=31536000, immutable',
      },
    },
  },

  runtimeConfig: {
    apiInternalBase: process.env.NUXT_INTERNAL_API_BASE || 'http://backend:8000',
    public: {
      siteUrl: process.env.NUXT_PUBLIC_SITE_URL || '',
      apiBase: process.env.NUXT_PUBLIC_API_BASE || '',
      tracknodeApiKey: process.env.NUXT_PUBLIC_TRACKNODE_API_KEY || '',
      tracknodeTrackerSrc:
        process.env.NUXT_PUBLIC_TRACKNODE_TRACKER_SRC || 'https://tracknode.ru/tracker.js',
    },
  },
})
