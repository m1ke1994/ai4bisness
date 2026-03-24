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

const pageTitle = 'AI отдел продаж для бизнеса'
const pageDescription =
  'AI4Business внедряет ИИ-отдел продаж для сайта и мессенджеров: быстрые ответы, квалификация лидов, интеграции и аналитика.'

const setMeta = (name, content) => {
  if (!content || typeof document === 'undefined') return

  let element = document.head.querySelector(`meta[name="${name}"]`)
  if (!element) {
    element = document.createElement('meta')
    element.setAttribute('name', name)
    document.head.appendChild(element)
  }
  element.setAttribute('content', content)
}

onMounted(() => {
  document.title = pageTitle
  setMeta('description', pageDescription)
  useRevealOnScroll()
})
</script>
