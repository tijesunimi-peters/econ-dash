# Sunburst Chart Implementation Plan

**Date:** 2026-03-13
**Status:** Planning Phase
**Task:** Replace treemap with sunburst chart for sector drill-down visualization

## Overview

Current dashboard uses a single-level treemap (sectors only) that requires clicking to drill down to sub-industries table view. Replacing with sunburst chart that shows both sectors (inner ring) and sub-industries (outer ring) in one visualization.

**Benefits:**
- See full sector → sub-industry hierarchy at a glance
- Better visual exploration of economic structure
- Single chart instead of switching between treemap and table
- Maintain same color-coding (red/green for YoY changes)

## Implementation Tasks

### 1. Create Sunburst Component
- [ ] Create `frontend/components/sunburst_sector_viz.py`
  - Build `build_sector_sunburst(sectors_with_subitems, country_name)` function
  - Transform flat sectors + sub-industries into hierarchical structure for Plotly
  - Configure color scale (red for negative YoY, green for positive)
  - Set up hover templates and click extraction
  - Estimated: 1.5 hours

### 2. Update API Data Flow
- [ ] Modify `frontend/callbacks.py` - `update_treemap()` callback (line 437-447)
  - Fetch sectors from `get_country_summary()`
  - For each sector, fetch sub-industries from `get_sector_summary()`
  - Combine into hierarchical structure
  - Pass to `build_sector_sunburst()`
  - Estimated: 45 minutes

### 3. Update Click Handler
- [ ] Modify `frontend/callbacks.py` - `on_treemap_click()` callback (line 178-194)
  - Rename to `on_sunburst_click()` or keep same name
  - Extract depth level from sunburst click event
  - Handle depth 1 (sector) click → navigate to sub_industries view
  - Handle depth 2 (sub-industry) click → navigate to indicators view
  - Estimated: 45 minutes

### 4. Update Imports
- [ ] Modify `frontend/components/__init__.py` (line ~1900)
  - Add import for new sunburst component
  - Keep treemap as fallback
  - Estimated: 15 minutes

### 5. Styling & Responsiveness
- [ ] Adjust CSS if needed in `frontend/assets/homepage.css`
  - Ensure sunburst responsive at all breakpoints (4K down to mobile)
  - Verify colors visible on dark theme
  - Estimated: 30 minutes

### 6. Testing
- [ ] Functional Testing
  - [ ] Sunburst renders with 2 rings
  - [ ] Colors match YoY changes
  - [ ] Sector click navigates correctly
  - [ ] Sub-industry click navigates correctly
  - [ ] Back button returns to sunburst

- [ ] Responsive Testing
  - [ ] Desktop (1440px) - full size
  - [ ] Tablet (768px) - scales down
  - [ ] Mobile (375px) - readable and clickable

- [ ] Performance Testing
  - [ ] Page loads in <2s (with N+1 API calls)
  - [ ] Sunburst renders smoothly
  - [ ] No lag on clicks
  - Estimated: 1.5 hours

**Total Estimated Effort:** 4.5-5 hours

## Key Design Decisions

### Data Fetching Strategy
**Chosen: N+1 API calls with client-side merging**
- Pros: Clean separation of concerns, can cache sub-industries separately
- Cons: Multiple API calls, slightly slower but acceptable

Alternative considered: Create new backend endpoint combining sectors + sub-industries (backend changes)

### Color Scaling
- Use same color scale for both sector and sub-industry rings
- Red: YoY < -5%
- Gray: -5% to +5%
- Green: YoY > +5%
- Calculate min/max across all levels for consistent scaling

### Click Behavior
- Depth 1 (Sector): Navigate to `level="sub_industries"`, set `sector_id`
- Depth 2 (Sub-industry): Navigate to `level="indicators"`, set `sub_industry_id`
- Allows continuing drill-down to indicators from sunburst

## Files to Modify

1. **NEW** `frontend/components/sunburst_sector_viz.py` (250-300 lines)
2. **UPDATE** `frontend/components/__init__.py` (1 import line)
3. **UPDATE** `frontend/callbacks.py` (update 2 callbacks)
4. **UPDATE** `frontend/assets/homepage.css` (if needed for sizing)
5. **UPDATE** `frontend/layouts.py` (update ID if renaming "treemap")

## Rollback Plan
- Keep `build_sector_treemap()` in code
- If issues arise, switch back to treemap by reverting 2 callback updates
- Clean git history with interactive rebase if needed

## Performance Considerations

### Current (Treemap):
- 1 API call: `GET /countries/:id/summary` → ~100ms
- Render treemap: ~200ms
- Total: ~300ms

### New (Sunburst):
- 1 API call: `GET /countries/:id/summary` → ~100ms
- N API calls: `GET /sectors/:id/summary` × N → ~50ms × 5 sectors = ~250ms
- Data merge & transform: ~50ms
- Render sunburst: ~200ms
- **Total: ~600ms** (acceptable, <2s target)

### Optimization Options (if needed later)
- Cache sector summaries in component state
- Create new backend endpoint combining all data (1 call instead of N+1)
- Lazy-load sub-industries on sector click instead of all at once

## Testing Checklist

### Functional
- [ ] Sunburst renders on country selection
- [ ] Inner ring = sectors with correct names
- [ ] Outer ring = sub-industries for each sector
- [ ] Colors gradated by YoY% correctly
- [ ] Clicking sector (depth 1) navigates to sub_industries detail view
- [ ] Clicking sub-industry (depth 2) navigates to indicators view
- [ ] Back button returns to sunburst
- [ ] No errors in browser console

### Responsive
- [ ] 4K (3840px): Sunburst displays full size, readable
- [ ] 1440p: Sunburst fits well in layout
- [ ] 1080p: Sunburst responsive
- [ ] Tablet (768px): Sunburst scales down, still clickable
- [ ] Mobile (375px): Sunburst readable, touch targets work

### Performance
- [ ] Page loads in <2s (including API calls)
- [ ] Sunburst renders without lag
- [ ] Clicking doesn't cause noticeable delay (<100ms response)
- [ ] No console warnings

### Browser Compatibility
- [ ] Chrome/Edge 120+
- [ ] Firefox 121+
- [ ] Safari 16+
- [ ] Mobile Safari (iOS 15+)

## Success Criteria

✅ Sunburst chart displays showing sectors (inner) and sub-industries (outer)
✅ Click drill-down works for both levels
✅ Color-coding matches YoY changes
✅ Responsive at all breakpoints
✅ Performance <2s page load + <100ms interaction response
✅ No console errors
✅ All tests passing

## Notes

- Keep treemap function in codebase as fallback (don't delete)
- Similar patterns exist in `build_sparkline_table()` (line 158) for row click handling
- Correlation heatmap (line 847) uses similar click event extraction
- Consider future: Could apply same sunburst pattern to other hierarchical data

---

**Next Step:** After implementation, run comprehensive testing per checklist above
