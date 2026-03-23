<template>
  <div>
    <HeroSection />
    <WhatSellerCan />
    <AiValueSection />
    <PricingSection />
    <IntegrationSteps />
    <ReviewsSection />
    <ContactFeedbackSection />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import HeroSection from '~/components/HeroSection.vue'
import WhatSellerCan from '~/components/WhatSellerCan.vue'
import IntegrationSteps from '~/components/IntegrationSteps.vue'
import ReviewsSection from '~/components/ReviewsSection.vue'
import PricingSection from '~/components/PricingSection.vue'
import AiValueSection from '~/components/AiValueSection.vue'
import ContactFeedbackSection from '~/components/ContactFeedbackSection.vue'
import { useRevealOnScroll } from '~/composables/useRevealOnScroll'

const runtimeConfig = useRuntimeConfig()
const siteUrl = String(runtimeConfig.public.siteUrl || '').replace(/\/+$/, '')
const canonicalUrl = siteUrl ? `${siteUrl}/` : undefined

useServerSeoMeta({
  title: 'AI отдел продаж для бизнеса',
  description:
    'AI4Business внедряет ИИ-отдел продаж для сайта и мессенджеров: быстрые ответы, квалификация лидов, интеграции и аналитика.',
  ogTitle: 'AI отдел продаж для бизнеса',
  ogDescription:
    'AI4Business внедряет ИИ-отдел продаж для сайта и мессенджеров: быстрые ответы, квалификация лидов, интеграции и аналитика.',
  robots: 'index, follow',
})

useHead({
  link: canonicalUrl
    ? [
        {
          rel: 'canonical',
          href: canonicalUrl,
        },
      ]
    : [],
})

onMounted(() => {
  useRevealOnScroll()
})
</script>
