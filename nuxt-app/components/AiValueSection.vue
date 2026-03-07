<script setup>
import { computed } from 'vue'
import { fetchSubscriptionsSection } from '~/data/api'
import { siteData } from '~/data/siteData'

const fallbackAiValueData = siteData.aiValue
const fallbackLaunchData = fallbackAiValueData?.meta?.launch || {}
const fallbackLaunchMeta = fallbackLaunchData?.meta || {}

const { data: subscriptionsSection } = useAsyncData('subscriptions-section', fetchSubscriptionsSection, {
  server: false,
  default: () => null,
})

const aiValueData = computed(() => {
  if (!subscriptionsSection.value) {
    return fallbackAiValueData
  }

  return {
    ...fallbackAiValueData,
    title: subscriptionsSection.value.title || fallbackAiValueData.title,
    items: subscriptionsSection.value.items.length ? subscriptionsSection.value.items : fallbackAiValueData.items,
    meta: {
      ...fallbackAiValueData.meta,
      subtitlePrefix: subscriptionsSection.value.subtitlePrefix || fallbackAiValueData.meta.subtitlePrefix,
      subtitleHighlight: subscriptionsSection.value.subtitleHighlight || fallbackAiValueData.meta.subtitleHighlight,
      launch: {
        ...fallbackLaunchData,
        description: subscriptionsSection.value.description || fallbackLaunchData.description,
        meta: {
          ...fallbackLaunchMeta,
          badgePrimary: subscriptionsSection.value.badgePrimary || fallbackLaunchMeta.badgePrimary,
          badgeSecondary: subscriptionsSection.value.badgeSecondary || fallbackLaunchMeta.badgeSecondary,
          leftLabel: subscriptionsSection.value.leftLabel || fallbackLaunchMeta.leftLabel,
          rightLabel: subscriptionsSection.value.rightLabel || fallbackLaunchMeta.rightLabel,
          paidTitle: subscriptionsSection.value.paidTitle || fallbackLaunchMeta.paidTitle,
          paidDescription: subscriptionsSection.value.paidDescription || fallbackLaunchMeta.paidDescription,
          noteDescription: subscriptionsSection.value.noteDescription || fallbackLaunchMeta.noteDescription,
        },
      },
    },
  }
})

const launchData = computed(() => aiValueData.value?.meta?.launch || {})
const valuePoints = computed(() => aiValueData.value?.items || [])
</script>

<template>
  <section
    id="ai-value"
    class="relative isolate scroll-mt-[92px] rounded-none bg-[#F3F4F7] py-10 sm:py-12 lg:scroll-mt-[104px] lg:py-16"
  >
    <div
      aria-hidden="true"
      class="pointer-events-none absolute inset-0 opacity-100"
      style="
        background:
          radial-gradient(36rem 18rem at 10% 0%, rgba(111, 99, 255, 0.10), transparent 72%),
          radial-gradient(34rem 18rem at 92% 12%, rgba(126, 182, 255, 0.10), transparent 72%),
          radial-gradient(30rem 16rem at 50% 100%, rgba(111, 99, 255, 0.05), transparent 78%);
      "
    />

    <div class="relative z-10 mx-auto w-full max-w-[1720px] px-4 sm:px-6 lg:px-10">
      <!-- Title -->
      <div class="text-center">
        <h2
          class="text-[34px] font-semibold leading-[1.06] tracking-[-0.03em] text-[#111218] sm:text-[44px] lg:text-[66px] lg:leading-[1.04]"
        >
          {{ aiValueData.title }}
        </h2>
        <h3
          class="mt-2 text-[30px] font-semibold leading-[1.06] tracking-[-0.03em] text-[#9EA4B8] sm:text-[40px] lg:mt-3 lg:text-[58px] lg:leading-[1.04]"
        >
          {{ aiValueData.meta.subtitlePrefix }}
          <span class="bg-[linear-gradient(90deg,#5E52DE_0%,#8075FF_55%,#6FA9FF_100%)] bg-clip-text text-transparent">
            {{ aiValueData.meta.subtitleHighlight }}
          </span>
        </h3>
      </div>

      <!-- вњ… Р’РµСЂС‚РёРєР°Р»СЊРЅС‹Р№ СЃС‚РµРє: 1) Р·Р°РїСѓСЃРє, 2) РёРЅС‚РµРіСЂР°С†РёРё, 3) РєР°РЅР°Р»С‹ -->
      <div class="mt-8 grid grid-cols-1 gap-5 sm:mt-10 lg:gap-6">
        <!-- 1) Р—Р°РїСѓСЃРєР°РµРј AI-РїСЂРѕРґР°РІС†Р° -->
     <div
  class="relative overflow-hidden rounded-[30px] border border-[#DADFF3] bg-[linear-gradient(145deg,rgba(111,99,255,0.10)_0%,rgba(255,255,255,0.95)_35%,rgba(111,99,255,0.04)_100%)] p-5 shadow-[0_24px_70px_rgba(38,44,88,0.10)] sm:rounded-[32px] sm:p-6 lg:p-7"
>
  <div
    aria-hidden="true"
    class="pointer-events-none absolute inset-0 opacity-[0.25]"
    style="
      background-image: repeating-linear-gradient(
        130deg,
        rgba(111, 99, 255, 0.14) 0px,
        rgba(111, 99, 255, 0.14) 1px,
        transparent 1px,
        transparent 14px
      );
    "
  ></div>
  <div
    aria-hidden="true"
    class="pointer-events-none absolute -left-16 -top-16 h-40 w-40 rounded-full bg-[rgba(111,99,255,0.14)] blur-3xl"
  ></div>
  <div
    aria-hidden="true"
    class="pointer-events-none absolute -bottom-12 right-0 h-36 w-36 rounded-full bg-[rgba(126,182,255,0.16)] blur-3xl"
  ></div>

  <div class="relative">
    <div class="flex flex-wrap items-center gap-2.5">
      <span
        class="inline-flex items-center rounded-full border border-[#CFC8FF] bg-[rgba(111,99,255,0.08)] px-3 py-1.5 text-[11px] font-semibold tracking-[0.04em] text-[#5B50CF]"
      >
        {{ launchData.meta.badgePrimary }}
      </span>
      <span
        class="inline-flex items-center rounded-full border border-[#E3E7F4] bg-white/80 px-3 py-1.5 text-[11px] font-medium tracking-[-0.01em] text-[#5B627E]"
      >
        {{ launchData.meta.badgeSecondary }}
      </span>
    </div>

    <h4
      class="mt-4 text-[22px] font-semibold leading-[1.08] tracking-[-0.03em] text-[#141633] sm:text-[26px] lg:text-[30px]"
    >
      {{ launchData.title }}
    </h4>

    <p class="mt-3 max-w-[980px] text-[14px] leading-[1.5] tracking-[-0.01em] text-[#646C89] sm:text-[15px] lg:text-[16px]">
      {{ launchData.description }}
    </p>

    <!-- вњ… Р”Р’Р• РљРћР›РћРќРљР Р’ Р“РћР РР—РћРќРўРђР›Р¬ (РІСЃРµРіРґР° СЂСЏРґРѕРј) -->
    <div class="mt-6 overflow-hidden rounded-[22px] border border-white/40 bg-white/55 shadow-[0_18px_55px_rgba(18,26,52,0.08)]">
      <div class="relative grid grid-cols-1 gap-0 sm:grid-cols-2">

        <!-- LEFT: Р‘РµСЃРїР»Р°С‚РЅР°СЏ РѕСЃРЅРѕРІР° -->
        <div class="p-4 sm:p-5 lg:p-6">
          <div class="inline-flex items-center gap-2 rounded-full border border-white/50 bg-white/70 px-3 py-1.5 text-[12px] font-semibold text-[#141633]">
            <span class="h-2 w-2 rounded-full bg-[#78F7C7]" aria-hidden="true"></span>
            {{ launchData.meta.leftLabel }}
          </div>

          <div class="mt-4 grid gap-2.5">
            <div
              v-for="point in valuePoints"
              :key="point.id"
              class="fade-item flex items-start gap-2.5 rounded-[18px] border border-white/50 bg-white/70 px-3.5 py-3 shadow-[0_14px_36px_rgba(18,26,52,0.05)] backdrop-blur-sm"
            >
              <span
                aria-hidden="true"
                class="mt-0.5 grid h-6 w-6 shrink-0 place-items-center rounded-full bg-[linear-gradient(135deg,#4B39FF_0%,#8A7DFF_100%)] shadow-[0_10px_22px_rgba(89,75,255,0.24)]"
              >
                <svg viewBox="0 0 16 16" class="h-3.5 w-3.5 text-white" fill="none">
                  <path d="M4 8.2l2.1 2.1L12 4.7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
              </span>
              <span class="text-[13px] leading-[1.38] tracking-[-0.01em] text-[#20253A] sm:text-[14px]">
                {{ point.text }}
              </span>
            </div>
          </div>
        </div>

        <!-- RIGHT: РџР»Р°С‚РЅР°СЏ РѕСЃРЅРѕРІР° -->
        <div class="border-t border-[rgba(90,98,126,0.18)] p-4 sm:border-l sm:border-t-0 sm:p-5 lg:p-6">
          <div class="inline-flex items-center gap-2 rounded-full border border-white/50 bg-white/70 px-3 py-1.5 text-[12px] font-semibold text-[#141633]">
            <span class="h-2 w-2 rounded-full bg-[#6F63FF]" aria-hidden="true"></span>
            {{ launchData.meta.rightLabel }}
          </div>

          <div class="mt-4 rounded-[22px] border border-white/50 bg-white/75 p-4 shadow-[0_18px_55px_rgba(18,26,52,0.06)]">
            <div class="flex items-start gap-3">
              <span
                aria-hidden="true"
                class="mt-0.5 grid h-7 w-7 shrink-0 place-items-center rounded-full bg-[linear-gradient(135deg,#4B39FF_0%,#8A7DFF_100%)] shadow-[0_12px_26px_rgba(89,75,255,0.24)]"
              >
                <svg viewBox="0 0 16 16" class="h-3.5 w-3.5 text-white" fill="none">
                  <path d="M4 8.2l2.1 2.1L12 4.7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
              </span>

              <div>
                <div class="text-[14px] font-semibold tracking-[-0.02em] text-[#141633] sm:text-[15px]">
                  {{ launchData.meta.paidTitle }}
                </div>
                <div class="mt-1 text-[13px] leading-[1.5] tracking-[-0.01em] text-[#646C89] sm:text-[14px]">
                  {{ launchData.meta.paidDescription }}
                </div>
              </div>
            </div>
          </div>

          <div class="mt-4 rounded-[18px] border border-[#DCDFF3] bg-[linear-gradient(135deg,rgba(111,99,255,0.08)_0%,rgba(126,182,255,0.06)_100%)] p-4 shadow-[0_14px_34px_rgba(92,80,255,0.08)]">
            <div class="text-[13px] font-semibold tracking-[-0.01em] text-[#2D3350]">{{ launchData.meta.noteTitle }}</div>
            <p class="mt-2 text-[12px] leading-[1.45] text-[#5E6685] sm:text-[13px]">
              {{ launchData.meta.noteDescription }}
            </p>
          </div>
        </div>
      </div>
    </div>
    <!-- /2 columns -->
  </div>
</div>

        


      
      </div>
      <!-- /stack -->
    </div>
  </section>
</template>


