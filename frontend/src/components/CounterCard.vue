<script setup>
defineProps({
  counter: {
    type: Number,
    required: true,
  },
})

const emit = defineEmits(['increment'])
</script>

<template>
  <section
    class="rounded-2xl border border-white/10 bg-white/5 p-6 shadow-2xl shadow-black/20 backdrop-blur"
  >
    <p class="text-sm font-medium uppercase tracking-[0.2em] text-cyan-300">Pinia Counter</p>
    <p class="mt-3 text-4xl font-bold text-white">{{ counter }}</p>
    <button
      type="button"
      class="mt-5 inline-flex items-center rounded-xl bg-cyan-400 px-4 py-2 font-semibold text-slate-950 transition hover:bg-cyan-300 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-200"
      @click="emit('increment')"
    >
      Increment
    </button>
  </section>
</template>
