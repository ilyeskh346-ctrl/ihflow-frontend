# IH Flow — Instagram DM Automation Platform

## Project Overview
A static single-page landing website for IH Flow, an Instagram DM automation platform. Built for creators and brands to automate replies, send links, and capture leads.

## Structure
- `index.html` — The entire frontend: a self-contained static HTML file with embedded CSS and JavaScript (no build system or dependencies).

## Running
- Served via Python's built-in HTTP server: `python3 -m http.server 5000 --bind 0.0.0.0`
- Accessible at port 5000

## Deployment
- Configured as a **static** deployment with `publicDir: "."`.

## Key Features
- **Bot creation wizard** with activity types: Car, E-commerce
- **Car activity type**: Custom product table (Car Name, Color, Motor Type, Description, Qty, Price)
- **Orders view**: Dynamically shows color and motor type columns for Car bots
- **Realtime orders**: Supabase Realtime subscription auto-updates orders table
- **Terms of Service**: Signup form requires checkbox acceptance before account creation; ToS modal with full 14-section text; terms_accepted + terms_accepted_at stored in Supabase user metadata
- **Legal section in dashboard**: Sidebar shows Legal submenu under Orders with three pages: Terms of Service, Privacy Policy, Cookie Policy — each a full professional SaaS legal page
- **Internationalization**: EN / AR / FR with 340+ translation keys covering all dashboard UI text (Overview, Total Orders, Today's Messages, Account Center, Profile, Subscription & Billing, Security, Orders table headers, etc.)
- **RTL layout**: Full Arabic RTL support — sidebar stays LEFT in all languages, text direction flips RTL, inputs/modals/canvas all respect direction; `[dir="rtl"] .sidebar{left:0;right:auto}` keeps layout intact
- **Dynamic table headers**: Orders table headers re-translate when language is switched (uses `t()` function and `currentActiveColumns` global to re-render on language change)
- **Smart Orders columns**: `ORDER_COLUMNS` array + `computeActiveColumns(orders)` auto-hide any column that is NULL across all visible orders; always shows: customer_name, phone_number, status; optional: state, address, product_name, quantity, size, color, motor_type, details (jsonb)
- **FAQs page**: Full CRUD dashboard page — Supabase `faqs` table (id, bot_id, question, answer, created_at); sidebar item with question mark icon; bot-selector dropdown; add/edit modal; delete with confirm; `loadFaqs`, `filterFaqsByBot`, `renderFaqs`, `openFaqModal`, `closeFaqModal`, `saveFaq`, `deleteFaq`, `escHtml` functions
- **Supabase**: `https://muhxkvtniuinrspwhzhn.supabase.co`
