<template>
  <div class="flex min-h-screen flex-col overflow-x-hidden">
    <AppHeader />

    <main class="flex-1 overflow-x-hidden pt-[74px] lg:pt-[88px]">
      <slot />
    </main>

    <AppFooter />
  </div>
</template>

<script setup>
import AppHeader from '~/components/AppHeader.vue'
import AppFooter from '~/components/AppFooter.vue'
</script>
