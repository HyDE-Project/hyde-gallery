# Hyprdots theme Gallery

A repo for themes I Stole from the rightful Owner. 

## Theme List

The Mac OS theme selects HyDE's `macos` Waybar layout and matching `macos.css`
on theme/color updates through `$WAYBAR_LAYOUT` in `hypr.theme`. This requires
HyDE's theme-layout support; older versions can apply the same preset with
`hyde-shell waybar --set macos`. Themes without this setting keep the selected
Waybar layout. Leaving a theme preset restores the layout and CSS selected before
entering it. A manual selection within a preset lasts until the next theme/color update.

| Theme-Theme | vsCode Theme Extension | Owner |
|------------|------------|------------| 
| Catppuccin-Mocha | catppuccin.catppuccin-vsc~Catppuccin Mocha | https://github.com/prasanthrangan/hyprdots | 
| Catppuccin-Latte | Catppuccin.catppuccin-vsc~Catppuccin Latte | https://github.com/prasanthrangan/hyprdots | 
| Decay-Green | decaycs.decay~Decayce | https://github.com/prasanthrangan/hyprdots | 
| Rose-Pine | mvllow.rose-pine~Rosé Pine | https://github.com/prasanthrangan/hyprdots | 
| Tokyo-Night | enkia.tokyo-night~Tokyo Night | https://github.com/prasanthrangan/hyprdots | 
| Material-Sakura | mvllow.rose-pine~Rosé Pine Moon | https://github.com/prasanthrangan/hyprdots | 
| Graphite-Mono | StepanVanzuriak.mono~mono dark | https://github.com/prasanthrangan/hyprdots | 
| Cyberpunk-Edge | JWSandeman.cyberpunk2077-theme~cyberpunk2077 | https://github.com/prasanthrangan/hyprdots | 
| Frosted-Glass | msnilshartmann.blue-light~Blue Light Theme | https://github.com/prasanthrangan/hyprdots | 
| Gruvbox-Retro | jdinhlife.gruvbox~Gruvbox Dark Medium | https://github.com/prasanthrangan/hyprdots | 
| Synth-Wave | robbowen.synthwave-vscode~SynthWave '84 | https://github.com/prasanthrangan/hyprdots | 
| MacOS | davidbwaters.macos-modern-theme~MacOS Modern Dark - Xcode Modern | https://github.com/T-Crypt/hyprdots | 
| Windows-11 | extensioncreator.windows-11-color-theme~Windows 11 Dark | https://github.com/T-Crypt/hyprdots | 
| Hackthebox | silofy.hackthebox~Hack The Box | https://github.com/T-Crypt/hyprdots | 


## Patch 

> [!IMPORTANT]
> + Make sure you have [Hyprdots installed.](https://github.com/prasanthrangan/hyprdots)
> + It is better to enclose each field with ' single qoutes '  to avoid problems



```
Hyprdots theme patch 'Theme-Name' 'https://github.com/kRHYME7/Hyprdots-gallery' 'id.extension~Extension theme name'
```

#### Example


```
Hyprdots theme patch 'MacOS' 'https://github.com/kRHYME7/Hyprdots-gallery' 'davidbwaters.macos-modern-theme~MacOS Modern Dark - Xcode Modern'
```

```
Hyprdots theme patch 'Windows-11' 'https://github.com/kRHYME7/Hyprdots-gallery' 'extensioncreator.windows-11-color-theme~Windows 11 Dark'
```




# TODO

+ Add a metadata so that this repo can be fetched using the themepatcher.(With preview)
+ I am not planning to maintain all themes(Will try to use the original repo as source)   
+ Whatever comes to mind
