<script setup>
import { computed } from 'vue'
import { siteData } from '~/data/siteData'
import Social_Media from '~/components/Social_Media.vue'
import IntegrationsAnalyticsSection from '~/components/IntegrationsAnalyticsSection.vue'

const advantagesData = siteData.advantages
const trainingData = advantagesData.meta.training
const summaryData = advantagesData.meta.summary
const compareRows = advantagesData.items
const checkIcon = advantagesData.media.icon.src

const trainingRows = computed(() => {
  const rows = []
  for (let index = 0; index < trainingData.items.length; index += 2) {
    rows.push(trainingData.items.slice(index, index + 2))
  }
  return rows
})
</script>

<template>
<section
id="advantages"
class="relative z-10 bg-[#F3F4F7] py-10 sm:py-12 lg:py-16"
>

<div class="mx-auto w-full max-w-[1720px] px-4 sm:px-6 lg:px-10">

<div class="relative overflow-hidden bg-white space-y-10 lg:space-y-12">


<!-- ================================= -->
<!-- БЛОК ОБУЧЕНИЯ AI -->
<!-- ================================= -->

<div class="px-4 sm:px-6 lg:px-10">

<div
class="relative overflow-hidden rounded-[22px] border border-[#E8EBF4] bg-[linear-gradient(180deg,#FFFFFF_0%,#F7F8FC_100%)] p-5 shadow-[0_18px_60px_rgba(20,27,58,0.06)] sm:p-7 lg:p-8"
>

<div
class="pointer-events-none absolute inset-0 opacity-80"
style="
background:
radial-gradient(34rem 18rem at 8% 10%, rgba(75, 57, 255, 0.08), transparent 72%),
radial-gradient(30rem 18rem at 92% 88%, rgba(125, 108, 255, 0.08), transparent 72%);
"
/>

<div class="relative grid gap-6 lg:grid-cols-[minmax(0,1.05fr)_minmax(0,0.95fr)] lg:items-start">

<!-- LEFT -->

<div class="text-left space-y-4">

<div
class="inline-flex items-center gap-2 rounded-full border border-[#E3E7F2] bg-white/90 px-3 py-2 shadow-sm"
>
<span
class="grid h-6 w-6 place-items-center rounded-full bg-[linear-gradient(135deg,#4B39FF_0%,#8A7DFF_100%)]"
>
<img :src="checkIcon" class="h-3.5 w-3.5 brightness-[5] saturate-0"/>
</span>

<span class="text-[14px] font-medium text-[#2F3452] sm:text-[18px]">
{{ trainingData.title }}
</span>

</div>


<div class="space-y-2.5">

<div
v-for="row in trainingRows"
:key="row[0].id"
class="grid grid-cols-2 gap-2.5"
>

<div
v-for="item in row"
:key="item.id"
class="fade-item flex items-center justify-center gap-2 rounded-[12px] border border-[#E6EAF4] bg-white/85 px-3 py-2 text-[15px] font-medium text-[#343A57]"
>

<img :src="checkIcon" class="h-3.5 w-3.5"/>
<span>{{ item.title }}</span>

</div>

<div v-if="row.length === 1"></div>

</div>

</div>

</div>


<!-- RIGHT -->

<div
class="relative overflow-hidden rounded-[20px] border border-[#D9DEF0] bg-[#5b6098] p-5 shadow-[0_24px_60px_rgba(18,26,52,0.18)] text-white"
>

<div
class="pointer-events-none absolute -right-14 -top-14 h-32 w-32 rounded-full bg-[#171B42]/20 blur-3xl"
/>

<div class="relative space-y-4">

<div
class="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-3 py-1.5 text-[12px]"
>
<span class="h-2 w-2 rounded-full bg-[#78F7C7]" />
{{ trainingData.meta.rightPill }}
</div>

<p class="text-[20px] font-medium leading-[1.4]">
{{ trainingData.meta.rightTitle }}
</p>

<div class="space-y-2">

<div
v-for="bullet in trainingData.meta.rightBullets"
:key="bullet.id"
class="flex items-start gap-2 text-[18px]"
>

<img :src="checkIcon" class="h-3.5 w-3.5 brightness-[4] saturate-0"/>

<span>{{ bullet.text }}</span>

</div>

</div>

</div>

</div>

</div>

</div>

</div>


<!-- ================================= -->
<!-- БЛОК СРАВНЕНИЯ -->
<!-- ================================= -->

<div class="summary-shell relative overflow-hidden rounded-[26px] border border-[#E6EAF4] bg-white shadow-[0_30px_90px_rgba(18,26,52,0.12)]">

<div class="relative p-6 lg:p-8 space-y-6">


<!-- HEADER -->

<div class="space-y-2 max-w-[900px] ">

<div class="text-[14px] font-semibold text-[#2F3452]">
{{ summaryData.subtitle }}
</div>

<div class="text-[20px] lg:text-[26px] font-semibold text-[#141633]">
{{ summaryData.title }}
</div>

</div>


<!-- TABLE -->

<div class="rounded-[22px] border border-[#E6EAF4] bg-white/60 overflow-hidden">


<!-- DESKTOP -->

<div class="hidden lg:block w-[90%] m-auto">

<div class="flex text-center px-6 pt-6 pb-4 text-[20px] font-semibold">

<div class="w-[30%]">
{{ summaryData.meta.desktopStageLabel }}
</div>

<div class="w-[35%] text-[#4B39FF]">
{{ summaryData.meta.desktopAiLabel }}
</div>

<div class="w-[35%]">
{{ summaryData.meta.desktopHumanLabel }}
</div>

</div>


<div class="divide-y divide-[#E8EBF4]">

<div
v-for="r in compareRows"
:key="r.id"
class="fade-item flex px-6 py-6 items-center"
>

<div class="w-[30%] text-center">

<div class="text-[16px] font-semibold text-[#141633]">
{{ r.title }}
</div>

<div class="text-[13px] text-[#7A809A] mt-1">
{{ summaryData.meta.stageDescriptionLabel }}
</div>

</div>


<div class="w-[35%] flex justify-center">

<div class="max-w-[340px] w-full rounded-[18px] border border-[#E6EAF4] bg-white p-5 shadow-sm">

<div class="flex items-start gap-3">

<span
class="flex items-center justify-center w-7 h-7 min-w-[28px] min-h-[28px] shrink-0 rounded-full bg-gradient-to-r from-[#4B39FF] to-[#8A7DFF] text-white"
>
✓
</span>

<div class="text-[15px] text-[#141633] leading-[1.5]">
{{ r.aiDescription }}
</div>

</div>

</div>

</div>


<div class="w-[35%] flex justify-center">

<div class="max-w-[340px] w-full rounded-[18px] border border-[#E6EAF4] bg-white p-5 shadow-sm">

<div class="flex items-start gap-3">

<span class="grid h-7 w-7 place-items-center rounded-full bg-[#111827]/5">
—
</span>

<div class="text-[15px] text-[#2B2E3A] leading-[1.5]">
{{ r.humanDescription }}
</div>

</div>

</div>

</div>

</div>

</div>

</div>


<!-- MOBILE -->

<div class="lg:hidden px-4 pb-6 pt-4 space-y-4">

<div
v-for="r in compareRows"
:key="r.id"
class="fade-item rounded-[18px] border border-[#E6EAF4] bg-white p-4 shadow-sm space-y-3"
>

<div class="font-semibold text-[15px] text-[#141633]">
{{ r.title }}
</div>

<div class="space-y-2">

<div class="space-y-1 rounded-[12px] border border-[#ECEFFF] bg-[#F7F8FF] p-3">

<div class="flex items-center gap-2 text-[12px] font-semibold text-[#4B39FF]">
<span>✓</span>
<span>{{ summaryData.meta.mobileAiLabel || summaryData.meta.desktopAiLabel }}</span>
</div>

<div class="text-[14px] text-[#141633]">
{{ r.aiDescription }}
</div>

</div>

<div class="space-y-1 rounded-[12px] border border-[#E8EBF4] bg-[#F9FAFC] p-3">

<div class="flex items-center gap-2 text-[12px] font-semibold text-[#2B2E3A]">
<span>—</span>
<span>{{ summaryData.meta.mobileHumanLabel || summaryData.meta.desktopHumanLabel }}</span>
</div>

<div class="text-[14px] text-[#2B2E3A]">
{{ r.humanDescription }}
</div>

</div>

</div>

</div>

</div>


<div class="text-center text-[13px] text-[#6B7190] pb-6">
{{ summaryData.meta.desktopFooter }}
</div>

</div>

</div>


<Social_Media />
<IntegrationsAnalyticsSection />

</div>

</div>
</div>

</section>
</template>

<style scoped>
.summary-shell{
background-image:
radial-gradient(1200px 320px at 50% 0%, rgba(75,57,255,0.06), transparent 60%),
radial-gradient(900px 280px at 85% 70%, rgba(138,125,255,0.06), transparent 62%);
}
</style>

