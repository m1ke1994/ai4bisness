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

onMounted(() => {
  useRevealOnScroll()
})
</script>
