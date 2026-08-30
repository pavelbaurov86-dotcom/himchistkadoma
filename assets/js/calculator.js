(function (root) {
  "use strict";

  var PRICES = {
    sofa_straight: 4500,
    sofa_corner: 5400,
    sofa_large_corner: 7200,
    sofa_u: 9000,
    chair_kitchen: 720,
    armchair: 1800,
    mattress_single: 1350,
    mattress_double: 2700,
    curtains: 180,
    carpet: 450,
    ac: 3150,
    windows: 585,
  };

  var LABELS = {
    sofa_straight: "Диван прямой",
    sofa_corner: "Диван угловой",
    sofa_large_corner: "Диван большой угловой",
    sofa_u: "Диван П-образный",
    chair_kitchen: "Стул кухонный с тканевой спинкой",
    armchair: "Кресло",
    mattress_single: "Матрас односпальный (сторона)",
    mattress_double: "Матрас двуспальный (сторона)",
    curtains: "Шторы, м²",
    carpet: "Ковёр, м²",
    ac: "Кондиционер",
    windows: "Окно, створка",
  };

  var DRYING_RATE = 1.3;

  function toQty(value) {
    var n = Number(value);
    if (!isFinite(n) || n < 0) return 0;
    return Math.floor(n);
  }

  function computeTotal(items, drying) {
    var subtotal = 0;
    if (!items || !items.length) return 0;
    for (var i = 0; i < items.length; i++) {
      var row = items[i] || {};
      var price = Number(row.price);
      var qty = toQty(row.qty);
      if (!isFinite(price) || price < 0 || qty === 0) continue;
      subtotal += price * qty;
    }
    if (!isFinite(subtotal) || subtotal <= 0) return 0;
    var total = drying ? Math.round(subtotal * DRYING_RATE) : subtotal;
    return isFinite(total) ? total : 0;
  }

  function formatMoney(n) {
    var v = computeTotal([{ price: n, qty: 1 }], false);
    return String(v).replace(/\B(?=(\d{3})+(?!\d))/g, "\u00a0") + "\u00a0₽";
  }

  function collectState(root) {
    var items = [];
    var lines = [];
    var inputs = root.querySelectorAll("[data-calc-item]");
    for (var i = 0; i < inputs.length; i++) {
      var el = inputs[i];
      var key = el.getAttribute("data-calc-item");
      var qty = toQty(el.value);
      var price = PRICES[key];
      if (price == null) continue;
      el.value = String(qty);
      if (qty <= 0) continue;
      items.push({ key: key, price: price, qty: qty });
      lines.push(LABELS[key] + " × " + qty + " — от " + formatMoney(price * qty));
    }
    var drying = !!(root.querySelector("[data-calc-drying]") || {}).checked;
    var total = computeTotal(items, drying);
    return { items: items, lines: lines, drying: drying, total: total };
  }

  function renderTotal(root, state) {
    var money = root.querySelector("[data-calc-total]");
    var hint = root.querySelector("[data-calc-hint]");
    if (money) money.textContent = formatMoney(state.total).replace("\u00a0₽", "") + "\u00a0₽";
    if (hint) {
      if (state.total === 0) hint.textContent = "Добавьте позиции — сумма считается сразу";
      else if (state.drying) hint.textContent = "Включая сушку +30%";
      else hint.textContent = "Ориентир «от». Точную цену фиксируем по фото";
    }
  }

  function draftText(state) {
    var parts = state.lines.slice();
    if (state.drying) parts.push("Нужна сушка (+30%)");
    parts.push("Итого от " + formatMoney(state.total));
    return parts.join("\n");
  }

  function fillRequest(state) {
    var text = draftText(state);
    try { sessionStorage.setItem("him-calc-draft", text); } catch (e) {}
    var comment = document.getElementById("comment");
    if (!comment) return false;
    comment.value = text;
    comment.dispatchEvent(new Event("input", { bubbles: true }));
    return true;
  }

  function onStepper(btn) {
    var key = btn.getAttribute("data-calc-step");
    var dir = Number(btn.getAttribute("data-dir") || "1");
    var input = document.querySelector('[data-calc-item="' + key + '"]');
    if (!input) return;
    var next = toQty(input.value) + dir;
    if (next < 0) next = 0;
    if (next > 99) next = 99;
    input.value = String(next);
    input.dispatchEvent(new Event("input", { bubbles: true }));
  }

  function init(root) {
    if (!root || root.dataset.calcReady === "1") return;
    root.dataset.calcReady = "1";

    function refresh() {
      renderTotal(root, collectState(root));
    }

    root.addEventListener("click", function (e) {
      var step = e.target.closest("[data-calc-step]");
      if (step) {
        e.preventDefault();
        onStepper(step);
        return;
      }
      var lock = e.target.closest("[data-calc-lock]");
      if (lock) {
        e.preventDefault();
        var state = collectState(root);
        var filled = fillRequest(state);
        var form = document.getElementById("form-block");
        if (form) {
          if (window.scrollToId) window.scrollToId("form-block");
          else form.scrollIntoView({ behavior: "smooth", block: "start" });
          var comment = document.getElementById("comment");
          if (comment) comment.focus();
        } else if (!filled) {
          window.location.href = "index.html#form-block";
        }
      }
    });

    root.addEventListener("input", function (e) {
      if (e.target.matches("[data-calc-item], [data-calc-drying]")) refresh();
    });
    root.addEventListener("change", function (e) {
      if (e.target.matches("[data-calc-item], [data-calc-drying]")) refresh();
    });

    refresh();
  }

  var api = {
    prices: PRICES,
    labels: LABELS,
    dryingRate: DRYING_RATE,
    computeTotal: computeTotal,
    formatMoney: formatMoney,
    collectState: collectState,
    init: init,
  };

  root.HimchistkaCalc = api;
})(typeof window !== "undefined" ? window : globalThis);

if (typeof document !== "undefined") {
  document.addEventListener("DOMContentLoaded", function () {
    var root = document.getElementById("calculator");
    if (root && window.HimchistkaCalc) window.HimchistkaCalc.init(root);
    var comment = document.getElementById("comment");
    if (comment && !comment.value) {
      try {
        var draft = sessionStorage.getItem("him-calc-draft");
        if (draft) comment.value = draft;
      } catch (e) {}
    }
  });
}
