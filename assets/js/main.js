(function () {
  "use strict";

  var SCRIPT_URL =
    "https://script.google.com/macros/s/AKfycbybXYyLaTEnCSd8pVNKS9bG_FxcVu9e2MNln4-XEUbPO3M2wMyo0pdeXGWQfV8cnxg4tg/exec";

  function $(sel, root) {
    return (root || document).querySelector(sel);
  }

  function $$(sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  }

  function scrollToId(id) {
    var el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  window.scrollToId = scrollToId;

  /* Year */
  var yearEl = $("#year");
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  /* Mobile menu */
  var menu = $("#mobile-menu");
  var burger = $("#burger");

  function openMenu() {
    if (!menu || !burger) return;
    menu.classList.add("open");
    burger.classList.add("active");
    burger.setAttribute("aria-expanded", "true");
    document.body.classList.add("menu-open");
  }

  function closeMenu() {
    if (!menu || !burger) return;
    menu.classList.remove("open");
    burger.classList.remove("active");
    burger.setAttribute("aria-expanded", "false");
    document.body.classList.remove("menu-open");
  }

  function toggleMenu() {
    if (!menu) return;
    if (menu.classList.contains("open")) closeMenu();
    else openMenu();
  }

  window.toggleMobileMenu = toggleMenu;
  window.closeMobileMenu = closeMenu;

  if (burger) {
    burger.addEventListener("click", function (e) {
      e.preventDefault();
      toggleMenu();
    });
  }

  if (menu) {
    menu.addEventListener("click", function (e) {
      var link = e.target.closest("a");
      if (!link) return;
      closeMenu();
      var href = link.getAttribute("href") || "";
      if (href.charAt(0) === "#") {
        e.preventDefault();
        scrollToId(href.slice(1));
      }
    });
  }

  /* Smooth hash links in desktop nav */
  document.addEventListener("click", function (e) {
    var link = e.target.closest('a[href^="#"]');
    if (!link) return;
    var id = link.getAttribute("href").slice(1);
    if (!id || !document.getElementById(id)) return;
    e.preventDefault();
    scrollToId(id);
  });

  /* Russian phone mask: +7 | 915 754-81-15 */
  function digitsOnly(value) {
    return String(value || "").replace(/\D/g, "");
  }

  function normalizeMobileDigits(value) {
    var d = digitsOnly(value);
    if (d.indexOf("8") === 0 && d.length >= 11) d = d.slice(1);
    if (d.indexOf("7") === 0 && d.length >= 11) d = d.slice(1);
    return d.slice(0, 10);
  }

  function formatMobileMask(digits) {
    var d = digits.slice(0, 10);
    var out = "";
    if (d.length > 0) out += d.slice(0, Math.min(3, d.length));
    if (d.length > 3) out += " " + d.slice(3, Math.min(6, d.length));
    if (d.length > 6) out += "-" + d.slice(6, Math.min(8, d.length));
    if (d.length > 8) out += "-" + d.slice(8, Math.min(10, d.length));
    return out;
  }

  function countDigitsLeft(value, caret) {
    return digitsOnly(value.slice(0, caret)).length;
  }

  function caretFromDigitIndex(formatted, digitIndex) {
    if (digitIndex <= 0) return 0;
    var seen = 0;
    for (var i = 0; i < formatted.length; i++) {
      if (/\d/.test(formatted.charAt(i))) {
        seen += 1;
        if (seen >= digitIndex) return i + 1;
      }
    }
    return formatted.length;
  }

  function initPhoneMasks(root) {
    var inputs = $$(
      'input[name="phone"][type="tel"], .phone-input-wrap input[type="tel"]',
      root || document
    );
    inputs.forEach(function (input) {
      if (input.dataset.maskReady === "1") return;
      input.dataset.maskReady = "1";
      input.setAttribute("maxlength", "13");
      input.setAttribute("autocomplete", "tel-national");

      function applyMask(keepCaret) {
        var start = input.selectionStart || 0;
        var digitPos = countDigitsLeft(input.value, start);
        var digits = normalizeMobileDigits(input.value);
        var formatted = formatMobileMask(digits);
        input.value = formatted;
        if (keepCaret && document.activeElement === input) {
          var next = caretFromDigitIndex(formatted, digitPos);
          try {
            input.setSelectionRange(next, next);
          } catch (e) {}
        }
      }

      input.addEventListener("input", function () {
        applyMask(true);
      });

      input.addEventListener("paste", function () {
        requestAnimationFrame(function () {
          applyMask(true);
        });
      });

      input.addEventListener("blur", function () {
        applyMask(false);
      });
    });
  }

  /* Form submit */
  window.handleSubmit = function (event) {
    event.preventDefault();

    var form = $("#request-form") || (event.target && event.target.closest("form"));
    if (!form) return false;

    var nameInput = form.querySelector('[name="name"]');
    var phoneInput = form.querySelector('[name="phone"]');
    var success = form.querySelector(".form-success") || $("#form-success");
    var error = form.querySelector(".form-error") || $("#form-error");

    var name = nameInput ? nameInput.value.trim() : "";
    var phoneRaw = phoneInput ? phoneInput.value.trim() : "";
    var digits = normalizeMobileDigits(phoneRaw);

    if (!name || digits.length < 10) {
      if (success) success.style.display = "none";
      if (error) error.style.display = "block";
      return false;
    }

    if (success) success.style.display = "none";
    if (error) error.style.display = "none";

    var formData = new FormData(form);
    formData.set("phone", "+7" + digits);

    var submitBtn = form.querySelector('[type="submit"]');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.dataset.label = submitBtn.textContent;
      submitBtn.textContent = "Отправка…";
    }

    fetch(SCRIPT_URL, { method: "POST", body: formData })
      .then(function (response) {
        if (!response.ok) throw new Error("Network response was not ok");
        return response.text();
      })
      .then(function () {
        if (success) success.style.display = "block";
        form.reset();
        var uploadInfo = form.querySelector(".upload-info") || $("#upload-info");
        if (uploadInfo) uploadInfo.textContent = "Файлы не выбраны";
      })
      .catch(function (err) {
        console.error(err);
        if (success) success.style.display = "none";
        if (error) error.style.display = "block";
      })
      .finally(function () {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = submitBtn.dataset.label || "Отправить заявку";
        }
      });

    return false;
  };

  /* Upload area */
  function initUpload(root) {
    var uploadArea = (root || document).querySelector("#upload-area") || (root || document).querySelector(".upload-area");
    var photosInput = (root || document).querySelector("#photos") || (root || document).querySelector('input[type="file"][name="photos"]');
    if (!uploadArea || !photosInput) return;

    var uploadInfo = (root || document).querySelector("#upload-info") || (root || document).querySelector(".upload-info");

    function updateUploadInfo() {
      if (!uploadInfo) return;
      var count = photosInput.files ? photosInput.files.length : 0;
      if (count === 0) uploadInfo.textContent = "Файлы не выбраны";
      else if (count === 1) uploadInfo.textContent = "Прикреплено 1 фото";
      else uploadInfo.textContent = "Прикреплено " + count + " фото";
    }

    uploadArea.addEventListener("click", function () {
      photosInput.click();
    });

    uploadArea.addEventListener("dragover", function (e) {
      e.preventDefault();
      uploadArea.classList.add("dragover");
    });

    uploadArea.addEventListener("dragleave", function (e) {
      e.preventDefault();
      uploadArea.classList.remove("dragover");
    });

    uploadArea.addEventListener("drop", function (e) {
      e.preventDefault();
      uploadArea.classList.remove("dragover");
      if (e.dataTransfer.files && e.dataTransfer.files.length) {
        photosInput.files = e.dataTransfer.files;
        updateUploadInfo();
      }
    });

    photosInput.addEventListener("change", updateUploadInfo);
    updateUploadInfo();
  }

  /* Gallery arrows */
  function initGalleries() {
    $$(".gallery-wrapper").forEach(function (wrapper) {
      var grid = wrapper.querySelector(".gallery-grid");
      if (!grid) return;

      var btnLeft = wrapper.querySelector(".gallery-arrow-left");
      var btnRight = wrapper.querySelector(".gallery-arrow-right");

      function scrollByAmount(dir) {
        var item = grid.querySelector(".gallery-item");
        var step = item ? item.getBoundingClientRect().width + 14 : 200;
        grid.scrollBy({ left: dir * step, behavior: "smooth" });
      }

      function setArrowState(btn, hidden) {
        if (!btn) return;
        btn.classList.toggle("is-hidden", hidden);
        btn.disabled = hidden;
        btn.setAttribute("aria-hidden", hidden ? "true" : "false");
      }

      function updateArrows() {
        if (wrapper._arrowRaf) return;
        wrapper._arrowRaf = requestAnimationFrame(function () {
          wrapper._arrowRaf = 0;
          var maxScroll = Math.max(0, grid.scrollWidth - grid.clientWidth);
          var left = grid.scrollLeft || 0;
          var eps = 16;
          var noScroll = maxScroll <= eps;
          var atStart = noScroll || left <= eps;
          var atEnd = noScroll || left >= maxScroll - eps;
          setArrowState(btnLeft, atStart);
          setArrowState(btnRight, atEnd);
        });
      }

      if (btnLeft) {
        btnLeft.addEventListener("click", function () {
          scrollByAmount(-1);
        });
      }
      if (btnRight) {
        btnRight.addEventListener("click", function () {
          scrollByAmount(1);
        });
      }

      grid.addEventListener("scroll", updateArrows, { passive: true });
      if ("onscrollend" in grid) {
        grid.addEventListener("scrollend", updateArrows);
      }
      window.addEventListener("resize", updateArrows);
      window.addEventListener("load", updateArrows);

      if ("ResizeObserver" in window) {
        var ro = new ResizeObserver(function () {
          updateArrows();
        });
        ro.observe(grid);
        wrapper.querySelectorAll(".gallery-item").forEach(function (item) {
          ro.observe(item);
        });
      }

      $$("img", grid).forEach(function (img) {
        if (!img.complete) img.addEventListener("load", updateArrows);
      });

      updateArrows();
      requestAnimationFrame(updateArrows);
    });
  }

  /* Before / After split sliders */
  function initBeforeAfter() {
    var sliders = $$(".ba-slider");
    if (!sliders.length) return;

    var reduceMotion =
      window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var demoStopped = false;
    var demoRaf = 0;

    sliders.forEach(function (slider) {
      var handle = slider.querySelector(".ba-handle");
      if (!handle) return;

      var grid = slider.closest(".gallery-grid");
      var dragging = false;
      var activePointer = null;

      function setPos(pct) {
        pct = Math.max(0, Math.min(100, pct));
        slider.style.setProperty("--pos", pct + "%");
        slider.dataset.pos = String(Math.round(pct));
        handle.setAttribute("aria-valuenow", String(Math.round(pct)));
      }

      function clientXFromEvent(e) {
        if (e.touches && e.touches[0]) return e.touches[0].clientX;
        if (e.changedTouches && e.changedTouches[0]) return e.changedTouches[0].clientX;
        return e.clientX;
      }

      function posFromEvent(e) {
        var rect = slider.getBoundingClientRect();
        if (rect.width <= 0) return Number(slider.dataset.pos || 50);
        return ((clientXFromEvent(e) - rect.left) / rect.width) * 100;
      }

      function stopDemo() {
        if (demoStopped) return;
        demoStopped = true;
        if (demoRaf) cancelAnimationFrame(demoRaf);
        demoRaf = 0;
        sliders.forEach(function (s) {
          s.classList.remove("ba-demoing");
        });
      }

      function endDrag() {
        if (!dragging) return;
        dragging = false;
        activePointer = null;
        slider.classList.remove("is-dragging");
        if (grid) grid.classList.remove("is-ba-dragging");
      }

      function onMove(e) {
        if (!dragging) return;
        if (activePointer != null && e.pointerId != null && e.pointerId !== activePointer) return;
        if (e.cancelable) e.preventDefault();
        setPos(posFromEvent(e));
      }

      function onUp(e) {
        if (!dragging) return;
        if (activePointer != null && e.pointerId != null && e.pointerId !== activePointer) return;
        try {
          if (e.pointerId != null && handle.releasePointerCapture) {
            handle.releasePointerCapture(e.pointerId);
          }
        } catch (err) {}
        endDrag();
        handle.removeEventListener("pointermove", onMove);
        handle.removeEventListener("pointerup", onUp);
        handle.removeEventListener("pointercancel", onUp);
        window.removeEventListener("pointermove", onMove);
        window.removeEventListener("pointerup", onUp);
        window.removeEventListener("pointercancel", onUp);
        window.removeEventListener("mousemove", onMove);
        window.removeEventListener("mouseup", onUp);
        window.removeEventListener("touchmove", onMove);
        window.removeEventListener("touchend", onUp);
        window.removeEventListener("touchcancel", onUp);
      }

      function startDrag(e) {
        if (typeof e.button === "number" && e.button > 0) return;
        stopDemo();
        dragging = true;
        activePointer = e.pointerId != null ? e.pointerId : null;
        slider.classList.add("is-dragging");
        if (grid) grid.classList.add("is-ba-dragging");
        setPos(posFromEvent(e));

        if (e.pointerId != null && handle.setPointerCapture) {
          try {
            handle.setPointerCapture(e.pointerId);
          } catch (err) {}
          handle.addEventListener("pointermove", onMove);
          handle.addEventListener("pointerup", onUp);
          handle.addEventListener("pointercancel", onUp);
        } else if (e.type.indexOf("touch") === 0) {
          window.addEventListener("touchmove", onMove, { passive: false });
          window.addEventListener("touchend", onUp);
          window.addEventListener("touchcancel", onUp);
        } else {
          window.addEventListener("mousemove", onMove);
          window.addEventListener("mouseup", onUp);
        }

        if (e.cancelable) e.preventDefault();
        e.stopPropagation();
      }

      handle.addEventListener("pointerdown", startDrag);
      handle.addEventListener("mousedown", function (e) {
        if (window.PointerEvent) return;
        startDrag(e);
      });
      handle.addEventListener(
        "touchstart",
        function (e) {
          if (window.PointerEvent) return;
          startDrag(e);
        },
        { passive: false }
      );

      // Click anywhere on the card also moves the split
      slider.addEventListener("pointerdown", function (e) {
        if (e.target === handle || handle.contains(e.target)) return;
        startDrag(e);
      });

      handle.addEventListener("keydown", function (e) {
        var cur = Number(slider.dataset.pos || 50);
        if (e.key === "ArrowLeft") {
          e.preventDefault();
          stopDemo();
          setPos(cur - 3);
        } else if (e.key === "ArrowRight") {
          e.preventDefault();
          stopDemo();
          setPos(cur + 3);
        } else if (e.key === "Home") {
          e.preventDefault();
          stopDemo();
          setPos(0);
        } else if (e.key === "End") {
          e.preventDefault();
          stopDemo();
          setPos(100);
        }
      });
    });

    function animatePos(slider, from, to, duration) {
      return new Promise(function (resolve) {
        var start = performance.now();
        function ease(t) {
          return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
        }
        function frame(now) {
          if (demoStopped) {
            resolve();
            return;
          }
          var t = Math.min(1, (now - start) / duration);
          var pct = from + (to - from) * ease(t);
          slider.style.setProperty("--pos", pct + "%");
          slider.dataset.pos = String(Math.round(pct));
          var h = slider.querySelector(".ba-handle");
          if (h) h.setAttribute("aria-valuenow", String(Math.round(pct)));
          if (t < 1) {
            demoRaf = requestAnimationFrame(frame);
          } else {
            resolve();
          }
        }
        demoRaf = requestAnimationFrame(frame);
      });
    }

    function wait(ms) {
      return new Promise(function (resolve) {
        setTimeout(resolve, ms);
      });
    }

    async function runHint(slider) {
      if (demoStopped || reduceMotion) return;
      slider.classList.add("ba-demoing");
      await animatePos(slider, 50, 22, 900);
      if (demoStopped) return;
      await animatePos(slider, 22, 78, 1100);
      if (demoStopped) return;
      await animatePos(slider, 78, 50, 900);
      if (demoStopped) return;
      await wait(350);
      if (demoStopped) return;
      await animatePos(slider, 50, 30, 700);
      if (demoStopped) return;
      await animatePos(slider, 30, 50, 700);
      slider.classList.remove("ba-demoing");
    }

    var first = sliders[0];
    if (reduceMotion || !first) return;

    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (!entry.isIntersecting || demoStopped) return;
            io.disconnect();
            runHint(first);
          });
        },
        { threshold: 0.35 }
      );
      io.observe(first);
    } else {
      runHint(first);
    }
  }

  /* Lightbox (legacy thumbs, if present) */
  function initLightbox() {
    var modal = $("#workModal");
    var modalImg = $("#workModalImg");
    var closeBtn = $("#workModalClose");
    var thumbs = $$(".work-thumb");
    if (!modal || !modalImg || !thumbs.length) return;

    function openModal(src, alt) {
      modalImg.src = src;
      modalImg.alt = alt || "Фото работы";
      modal.classList.add("open");
      document.body.style.overflow = "hidden";
    }

    function closeModal() {
      modal.classList.remove("open");
      document.body.style.overflow = "";
      modalImg.removeAttribute("src");
    }

    thumbs.forEach(function (thumb) {
      thumb.addEventListener("click", function () {
        var full = thumb.getAttribute("data-full") || thumb.src;
        openModal(full, thumb.alt);
      });
    });

    modal.addEventListener("click", function (e) {
      if (e.target === modal) closeModal();
    });

    if (closeBtn) closeBtn.addEventListener("click", closeModal);

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && modal.classList.contains("open")) closeModal();
    });
  }

  /* Sticky header elevation */
  function initHeaderScroll() {
    var header = document.querySelector(".site-header");
    if (!header) return;
    var scrolled = false;
    function onScroll() {
      var next = window.scrollY > 12;
      if (next === scrolled) return;
      scrolled = next;
      header.classList.toggle("is-scrolled", scrolled);
    }
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* Scroll reveal */
  function initReveal() {
    var nodes = $$(".reveal");
    if (!nodes.length) return;

    function show(n) {
      n.classList.add("is-visible");
    }

    if (!("IntersectionObserver" in window)) {
      nodes.forEach(show);
      return;
    }

    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            show(entry.target);
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.01, rootMargin: "0px 0px -8% 0px" }
    );

    nodes.forEach(function (n) {
      io.observe(n);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    function safe(fn) {
      try {
        fn();
      } catch (err) {
        console.error(err);
      }
    }

    function whenIdle(fn) {
      if ("requestIdleCallback" in window) {
        requestIdleCallback(function () {
          safe(fn);
        }, { timeout: 2000 });
      } else {
        setTimeout(function () {
          safe(fn);
        }, 1);
      }
    }

    safe(initHeaderScroll);
    safe(function () { initUpload(document); });
    safe(function () { initPhoneMasks(document); });
    whenIdle(initReveal);
    whenIdle(initGalleries);
    whenIdle(initBeforeAfter);
    whenIdle(initLightbox);
  });
})();
