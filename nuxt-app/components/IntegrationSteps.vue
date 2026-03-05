<script setup>
import { siteData } from '~/data/siteData'

const integrationStepsData = siteData.steps
const integrationSteps = integrationStepsData.items
const firstRowSteps = integrationSteps.slice(0, 3)
const secondRowSteps = integrationSteps.slice(3, 5)

const ctaData = integrationStepsData.cta
const ctaTitleLines = ctaData.titleLines || []
</script>

<template>
<section
  id="steps"
  class="relative isolate overflow-x-hidden bg-[#F3F4F7] py-10 sm:py-12 lg:py-16"
>
<div class="mx-auto w-full max-w-[1720px] px-4 sm:px-6 lg:px-10">

<!-- заголовок -->
<div class="text-center">

<h2
class="text-[30px] font-semibold tracking-[-0.02em] !text-black sm:text-[34px] md:text-[40px] lg:text-[42px] xl:text-[48px]"
>
{{ integrationStepsData.title }}
</h2>

<h3
class="mt-3 text-[30px] font-semibold tracking-[-0.02em] !text-gray-400 sm:text-[34px] md:text-[40px] lg:mt-4 lg:text-[42px] xl:text-[48px]"
>
{{ integrationStepsData.subtitle }}
</h3>

</div>


<div class="mt-10 sm:mt-14 lg:mt-20">


<!-- ========================= -->
<!-- MOBILE -->
<!-- ========================= -->

<div class="flex flex-col gap-4 lg:hidden">

  <!-- STEPS -->
  <div
    v-for="step in integrationSteps"
    :key="step.id"
    class="fade-item relative flex w-full max-w-full min-h-[520px] flex-col overflow-hidden rounded-[26px] bg-[#E9EBF2] p-6"
  >

    <div>

      <p class="text-[15px] text-gray-500 sm:text-lg">
        {{ step.day }}
      </p>

      <h4 class="mt-2 text-[20px] font-semibold leading-tight text-black sm:mt-3 sm:text-2xl">
        {{ step.title }}
      </h4>

      <p class="mt-3 text-[15px] leading-relaxed text-gray-500 sm:mt-4 sm:text-base">
        {{ step.description }}
      </p>

    </div>

    <div class="mt-auto flex h-[200px] items-end justify-center">

      <img
        v-if="step.media.image.src"
        :src="step.media.image.src"
        :alt="step.media.image.alt"
        class="max-h-[260px] w-auto max-w-full object-contain sm:max-h-[170px]"
        loading="lazy"
        draggable="false"
      />

    </div>

  </div>


  <!-- CTA MOBILE -->

  <div
    class="fade-item relative w-full max-w-full overflow-hidden rounded-[26px] bg-[#1B1730] p-6"
  >

    <img
      :src="ctaData.media.background.src"
      alt=""
      class="pointer-events-none absolute inset-0 h-full w-full object-cover"
    />

    <div
      class="absolute inset-0 bg-[linear-gradient(180deg,rgba(20,16,34,0.35)_0%,rgba(44,31,85,0.52)_50%,rgba(74,56,145,0.78)_100%)]"
    ></div>

    <div class="relative z-10 flex min-h-[520px] flex-col">

      <h4
        class="text-[28px] font-semibold leading-[0.98] tracking-[-0.03em] text-white sm:text-[34px]"
      >
        {{ ctaTitleLines[0] }}<br />
        {{ ctaTitleLines[1] }}
      </h4>

      <div class="mt-auto flex h-[220px] items-end justify-center">

        <img
          v-if="ctaData.media.image.src"
          :src="ctaData.media.image.src"
          :alt="ctaData.media.image.alt"
          class="max-h-[260px] w-auto max-w-full object-contain sm:max-h-[170px]"
          loading="lazy"
          draggable="false"
        />

      </div>

    </div>

  </div>

</div>



<!-- ========================= -->
<!-- DESKTOP -->
<!-- ========================= -->

<div class="hidden lg:block">


<!-- row 1 -->

<div class="grid grid-cols-2 gap-6 xl:grid-cols-3 xl:gap-10">

<div
v-for="step in firstRowSteps"
:key="step.id"
class="fade-item relative flex min-h-[520px] flex-col rounded-[32px] bg-[#E9EBF2] p-8 xl:h-[520px] xl:p-10"
>

<div>

<p class="text-base !text-gray-500 xl:text-lg">
{{ step.day }}
</p>

<h4 class="mt-3 text-[22px] font-semibold leading-tight !text-black xl:text-2xl">
{{ step.title }}
</h4>

<p class="mt-4 leading-relaxed !text-gray-500">
{{ step.description }}
</p>

</div>


<div class="mt-auto flex h-[220px] items-end justify-center">

<img
v-if="step.media.image.src"
:src="step.media.image.src"
:alt="step.media.image.alt"
class="max-h-[250px] w-auto object-contain"
loading="lazy"
draggable="false"
/>

</div>

</div>

</div>



<!-- row 2 -->

<div class="mt-10 grid grid-cols-2 gap-6 xl:grid-cols-3 xl:gap-10">

<div
v-for="step in secondRowSteps"
:key="step.id"
class="fade-item relative flex min-h-[520px] flex-col rounded-[32px] bg-[#E9EBF2] p-8 xl:h-[520px] xl:p-10"
>

<div>

<p class="text-base !text-gray-500 xl:text-lg">
{{ step.day }}
</p>

<h4 class="mt-3 text-[22px] font-semibold leading-tight !text-black xl:text-2xl">
{{ step.title }}
</h4>

<p class="mt-4 leading-relaxed !text-gray-500">
{{ step.description }}
</p>

</div>


<div class="mt-auto flex h-[220px] items-end justify-center">

<img
v-if="step.media.image.src"
:src="step.media.image.src"
:alt="step.media.image.alt"
class="max-h-[250px] w-auto object-contain"
loading="lazy"
draggable="false"
/>

</div>

</div>



<!-- CTA DESKTOP -->

<div
class="fade-item relative overflow-hidden rounded-[32px] bg-[#1B1730] p-8 xl:h-[520px] xl:p-10"
>

<img
:src="ctaData.media.background.src"
alt=""
class="pointer-events-none absolute inset-0 h-full w-full object-cover"
/>

<div
class="absolute inset-0 bg-[linear-gradient(180deg,rgba(20,16,34,0.35)_0%,rgba(44,31,85,0.52)_50%,rgba(74,56,145,0.78)_100%)]"
></div>


<div class="relative z-10 flex h-full flex-col">

<h4
class="text-[30px] font-semibold leading-[0.96] tracking-[-0.03em] text-white xl:text-[40px]"
>
{{ ctaTitleLines[0] }}<br />
{{ ctaTitleLines[1] }}
</h4>


<div class="mt-auto flex h-[240px] items-end justify-center">

<img
v-if="ctaData.media.image.src"
:src="ctaData.media.image.src"
:alt="ctaData.media.image.alt"
class="max-h-[250px] w-auto object-contain"
loading="lazy"
draggable="false"
/>

</div>

</div>

</div>

</div>

</div>


</div>
</div>

</section>
</template>
