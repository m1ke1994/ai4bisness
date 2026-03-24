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
            loading="lazy"
            decoding="async"
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

          <RouterLink
            v-for="item in legalItems"
            :key="item.id"
            :to="item.href"
            class="text-[15px] leading-none tracking-[-0.02em] text-[#8E91A9] transition hover:text-white sm:text-[17px] lg:text-[18px]"
          >
            {{ item.label }}
          </RouterLink>

          <RouterLink
            to="/company-brief"
            target="_blank"
            rel="noopener noreferrer"
            class="inline-flex h-[38px] items-center justify-center rounded-[12px] border border-[#393E5A] bg-[linear-gradient(90deg,rgba(111,99,255,0.18)_0%,rgba(139,127,255,0.10)_100%)] px-4 text-[14px] font-medium leading-none tracking-[-0.01em] text-white transition hover:border-[#5A62A2] hover:bg-[linear-gradient(90deg,rgba(111,99,255,0.28)_0%,rgba(139,127,255,0.16)_100%)] sm:h-[42px] sm:text-[15px]"
          >
            Заполнить анкету
          </RouterLink>

        </div>

      </div>

    </div>
  </footer>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useAsyncData } from '~/composables/useAsyncData'
import { computed } from 'vue'
import { fetchFooterSection } from '~/data/api'
import { siteData } from '~/data/siteData'

const footerData = siteData.footer

const legalColumn = footerData.items.find(
  (column) => column.slug === 'legal'
)

const { data: footerSection } = useAsyncData('footer-section', fetchFooterSection, {
  default: () => null,
})

const brandName = computed(() => footerSection.value?.brandName || footerData.meta.brandName)
const brandHref = computed(() => footerSection.value?.logoLink || footerData.meta.brandHref)
const logoSrc = computed(() => footerSection.value?.logo || footerData.media.logo.src)
const logoAlt = computed(() => brandName.value || footerData.media.logo.alt)

const normalizeLegalHref = (href) => {
  const value = String(href || '').trim().toLowerCase()
  if (value.includes('privacy') || value.includes('/policy')) {
    return '/policy'
  }
  return '/terms'
}

const mapLegalItems = (items) => {
  if (!Array.isArray(items)) {
    return []
  }

  const mapped = items
    .map((item, index) => ({
      id: item.id || `legal-link-${index + 1}`,
      label: String(item.label || item.title || '').trim(),
      href: normalizeLegalHref(item.href),
    }))
    .filter((item) => item.label && item.href)

  const byHref = new Map()
  for (const item of mapped) {
    if (!byHref.has(item.href)) {
      byHref.set(item.href, item)
    }
  }

  return Array.from(byHref.values())
}

const legalItems = computed(() => {
  if (footerSection.value?.links?.length) {
    return mapLegalItems(footerSection.value.links)
  }

  return mapLegalItems(legalColumn?.links || [])
})
</script>


