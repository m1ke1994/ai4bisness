<script setup>
import { computed } from 'vue'
import { siteData } from '~/data/siteData'

const integrationsData = computed(() => siteData?.aiValue?.meta?.integrations || {})
const integrationsRows = computed(() => integrationsData.value?.items || [])

const getRowImageSrc = (row) => {
  if (row?.img) return row.img
  const src = row?.media?.image?.src
  return src || ''
}

const getRowImageAlt = (row) => {
  return row?.media?.image?.alt || row?.title || ''
}
</script>

<template>
  <section
    id="integrations"
    class="relative overflow-hidden rounded-[32px] border border-[#E1E5F2] bg-white p-6 shadow-[0_18px_54px_rgba(18,26,52,0.08)] sm:p-8 "
  >
    <div aria-hidden="true" class="pointer-events-none absolute -right-12 -top-10 h-40 w-40 rounded-full bg-[rgba(111,99,255,0.10)] blur-3xl" />
    <div aria-hidden="true" class="pointer-events-none absolute -left-12 -bottom-10 h-40 w-40 rounded-full bg-[rgba(126,182,255,0.12)] blur-3xl" />

    <div class="relative mx-auto w-full max-w-full sm:w-[70%]">

      <!-- Р—Р°РіРѕР»РѕРІРѕРє -->
      <h3 class="text-[22px] font-semibold tracking-[-0.03em] text-[#0B0D1A] sm:text-[28px]">
        {{ integrationsData.title }}
      </h3>

      <!-- РўР°Р±Р»РёС†Р° -->
      <div class="mt-6 overflow-hidden rounded-[22px] border border-[#E7EAF4] bg-white">
        <div class="divide-y divide-[#EEF1FA]">

          <div
            v-for="row in integrationsRows"
            :key="row.id"
            class="fade-item grid grid-cols-1 gap-4 px-5 py-5 sm:grid-cols-[minmax(260px,1fr)_minmax(380px,1.8fr)_140px] sm:items-center sm:gap-8 sm:px-6"
          >

            <!-- LEFT -->
            <div class="min-w-0">
              <div class="text-[18px] font-semibold tracking-[-0.02em] text-[#0B0D1A]">
                {{ row.title }}
              </div>

              <div class="mt-2 text-[14px] leading-[1.5] text-[#444] sm:hidden">
                {{ row.description }}
              </div>
            </div>

            <!-- CENTER -->
            <div class="hidden sm:block">
              <div class="text-[15px] leading-[1.6] text-[#444]">
                {{ row.description }}
              </div>
            </div>

            <!-- RIGHT: РРљРћРќРљР -->
            <div class="flex items-center justify-between gap-2">

              <div class="icon-box">
                <img
                  :src="getRowImageSrc(row)"
                  :alt="getRowImageAlt(row)"
                  loading="lazy"
                />
              </div>

            </div>

          </div>

        </div>
      </div>

    </div>
  </section>
</template>

<style scoped>

.icon-box{
  width:150px;
  height:150px;

  display:flex;
  align-items:center;
  justify-content:center;

  flex-shrink:0;
}

.icon-box img{
  max-width:100%;
  max-height:100%;
  object-fit:contain;
}

</style>
