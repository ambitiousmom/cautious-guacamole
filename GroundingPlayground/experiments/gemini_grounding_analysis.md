# Gemini Grounding Analysis Experiment

## Objective
Understand what structured and unstructured attributes Gemini extracts from Google Maps, and how query intent affects retrieval.

---

## Method 1: Query Variations (Same Entity, Different Intents)

### Target Entity: Din Tai Fung Bellevue

| # | Query | Intent | Expected Attribute |
|---|-------|--------|-------------------|
| 1 | Does Din Tai Fung Bellevue have outdoor seating? | Amenity check | `Outdoor seating` |
| 2 | What time does Din Tai Fung Bellevue close on Friday? | Hours lookup | `Hours` array |
| 3 | Is Din Tai Fung Bellevue good for a date? | Occasion/vibe | `Occasion` insights |
| 4 | What should I order at Din Tai Fung Bellevue? | Menu/popular | `Most Ordered` |
| 5 | Does Din Tai Fung Bellevue take reservations? | Booking | `Reservations` flag |
| 6 | Is Din Tai Fung Bellevue wheelchair accessible? | Accessibility | `Wheelchair accessible` |
| 7 | Does Din Tai Fung Bellevue have vegan options? | Dietary | `Vegan options` / review inference |
| 8 | What do people complain about at Din Tai Fung Bellevue? | Negative reviews | Review extraction |
| 9 | Is Din Tai Fung Bellevue expensive? | Price | `Price range` |
| 10 | Does Din Tai Fung Bellevue have parking? | Amenity | `Parking` flag |
| 11 | Does Din Tai Fung Bellevue have wifi? | Amenity | `Wi-Fi` flag |
| 12 | Can I bring kids to Din Tai Fung Bellevue? | Suitability | `Good for kids` |
| 13 | Does Din Tai Fung Bellevue do takeout? | Service mode | `Takeout` flag |
| 14 | What's the address of Din Tai Fung Bellevue? | Basic lookup | `Address` |
| 15 | Show me photos of Din Tai Fung Bellevue | Media | Photos array |

---

## Method 2: Entity Comparison (Same Query, Different Entities)

### Test Query: "Does [ENTITY] have outdoor seating?"

| # | Entity | Type | Popularity | Expected Data Richness |
|---|--------|------|------------|------------------------|
| 1 | Din Tai Fung Bellevue | Restaurant (chain) | High | Rich |
| 2 | Canlis Seattle | Restaurant (fine dining) | High | Rich |
| 3 | Bob's Burgers Redmond | Restaurant (local) | Low | Sparse |
| 4 | Starbucks Reserve Roastery Seattle | Cafe (flagship) | High | Rich |
| 5 | Joe's Corner Coffee | Cafe (fictional/small) | Low | Sparse |
| 6 | Overlake Medical Center | Healthcare | Medium | Different schema |
| 7 | Bellevue Square | Mall | High | Different schema |
| 8 | Mike's Plumbing Bellevue | Service business | Low | Minimal |
| 9 | Marriott Bellevue | Hotel | High | Different schema |
| 10 | REI Bellevue | Retail | High | Different schema |

---

## Method 3: Known Google Maps Attributes

### Attribute Categories to Probe

#### Service Options
- [ ] Dine-in
- [ ] Takeout
- [ ] Delivery
- [ ] Curbside pickup
- [ ] No-contact delivery

#### Accessibility
- [ ] Wheelchair accessible entrance
- [ ] Wheelchair accessible restroom
- [ ] Wheelchair accessible seating

#### Amenities
- [ ] Wi-Fi
- [ ] Parking (free, paid, street, lot)
- [ ] Outdoor seating
- [ ] Rooftop
- [ ] Live music
- [ ] Fireplace
- [ ] Restroom

#### Crowd
- [ ] Good for kids
- [ ] Good for groups
- [ ] LGBTQ+ friendly
- [ ] Casual
- [ ] Romantic
- [ ] Trendy

#### Dining
- [ ] Serves breakfast
- [ ] Serves lunch
- [ ] Serves dinner
- [ ] Serves brunch
- [ ] Serves happy hour
- [ ] Serves vegetarian
- [ ] Serves vegan
- [ ] Halal
- [ ] Kosher

#### Payments
- [ ] Accepts credit cards
- [ ] Accepts debit cards
- [ ] Accepts NFC mobile payments
- [ ] Accepts cash only

#### Reservations
- [ ] Accepts reservations
- [ ] Requires reservations
- [ ] Waitlist available

#### Health & Safety
- [ ] Mask required
- [ ] Staff wear masks
- [ ] Temperature check required

---

## Data Collection Template

For each query, capture:

```
Query ID: ___
Query Text: ___
Entity: ___
Timestamp: ___

STRUCTURED ATTRIBUTES FOUND:
- [ ] Place ID
- [ ] Name
- [ ] Category
- [ ] Address
- [ ] Phone
- [ ] Website
- [ ] Hours
- [ ] Rating
- [ ] Price range
- [ ] Coordinates
- [ ] Description
- [ ] (List any amenity booleans)

SEMI-STRUCTURED DATA FOUND:
- [ ] Review summary (AI-generated)
- [ ] Tips
- [ ] Most Ordered
- [ ] Occasion
- [ ] Highlights

UNSTRUCTURED DATA FOUND:
- [ ] Full reviews (count: ___)
- [ ] Photos (count: ___)

QUERY-SPECIFIC ATTRIBUTE:
- Attribute name: ___
- Value: ___
- Was it in structured data or inferred from reviews?: ___

NOTES:
___
```

---

## Status Tracking

### Method 1 Progress
| Query # | Captured | Analyzed |
|---------|----------|----------|
| 1 | ✅ | ✅ |
| 2 | ⬜ | ⬜ |
| 3 | ⬜ | ⬜ |
| ... | ... | ... |

### Method 2 Progress
| Entity # | Captured | Analyzed |
|----------|----------|----------|
| 1 | ⬜ | ⬜ |
| 2 | ⬜ | ⬜ |
| ... | ... | ... |

### Method 3 Progress
| Attribute Category | Probed | Documented |
|--------------------|--------|------------|
| Service Options | ⬜ | ⬜ |
| Accessibility | ⬜ | ⬜ |
| ... | ... | ... |
