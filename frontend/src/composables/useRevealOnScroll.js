export const useRevealOnScroll = () => {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible')
          observer.unobserve(entry.target)
        }
      })
    },
    {
      threshold: 0.2,
    },
  )

  const items = document.querySelectorAll('.fade-item')

  items.forEach((item) => observer.observe(item))
}
