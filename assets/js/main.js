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
    var digits = phoneRaw.replace(/\D/g, "");

    if (!name || digits.length < 10) {
      if (success) success.style.display = "none";
      if (error) error.style.display = "block";
      return false;
    }

    if (success) success.style.display = "none";
    if (error) error.style.display = "none";

    var formData = new FormData(form);
    formData.set("phone", "+7 " + phoneRaw);

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
        var step = item ? item.getBoundingClientRect().width + 12 : 200;
        grid.scrollBy({ left: dir * step, behavior: "smooth" });
      }

      if (btnLeft) btnLeft.addEventListener("click", function () { scrollByAmount(-1); });
      if (btnRight) btnRight.addEventListener("click", function () { scrollByAmount(1); });
    });
  }

  /* Lightbox */
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
    function onScroll() {
      if (window.scrollY > 12) header.classList.add("is-scrolled");
      else header.classList.remove("is-scrolled");
    }
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* Scroll reveal */
  function initReveal() {
    var nodes = $$(".reveal");
    if (!nodes.length) return;
    if (!("IntersectionObserver" in window)) {
      nodes.forEach(function (n) {
        n.classList.add("is-visible");
      });
      return;
    }
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    nodes.forEach(function (n) {
      io.observe(n);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initUpload(document);
    initGalleries();
    initLightbox();
    initHeaderScroll();
    initReveal();
  });
})();
