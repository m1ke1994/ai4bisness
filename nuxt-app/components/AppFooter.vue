<template>
  <footer class="w-full bg-black">
    <div class="mx-auto w-full max-w-[1720px] px-4 py-10 sm:px-6 sm:py-12 lg:px-10 lg:py-14">

      <div class="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">

        <!-- ЛОГО -->
        <a
          :href="footerData.meta.brandHref"
          class="inline-flex items-center gap-3 text-white"
          :aria-label="footerData.meta.brandName"
        >
          <img
            :src="footerData.media.logo.src"
            :alt="footerData.media.logo.alt"
            class="h-[56px] w-auto rounded-full sm:h-[62px] lg:h-[80px]"
            draggable="false"
          />

          <span
            class="text-[20px] font-semibold leading-none tracking-[-0.02em] sm:text-[24px] lg:text-[26px]"
          >
            {{ footerData.meta.brandName }}
          </span>
        </a>

        <!-- ССЫЛКИ -->
        <div class="flex flex-wrap items-center gap-x-6 gap-y-2 lg:gap-x-8">

          <a
            v-for="item in legalItems"
            :key="item.id"
            :href="item.href"
            class="text-[15px] leading-none tracking-[-0.02em] text-[#8E91A9] transition hover:text-white sm:text-[17px] lg:text-[18px]"
            @click.prevent="item.href === '#'"
          >
            {{ item.label }}
          </a>

        </div>

      </div>

    </div>
  </footer>
</template>

<script setup>
import { siteData } from '~/data/siteData'

const footerData = siteData.footer

const navigationColumn = footerData.items.find(
  (column) => column.slug === 'navigation'
)

const legalColumn = footerData.items.find(
  (column) => column.slug === 'legal'
)

const navItems = navigationColumn?.links || []
const legalItems = legalColumn?.links || []
</script>
