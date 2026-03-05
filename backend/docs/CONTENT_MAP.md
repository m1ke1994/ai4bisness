# Content Map

Источник контента фронтенда: `nuxt-app/data/siteData.ts`.
Дополнительный контент документов: `nuxt-app/pages/privacy-policy.vue`, `nuxt-app/pages/public-offer.vue`, `nuxt-app/pages/user-agreement.vue`.

| Section | Model(s) | Fields | Repeatable items | Images/media | Notes |
|---|---|---|---|---|---|
| `meta` / общие настройки | `SiteSettings` | `brand_name`, `site_name`, `domain`, `description`, `locale`, `theme`, `support_email`, `contact_form_open_event`, `logo`, `logo_alt`, `favicon` | - | `logo`, `favicon` | Используется в header/footer/SEO и как часть `site-data`. |
| `assets` (registry + media map) | `SiteSettings` + секционные модели (агрегируется в API) | `title`, `description`, карта медиа по ключам (`logo`, `heroPhone`, `heroTexture`, ...) | `items[]` (собирается из моделей как реестр) | Все медиа из секций | Отдельной модели asset-registry не требуется, реестр формируется на лету. |
| `nav` / Header | `HeaderSection`, `HeaderNavItem`, `HeaderMobileSocialItem` | `brand_href`, ARIA-поля (`desktop_nav`, `mobile_nav`, `mobile_dialog`, `open_menu`, `close_menu`) | `items[]` (меню), `mobileSocials[]` | Логотип и иконки mobile social | Сортировка по `order`, флаг `is_active`. |
| `hero` | `HeroSection`, `HeroStatItem` | `title`, `subtitle`, `description`, `stats_disclaimer`, `phone_alt`, `image_vars` | `items[]` (статы) | `phone_image`, `texture_image` | `image_vars` хранится JSON для css-переменных. |
| `heroLogos` | `HeroLogosSection`, `HeroLogoItem` | - | `items[]` (логотипы) | `logo` (или исходный путь) | В исходнике есть ссылки `/images/1.svg..5.svg`, файлов в репо нет — нужен fallback path. |
| `advantages` (whatSellerCan) | `AdvantagesSection`, `AdvantagesStatItem`, `TrainingSourceItem`, `TrainingRightBulletItem`, `ComparisonRowItem`, `AdvantagesAiSummaryItem`, `AdvantagesHumanLimitItem` | training/summary-поля, labels для desktop/mobile, `training_right_pill`, `training_right_title` | stats, training sources, bullets, comparison rows, aiSummary, humanLimits | `check_icon` | Поля summary используются в таблице сравнения и мобильной версии. |
| `aiValue` | `AiValueSection`, `AiValuePointItem`, `AiIntegrationItem` | `title`, `subtitle_prefix`, `subtitle_highlight`, launch-поля (`badge*`, `left/right_label`, `paid_*`, `note_*`), `integrations_title`, `integrations_subtitle`, `integrations_add_aria_label` | value points, integration rows | `integrations_banner`, row image | Сортировка integration rows по `order`. |
| `channels` (social media block) | `ChannelsSection`, `ChannelItem` | `title`, `subtitle`, `description`, `item_aria_label_prefix` | `items[]` (каналы) | `background_image`, `primary_image`, `secondary_image`, иконки каналов | Каналы также переиспользуются в `contacts.socials`. |
| `steps` (integration steps) | `StepsSection`, `StepItem`, `StepCtaActionItem` | `title`, `subtitle`, `cta_title`, `cta_button_label`, `cta_button_href` | `items[]` (этапы), `cta.actions[]` | step images, `cta_image`, `cta_background` | `cta.titleLines` формируется split по `\n`. |
| `pricing` | `PricingSection`, `PricingPlan`, `PricingPlanFeature` | `title`, `subtitle`, `channels_label`; поля плана: `title`, `subtitle`, `channels`, `accent_badge`, `inherit_line`, `featured`, `dark_card`, `cta_label`, `cta_href` | `items[]` (планы), `features[]` | - | Сортировка планов и фич по `order`. |
| `reviews` | `ReviewsSection`, `ReviewItem`, `ReviewPreviewParagraph`, `ReviewPreviewBullet`, `ReviewDetailParagraph`, `ReviewResultItem` | `title`, `subtitle`, action labels (`read_more`, `close_modal_aria`, `prev/next`, pagination labels), `modal_results_title` | review cards + вложенные списки параграфов/буллетов/results | - | Для модалки нужен полный текст `detailsParagraphs` и `results`. |
| `contacts` | `ContactsSection`, `ContactMessenger`, `ContactFormField`, `ContactPhone`, `ContactEmail` | heading (`title`, `subtitle`, `heading_line3`), `description`, card (`title_line1`, `title_line2`, `response_time`), form (`title`, `subtitle`, `submit_label`, `close_aria_label`) | messengers, form fields, phones, emails | `section_background_image`, `card_background_image`, иконки мессенджеров | `socials` в API дублируются из `ChannelItem`. |
| `footer` | `FooterSection`, `FooterColumn`, `FooterLink` | `brand_name`, `brand_href`, `support_email`, `nav_aria_label` | `items[]` columns + links | `logo` | Колонки: `navigation`, `legal`. |
| Policy pages (`privacy`, `offer`, `terms`) | `PolicyPage`, `PolicySection`, `PolicyParagraph` | `slug`, `title`, `back_button_label` | sections + paragraphs | - | Сидер парсит тексты из `nuxt-app/pages/*.vue`. |

## Используемые изображения/иконки из фронтенда

Основной набор путей (из `siteData.ts` и компонентов):

- `/images/logo.png`, `/images/hiro.png`, `/images/tilda.png`, `/images/dialog.png`, `/images/dialog2.png`
- `/images/bg-fon.png`, `/images/bg.png`, `/images/banner.png`, `/images/banner 3.png`
- `/images/13.png`, `/images/11.png`, `/images/12.png`, `/images/icon icon.png`, `/images/10.png`, `/images/briffing.png`
- `/images/tovar_fids.png`, `/images/slack.png`, `/images/yandex_google.png`, `/images/api.png`
- `/images/vecor.svg`
- `/images/icons/{web,telegram,avito,instagram,facebook,whatsapp,youtube,tiktok,mail,vk,Max}.svg`

Отсутствуют в `nuxt-app/public/images`, но присутствуют в контенте как ссылки:

- `/images/1.svg`, `/images/2.svg`, `/images/3.svg`, `/images/4.svg`, `/images/5.svg`

Для этих путей сидер сохраняет исходный путь в fallback-поле, чтобы API не терял ссылку.
