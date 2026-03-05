<template>
  <section
    id="reviews"
    class="overflow-x-hidden bg-[#020205] py-10 sm:py-12 lg:py-16"
    aria-labelledby="reviews-title"
  >
    <div class="mx-auto w-full max-w-[1720px] px-4 sm:px-6 lg:px-10">
      <div class="flex flex-col gap-6 md:flex-row md:items-end md:justify-between">
        <div class="max-w-[640px]">
          <h2
            id="reviews-title"
            class="text-[42px] font-semibold leading-[0.95] tracking-[-0.03em] text-white sm:text-[56px] lg:text-[54px]"
          >
            {{ reviewsData.title }}
            <span class="mt-2 block text-[#A8ADC4]">{{ reviewsData.subtitle }}</span>
          </h2>
        </div>

        <div class="flex items-center gap-3">
          <button
            type="button"
            class="inline-flex h-12 w-12 items-center justify-center rounded-full border border-white/10 bg-[#151723] text-[#D8DBEF] transition hover:border-white/25 hover:bg-[#1A1D2B] disabled:cursor-not-allowed disabled:opacity-40"
            :disabled="currentIndex === 0"
            :aria-label="reviewActions.prevPageAria || 'Предыдущие отзывы'"
            @click="goPrev"
          >
            <svg viewBox="0 0 20 20" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="1.75">
              <path d="M11.75 4.25 6 10l5.75 5.75" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
          </button>

          <button
            type="button"
            class="inline-flex h-12 w-12 items-center justify-center rounded-full border border-white/10 bg-[#151723] text-[#D8DBEF] transition hover:border-white/25 hover:bg-[#1A1D2B] disabled:cursor-not-allowed disabled:opacity-40"
            :disabled="currentIndex >= maxStartIndex"
            :aria-label="reviewActions.nextPageAria || 'Следующие отзывы'"
            @click="goNext"
          >
            <svg viewBox="0 0 20 20" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="1.75">
              <path d="M8.25 4.25 14 10l-5.75 5.75" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
          </button>
        </div>
      </div>

      <div class="mt-10 overflow-hidden sm:mt-12" ref="viewportRef">
        <div
          ref="trackRef"
          class="flex transition-transform duration-500 ease-out"
          :class="isDragging ? 'duration-0' : ''"
          :style="{
            transform: `translate3d(${trackTranslateX}px,0,0)`,
            touchAction: 'pan-y',
          }"
          @pointerdown="onPointerDown"
          @pointermove="onPointerMove"
          @pointerup="onPointerUp"
          @pointercancel="onPointerCancel"
        >
          <div
            v-for="review in reviews"
            :key="review.id"
            class="min-w-0 shrink-0 px-2 sm:px-3"
            :style="{ width: `${100 / slidesPerView}%` }"
          >
            <article
              class="fade-item flex h-full min-w-0 flex-col rounded-[28px] border border-white/5 bg-[#1F2230] p-5 text-left shadow-[0_20px_60px_rgba(0,0,0,0.28)] sm:min-h-[500px] sm:p-8 lg:h-[520px] lg:p-10"
            >
              <div class="min-h-0 flex-1 overflow-hidden">
                <h3 class="break-words text-[28px] font-medium leading-tight tracking-[-0.02em] text-white">
                  {{ review.company }}
                </h3>

                <p class="mt-4 break-words text-[15px] font-semibold leading-snug text-[#A8ADC4]">
                  {{ review.person }}
                </p>

                <div class="mt-6 space-y-4 text-[14px] leading-[1.55] text-[#C4C8DD] sm:text-[15px]">
                  <p v-for="paragraph in review.previewParagraphs" :key="paragraph.id">
                    {{ paragraph.text }}
                  </p>

                  <ul v-if="review.previewBullets?.length" class="list-disc space-y-1.5 pl-5 marker:text-[#A7ACC3]">
                    <li v-for="bullet in review.previewBullets" :key="bullet.id">
                      {{ bullet.text }}
                    </li>
                  </ul>
                </div>
              </div>

              <button
                type="button"
                class="mt-6 inline-flex h-[48px] w-full max-w-full shrink-0 items-center justify-center rounded-[14px] border border-white text-white transition hover:bg-white hover:text-black sm:max-w-[200px]"
                @click="openReview(review)"
              >
                {{ reviewActions.readMore }}
              </button>
            </article>
          </div>
        </div>
      </div>

      <div
        v-if="paginationCount > 1"
        class="mt-6 flex items-center justify-center gap-2"
        :aria-label="reviewActions.paginationAria || 'Пагинация отзывов'"
      >
        <button
          v-for="dot in paginationCount"
          :key="`dot-${dot}`"
          type="button"
          class="h-2 rounded-full transition"
          :class="dot - 1 === currentIndex ? 'w-8 bg-white' : 'w-2 bg-white/25 hover:bg-white/45'"
          :aria-label="`${reviewActions.paginationGoTo || 'Перейти к странице'} ${dot}`"
          :aria-current="dot - 1 === currentIndex ? 'true' : 'false'"
          @click="setIndex(dot - 1)"
        />
      </div>
    </div>
  </section>

  <Teleport to="body">
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="activeReview"
        class="fixed inset-0 z-[220] bg-black/75 p-4 backdrop-blur-sm sm:p-6"
        role="dialog"
        aria-modal="true"
        :aria-labelledby="`review-modal-title-${activeReview.id}`"
        @click.self="closeReview"
      >
        <div class="flex min-h-full items-center justify-center">
          <Transition
            enter-active-class="transition duration-200 ease-out"
            enter-from-class="translate-y-2 scale-[0.98] opacity-0"
            enter-to-class="translate-y-0 scale-100 opacity-100"
            leave-active-class="transition duration-150 ease-in"
            leave-from-class="translate-y-0 scale-100 opacity-100"
            leave-to-class="translate-y-2 scale-[0.98] opacity-0"
            appear
          >
            <div
              v-if="activeReview"
              class="w-full max-w-4xl overflow-hidden rounded-[24px] border border-white/10 bg-[#121420] shadow-[0_30px_100px_rgba(0,0,0,0.55)]"
            >
              <div class="flex items-start justify-between gap-4 border-b border-white/10 px-5 py-5 sm:px-7">
                <div>
                  <h3
                    :id="`review-modal-title-${activeReview.id}`"
                    class="text-2xl font-semibold tracking-[-0.02em] text-white sm:text-[30px]"
                  >
                    {{ activeReview.company }}
                  </h3>
                  <p class="mt-2 text-sm font-medium text-[#A8ADC4] sm:text-base">
                    {{ activeReview.person }}
                  </p>
                </div>

                <button
                  ref="closeButtonRef"
                  type="button"
                  class="inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-white/10 bg-white/5 text-white transition hover:bg-white/10 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/60"
                  :aria-label="reviewActions.closeModalAria"
                  @click="closeReview"
                >
                  <svg viewBox="0 0 20 20" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="1.75">
                    <path d="M5 5l10 10M15 5 5 15" stroke-linecap="round" />
                  </svg>
                </button>
              </div>

              <div class="max-h-[70vh] overflow-y-auto px-5 py-6 sm:px-7 sm:py-7">
                <div class="space-y-5 text-[15px] leading-[1.65] text-[#D4D8EA] sm:text-base">
                  <p v-for="paragraph in activeReview.detailsParagraphs" :key="paragraph.id">
                    {{ paragraph.text }}
                  </p>

                  <div v-if="activeReview.results?.length" class="rounded-2xl border border-white/8 bg-white/3 p-4 sm:p-5">
                    <p class="text-sm font-semibold uppercase tracking-[0.08em] text-[#A8ADC4]">
                      {{ reviewsData.meta.modalResultsTitle }}
                    </p>
                    <ul class="mt-3 list-disc space-y-2 pl-5 marker:text-[#C4C8DD]">
                      <li v-for="result in activeReview.results" :key="result.id">
                        {{ result.text }}
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </Transition>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { siteData } from '~/data/siteData'

const reviewsData = siteData.reviews
const reviews = reviewsData.items
const reviewActions = reviewsData.meta.actions

const viewportRef = ref(null)
const trackRef = ref(null)
const viewportWidth = ref(0)
const viewportPx = ref(0)

const currentIndex = ref(0)
const isDragging = ref(false)
const dragOffsetX = ref(0)

const activeReview = ref(null)
const closeButtonRef = ref(null)
let previousBodyOverflow = ''

let pointerId = null
let startX = 0
let startY = 0
let lockedAxis = null
let resizeObserver = null

const slidesPerView = computed(() => (viewportWidth.value >= 1024 ? 3 : 1))
const maxStartIndex = computed(() => Math.max(0, reviews.length - slidesPerView.value))
const paginationCount = computed(() => maxStartIndex.value + 1)
const slideWidthPx = computed(() => {
  if (!viewportPx.value || !slidesPerView.value) return 0
  return viewportPx.value / slidesPerView.value
})

const trackTranslateX = computed(() => {
  return -(currentIndex.value * slideWidthPx.value) + dragOffsetX.value
})

const clamp = (value, min, max) => Math.min(max, Math.max(min, value))
const setIndex = (value) => {
  currentIndex.value = clamp(value, 0, maxStartIndex.value)
}

const goPrev = () => setIndex(currentIndex.value - 1)
const goNext = () => setIndex(currentIndex.value + 1)

const getSwipeThreshold = () => {
  return clamp((slideWidthPx.value || 320) * 0.18, 40, 140)
}

const resetDragState = () => {
  isDragging.value = false
  dragOffsetX.value = 0
  pointerId = null
  lockedAxis = null
}

const onPointerDown = (event) => {
  if (activeReview.value || maxStartIndex.value === 0) return
  if (event.pointerType === 'mouse' && event.button !== 0) return

  pointerId = event.pointerId
  startX = event.clientX
  startY = event.clientY
  lockedAxis = null
  isDragging.value = true
  dragOffsetX.value = 0
  trackRef.value?.setPointerCapture?.(pointerId)
}

const onPointerMove = (event) => {
  if (!isDragging.value || pointerId !== event.pointerId) return

  const dx = event.clientX - startX
  const dy = event.clientY - startY

  if (!lockedAxis) {
    if (Math.abs(dx) < 6 && Math.abs(dy) < 6) return
    lockedAxis = Math.abs(dx) > Math.abs(dy) ? 'x' : 'y'
  }

  if (lockedAxis === 'y') {
    dragOffsetX.value = 0
    return
  }

  event.preventDefault?.()
  const maxPull = (slideWidthPx.value || 320) * 0.35
  dragOffsetX.value = clamp(dx, -maxPull, maxPull)
}

const finishDrag = () => {
  if (!isDragging.value) return

  const delta = dragOffsetX.value
  const threshold = getSwipeThreshold()

  if (Math.abs(delta) >= threshold) {
    if (delta < 0) goNext()
    else goPrev()
  }

  resetDragState()
}

const onPointerUp = (event) => {
  if (!isDragging.value || pointerId !== event.pointerId) return
  finishDrag()
}

const onPointerCancel = (event) => {
  if (!isDragging.value || pointerId !== event.pointerId) return
  resetDragState()
}

const openReview = async (review) => {
  activeReview.value = review
  await nextTick()
  closeButtonRef.value?.focus()
}

const closeReview = () => {
  activeReview.value = null
}

const updateViewport = () => {
  if (typeof window === 'undefined') return
  viewportWidth.value = window.innerWidth
  viewportPx.value = viewportRef.value?.clientWidth || 0
}

const handleKeydown = (event) => {
  if (event.key === 'Escape' && activeReview.value) {
    closeReview()
    return
  }

  if (activeReview.value) return
  if (event.key === 'ArrowLeft') goPrev()
  if (event.key === 'ArrowRight') goNext()
}

watch([maxStartIndex, slidesPerView], () => {
  setIndex(currentIndex.value)
})

watch(activeReview, (review) => {
  if (typeof document === 'undefined') return

  if (review) {
    previousBodyOverflow = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    return
  }

  document.body.style.overflow = previousBodyOverflow
})

onMounted(() => {
  updateViewport()
  window.addEventListener('resize', updateViewport)
  window.addEventListener('keydown', handleKeydown)

  if ('ResizeObserver' in window && viewportRef.value) {
    resizeObserver = new ResizeObserver(() => {
      viewportPx.value = viewportRef.value?.clientWidth || 0
    })
    resizeObserver.observe(viewportRef.value)
  }
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateViewport)
  window.removeEventListener('keydown', handleKeydown)
  resizeObserver?.disconnect()

  if (typeof document !== 'undefined') {
    document.body.style.overflow = previousBodyOverflow
  }
})
</script>
