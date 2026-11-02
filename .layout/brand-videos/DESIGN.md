# Brand Videos/Carousels — Design System
> Bold, cinematic, legible on dark. GSAP-ready with strong hierarchy.

## Quick Reference
**Aesthetic:** Dark surfaces, warm text, high-contrast CTAs. Prioritize legibility at small sizes.

### Color Palette
| Role | Token | Value |
|---|---|---|
| Background | `--bg-dark` | `#15100b` |
| Surface/panels | `--bg-surface` | `#231a14` |
| Primary text | `--text-primary` | `#F5EFE7` |
| Accent/highlights | `--text-accent` | `#BB9457` |
| CTA primary | `--cta-primary` | `#6F1D1B` |
| CTA hover | `--cta-hover` | `#5a1715` |

### Typography
- **UI/overlays:** `Inter` 600-700 (avoid thin weights)
- **Hero titles:** `Playfair Display` 700-900
- **Scale:** ensure legible at small sizes; consider text shadow for busy backgrounds

### Transparent PNG Illustration Recipe
**Light background**
- Outline/stroke: 2px `#432818`
- Shadow/depth: 2px offset or soft shadow in `#6F1D1B`
- Fill/highlight: `#BB9457`, `#FFFFFF` for contrast

**Dark background (#15100b)**
- Outline/stroke: 3px `#EFE3D2` (thicker for legibility)
- Shadow/depth: swap to `#432818` (darker/deeper, not maroon)
- Fill/highlight: `#BB9457`, keep details visible

**Rationale:** Thicker stroke on dark prevents fading; shadow swap maintains depth without competing.

### GSAP/Carousel Guidance
1. **Animations:** prefer transforms/opacity (avoid layout thrash)
2. **States:** active/inactive clearly distinct, focusable
3. **Legibility:** high contrast, text shadow if needed
4. **Performance:** minimize repaints
5. **Accessibility:** respect reduced motion
6. **Don't rely on color alone** for states

### Rules
1. **Background:** prefer `#15100b` over `#432818` (less muddy)
2. **Weights:** use 600-700 for on-screen text
3. **CTAs:** Harvest Gold for highlights, Deep Maroon for primary CTAs
4. **Consistency:** follow illustration recipe exactly
5. **Clarity:** test at thumbnail size
