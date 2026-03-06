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
- **Internationalization**: EN / AR / FR for all UI text including ToS-related strings
- **Supabase**: `https://muhxkvtniuinrspwhzhn.supabase.co`
