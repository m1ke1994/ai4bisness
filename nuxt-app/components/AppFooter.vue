<template>
  <footer class="w-full bg-black">
    <div class="mx-auto w-full max-w-[1720px] px-4 py-10 sm:px-6 sm:py-12 lg:px-10 lg:py-14">

      <div class="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">

        <!-- ЛОГО -->
        <a
          :href="brandHref"
          class="inline-flex items-center gap-3 text-white"
          :aria-label="brandName"
        >
          <img
            :src="logoSrc"
            :alt="logoAlt"
            class="h-[56px] w-auto rounded-full sm:h-[62px] lg:h-[80px]"
            draggable="false"
          />

          <span
            class="text-[20px] font-semibold leading-none tracking-[-0.02em] sm:text-[24px] lg:text-[26px]"
          >
            {{ brandName }}
          </span>
        </a>

        <!-- ССЫЛКИ -->
        <div class="flex flex-wrap items-center gap-x-6 gap-y-2 lg:gap-x-8">

          <NuxtLink
            v-for="item in legalItems"
            :key="item.id"
            :to="item.href"
            class="text-[15px] leading-none tracking-[-0.02em] text-[#8E91A9] transition hover:text-white sm:text-[17px] lg:text-[18px]"
          >
            {{ item.label }}
          </NuxtLink>

        </div>

      </div>

    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'
import { fetchFooterSection } from '~/data/api'
import { siteData } from '~/data/siteData'

const footerData = siteData.footer

const legalColumn = footerData.items.find(
  (column) => column.slug === 'legal'
)

const { data: footerSection } = useAsyncData('footer-section', fetchFooterSection, {
  server: false,
  default: () => null,
})

const brandName = computed(() => footerSection.value?.brandName || footerData.meta.brandName)
const brandHref = computed(() => footerSection.value?.logoLink || footerData.meta.brandHref)
const logoSrc = computed(() => footerSection.value?.logo || footerData.media.logo.src)
const logoAlt = computed(() => brandName.value || footerData.media.logo.alt)

const legalItems = computed(() => {
  if (footerSection.value?.links?.length) {
    return footerSection.value.links
  }

  return legalColumn?.links || []
})
</script>
