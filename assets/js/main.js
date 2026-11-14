/* La Vida — interactions
   Edit the CONFIG block to change wedding details. */
(function () {
  "use strict";

  const CONFIG = {
    weddingDate: "2027-03-29T00:00:00+01:00", // Abuja time (WAT)
    whatsapp: "2348068015338",                 // digits only, international format
    couple: "Davida & Omoniyi",
  };

  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduceMotion = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
  const hasGsap = typeof window.gsap !== "undefined";

  /* ================================================================
     Story content (the couple's own words; edit here)
     A line starting with * is shown as a pull quote.
     ================================================================ */
  const CHAPTERS = [
    { date: "29 September 2026", title: "The Day Our Paths Crossed",
      gist: "At an education summit, Lanre introduced Omoniyi to Davida. A brief hello, an Instagram follow, and the first page of an extraordinary story.",
      text: ["It all began on September 29, 2026, at the Experience AI Launch and Future of Education in Nigeria Summit, organised by the Aid for Rural Education Access Initiative (AREAi).",
        "It was a day filled with conversations about education, innovation, and the future of learning in Nigeria. Somewhere in the middle of it all, two people who shared a passion for education were about to meet for the very first time.",
        "*Omoniyi's boss, Lanre, introduced him to Davida.",
        "It was a brief encounter. With the responsibilities of hosting an important event and several people requiring his attention, Omoniyi could barely manage more than a short conversation.",
        "But something about that introduction stayed with him.",
        "Later that day, he found Davida on Instagram and followed her.",
        "No messages were exchanged. No grand romantic gestures followed. Just a quiet connection between two people who had no idea how significantly their lives were about to change.",
        "Little did they know that what seemed like an ordinary introduction would become the first page of an extraordinary story."] },
    { date: "6 October 2026", title: "The Conversation That Never Really Ended",
      gist: "An 8 p.m. virtual coffee chat about the DOE Foundation. The agenda was professional. The conversation had other plans.",
      text: ["A few days later, their paths crossed again, this time through a conversation about purpose.",
        "Omoniyi had become interested in Davida's work through the DOE Foundation and reached out to learn more about the organisation. He wanted to understand its mission, explore how she could strengthen its positioning, and discuss opportunities for collaboration between their organisations.",
        "He suggested a virtual coffee chat for 8 p.m. on October 6.",
        "*The agenda was professional. The conversation, however, had other plans.",
        "What began as a discussion about education, organisational development, and social impact gradually unfolded into something far more personal.",
        "They spoke about their ambitions, their experiences, their convictions, and the things that mattered most to them.",
        "Minutes became hours.",
        "Somewhere between conversations about changing lives and building meaningful organisations, they began discovering each other.",
        "There was an unexpected ease to it all. A familiarity that neither could quite explain.",
        "And when that first conversation finally ended, something had quietly begun.",
        "*They never really stopped talking after that night."] },
    { date: "9 October 2026", title: "The Day Purpose Met Love",
      gist: "In a rural classroom, Omoniyi watched Davida teach with passion, patience and purpose, and found they shared a faith as well as a calling.",
      text: ["That Friday, Davida had a training programme in a rural community.",
        "During their conversations, Omoniyi had expressed his desire to see the work she was doing firsthand. He wanted to understand the communities she served and witness the passion behind the vision she had shared with him.",
        "So, he went.",
        "And what he saw left him in awe.",
        "*There she was, standing before the children, teaching with passion, patience, and an unmistakable sense of purpose.",
        "As Omoniyi watched Davida interact with the learners, he saw beyond her professional commitment. He saw a woman whose compassion was evident in her actions, whose convictions shaped her work, and whose heart was invested in making life better for others.",
        "It was one thing to hear her speak about her passion for education.",
        "It was another thing entirely to watch her live it.",
        "During the visit, Omoniyi shared something close to his heart. Beyond the educational opportunities being provided, wouldn't it be wonderful if the children also had the opportunity to hear about Jesus Christ and receive the gift of salvation?",
        "Davida shared his conviction.",
        "And in that moment, something became clearer.",
        "Their connection was not simply about a shared interest in education. It was also about faith, service, and a desire to see lives transformed.",
        "For Omoniyi, this was particularly significant.",
        "He had begun to see in Davida someone with whom he could pursue purpose, serve God, build meaningful things, and perhaps share the rest of his life.",
        "What had started as admiration was becoming something much deeper."] },
    { date: "9 October 2026", title: "Of Ice Cream, Spider-Man, and a Beautiful Realisation",
      gist: "Ice cream, a cinema trip to see Spider-Man, and by the end of the evening a quiet certainty: he wanted to marry Davida.",
      text: ["After the training, neither of them was quite ready for the day to end.",
        "So, they went out for ice cream.",
        "There were stories to share, questions to ask, and the kind of laughter that makes time pass unnoticed.",
        "What had begun that morning in a rural classroom continued over ice cream, with two people discovering how effortlessly their conversations could move between the serious and the wonderfully ordinary.",
        "And somehow, the day led them to the cinema.",
        "They watched Spider-Man together.",
        "There were no elaborate plans, no candlelit dinner, and no carefully rehearsed romantic declarations.",
        "Just a rural community visit, ice cream, a movie, and two people enjoying each other's company.",
        "But sometimes, the moments that change our lives arrive without announcing themselves.",
        "By the time the evening ended, Omoniyi had come to a quiet but profound realisation.",
        "*He wanted to marry Davida.",
        "He did not know everything about her yet. There were still countless stories to hear, experiences to share, and things to discover.",
        "But he had seen something that day that resonated deeply with the kind of life he hoped to build.",
        "A life of faith.", "A life of service.", "A life of purpose.",
        "*And perhaps, a life with her."] },
    { date: "October 2026", title: "Two Weeks That Felt Like Twenty Years",
      gist: "Late-night conversations, dreams of Glasgow, and a nickname that became part of their story: Vida, the Spanish word for life.",
      text: ["What followed was a beautiful season of discovery.",
        "Conversations stretched late into the night. Laughter became familiar. Dreams were shared, questions were asked, and the distance between two people who had only recently met began to feel remarkably small.",
        "They discovered how much they had in common, particularly their commitment to education and their desire to make a meaningful difference in the lives of others.",
        "There were conversations about Glasgow, too.",
        "Davida had first introduced Omoniyi to the possibility of studying at the University of Glasgow. He eventually applied and received an offer to study for an MSc in AI in Education, while Davida pursued an application for the MSc in Education, Public Policy & Equity.",
        "Suddenly, a city neither had originally imagined as part of their shared story became a place around which they could dream, pray, and plan.",
        "Could Glasgow become a mission field?",
        "Could their different academic interests complement each other in ways that would strengthen their work in education?",
        "Could the things they were individually passionate about become part of something they might one day build together?",
        "They did not have all the answers.",
        "But they shared a willingness to seek God's direction while continuing the work that mattered to them, particularly in Nigeria.",
        "And somewhere in those conversations, Omoniyi began calling Davida by a name that would eventually become part of their story.",
        "*Vida.",
        "The Spanish word for life.",
        "A simple nickname, affectionately given, that would grow into something far more meaningful."] },
    { date: "October 2026", title: "When Friendship Became a Promise",
      gist: "Omoniyi asked Davida to be his girlfriend, and she even chose to support Manchester United, despite its rather unpredictable fortunes.",
      text: ["As their connection deepened, what had begun as a professional conversation grew into a relationship built on friendship, affection, faith, and shared purpose.",
        "*Omoniyi asked Davida to be his girlfriend.",
        "It was a decision to move beyond the excitement of discovering each other and begin intentionally building a relationship.",
        "There was still so much to learn, but they were choosing to learn it together.",
        "The days that followed brought more conversations, more laughter, and a growing appreciation for the little things.",
        "The thoughtful messages.", "The late-night calls.", "The encouragement to pursue opportunities.", "The prayers offered in moments of uncertainty.",
        "The willingness to listen, to challenge each other with kindness, and to celebrate each other's accomplishments.",
        "Even Manchester United somehow found its way into their love story, with Davida choosing to support Omoniyi's beloved football club despite its rather unpredictable fortunes.",
        "Love, it seemed, was already teaching them the beauty of both grand convictions and small gestures.",
        "And as the weeks passed, they continued to discover that the most meaningful relationships are not simply about finding someone whose company you enjoy, but someone with whom you can grow."] },
    { date: "La Corona de la Vida", title: "The Crown of Life",
      gist: "La from Lawson, Vida from Davida. Two names woven into one, and a reminder of the crown of life promised in James 1:12.",
      text: ["There is a deeper meaning behind the name Vida.",
        "In Spanish, La Corona de la Vida means The Crown of Life, an expression that also carries profound significance in their Christian faith.",
        "James 1:12 speaks of the Crown of Life that God has promised to those who love Him and remain steadfast.",
        "For Omoniyi and Davida, the expression became a beautiful reminder of the kind of life they hoped to build: one grounded in faith, strengthened by grace, and devoted to loving God and serving others.",
        "Over time, the words took on another special meaning.",
        "*La Vida.",
        "La, from Lawson.", "Vida, from Davida.",
        "Two names, woven into one.",
        "And in Spanish, La Vida means The Life.",
        "It was more than a wedding theme.",
        "It became a fitting expression of their story, a celebration of two lives brought together through an unexpected introduction, a shared passion for education, and a growing love rooted in faith."] },
    { date: "Our Forever", title: "The Beautiful Life Ahead", forest: true,
      gist: "An introduction, an Instagram follow, an 8 p.m. coffee chat, a classroom, ice cream and Spider-Man. This is our story. This is La Vida.",
      text: ["Looking back, it is remarkable how the smallest moments became the most significant ones.",
        "An introduction at an education summit.", "An Instagram follow.",
        "An 8 p.m. coffee chat that became so much more than a professional meeting.",
        "A Friday morning in a rural classroom.", "Ice cream.", "Spider-Man.",
        "And a quiet realisation that something extraordinary might be unfolding.",
        "Their story has never been simply about how they met.",
        "It is about the values that brought them closer, the faith that continues to guide them, and the shared desire to live lives that make a difference.",
        "They still believe there is much to discover, many lessons to learn, and countless opportunities to grow.",
        "They do not claim to know every detail of what the future holds.",
        "*But they trust the One who holds the future.",
        "And as they prepare to begin this new chapter together, they do so with gratitude for the journey that brought them here and hope for all that lies ahead.",
        "Because sometimes, the most beautiful stories begin when two people are simply doing what they believe they were called to do.",
        "And somewhere along the way, they find each other.",
        "*This is our story. This is La Vida."] },
  ];
  const ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"];

  /* ================================================================
     Personal links: …/#tolu-adebayo greets that guest by name
     ================================================================ */
  let guest = "";
  const sectionIds = new Set($$("[id]").map((e) => e.id));
  function readGuest() {
    let h = "";
    try { h = decodeURIComponent(location.hash.slice(1)); } catch (_) { h = location.hash.slice(1); }
    if (!h || sectionIds.has(h) || !/^[a-z0-9-]+$/i.test(h)) return;
    guest = h.split("-").filter(Boolean).map((w) => w[0].toUpperCase() + w.slice(1).toLowerCase()).join(" ");
    const dear = $("#dear"); dear.textContent = "Dear " + guest + ","; dear.hidden = false;
    $("#op-for").textContent = "For " + guest;
    const n = $("#guest-name"); if (!n.value) n.value = guest;
  }
  readGuest();
  addEventListener("hashchange", readGuest);
  $$('a[href^="#"]').forEach((a) => a.addEventListener("click", (e) => {
    const t = document.getElementById(a.getAttribute("href").slice(1));
    if (!t) return;
    e.preventDefault();
    t.scrollIntoView({ behavior: reduceMotion() ? "auto" : "smooth", block: "start" });
  }));

  /* ================================================================
     The envelope
     ================================================================ */
  const opener = $("#opener"), env = $("#env"), flap = $("#env-flap"), seal = $("#seal");
  const ribbonCv = $("#ribbon"), rctx = ribbonCv.getContext("2d");
  const ribbonImg = new Image();
  ribbonImg.decoding = "async";
  ribbonImg.src = "assets/img/ribbon-silk.webp";
  const RB = { top: 0, bot: 0, amp: 0, phase: 0 };
  const SEAL_Y = .57;

  function sizeRibbon() {
    const dpr = Math.min(2, devicePixelRatio || 1);
    const w = ribbonCv.clientWidth, h = ribbonCv.clientHeight;
    if (ribbonCv.width !== Math.round(w * dpr) || ribbonCv.height !== Math.round(h * dpr)) {
      ribbonCv.width = Math.round(w * dpr); ribbonCv.height = Math.round(h * dpr);
    }
    rctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    return [w, h];
  }
  function drawRibbon() {
    const [W, H] = sizeRibbon();
    rctx.clearRect(0, 0, W, H);
    if (!ribbonImg.complete || !ribbonImg.naturalWidth) return;
    const rw = Math.max(44, Math.min(66, W * .14));
    const k = rw / ribbonImg.naturalWidth;
    const sy = H * SEAL_Y, cx = W / 2;
    half(sy, sy + 30, -1, RB.top, rw, k, cx, H);
    half(sy, H - sy + 30, 1, RB.bot, rw, k, cx, H);
  }
  function half(y0, len, dir, p, rw, k, cx, H) {
    const step = 3, shift = p * (len + 160);
    const imgH = ribbonImg.naturalHeight, sliceSrc = step / k;
    const release = Math.min(1, p * 3);
    for (let s = 0; s < len; s += step) {
      const y = y0 + dir * (s + shift) - (dir < 0 ? step : 0);
      if (y < -20 || y > H + 20) continue;
      const loose = 1 - s / len;
      const sway = RB.amp * Math.sin(s * .02 + RB.phase * (dir < 0 ? 1 : -1)) * (.35 + .65 * loose) * release;
      const twist = 1 - .6 * Math.abs(Math.sin(s * .012 + RB.phase * .8)) * release * loose;
      const w = rw * twist;
      let src = ((s / k) % (imgH - sliceSrc - 1));
      const x = cx - w / 2 + sway;
      // soft contact shadow on the paper
      rctx.globalAlpha = .1 * (1 - release * .8);
      rctx.fillStyle = "#3c2a10";
      rctx.fillRect(x + 3, y + 3, w, step + .5);
      rctx.globalAlpha = 1;
      rctx.drawImage(ribbonImg, 0, src, ribbonImg.naturalWidth, sliceSrc, x, y, w, step + .6);
      if (twist < .97) { rctx.fillStyle = "rgba(110,60,50," + ((1 - twist) * .45).toFixed(3) + ")"; rctx.fillRect(x + w * .14, y, w * .72, step + .6); }
    }
  }
  ribbonImg.onload = drawRibbon;
  addEventListener("resize", () => { if (!opener.classList.contains("done")) drawRibbon(); });
  drawRibbon();

  document.documentElement.classList.add("locked");
  let opened = false;

  function finishOpening() {
    opener.classList.add("done");
    document.documentElement.classList.remove("locked");
    if (hasGsap) gsap.ticker.remove(drawRibbon);
    window.scrollTo(0, 0);
    const h = $(".hero-card");
    if (hasGsap && !reduceMotion()) gsap.from(h, { y: 18, opacity: 0, duration: .9, ease: "power2.out", clearProps: "all" });
  }

  function openEnvelope() {
    if (opened) return;
    opened = true;
    seal.disabled = true;
    if (!hasGsap || reduceMotion()) {
      opener.style.transition = "opacity .45s ease";
      opener.style.opacity = "0";
      setTimeout(finishOpening, 460);
      return;
    }
    gsap.ticker.add(drawRibbon);
    const vh = innerHeight;
    const tl = gsap.timeline({ onComplete: finishOpening });
    // 1 · anticipation: the seal gives under the touch, the envelope settles
    tl.to(seal, { scale: .93, duration: .1, ease: "power1.in" })
      .to(seal, { scale: 1, duration: .28, ease: "power2.out" })
      .to(env, { y: 3, duration: .14, yoyo: true, repeat: 1, ease: "sine.inOut" }, "<")
      .to(["#op-hint", "#op-title", "#op-for"], { opacity: 0, y: -10, duration: .4, stagger: .04, ease: "power1.out" }, "<")
      // 2 · ribbon loosens; 3 · seal lifts away
      .addLabel("release", .3)
      .to("#seal-wrap", { y: -22, scale: 1.08, duration: .4, ease: "power2.out" }, "release")
      .to("#seal-shadow", { x: 18, y: 34, scale: 1.3, opacity: .3, duration: .4, ease: "power2.out" }, "release")
      .to(RB, { amp: 14, duration: .45, ease: "sine.out" }, "release")
      .to(RB, { phase: 8, duration: 1.2, ease: "none" }, "release")
      .to(RB, { top: 1, duration: .95, ease: "power2.in" }, "release+=.12")
      .to(RB, { bot: 1, duration: .95, ease: "power2.in" }, "release+=.06")
      .to("#seal-wrap", { y: -vh * .4, x: 30, rotation: -16, opacity: 0, duration: .75, ease: "power2.in" }, "release+=.4")
      .to("#seal-shadow", { opacity: 0, duration: .25 }, "release+=.4")
      // 4 · the flap folds back
      .addLabel("flap", "release+=.55")
      .to("#flap-shadow", { opacity: 0, duration: .35, ease: "power1.out" }, "flap")
      .to("#pocket-edge", { opacity: 1, duration: .5 }, "flap+=.3")
      .to(flap, {
        rotationX: 178, duration: .9, ease: "power2.inOut",
        onUpdate() {
          const r = gsap.getProperty(flap, "rotationX");
          flap.style.zIndex = r > 90 ? 2 : 6;
          $("#shade-front").style.opacity = (Math.sin(r * Math.PI / 180) * .3).toFixed(3);
          $("#shade-back").style.opacity = (r > 90 ? .5 * (1 - (r - 90) / 90) : .5).toFixed(3);
        }
      }, "flap")
      // 5 · the card rises with weight
      .addLabel("rise", "flap+=.5")
      .to("#env-card", { yPercent: -36, duration: .9, ease: "power3.out" }, "rise")
      // 6 · the invitation opens into the page
      .addLabel("expand", "rise+=.62")
      .to(["#env-pocket", ".env-inside", "#ribbon"], { yPercent: 30, opacity: 0, duration: .6, ease: "power2.in" }, "expand")
      .to(flap, { opacity: 0, duration: .35 }, "expand")
      .to("#env-card", { scale: 1.18, opacity: 0, duration: .65, ease: "power2.in" }, "expand+=.08")
      .to(opener, { opacity: 0, duration: .45, ease: "power1.out" }, "expand+=.3");
  }
  seal.addEventListener("click", openEnvelope);
  seal.addEventListener("pointerdown", () => { if (hasGsap && !opened) gsap.to(seal, { scale: .95, duration: .12 }); });

  /* ================================================================
     Countdown
     ================================================================ */
  (function () {
    const target = new Date(CONFIG.weddingDate).getTime();
    const pad = (n) => String(n).padStart(2, "0");
    const d = $("#cd-d"), h = $("#cd-h"), m = $("#cd-m"), s = $("#cd-s");
    function tick() {
      let ms = Math.max(0, target - Date.now());
      const D = Math.floor(ms / 864e5); ms -= D * 864e5;
      const H = Math.floor(ms / 36e5); ms -= H * 36e5;
      const M = Math.floor(ms / 6e4); ms -= M * 6e4;
      d.textContent = D; h.textContent = pad(H); m.textContent = pad(M); s.textContent = pad(Math.floor(ms / 1000));
    }
    tick(); setInterval(tick, 1000);
  })();

  /* ================================================================
     Story: paper letters
     ================================================================ */
  const track = $("#track"), dotsEl = $("#dots"), prev = $("#prev"), next = $("#next");
  const POSY = ["floral-posy-1.webp", "floral-posy-2.webp", "floral-posy-3.webp", "floral-posy-4.webp"];
  CHAPTERS.forEach((c, i) => {
    const card = document.createElement("article");
    card.className = "paper lcard" + (c.forest ? " forest" : "");
    card.setAttribute("aria-label", "Chapter " + (i + 1) + ": " + c.title);
    card.innerHTML =
      (c.forest
        ? '<svg class="crown-mark" aria-hidden="true"><use href="#crown"/></svg>'
        : '<img class="posy botan" src="assets/img/' + POSY[i % 4] + '" alt="" loading="lazy" decoding="async">') +
      '<span class="num">Chapter ' + ROMAN[i] + '</span><p class="ldate"></p><h3></h3><p class="gist"></p>' +
      '<button class="btn-line" type="button" data-i="' + i + '"><svg aria-hidden="true"><use href="#heart"/></svg>Read our letter</button>';
    $(".ldate", card).textContent = c.date;
    $("h3", card).textContent = c.title;
    $(".gist", card).textContent = c.gist;
    track.appendChild(card);
    const dot = document.createElement("button");
    dot.type = "button"; dot.setAttribute("aria-label", "Chapter " + (i + 1)); dot.dataset.i = i;
    dotsEl.appendChild(dot);
  });
  const cards = $$(".lcard", track), dots = $$("button", dotsEl);
  let cur = 0;
  function centreOf(i) { const c = cards[i]; return c.offsetLeft - (track.clientWidth - c.offsetWidth) / 2; }
  function go(i) {
    i = Math.max(0, Math.min(cards.length - 1, i));
    track.scrollTo({ left: centreOf(i), behavior: reduceMotion() ? "auto" : "smooth" });
  }
  function update() {
    let best = 0, bd = Infinity;
    cards.forEach((c, i) => { const d = Math.abs(centreOf(i) - track.scrollLeft); if (d < bd) { bd = d; best = i; } });
    cur = best;
    dots.forEach((b, i) => b.setAttribute("aria-current", i === cur ? "true" : "false"));
    prev.disabled = cur === 0; next.disabled = cur === cards.length - 1;
  }
  let raf = 0;
  track.addEventListener("scroll", () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(update); }, { passive: true });
  prev.addEventListener("click", () => go(cur - 1));
  next.addEventListener("click", () => go(cur + 1));
  dots.forEach((b) => b.addEventListener("click", () => go(+b.dataset.i)));
  track.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight") { e.preventDefault(); go(cur + 1); }
    if (e.key === "ArrowLeft") { e.preventDefault(); go(cur - 1); }
  });
  update();

  const dlg = $("#letter"), paperEl = $("#letter-paper"), txt = $("#letter-text");
  let openIdx = 0, closing = false;
  function fill(i) {
    openIdx = i;
    const c = CHAPTERS[i];
    $("#letter-date").textContent = c.date;
    $("#letter-title").textContent = c.title;
    txt.textContent = "";
    c.text.forEach((t) => {
      const p = document.createElement("p");
      if (t[0] === "*") { p.className = "pull"; t = t.slice(1); }
      p.textContent = t; txt.appendChild(p);
    });
    $("#letter-prev").disabled = i === 0;
    $("#letter-next").disabled = i === CHAPTERS.length - 1;
    $("#letter-scroll").scrollTop = 0;
  }
  function openLetter(i) {
    fill(i);
    if (typeof dlg.showModal === "function") { if (!dlg.open) dlg.showModal(); } else dlg.setAttribute("open", "");
    if (hasGsap && !reduceMotion()) gsap.fromTo(paperEl, { y: 40, rotation: -1.2, opacity: 0, scale: .97 }, { y: 0, rotation: 0, opacity: 1, scale: 1, duration: .55, ease: "power3.out" });
    $("#letter-close").focus();
  }
  function closeLetter() {
    if (closing) return;
    const done = () => { closing = false; if (dlg.open) dlg.close(); else dlg.removeAttribute("open"); go(openIdx); const b = cards[openIdx] && $(".btn-line", cards[openIdx]); if (b) b.focus({ preventScroll: true }); };
    if (hasGsap && !reduceMotion()) { closing = true; gsap.to(paperEl, { y: 30, rotation: .8, opacity: 0, duration: .32, ease: "power2.in", onComplete: done }); }
    else done();
  }
  function turn(i) {
    if (hasGsap && !reduceMotion()) {
      const dir = i > openIdx ? 1 : -1;
      gsap.to(paperEl, { x: -30 * dir, opacity: 0, duration: .2, ease: "power1.in", onComplete() { fill(i); gsap.fromTo(paperEl, { x: 30 * dir, opacity: 0 }, { x: 0, opacity: 1, duration: .3, ease: "power2.out" }); } });
    } else fill(i);
  }
  track.addEventListener("click", (e) => { const b = e.target.closest(".btn-line"); if (b) openLetter(+b.dataset.i); });
  $("#letter-close").addEventListener("click", closeLetter);
  $("#letter-prev").addEventListener("click", () => turn(openIdx - 1));
  $("#letter-next").addEventListener("click", () => turn(openIdx + 1));
  dlg.addEventListener("cancel", (e) => { e.preventDefault(); closeLetter(); });
  dlg.addEventListener("click", (e) => { if (e.target === dlg) closeLetter(); });

  /* ================================================================
     RSVP → WhatsApp
     ================================================================ */
  const form = $("#rsvp-form"), nextStep = $("#next-step"), err = $("#rsvp-error"), wa = $("#rsvp-whatsapp");
  let reply = "";
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const name = form.name.value.trim(), attending = form.attending.value;
    form.name.removeAttribute("aria-invalid");
    if (!name) { err.textContent = "Please add your full name so we know who is replying."; form.name.setAttribute("aria-invalid", "true"); form.name.focus(); return; }
    if (!attending) { err.textContent = "Please let us know whether you'll be joining us."; $("#attend-yes").focus(); return; }
    err.textContent = "";
    const phone = form.phone.value.trim(), msg = form.message.value.trim();
    reply = [
      "RSVP · La Vida · " + CONFIG.couple + " · 29 March 2027",
      "Name: " + name,
      "White wedding: " + (attending === "yes" ? "Joyfully accepts" : "Regretfully declines"),
      phone ? "Phone: " + phone : "",
      msg ? "Message: " + msg : "",
    ].filter(Boolean).join("\n");
    $("#rsvp-text").textContent = reply;
    wa.href = "https://wa.me/" + CONFIG.whatsapp + "?text=" + encodeURIComponent(reply);
    form.hidden = true; nextStep.hidden = false;
    $("#next-title").focus({ preventScroll: true });
    nextStep.scrollIntoView({ behavior: reduceMotion() ? "auto" : "smooth", block: "center" });
  });
  $("#rsvp-copy").addEventListener("click", async () => {
    const s = $("#copy-status");
    try { await navigator.clipboard.writeText(reply); s.textContent = "Copied. Paste it into a message to +234 806 801 5338."; }
    catch (_) { s.textContent = "Copying isn't available here. Select the text above and copy it."; }
  });
  $("#rsvp-edit").addEventListener("click", () => { nextStep.hidden = true; form.hidden = false; $("#copy-status").textContent = ""; form.name.focus(); });
})();
