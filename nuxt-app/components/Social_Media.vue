<script setup>
import { siteData } from '~/data/siteData'

const channelsData = siteData.channels
const channelItems = channelsData.items
</script>

<template>
  <div
    class="relative overflow-hidden rounded-[30px] border border-[#E1E5F2] bg-[#0b0f2a] p-5 pb-0 shadow-[0_22px_70px_rgba(18,26,52,0.18)] sm:rounded-[32px] sm:p-6 sm:pb-0 lg:p-7 lg:pb-0 py-2"
  >
    <img
      :src="channelsData.media.background.src"
      alt=""
      aria-hidden="true"
      class="pointer-events-none absolute inset-0 h-full w-full object-cover opacity-[0.75]"
      draggable="false"
    />

    <div
      aria-hidden="true"
      class="pointer-events-none absolute inset-0 bg-[linear-gradient(180deg,rgba(5,8,26,0.78)_0%,rgba(5,8,26,0.58)_45%,rgba(5,8,26,0.84)_100%)]"
    />
    <div
      aria-hidden="true"
      class="pointer-events-none absolute inset-0 opacity-[0.18]"
      style="
        background-image: repeating-linear-gradient(
          130deg,
          rgba(255, 255, 255, 0.20) 0px,
          rgba(255, 255, 255, 0.20) 1px,
          transparent 1px,
          transparent 16px
        );
      "
    />
    <div aria-hidden="true" class="pointer-events-none absolute -top-16 -right-24 h-64 w-64 rounded-full bg-[#6F63FF]/25 blur-3xl" />
    <div aria-hidden="true" class="pointer-events-none absolute -bottom-20 -left-24 h-64 w-64 rounded-full bg-[#7BB3FF]/20 blur-3xl" />

    <div class="relative grid gap-6 lg:grid-cols-[minmax(0,1.05fr)_minmax(0,0.95fr)] lg:items-center">
      <div class="h-full rounded-[24px] p-4 shadow-[0_20px_50px_rgba(18,26,52,0.12)] sm:p-5 lg:p-6">
        <div
          class="inline-flex items-center gap-2 rounded-full border border-[#E3E8F6] bg-white px-3 py-1.5 text-[11px] font-medium tracking-[-0.01em] text-[#59607D]"
        >
          <span class="h-2 w-2 rounded-full bg-[#6F63FF] shadow-[0_0_14px_rgba(111,99,255,0.75)]" aria-hidden="true" />
          {{ channelsData.subtitle }}
        </div>

        <h4 class="mt-4 text-[22px] font-semibold tracking-[-0.03em] text-[#fbfcfd] sm:text-[26px]">
          {{ channelsData.title }}
        </h4>

        <p class="mt-2 max-w-[720px] text-[13px] leading-[1.55] text-[#fafbfc] sm:text-[14px]">
          {{ channelsData.description }}
        </p>

        <div class="mt-5 grid grid-cols-2 gap-2.5 sm:grid-cols-3 lg:grid-cols-4">
          <a
            v-for="item in channelItems"
            :key="item.id"
            :href="item.href"
            :aria-label="`${channelsData.meta.itemAriaLabelPrefix} ${item.name}`"
            target="_blank"
            rel="noopener noreferrer"
            class="group flex min-h-[44px] items-center justify-center gap-2 rounded-[14px] border border-[#E5E9F5] bg-white px-3 py-2 text-[12px] font-medium tracking-[-0.01em] text-black shadow-[0_10px_24px_rgba(0,0,0,0.08)] transition hover:-translate-y-0.5 hover:border-[#D3DAEF] hover:bg-[#FBFCFF]"
          >
            <img
              :src="item.icon.src"
              :alt="item.icon.alt"
              class="h-4 w-4 shrink-0 object-contain opacity-90 transition group-hover:opacity-100"
            />
            <span class="truncate">{{ item.name }}</span>
          </a>
        </div>
      </div>

      <div class="relative mx-auto w-full max-w-[620px] self-end">
        <div
          aria-hidden="true"
          class="pointer-events-none absolute -inset-10 rounded-[40px] bg-[radial-gradient(closest-side,rgba(111,99,255,0.22),transparent_70%)] blur-2xl"
        />
        <div class="relative flex items-end justify-center gap-3 sm:gap-4">
          <img
            :src="channelsData.media.image.src"
            :alt="channelsData.media.image.alt"
            class="h-auto w-[46%] object-contain translate-y-[6px] sm:translate-y-[10px] lg:translate-y-[14px]"
            draggable="false"
          />
          <img
            :src="channelsData.media.secondaryImage.src || channelsData.media.image.src"
            :alt="channelsData.media.secondaryImage.alt"
            class="h-auto w-[46%] object-contain translate-y-[6px] sm:translate-y-[10px] lg:translate-y-[14px]"
            draggable="false"
            @error="($event) => ($event.target.src = channelsData.media.image.src)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

