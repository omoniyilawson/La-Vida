# La Vida: Davida & Omoniyi

A digital wedding invitation for 29 March 2027, Abuja.

## What's in the folder

```
index.html              the whole invitation
assets/
  css/styles.css        all styling (colours and fonts are at the top)
  js/main.js            interactions: envelope, countdown, story letters, RSVP
  js/gsap.min.js        animation library (GSAP 3.12.5, included so nothing loads from elsewhere)
  fonts/                Cormorant Garamond, Pinyon Script, Jost (self-hosted)
  img/                  wax seal, papers, ribbon and the watercolour botanicals (WebP)
  source/wax-seal-1024.png   full-resolution wax seal with transparency
tools/                  the Python scripts that rendered the artwork (only needed to regenerate it)
```

## Put it online with GitHub Pages

1. Create a **public** repository on github.com, for example `la-vida`.
2. **Add file → Upload files**. Drag in everything *inside* this folder (index.html, assets, tools, README.md) and commit.
3. **Settings → Pages** → Source: *Deploy from a branch* → Branch: `main`, folder `/ (root)` → **Save**.
4. After a minute or two it's live at `https://YOUR-USERNAME.github.io/la-vida/`.

To update the site later, upload the changed file again with the same name and commit.

## Personal invitation links

Add a guest's name to the end of the address, using hyphens between words:

`https://YOUR-USERNAME.github.io/la-vida/#tolu-adebayo`

The envelope then says "For Tolu Adebayo", the invitation opens with "Dear Tolu Adebayo," and the RSVP name is filled in.
Use plain letters only. Names with accents or apostrophes still work, but they won't show the greeting.

## Updating wedding details

| To change | Edit |
| --- | --- |
| Wedding date used by the countdown | `assets/js/main.js` → `CONFIG.weddingDate` |
| WhatsApp number for RSVPs | `assets/js/main.js` → `CONFIG.whatsapp` (digits only, e.g. 2348068015338) and the number shown in `index.html` (search for "806 801 5338") |
| Story chapters | `assets/js/main.js` → `CHAPTERS` (a line starting with `*` becomes a pull quote) |
| Venue, programme times, traditional wedding date, hotels, gift details | `index.html`. Search for "to be announced", "Time TBC", "Details to follow" and "Hotel recommendations" |
| Colours and fonts | top of `assets/css/styles.css` |

## How the RSVP works

The form checks that the guest gave a name and an answer, then writes their reply as a message.
"Open WhatsApp to send" opens WhatsApp addressed to +234 806 801 5338 with that message already filled in.
**A reply only reaches you when the guest presses Send in WhatsApp**, and the page tells them so.
Nothing is stored on the website.

## Accessibility and motion

- The wax seal is a real button, so it works with the keyboard (Tab, then Enter).
- Story cards respond to the arrow keys. Letters close with Escape and return focus to the card.
- If a guest's device is set to reduce motion, the envelope fades instead of animating.

## About the artwork

The seal, papers, ribbon and botanicals were rendered with code (see `tools/`). They are not hand-painted.
- **Wax seal:** a 3D height map lit from the upper-left, with the LV monogram drawn from Cormorant Garamond letter shapes.
- **Botanicals:** a watercolour simulation in which pigment layers glaze over each other, pools at drying edges and settles into the paper grain.

To use commissioned hand-painted art instead, replace the files in `assets/img/` with the same names and similar proportions. Use WebP with a transparent background for the florals.
