// Centralized mock/content data for all landing sections.
// Keep only display/content data and asset paths here.

const navigationItems = [
  { label: 'Преимущества', href: '#advantages' },
  { label: 'Этапы', href: '#steps' },
  { label: 'Отзывы', href: '#reviews' },
  { label: 'Контакты', href: '#contacts' },
  { label: 'Тарифы', href: '#pricing' },
]

const socialMedia = [
  { id: 'site', name: 'Сайт', icon: '/images/icons/web.svg', href: 'https://example.com' },
  { id: 'telegram', name: 'Telegram', icon: '/images/icons/telegram.svg', href: 'https://example.com' },
  { id: 'avito', name: 'Avito', icon: '/images/icons/avito.svg', href: 'https://example.com' },
  { id: 'instagram', name: 'Instagram', icon: '/images/icons/instagram.svg', href: 'https://example.com' },
  { id: 'facebook', name: 'Facebook', icon: '/images/icons/facebook.svg', href: 'https://example.com' },
  { id: 'whatsapp', name: 'WhatsApp', icon: '/images/icons/whatsapp.svg', href: 'https://example.com' },
  { id: 'youtube', name: 'YouTube', icon: '/images/icons/youtube.svg', href: 'https://example.com' },
  { id: 'tiktok', name: 'TikTok', icon: '/images/icons/tiktok.svg', href: 'https://example.com' },
  { id: 'mail', name: 'Mail', icon: '/images/icons/mail.svg', href: 'https://example.com' },
  { id: 'vk', name: 'ВКонтакте', icon: '/images/icons/vk.svg', href: 'https://example.com' },
  { id: 'max', name: 'Max', icon: '/images/icons/Max.svg', href: 'https://example.com' },
]

const legacyData = {
  // SECTION: shared/assets/events
  // Contains reusable asset paths and event names used across multiple sections.
  events: {
    contactFormOpen: 'contact-feedback-form:open',
  },

  assets: {
    icons: {
      check: '/images/vecor.svg',
    },
    images: {
      logo: '/images/logo.png',
      heroPhone: '/images/hiro.png',
      heroTexture: '/images/tilda.png',
      socialPhone: '/images/dialog.png',
      socialPhoneSecondary: '/images/dialog2.png',
      sectionBackground: '/images/bg-fon.png',
      ctaBackground: '/images/bg.png',
      integrationsBanner: '/images/banner.png',
      integrationsStepDay1: '/images/13.png',
      integrationsStepDay2: '/images/11.png',
      integrationsStepDay3: '/images/12.png',
      integrationsStepDay4: '/images/icon icon.png',
      integrationsStepMonthly: '/images/10.png',
    },
  },

  // SECTION: header
  // Top navigation, brand and mobile menu metadata.
  header: {
    brandName: '4Business',
    brandHref: '/',
    navItems: navigationItems,
    aria: {
      desktopNav: 'Основная навигация',
      mobileNav: 'Мобильная навигация',
      mobileDialog: 'Мобильное меню',
      openMenu: 'Открыть меню',
      closeMenu: 'Закрыть меню',
    },
    mobileSocialItems: [
      { id: 'whatsapp', label: 'WhatsApp', href: '#' },
      { id: 'instagram', label: 'Instagram', href: '#' },
      { id: 'telegram', label: 'Telegram', href: '#' },
    ],
  },

  // SECTION: footer
  // Footer branding, navigation, contacts and legal links.
  footer: {
    brandName: 'Ai4Business',
    brandHref: '/',

   
    legalItems: [
      { label: 'Политика конфиденциальности', href: '#' },
      { label: 'Публичная оферта', href: '#' },
      { label: 'Пользовательское соглашение', href: '#' },
    ],
  },

  // SECTION: hero
  // Hero headings, descriptive copy, metrics and image config vars.
  hero: {
    titleLines: ['ИИ отдел продаж', 'для вашего бизнеса'],
    description: 'Отвечает мгновенно 24/7 на всех языках тысячам клиентов одновременно',
    statsDisclaimer:
      'Средние показатели конверсии основаны на анализе более 3 000 веб-сайтов, использующих наш AI Chatbot.',
    phoneAlt: 'Интерфейс переписки в мессенджере на смартфоне',
    stats: [
      { value: '260%', label: 'Рост конверсии веб-сайта' },
      { value: '72%', label: 'Конверсия из чата в горячий лид' },
      { value: '210%', label: 'Улучшение качества входящих лидов' },
    ],
    imageVars: {
      mobile: {
        '--hiro-mobile-w': '320px',
        '--hiro-mobile-max-w': '86vw',
        '--hiro-mobile-w-sm': '360px',
        '--hiro-mobile-max-w-sm': '80vw',
      },
      desktop: {
        '--hiro-desktop-right': '50px',
        '--hiro-desktop-bottom': '-100px',
        '--hiro-desktop-w': '600px',
        '--hiro-desktop-w-xl': '600px',
        '--hiro-desktop-w-2xl': '600px',
      },
      floatingBadges: {
        '--hero-badges-left': '2%',
        '--hero-badges-top': '49%',
      },
    },
  },

  // SECTION: hero-logos
  // Partner/brand logo strip under hero.
  heroLogos: {
    logos: ['/images/1.svg', '/images/2.svg', '/images/3.svg', '/images/4.svg', '/images/5.svg'],
  },

  // SECTION: what-seller-can (advantages)
  // Comparison content, training sources and explanatory copy.
  whatSellerCan: {
    stats: [
      { value: '0 тг', text: 'за установку ИИ' },
      { value: '100%', text: 'верификация от meta, google,\namocrm, bitrix и другие' },
      { value: '24/7', text: 'поддержка от проектных\nменеджеров' },
    ],
    training: {
      badge: 'Обучение ИИ на ваших данных',
      dataSources: [
        'Сайт',
        'Прайс-листы',
        'Товары и услуги',
        'Лучшие диалоги',
        'Скрипты',
        'FAQ',
        'Товарные фиды',
      ],
      rightPill: 'С первой минуты готов к работе',
      rightTitle:
        'ИИ-продажник с первой минуты работы знает про вашу компанию и продукт больше и лучше любого вашего самого опытного менеджера.',
      rightBullets: [
        'Отвечает по вашей продуктовой логике и терминологии',
        'Использует знания из лучших диалогов и скриптов продаж',
        'Работает с актуальными данными компании и ассортимента',
      ],
    },
    summary: {
     
      title: 'Эффективные растут не эффективные исчезают',
      desktopStageLabel: 'Этап',
      desktopAiLabel: 'ИИ-отдел продаж',
      desktopHumanLabel: 'Менеджер',
      mobileTitle: 'Сравнение по этапам',
      mobileSubtitle: 'Прокрути — детали ниже.',
      mobileAiLabel: 'ИИ-отдел продаж',
      mobileHumanLabel: 'Менеджер',
      mobileFooter: 'Итог: ИИ берёт поток, менеджер — закрывает.',
    },
    compareRows: [
      {
        label: 'Консультация',
        ai: 'Обучен на всей базе знаний компании и отвечает точно по любому товару или услуге с первой минуты.',
        human: 'Знает только основные позиции и отвечает в рамках своего опыта.',
      },
      {
        label: 'Прогрев клиента',
        ai: 'Системно выявляет потребность, после ответа всегда задаёт вопрос и подводит к целевому действию. Готов бесконечно разговаривать с клиентом.',
        human: 'Ведёт диалог по скрипту и зависит от настроения и загрузки. Выдыхается после 10 диалогов.',
      },
      {
        label: 'Дожим и возражения',
        ai: 'Дожимает до сделки: не «ну-у-у…», не «давайте потом». Обучен практикам продаж и найдёт 1001 способ обойти возражение.',
        human: 'Дожимает по настроению: спорит, давит, «выдыхается», уводит в «хорошо, давайте позже» и переносит.',
      },
      {
        label: 'Доппродажа',
        ai: 'Автоматически предлагает сопутствующие товары и увеличивает средний чек.',
        human: 'Предлагает дополнительные товары, если вспомнит.',
      },
      {
        label: 'Скорость ответа',
        ai: 'Отвечает за 1–5 секунд, 24/7.',
        human: 'Отвечает, когда освободится.',
      },
      {
        label: 'Одновременные диалоги',
        ai: 'Тысячи диалогов одновременно без потери качества.',
        human: '1–3 активных клиента одновременно.',
      },
      {
        label: 'Знание языков',
        ai: 'Тысячи языков — на каком пишет клиент, на таком и отвечает.',
        human: '1–3 языка максимум.',
      },
      {
        label: 'Этапы сделки',
        ai: 'Передаёт горячего клиента вашему менеджеру для закрытия сделки, поднимая мотивацию.',
        human: 'Устаёт от квалификации, тратит энергию на прогрев, не остаётся сил на дожим и закрытие сделки.',
      },
    ],
    aiSummary: [
      'Отвечает за 1–5 секунд 24/7 без перерывов и выходных',
      'Масштабируется на тысячи диалогов одновременно без потери качества',
      'Ведёт клиента по воронке: выявляет потребность и подводит к целевому действию',
      'Дожимает и отрабатывает возражения — без усталости и «давайте потом»',
      'Автоматически допродаёт и увеличивает средний чек',
      'Знает продукт: обучается на базе знаний, скриптах, диалогах, FAQ',
      'Говорит на языке клиента (много языков) и соблюдает терминологию компании',
      'Передаёт «горячих» лидов менеджеру на закрытие сделки',
    ],
    humanLimits: [
      'Ограничен временем: не 24/7, отвечает с задержкой',
      'Быстро выдыхается при потоке — падает качество',
      'Чаще действует по скрипту и настроению, зависит от загрузки',
      'Не держит в голове весь ассортимент и нюансы продукта',
    ],
  },

  // SECTION: ai-value
  // Value proposition cards and integrations list.
  aiValue: {
    title: 'ИИ — не статья расходов',
    subtitlePrefix: 'а',
    subtitleHighlight: 'источник дохода',
    launch: {
      badgePrimary: '7 дней теста',
      badgeSecondary: 'Без риска для бизнеса',
      
      description:
        'Вы получаете обучение, интеграции, поддержку и тестовый период до оплаты. Решение должно показать ценность в бизнесе, а не просто красиво выглядеть.',
      leftLabel: '0 Р',
      rightLabel: 'По подписке',
      valuePoints: [
        'Бесплатное обучение ИИ-продавца на ваших данных',
        'Безлимитное количество диалогов',
        'Настройка и интеграция всех каналов и сервисов',
        'Донастройка с сопровождением на всём периоде использования',
        'Тестовый период 7 дней без рисков',
      ],
      paidTitle: 'Платите только ежемесячную подписку',
      paidDescription:
        'Оплата начинается только после теста и подтверждения результата. Никаких разовых платежей за запуск — только ежемесячная подписка за использование и сопровождение.',
      noteDescription:
        'Подключаете подписку только если видите ценность для бизнеса',
    },
    integrations: {
      
      title: 'ИИ продажник получает и передает данные почти с любых источников',
      addAriaLabel: 'Добавить',
      rows: [
        {
          title: 'Интеграция с CRM',
          desc: 'Двигает этапы сделки, заполняет поля и ставит задачи',
          img:'/images/banner 3.png'
        },
        {
          title: 'Запись клиентов',
          desc: 'Назначает клиентам встречи и записи',
          img:'/images/banner.png'
        },
        {
          title: 'Товарные фиды',
          desc: 'Знает остатки по товарам на складе',
          img:'/images/tovar_fids.png'
        },
        {
          title: 'Slack',
          desc: 'Уведомления, управление беседами, совместная работа',
          img:'/images/slack.png'
        },
        {
          title: 'Google Analytics и Яндекс Метрика/Аналитика',
          desc: 'События, цели и отчёты по эффективности каналов',
          img:'/images/yandex_google.png'
        },
        {
          title: 'Пользовательские вебхуки и API-интеграции',
          desc: 'Подключение любых систем через API и вебхуки',
          img:'/images/api.png'
        },
      ],
    },
  },

  // SECTION: social-media (omnichannel card inside AI value area)
  // Channels list and media resources for omnichannel block.
  socialMedia: {
    pill: 'Омниканальность',
    title: '',
    description:
      'ИИ продажник работает во всех точках контакта с клиентом. Под каждый канал можно сделать свою роль: продажник, консультант, техподдержка',
    phoneAlt: 'Превью телефона',
  },

  // SECTION: integration-steps
  // Timeline cards and CTA texts for implementation stages.
  integrationSteps: {
    title: 'Этапы интеграции',
    subtitle: 'ИИ-продавца',
    ctaTitle: 'От брифинга до\nИИ-продаж за 7 дней',
    ctaButtonLabel: 'Оставить заявку',
    steps: [
      {
        day: 'День 1',
        title: 'Брифинг',
        desc: 'Проводим интервью, узнаем все необходимое для настройки бота',
        image: '/images/13.png',
      },
      {
        day: 'День 2-5',
        title: 'Создание бота',
        desc: 'Технические и sales-специалисты разрабатывают логику и сценарии работы AI-продавца',
        image: '/images/11.png',
      },
      {
        day: 'День 6',
        title: 'Тестирование чат-бота',
        desc: 'Создаем прототип бота и проводим тестирование сценариев общения',
        image: '/images/12.png',
      },
      {
        day: 'День 7',
        title: 'Релиз чат-бота',
        desc: 'Подключаем чат-бота ко всем мессенджерам и интегрируем в вашу CRM',
        image: '/images/icon icon.png',
      },
      {
        day: 'Каждый месяц',
        title: 'Поддержка и аналитика',
        desc: 'Следим за качеством ответов и предоставляем отчеты о работе ИИ-продавца',
        image: '/images/10.png',
      },
      {
        imageSrc: '/images/briffing.png',
        // TODO: Replace with real Telegram/WhatsApp URLs.
        
      },
    ],
  },

  // SECTION: pricing
  // Pricing section headings and all plan cards.
  pricing: {
    title: 'Тарифы',
    subtitle: 'Выберите пакет под ваш бизнес',
    plans: [
      {
        key: 'smart',
        name: 'SMART AI',
        topBadge: 'Для сайта',
        channels: 'Сайт',
        ctaLabel: 'Оставить заявку',
        features: [
          'До 250 страниц сканирования сайта',
          'Настройка кнопки виджета',
          'Email-отчёт по лидам',
          'Лиды в Telegram',
          'Панель управления',
          'Настраиваемые ответы ИИ',
        ],
      },
      {
        key: 'pro',
        name: 'PRO AI',
        topBadge: 'Сайт + Meta',
        accentBadge: 'Популярный',
        inheritLine: '(всё из SMART +)',
        channels: 'Сайт + Meta',
        ctaLabel: 'Оставить заявку',
        featured: true,
        features: [
          'До 500 страниц сканирования сайта',
          'История бесед с клиентом',
          'Полная аналитика',
          'Интеграция Google Analytics + GTM',
          'Встроенная CRM',
          'Интеграция с популярными CRM',
          'Каталог товаров (1 фид, до 100 товаров)',
          'Синхронизация с товарными остатками каждые 24 часа',
          'Meta: инстаграм, фейсбук, ватсап',
        ],
      },
      {
        key: 'mega',
        name: 'MEGA AI',
        topBadge: 'Максимум каналов',
        accentBadge: 'Лучший выбор',
        inheritLine: '(всё из PRO +)',
        channels: 'Сайт + Meta + Telegram, VK, Max + YouTube + TikTok',
        ctaLabel: 'Оставить заявку',
        features: [
          'До 2 000 страниц сканирования сайта',
          'До 3 товарных фидов',
          'До 10 000 товаров',
          'Синхронизация c товарными остатками каждые 6 часов',
          'Интеграция с Avito',
          'Интеграция с системами бронирования Google Календарь, YClients',
          'Telegram, VK, Max — компаньон',
          'YouTube, TikTok — компаньон в комментариях',
          'Улучшенная версия ИИ',
        ],
      },
      {
        key: 'enterprise',
        name: 'ENTERPRISE',
        topBadge: 'Для корпораций',
        accentBadge: 'Максимум',
        inheritLine: '(всё из MEGA +)',
        channels: 'Полное масштабирование под крупный бизнес',
        ctaLabel: 'Оставить заявку',
        darkCard: true,
        features: [
          'До 10 000 страниц сканирования сайта',
          'До 10 товарных фидов',
          'До 200 000 товаров',
          'Синхронизация каждый 1 час',
          'Выделенная поддержка',
          'До 3 сайтов',
          'Индивидуальные интеграции',
        ],
      },
    ],
  },

  // SECTION: reviews
  // Testimonials section labels and review records used by slider + modal.
  reviews: {
    titleMain: 'Нам доверили.',
    titleAccent: 'И не пожалели.',
    actions: {
      readMore: 'Читать далее',
      closeModalAria: 'Закрыть окно отзыва',
      prevPageAria: 'Предыдущая группа отзывов',
      nextPageAria: 'Следующая группа отзывов',
      paginationAria: 'Индикатор страниц отзывов',
      paginationGoTo: 'Перейти к странице отзывов',
    },
    modalResultsTitle: 'Результаты',
    items: [
      {
        id: 'nova-invest',
        company: 'Nova Invest',
        person: 'Андрей, руководитель отдела продаж Nova Invest',
        previewParagraphs: [
          'Подключили  Ai4Business для первичной консультации и квалификации обращений с сайта. Поток стал обрабатываться быстрее, а менеджеры перестали тонуть в рутине.',
        ],
        previewBullets: [
          'сократили время первого ответа до секунд',
          'стало меньше «пустых» обращений в отделе продаж',
          'клиенты чаще доходят до заявки/звонка',
          'стали стабильнее показатели в выходные и вечером',
        ],
        detailsParagraphs: [
          'Нам было важно быстро отвечать и при этом не терять качество: клиенты часто задают похожие вопросы и ждут понятного, уверенного ответа.',
          ' Ai4Business взял на себя первичный диалог, уточнение потребностей и сбор контактов. Дальше менеджеры подключаются уже к «тёплым» лидам.',
          'Понравилось, что сценарии подстроили под нашу лексику и правила общения: без воды, по делу, с корректной подачей.',
          'В первые дни после запуска оперативно допилили ответы и формулировки — это сильно ускорило выход на стабильный результат.',
        ],
        results: [
          'Быстрый первый ответ на обращения с сайта',
          'Снижение нагрузки на менеджеров на первичном этапе',
          'Больше квалифицированных лидов в работе',
          'Стабильная обработка заявок вне рабочего времени',
        ],
      },
      {
        id: 'oknabutik',
        company: 'ОкнаБутик',
        person: 'Марина, менеджер по развитию ОкнаБутик',
        previewParagraphs: [
          'Запустили  Ai4Business, чтобы не терять заявки на расчёт и консультации. Клиенты получают ответы мгновенно, а мы — структурированные данные для расчёта.',
        ],
        previewBullets: [
          'быстрее собираем параметры запроса',
          'меньше «пропущенных» сообщений',
          'менеджеры подключаются уже на этапе расчёта',
        ],
        detailsParagraphs: [
          'Раньше значительная часть времени уходила на повторяющиеся вопросы и уточнение базовых параметров. Это тормозило расчёт и снижало конверсию.',
          'Теперь  Ai4Business задаёт правильные вопросы по порядку, фиксирует ответы и передаёт менеджеру уже подготовленный запрос.',
          'Отдельно отмечу аккуратный стиль общения: без навязчивости, при этом уверенно ведёт клиента к следующему шагу.',
        ],
        results: [
          'Ускорение сбора данных для расчёта',
          'Снижение доли потерянных обращений',
          'Больше подготовленных заявок для менеджера',
        ],
      },
      {
        id: 'mob-md',
        company: 'MOB.md',
        person: 'Денис, операционный менеджер MOB.md',
        previewParagraphs: [
          'Подключили  Ai4Business для поддержки и консультаций по услугам/продукту. Стало меньше ожидания, а повторяющиеся вопросы закрываются автоматически.',
        ],
        previewBullets: [
          'меньше нагрузки на поддержку',
          'быстрее ответы по типовым запросам',
          'люди чаще доходят до целевого действия',
        ],
        detailsParagraphs: [
          'Основной запрос был простой: ускорить ответы и разгрузить команду. В часы пик поддержка не успевала, часть клиентов уходила.',
          ' Ai4Business закрывает типовые вопросы и помогает пользователю сделать следующий шаг: оформить заявку, уточнить детали, оставить контакт.',
          'Самое ценное — стабильность: качество ответа не «плывёт» от усталости, и клиент всегда получает понятную навигацию.',
        ],
        results: [
          'Сокращение времени ожидания ответа',
          'Снижение нагрузки на операторов/менеджеров',
          'Рост доли обращений, доведённых до заявки',
        ],
      },
      {
        id: 'academkids',
        company: 'AcademKids',
        person: 'Ольга, администратор AcademKids',
        previewParagraphs: [
          ' Ai4Business автоматизировал первичную запись и ответы на частые вопросы родителей. Теперь заявки не теряются вечером и в выходные.',
        ],
        previewBullets: [
          'запись работает 24/7',
          'быстрее собираем данные для администратора',
          'родители получают понятные ответы сразу',
        ],
        detailsParagraphs: [
          'В сфере обучения очень важна скорость реакции: родитель написал — хочет ответ сейчас. Раньше это зависело от загруженности администратора.',
          ' Ai4Business уточняет возраст, формат, интересующее направление, удобное время и передаёт нам уже готовую заявку.',
          'После запуска мы быстро подправили формулировки под наш тон общения и получили ровный, «брендовый» стиль диалога.',
        ],
        results: [
          'Стабильная запись 24/7',
          'Больше заявок с корректными данными',
          'Меньше ручной рутины у администратора',
        ],
      },
      {
        id: 'ru-biss',
        company: 'RU-BISS',
        person: 'Илья, руководитель проектов RU-BISS',
        previewParagraphs: [
          'Внедрили  Ai4Business для первичной консультации и маршрутизации обращений. Теперь клиент быстрее попадает в нужный сценарий, а менеджеры — в нужную задачу.',
        ],
        previewBullets: [
          'быстрее квалификация и распределение',
          'меньше разрозненных диалогов',
          'понятная логика общения и фиксация данных',
        ],
        detailsParagraphs: [
          'Нам важно, чтобы клиент сразу получал корректный ответ и понимал дальнейшие шаги.  Ai4Business помогает держать одинаковое качество коммуникации.',
          'Сценарии настроили так, чтобы бот задавал вопросы по делу и не перегружал клиента лишними деталями.',
          'После внедрения стало проще контролировать входящий поток: диалоги стали структурированными, а менеджеры получили фокус на закрытии.',
        ],
        results: [
          'Ускорение квалификации входящих обращений',
          'Снижение хаоса в коммуникациях',
          'Рост доли обращений, доведённых до следующего шага',
        ],
      },
      {
        id: 'pokolenie-plus',
        company: 'Поколение+',
        person: 'Светлана, управляющая Поколение+',
        previewParagraphs: [
          ' Ai4Business помог закрыть первичную коммуникацию: ответы на вопросы, запись/заявки и сбор контактов. В результате меньше пропущенных обращений.',
        ],
        previewBullets: [
          'клиенты получают ответ сразу',
          'всё фиксируется и ничего не теряется',
          'команда тратит время на важное, а не на рутину',
        ],
        detailsParagraphs: [
          'Мы искали решение, которое будет вежливо и понятно общаться, но при этом вести клиента к конкретному действию.',
          ' Ai4Business справился: уточняет запрос, даёт ответы, помогает записаться/оставить заявку и передаёт контакт нам.',
          'Особенно заметен эффект вне рабочего времени — когда раньше часть обращений просто «сгорала».',
        ],
        results: [
          'Сокращение пропущенных обращений',
          'Более стабильный поток заявок в нерабочее время',
          'Разгрузка сотрудников от повторяющихся вопросов',
        ],
      },
    ],
  },

  // SECTION: contacts (contact-feedback section)
  // Contact CTA block, messenger links and modal form labels/placeholders.
  contacts: {
    heading: {
      line1: 'Готовы увеличить эффективность',
      accent: 'и опередить конкурентов?',
      line3: 'Свяжитесь с нами',
    },
    description:
      "",
    card: {
      titleLine1: 'Выберите удобный',
      titleLine2: 'канал связи',
      responseTime: '',
    },
    links: {
      whatsapp: {
        href: 'https://wa.me/',
        icon: '/images/icons/whatsapp.svg',
        
        message:
          'Здравствуйте! Хочу увеличить эффективность продаж с помощью ИИ. Подскажите, что нужно для старта?',
        label: 'WhatsApp',
        ariaLabel: 'Написать в WhatsApp',
      },
      telegram: {
        href: 'https://t.me/',
        icon: '/images/icons/telegram.svg',
        
        label: 'Telegram',
        ariaLabel: 'Написать в Telegram',
      },
    },
    form: {
      title: 'Оставить заявку',
      subtitle: 'Мы свяжемся с вами и подберём оптимальный формат внедрения.',
      labels: {
        name: 'Имя',
        contact: 'Телефон / Email',
        comment: 'Комментарий',
      },
      placeholders: {
        name: 'Введите имя',
        contact: '+7 (...) или email',
        comment: 'Кратко опишите задачу',
      },
      submitLabel: 'Отправить заявку',
      closeAriaLabel: 'Закрыть форму',
    },
  },
}

const ensureModelItems = (items = [], mapItem = (item) => item) =>
  items.map((item, index) => ({
    sortOrder: index + 1,
    isActive: true,
    ...mapItem(item, index),
  }))

const mapTextItems = (items = [], prefix) =>
  ensureModelItems(items, (text, index) => ({
    id: `${prefix}-${index + 1}`,
    slug: `${prefix}-${index + 1}`,
    text,
  }))

const socialIconsById = Object.fromEntries(socialMedia.map((item) => [item.id, item.icon]))

const navItems = ensureModelItems(legacyData.header.navItems, (item) => ({
  id: `nav-${item.href.replace('#', '')}`,
  slug: item.href.replace('#', ''),
  label: item.label,
  href: item.href,
}))

const socialChannelItems = ensureModelItems(socialMedia, (item) => ({
  id: `channel-${item.id}`,
  slug: item.id,
  name: item.name,
  href: item.href,
  icon: {
    src: item.icon,
    alt: item.name,
  },
}))

const mobileSocialItems = ensureModelItems(legacyData.header.mobileSocialItems, (item) => ({
  id: `mobile-social-${item.id}`,
  slug: item.id,
  label: item.label,
  href: item.href,
  ariaLabel: item.label,
  icon: {
    src: socialIconsById[item.id] || '',
    alt: item.label,
  },
}))

const integrationPrimarySteps = legacyData.integrationSteps.steps.slice(0, 5)
const integrationCtaStep = legacyData.integrationSteps.steps[5] || {}

const pricingItems = ensureModelItems(legacyData.pricing.plans, (plan) => ({
  id: `pricing-${plan.key}`,
  slug: plan.key,
  title: plan.name,
  subtitle: plan.topBadge,
  
  channels: plan.channels,
  accentBadge: plan.accentBadge || '',
  inheritLine: plan.inheritLine || '',
  meta: {
    featured: Boolean(plan.featured),
    darkCard: Boolean(plan.darkCard),
  },
  cta: {
    id: `pricing-${plan.key}-cta`,
    slug: `pricing-${plan.key}-cta`,
    label: plan.ctaLabel,
    href: '#contacts',
    sortOrder: 1,
    isActive: true,
  },
  features: mapTextItems(plan.features || [], `pricing-${plan.key}-feature`),
}))

const reviewItems = ensureModelItems(legacyData.reviews.items, (review) => ({
  id: `review-${review.id}`,
  slug: review.id,
  company: review.company,
  person: review.person,
  previewParagraphs: mapTextItems(review.previewParagraphs || [], `${review.id}-preview-paragraph`),
  previewBullets: mapTextItems(review.previewBullets || [], `${review.id}-preview-bullet`),
  detailsParagraphs: mapTextItems(review.detailsParagraphs || [], `${review.id}-details-paragraph`),
  results: mapTextItems(review.results || [], `${review.id}-result`),
  media: {

  },
  meta: {
    rating: null,
  },
}))

const contactMessengers = ensureModelItems(
  [
    { key: 'whatsapp', ...legacyData.contacts.links.whatsapp },
    { key: 'telegram', ...legacyData.contacts.links.telegram },
  ],
  (item) => ({
    id: `messenger-${item.key}`,
    slug: item.key,
    name: item.label,
    label: item.label,
    href: item.href,
    icon: {
      src: item.icon,
      alt: item.label,
    },
    ariaLabel: item.ariaLabel,
  }),
)

const footerLegalLinks = ensureModelItems(legacyData.footer.legalItems, (item, index) => ({
  id: `footer-legal-${index + 1}`,
  slug: `legal-${index + 1}`,
  label: item.label,
  href: item.href,
}))

const footerColumns = ensureModelItems([
  {
    id: 'footer-column-navigation',
    slug: 'navigation',
    title: 'Навигация',
    links: navItems.map((item) => ({
      id: `footer-${item.id}`,
      slug: item.slug,
      label: item.label,
      href: item.href,
      sortOrder: item.sortOrder,
      isActive: item.isActive,
    })),
  },
  {
    id: 'footer-column-legal',
    slug: 'legal',
    title: 'Документы',
    links: footerLegalLinks,
  },
])

const assetRegistry = ensureModelItems([
  { id: 'asset-logo', slug: 'logo', src: legacyData.assets.images.logo, alt: legacyData.header.brandName },
  { id: 'asset-hero-phone', slug: 'hero-phone', src: legacyData.assets.images.heroPhone, alt: legacyData.hero.phoneAlt },
  { id: 'asset-hero-texture', slug: 'hero-texture', src: legacyData.assets.images.heroTexture, alt: '' },
  { id: 'asset-social-phone', slug: 'social-phone', src: legacyData.assets.images.socialPhone, alt: legacyData.socialMedia.phoneAlt },
  {
    id: 'asset-social-phone-secondary',
    slug: 'social-phone-secondary',
    src: legacyData.assets.images.socialPhoneSecondary,
    alt: `${legacyData.socialMedia.phoneAlt} 2`,
  },
  { id: 'asset-section-background', slug: 'section-background', src: legacyData.assets.images.sectionBackground, alt: '' },
  { id: 'asset-cta-background', slug: 'cta-background', src: legacyData.assets.images.ctaBackground, alt: '' },
  { id: 'asset-integrations-banner', slug: 'integrations-banner', src: legacyData.assets.images.integrationsBanner, alt: '' },
  { id: 'asset-check', slug: 'check', src: legacyData.assets.icons.check, alt: '' },
  ...ensureModelItems(legacyData.heroLogos.logos, (logo, index) => ({
    id: `asset-hero-logo-${index + 1}`,
    slug: `hero-logo-${index + 1}`,
    src: logo,
    alt: '',
  })),
  ...ensureModelItems(socialMedia, (item) => ({
    id: `asset-social-icon-${item.id}`,
    slug: `social-icon-${item.id}`,
    src: item.icon,
    alt: item.name,
  })),
])

export const siteData = {
  meta: {
    brandName: legacyData.header.brandName,
    siteName: legacyData.header.brandName,
    description: legacyData.hero.description,
    locale: 'ru-RU',
    theme: 'light',
    supportEmail: legacyData.footer.supportEmail,
  },

  events: legacyData.events,

  assets: {
    id: 'assets',
    title: 'Asset Registry',
    
    description: 'Реестр медиа, которые используются в лендинге.',
    items: assetRegistry,
    cta: null,
    media: {
      logo: { src: legacyData.assets.images.logo, alt: legacyData.header.brandName },
      heroPhone: { src: legacyData.assets.images.heroPhone, alt: legacyData.hero.phoneAlt },
      heroTexture: { src: legacyData.assets.images.heroTexture, alt: '' },
      socialPhone: { src: legacyData.assets.images.socialPhone, alt: legacyData.socialMedia.phoneAlt },
      socialPhoneSecondary: { src: legacyData.assets.images.socialPhoneSecondary, alt: `${legacyData.socialMedia.phoneAlt} 2` },
      sectionBackground: { src: legacyData.assets.images.sectionBackground, alt: '' },
      ctaBackground: { src: legacyData.assets.images.ctaBackground, alt: '' },
      integrationsBanner: { src: legacyData.assets.images.integrationsBanner, alt: '' },
      integrationsStepDay1: { src: legacyData.assets.images.integrationsStepDay1, alt: 'Брифинг' },
      integrationsStepDay2: { src: legacyData.assets.images.integrationsStepDay2, alt: 'Создание бота' },
      integrationsStepDay3: { src: legacyData.assets.images.integrationsStepDay3, alt: 'Тестирование чат-бота' },
      integrationsStepDay4: { src: legacyData.assets.images.integrationsStepDay4, alt: 'Релиз чат-бота' },
      integrationsStepMonthly: { src: legacyData.assets.images.integrationsStepMonthly, alt: 'Поддержка и аналитика' },
      integrationsCtaImage: { src: integrationCtaStep.imageSrc || '', alt: 'Брифинг' },
      checkIcon: { src: legacyData.assets.icons.check, alt: '' },
    },
    meta: {},
  },

  nav: {
    id: 'nav',
    items: navItems,
    cta: null,
    media: {
      logo: { src: legacyData.assets.images.logo, alt: legacyData.header.brandName },
    },
    meta: {
      brandHref: legacyData.header.brandHref,
      aria: legacyData.header.aria,
      mobileSocials: mobileSocialItems,
    },
  },

  hero: {
    id: 'hero',
    title: legacyData.hero.titleLines[0],
    subtitle: legacyData.hero.titleLines[1],
    description: legacyData.hero.description,
    items: ensureModelItems(legacyData.hero.stats, (item, index) => ({
      id: `hero-stat-${index + 1}`,
      slug: `hero-stat-${index + 1}`,
      value: item.value,
      text: item.label,
    })),
    cta: null,
    media: {
      image: { src: legacyData.assets.images.heroPhone, alt: legacyData.hero.phoneAlt },
      texture: { src: legacyData.assets.images.heroTexture, alt: '' },
    },
    meta: {
      statsDisclaimer: legacyData.hero.statsDisclaimer,
      imageVars: legacyData.hero.imageVars,
    },
  },

  heroLogos: {
    id: 'hero-logos',
    
    items: ensureModelItems(legacyData.heroLogos.logos, (logo, index) => ({
      id: `hero-logo-${index + 1}`,
      slug: `hero-logo-${index + 1}`,
      src: logo,
      alt: '',
    })),
    cta: null,
    media: {},
    meta: {},
  },

  advantages: {
    id: 'advantages',
    title: legacyData.whatSellerCan.training.badge,
    subtitle: legacyData.whatSellerCan.summary.title,
    description: legacyData.whatSellerCan.summary.desktopFooter,
    items: ensureModelItems(legacyData.whatSellerCan.compareRows, (row, index) => ({
      id: `advantage-row-${index + 1}`,
      slug: `advantage-row-${index + 1}`,
      title: row.label,
      aiDescription: row.ai,
      humanDescription: row.human,
    })),
    cta: null,
    media: {
      icon: { src: legacyData.assets.icons.check, alt: '' },
    },
    meta: {
      training: {
        id: 'advantages-training',
        title: legacyData.whatSellerCan.training.badge,
        
        items: ensureModelItems(legacyData.whatSellerCan.training.dataSources, (text, index) => ({
          id: `training-source-${index + 1}`,
          slug: `training-source-${index + 1}`,
          title: text,
        })),
        cta: null,
        media: {
          icon: { src: legacyData.assets.icons.check, alt: '' },
        },
        meta: {
          rightPill: legacyData.whatSellerCan.training.rightPill,
          rightTitle: legacyData.whatSellerCan.training.rightTitle,
          rightBullets: mapTextItems(legacyData.whatSellerCan.training.rightBullets, 'training-right-bullet'),
        },
      },
      summary: {
        id: 'advantages-summary',
        title: legacyData.whatSellerCan.summary.title,
        subtitle: legacyData.whatSellerCan.summary.kicker,
       
        items: [],
        cta: null,
        media: {},
        meta: {
          ...legacyData.whatSellerCan.summary,
          
        },
      },
      aiSummary: mapTextItems(legacyData.whatSellerCan.aiSummary, 'ai-summary'),
      humanLimits: mapTextItems(legacyData.whatSellerCan.humanLimits, 'human-limit'),
    },
  },

  aiValue: {
    id: 'ai-value',
    title: legacyData.aiValue.title,
    subtitle: `${legacyData.aiValue.subtitlePrefix} ${legacyData.aiValue.subtitleHighlight}`.trim(),
    description: '',
    items: mapTextItems(legacyData.aiValue.launch.valuePoints, 'ai-value-point'),
    cta: null,
    media: {
      integrationsBanner: { src: legacyData.assets.images.integrationsBanner, alt: '' },
    },
    meta: {
      subtitlePrefix: legacyData.aiValue.subtitlePrefix,
      subtitleHighlight: legacyData.aiValue.subtitleHighlight,
      launch: {
        id: 'ai-value-launch',
        title: legacyData.aiValue.launch.title,
        
        description: legacyData.aiValue.launch.description,
        items: [],
        cta: null,
        media: {},
        meta: {
          badgePrimary: legacyData.aiValue.launch.badgePrimary,
          badgeSecondary: legacyData.aiValue.launch.badgeSecondary,
          leftLabel: legacyData.aiValue.launch.leftLabel,
          rightLabel: legacyData.aiValue.launch.rightLabel,
          paidTitle: legacyData.aiValue.launch.paidTitle,
          paidDescription: legacyData.aiValue.launch.paidDescription,
          noteTitle: legacyData.aiValue.launch.noteTitle,
          noteDescription: legacyData.aiValue.launch.noteDescription,
        },
      },
      integrations: {
        id: 'ai-value-integrations',
        title: legacyData.aiValue.integrations.title,
        subtitle: legacyData.aiValue.integrations.pill,
       
        items: ensureModelItems(legacyData.aiValue.integrations.rows, (row, index) => ({
          id: `integration-row-${index + 1}`,
          slug: `integration-row-${index + 1}`,
          title: row.title,
          description: row.desc,
          media: {
            image: { src: row.img || legacyData.assets.images.integrationsBanner, alt: '' },
          },
        })),
        cta: null,
        media: {
          banner: { src: legacyData.assets.images.integrationsBanner, alt: '' },
        },
        meta: {
          addAriaLabel: legacyData.aiValue.integrations.addAriaLabel,
        },
      },
    },
  },

  channels: {
    id: 'channels',
    title: legacyData.socialMedia.title,
    subtitle: legacyData.socialMedia.pill,
    description: legacyData.socialMedia.description,
    items: socialChannelItems,
    cta: null,
    media: {
      background: { src: legacyData.assets.images.sectionBackground, alt: '' },
      image: { src: legacyData.assets.images.socialPhone, alt: legacyData.socialMedia.phoneAlt },
      secondaryImage: { src: legacyData.assets.images.socialPhoneSecondary, alt: `${legacyData.socialMedia.phoneAlt} 2` },
    },
    meta: {
      itemAriaLabelPrefix: 'Social link',
    },
  },

  steps: {
    id: 'steps',
    title: legacyData.integrationSteps.title,
    subtitle: legacyData.integrationSteps.subtitle,
 
    items: ensureModelItems(integrationPrimarySteps, (step, index) => ({
      id: `step-${index + 1}`,
      slug: `step-${index + 1}`,
      day: step.day,
      title: step.title,
      description: step.desc,
      media: {
        image: {
          src: step.image || step.imageSrc || '',
          alt: step.title || '',
        },
      },
    })),
    cta: {
      title: legacyData.integrationSteps.ctaTitle,
      titleLines: (legacyData.integrationSteps.ctaTitle || '').split('\n'),
      primary: {
        id: 'steps-cta-primary',
        slug: 'steps-cta-primary',
        label: legacyData.integrationSteps.ctaButtonLabel,
        href: '#contacts',
        sortOrder: 1,
        isActive: true,
      },
      actions: ensureModelItems(integrationCtaStep.actions || [], (action) => ({
        id: `steps-cta-${action.label.toLowerCase()}`,
        slug: action.label.toLowerCase(),
        label: action.label,
        href: action.href,
        ariaLabel: `Open ${action.label}`,
      })),
      media: {
        image: { src: integrationCtaStep.imageSrc || '', alt: 'Брифинг' },
        background: { src: legacyData.assets.images.ctaBackground, alt: '' },
      },
    },
    media: {
      ctaBackground: { src: legacyData.assets.images.ctaBackground, alt: '' },
    },
    meta: {},
  },

  pricing: {
    id: 'pricing',
    title: legacyData.pricing.title,
    subtitle: legacyData.pricing.subtitle,
  
    items: pricingItems,
    cta: null,
    media: {},
    meta: {
      channelsLabel: 'Каналы:',
    },
  },

  reviews: {
    id: 'reviews',
    title: legacyData.reviews.titleMain,
    subtitle: legacyData.reviews.titleAccent,
   
    items: reviewItems,
    cta: null,
    media: {},
    meta: {
      actions: legacyData.reviews.actions,
      modalResultsTitle: legacyData.reviews.modalResultsTitle,
    },
  },

  contacts: {
    id: 'contacts',
    title: legacyData.contacts.heading.line1,
    subtitle: legacyData.contacts.heading.accent,
    description: legacyData.contacts.description || '',
    items: contactMessengers,
    cta: null,
    media: {
      sectionBackground: { src: legacyData.assets.images.sectionBackground, alt: '' },
      cardBackground: { src: legacyData.assets.images.ctaBackground, alt: '' },
    },
    meta: {
      headingLine3: legacyData.contacts.heading.line3,
      card: legacyData.contacts.card,
      form: {
        id: 'contacts-form',
        title: legacyData.contacts.form.title,
        subtitle: legacyData.contacts.form.subtitle,
        fields: ensureModelItems(
          [
            {
              key: 'name',
              label: legacyData.contacts.form.labels.name,
              placeholder: legacyData.contacts.form.placeholders.name,
              type: 'text',
              required: true,
            },
            {
              key: 'contact',
              label: legacyData.contacts.form.labels.contact,
              placeholder: legacyData.contacts.form.placeholders.contact,
              type: 'text',
              required: true,
            },
            {
              key: 'comment',
              label: legacyData.contacts.form.labels.comment,
              placeholder: legacyData.contacts.form.placeholders.comment,
              type: 'textarea',
              required: false,
            },
          ],
          (field) => ({
            id: `contacts-form-${field.key}`,
            slug: field.key,
            ...field,
          }),
        ),
        submitLabel: legacyData.contacts.form.submitLabel,
        closeAriaLabel: legacyData.contacts.form.closeAriaLabel,
      },
    },
    phones: ensureModelItems([
      {
        id: 'contact-phone-main',
        slug: 'main',
        label: 'Телефон',
        value: legacyData.contacts.links.whatsapp.phoneE164 || '',
        href: legacyData.contacts.links.whatsapp.phoneE164 ? `tel:${legacyData.contacts.links.whatsapp.phoneE164}` : '',
      },
    ]),
    emails: ensureModelItems([
      {
        id: 'contact-email-support',
        slug: 'support',
        label: 'Email',
        value: legacyData.footer.supportEmail,
        href: `mailto:${legacyData.footer.supportEmail}`,
      },
    ]),
 
    socials: socialChannelItems,
    messengers: contactMessengers,
  },

  footer: {
    id: 'footer',
    items: footerColumns,
    cta: null,
    media: {
      logo: {
        src: legacyData.assets.images.logo,
        alt: legacyData.footer.brandName,
      },
    },
    meta: {
      brandName: legacyData.footer.brandName,
      brandHref: legacyData.footer.brandHref,
      supportEmail: legacyData.footer.supportEmail,
      navAriaLabel: 'Навигация в футере',
      
    },
  },
}
