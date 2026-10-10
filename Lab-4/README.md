# Lab 4 — Vibe Coding: Galaga Game Enhancements

## 1. Project Overview

This project enhances the **Galaga** arcade-lite game developed using Python and Pygame. The game features Bézier-curve motion, wave-based enemy spawning, formation swaying, diving attack patterns, player shooting, and projectile collisions.

The objective of this lab was to use an LLM (Gemini / Antigravity) as a coding assistant to understand, modify, debug, and test the existing game while keeping the implementation modular, well-engineered, and thoroughly verified.

## 2. Implemented Features

### Task 1 — Fix Entry & Dive Bézier Curve Path Bug
- Diagnosed the trajectory bulge where enemies overshot mid-flight during entry.
- Corrected the cubic Bézier polynomial formula in `bezier()` by squaring the parameter $t$ in the third weighted term (`3 * u * t * t * p2`).
- Restored smooth, continuous flight curves for all enemy entry and dive trajectories.

### Task 2 — Custom Enemy Tinting (`enemy_tint`)
- Implemented `enemy_tint(kind)` to override default enemy colors with high-contrast arcade neon palettes.
- Assigned unique colors: Neon Emerald for Boss (`(60, 240, 160)`), Vibrant Crimson for Red (`(255, 75, 95)`), and Electric Azure for Blue (`(75, 175, 255)`).

### Task 3 — Wave Start Banner Announcement (`on_wave_start`)
- Implemented `on_wave_start(wave)` called on wave creation and wave clears.
- Added a dynamic HUD banner display (`STAGE {wave} - GET READY`) rendered centered on screen for 2.0 seconds at the beginning of each wave.

### Task 4 — Player Shield Charges & Visual HUD (`shield_charges`)
- Implemented `shield_charges(wave)` granting hit-absorbing energy shields (`1 + (wave - 1) // 3` charges per wave).
- Added a cyan glowing energy shield ring around the player ship when active.
- Added a real-time `Shield` counter to the game HUD.

## 3. Technologies Used

- **Programming language:** Python 3.13
- **Game library:** Pygame
- **Development environment:** Visual Studio Code / Antigravity IDE
- **Version control:** Git and GitHub
- **LLM assistance:** Google Antigravity (Gemini)

## 4. Repository Structure

```text
Lab-4/
├── 31_galaga/
│   ├── game.py
│   └── README.md
├── before_edit.mp4
├── FINAL.mp4
├── Galaga_Repair_Enhancements.pdf
└── README.md
```

## 5. Running the Game

Install the required library:

```bash
pip install pygame
```

Navigate to the directory containing `game.py`:

```bash
cd 31_galaga
python game.py
```

### Controls

| Key | Action |
|---|---|
| Left Arrow / Right Arrow | Move ship left / right |
| Spacebar | Fire projectiles |
| R | Restart / Reset game |

## 6. Testing and Verification

The following behaviours were tested and verified during gameplay:

- Enemies enter along smooth Bézier curves without overshooting or bulging.
- Enemies settle smoothly into the swaying formation.
- Enemies peel off to dive and fire at the player.
- Enemy recoloring renders clearly according to enemy type.
- Wave announcement banner appears for 2 seconds at each wave start.
- Shield absorbs hits before losing a ship, and displays the cyan shield indicator and HUD count.
- Pressing `R` resets the game state properly.

## 7. Gameplay Demonstrations

- **Before modifications:** `before_edit.mp4`
- **After modifications:** `FINAL.mp4`

## 8. LLM Chat History

The complete LLM conversation documenting the assistance used during implementation, debugging, and testing is available here:

**[View Complete Chat History (PDF)](./Galaga_Repair_Enhancements.pdf)**

The conversation history is provided to support transparency and fulfill the lab's LLM pair-programming requirement.

## 9. Summary

This lab demonstrates the use of LLM-assisted pair programming to extend and repair an existing Python Pygame project through iterative bug fixing, mathematical verification, feature additions, and structured Git commits.
