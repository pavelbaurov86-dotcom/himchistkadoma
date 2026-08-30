(function () {
  "use strict";

  var Calc = window.HimchistkaCalc;
  if (!Calc) return;

  var STORAGE = "him-calc-cart";

  var CATS = [
    {
      id: "sofa",
      name: "Диваны",
      title: "Диван",
      from: 4500,
      qtyLabel: "Сколько штук",
      types: [
        { key: "sofa_straight", label: "Прямой", price: 4500 },
        { key: "sofa_corner", label: "Угловой", price: 5400 },
        { key: "sofa_large_corner", label: "Большой угловой", price: 7200 },
        { key: "sofa_u", label: "П-образный", price: 9000 },
      ],
    },
    {
      id: "chair",
      name: "Стулья",
      title: "Стул",
      from: 720,
      qtyLabel: "Сколько штук",
      types: [{ key: "chair_kitchen", label: "Стул кухонный", price: 720 }],
    },
    {
      id: "armchair",
      name: "Кресла",
      title: "Кресло",
      from: 1800,
      qtyLabel: "Сколько штук",
      types: [{ key: "armchair", label: "Кресло", price: 1800 }],
    },
    {
      id: "mattress",
      name: "Матрасы",
      title: "Матрас",
      from: 1350,
      qtyLabel: "Сколько сторон",
      types: [
        { key: "mattress_single", label: "Односпальный", price: 1350, unit: "/ сторона" },
        { key: "mattress_double", label: "Двуспальный", price: 2700, unit: "/ сторона" },
      ],
    },
    {
      id: "carpet",
      name: "Ковры",
      title: "Ковёр",
      from: 450,
      fromSuffix: " ₽/м²",
      qtyLabel: "Сколько м²",
      types: [{ key: "carpet", label: "Ковёр", price: 450, unit: "/ м²" }],
    },
    {
      id: "curtains",
      name: "Шторы",
      title: "Шторы",
      from: 180,
      fromSuffix: " ₽/м²",
      qtyLabel: "Сколько м²",
      types: [{ key: "curtains", label: "Шторы", price: 180, unit: "/ м²" }],
    },
    {
      id: "ac",
      name: "Кондиционер",
      title: "Кондиционер",
      from: 3150,
      qtyLabel: "Сколько штук",
      types: [{ key: "ac", label: "Кондиционер", price: 3150 }],
    },
    {
      id: "windows",
      name: "Окна",
      title: "Окна",
      from: 585,
      fromSuffix: " ₽/створка",
      qtyLabel: "Сколько створок",
      types: [{ key: "windows", label: "Окно", price: 585, unit: "/ створка" }],
    },
  ];

  var ICONS = {
    sofa: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M4 14V10a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v4"/><path d="M3 14h18v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-3z"/><path d="M7 8V6a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v2"/></svg>',
    chair: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M8 10V7a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v3"/><path d="M6 10h12v5H6z"/><path d="M8 15v4M16 15v4M7 19h10"/></svg>',
    armchair: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M7 10V7a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v3"/><path d="M5 10h14v5a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-5z"/><path d="M8 17v3M16 17v3"/></svg>',
    mattress: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M3 15h18v2a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-2z"/><path d="M4 15V9a3 3 0 0 1 3-3h10a3 3 0 0 1 3 3v6"/></svg>',
    carpet: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 10h18M8 5v14M16 5v14"/></svg>',
    curtains: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M4 5h16M6 5v14M18 5v14M12 5v14"/><path d="M6 19h12"/></svg>',
    ac: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><rect x="3" y="5" width="18" height="8" rx="2"/><path d="M7 17v2M12 16v3M17 17v2"/></svg>',
    windows: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><rect x="4" y="4" width="16" height="16" rx="1"/><path d="M12 4v16M4 12h16"/></svg>',
  };

  var state = {
    view: "tiles",
    catId: null,
    typeKey: null,
    qty: 1,
    drying: false,
    cart: [],
  };

  function money(n) {
    return Calc.formatMoney(n);
  }

  function loadCart() {
    try {
      var raw = sessionStorage.getItem(STORAGE);
      if (raw) state.cart = JSON.parse(raw) || [];
    } catch (e) {
      state.cart = [];
    }
  }

  function saveCart() {
    try {
      sessionStorage.setItem(STORAGE, JSON.stringify(state.cart));
    } catch (e) {}
  }

  function lineTotal(item) {
    return Calc.computeTotal([{ price: item.price, qty: item.qty }], item.drying);
  }

  function cartTotal() {
    var sum = 0;
    for (var i = 0; i < state.cart.length; i++) sum += lineTotal(state.cart[i]);
    return sum;
  }

  function catById(id) {
    for (var i = 0; i < CATS.length; i++) if (CATS[i].id === id) return CATS[i];
    return null;
  }

  function typeByKey(cat, key) {
    for (var i = 0; i < cat.types.length; i++) if (cat.types[i].key === key) return cat.types[i];
    return cat.types[0];
  }

  function draftFromCart() {
    var lines = [];
    for (var i = 0; i < state.cart.length; i++) {
      var it = state.cart[i];
      var extra = it.drying ? " + сушка" : "";
      lines.push(it.label + " × " + it.qty + extra + " — от " + money(lineTotal(it)));
    }
    lines.push("Итого от " + money(cartTotal()));
    return lines.join("\n");
  }

  function fillForm() {
    var text = draftFromCart();
    try {
      sessionStorage.setItem("him-calc-draft", text);
    } catch (e) {}
    var comment = document.getElementById("comment");
    if (comment) comment.value = text;
  }

  function el(html) {
    var t = document.createElement("template");
    t.innerHTML = html.trim();
    return t.content.firstChild;
  }

  function renderHeader(title, back) {
    return (
      '<header class="ca-top">' +
      '<button type="button" class="ca-x" data-ca="' +
      back +
      '" aria-label="Закрыть">×</button>' +
      "<h1>" +
      title +
      "</h1>" +
      "</header>"
    );
  }

  function renderTiles() {
    var cards = CATS.map(function (c) {
      var suffix = c.fromSuffix || " ₽";
      var from = c.fromSuffix ? "от " + c.from.toLocaleString("ru-RU") + suffix : "от " + money(c.from);
      return (
        '<button type="button" class="ca-tile" data-ca="open" data-id="' +
        c.id +
        '">' +
        '<span class="ca-ico" aria-hidden="true">' +
        ICONS[c.id] +
        "</span>" +
        "<strong>" +
        c.name +
        "</strong>" +
        "<span class=\"ca-from\">" +
        from +
        "</span>" +
        '<span class="ca-pick">Выбрать</span>' +
        "</button>"
      );
    }).join("");
    return (
      renderHeader("Что почистить?", "home") +
      '<div class="ca-grid">' +
      cards +
      "</div>"
    );
  }

  function renderCard() {
    var cat = catById(state.catId);
    if (!cat) return renderTiles();
    var t = typeByKey(cat, state.typeKey);
    var showTypes = cat.types.length > 1;
    var chips = "";
    if (showTypes) {
      chips =
        '<div class="ca-label">Какой ' +
        cat.title.toLowerCase() +
        "</div><div class=\"ca-chips\">" +
        cat.types
          .map(function (tp) {
            var on = tp.key === t.key ? " is-on" : "";
            return (
              '<button type="button" class="ca-chip' +
              on +
              '" data-ca="type" data-key="' +
              tp.key +
              '">' +
              tp.label +
              " · " +
              money(tp.price).replace("\u00a0₽", "") +
              "</button>"
            );
          })
          .join("") +
        "</div>";
    }
    var price = Calc.computeTotal([{ price: t.price, qty: state.qty }], state.drying);
    return (
      renderHeader(cat.title, "tiles") +
      '<div class="ca-sheet">' +
      chips +
      '<div class="ca-label">' +
      cat.qtyLabel +
      "</div>" +
      '<div class="ca-stepper">' +
      '<button type="button" data-ca="qty" data-dir="-1" aria-label="Меньше">−</button>' +
      "<span>" +
      state.qty +
      "</span>" +
      '<button type="button" data-ca="qty" data-dir="1" aria-label="Больше">+</button>' +
      "</div>" +
      '<label class="ca-switch"><span>Нужна сушка +30%</span>' +
      '<input type="checkbox" data-ca="dry"' +
      (state.drying ? " checked" : "") +
      "/><i></i></label>" +
      '<div class="ca-price">от ' +
      money(price) +
      "</div>" +
      '<button type="button" class="ca-add" data-ca="add">Добавить в заявку</button>' +
      "</div>"
    );
  }

  function renderCart() {
    if (!state.cart.length) {
      return (
        renderHeader("Заявка", "tiles") +
        '<div class="ca-empty"><p>Пока пусто.</p><p>Выберите, что почистить.</p>' +
        '<button type="button" class="ca-ghost" data-ca="tiles">К категориям</button></div>'
      );
    }
    var rows = state.cart
      .map(function (it, i) {
        return (
          '<div class="ca-line">' +
          '<span class="ca-ico">' +
          (ICONS[it.catId] || "") +
          "</span>" +
          "<div><strong>" +
          it.label +
          " × " +
          it.qty +
          "</strong><span>от " +
          money(lineTotal(it)) +
          (it.drying ? " · сушка" : "") +
          "</span></div>" +
          '<button type="button" class="ca-del" data-ca="del" data-i="' +
          i +
          '" aria-label="Удалить">×</button>' +
          '<div class="ca-mini">' +
          '<button type="button" data-ca="cartqty" data-i="' +
          i +
          '" data-dir="-1">−</button>' +
          "<span>" +
          it.qty +
          "</span>" +
          '<button type="button" data-ca="cartqty" data-i="' +
          i +
          '" data-dir="1">+</button></div></div>'
        );
      })
      .join("");
    return (
      renderHeader("Заявка", "tiles") +
      '<div class="ca-cart">' +
      rows +
      '<button type="button" class="ca-more" data-ca="tiles">+ Добавить ещё</button>' +
      "</div>"
    );
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function renderForm() {
    var draft = draftFromCart();
    try { sessionStorage.setItem("him-calc-draft", draft); } catch (e) {}
    return (
      renderHeader("Заявка", "cart") +
      '<div class="form-success" id="form-success">Заявка ушла, перезвоним</div>' +
      '<form class="ca-form" id="request-form" enctype="multipart/form-data" onsubmit="return handleSubmit(event)">' +
      '<div class="field"><label for="name">Имя</label>' +
      '<input id="name" name="name" required autocomplete="name" placeholder="Как к вам обращаться?"/></div>' +
      '<div class="field"><label for="phone">Телефон</label>' +
      '<div class="phone-input-wrap"><span class="phone-prefix">+7</span>' +
      '<input id="phone" name="phone" required type="tel" autocomplete="tel" inputmode="tel" placeholder="915 754-81-15"/></div>' +
      '<div class="form-error" id="form-error">Укажите корректный номер телефона.</div></div>' +
      '<div class="field"><label for="comment">Что нужно почистить?</label>' +
      '<textarea id="comment" name="comment" rows="5">' + escapeHtml(draft) + '</textarea></div>' +
      '<button class="ca-add" type="submit">Отправить заявку</button>' +
      "</form>"
    );
  }

  function renderBar() {
    var total = cartTotal();
    var empty = total <= 0;
    var left =
      state.view === "tiles" && empty
        ? "В заявке пусто"
        : "Итого от <b>" + money(total) + "</b>";
    var disabled = empty ? " disabled" : "";
    return (
      '<div class="ca-bar"><div class="ca-bar-sum">' +
      left +
      '</div><button type="button" class="ca-bar-btn"' +
      disabled +
      ' data-ca="go-request">Оставить заявку</button></div>'
    );
  }

  function render() {
    var root = document.getElementById("calc-app");
    var view = "";
    if (state.view === "card") view = renderCard();
    else if (state.view === "cart") view = renderCart();
    else if (state.view === "form") view = renderForm();
    else view = renderTiles();
    var hideBar = state.view === "form";
    root.innerHTML = view + (hideBar ? "" : renderBar());
    root.setAttribute("data-view", state.view);
    if (state.view === "form") fillForm();
  }

  function openCat(id) {
    var cat = catById(id);
    if (!cat) return;
    state.catId = id;
    state.typeKey = cat.types[0].key;
    state.qty = 1;
    state.drying = false;
    state.view = "card";
    render();
  }

  function onClick(e) {
    var btn = e.target.closest("[data-ca]");
    if (!btn) return;
    var act = btn.getAttribute("data-ca");
    if (act === "home") {
      window.location.href = "index.html";
      return;
    }
    if (act === "tiles") {
      state.view = "tiles";
      render();
      return;
    }
    if (act === "cart") {
      state.view = "cart";
      render();
      return;
    }
    if (act === "open") {
      openCat(btn.getAttribute("data-id"));
      return;
    }
    if (act === "type") {
      state.typeKey = btn.getAttribute("data-key");
      render();
      return;
    }
    if (act === "qty") {
      var d = Number(btn.getAttribute("data-dir"));
      state.qty = Math.max(1, Math.min(99, state.qty + d));
      render();
      return;
    }
    if (act === "add") {
      var cat = catById(state.catId);
      var t = typeByKey(cat, state.typeKey);
      state.cart.push({
        catId: cat.id,
        key: t.key,
        label: Calc.labels[t.key] || t.label,
        price: t.price,
        qty: state.qty,
        drying: state.drying,
      });
      saveCart();
      state.view = "tiles";
      render();
      return;
    }
    if (act === "del") {
      state.cart.splice(Number(btn.getAttribute("data-i")), 1);
      saveCart();
      render();
      return;
    }
    if (act === "cartqty") {
      var i = Number(btn.getAttribute("data-i"));
      var dir = Number(btn.getAttribute("data-dir"));
      var row = state.cart[i];
      if (!row) return;
      row.qty = Math.max(1, Math.min(99, row.qty + dir));
      saveCart();
      render();
      return;
    }
    if (act === "go-request") {
      if (cartTotal() <= 0) return;
      if (state.view === "cart") {
        state.view = "form";
      } else {
        state.view = "cart";
      }
      render();
    }
  }

  function onChange(e) {
    if (e.target.getAttribute("data-ca") === "dry") {
      state.drying = !!e.target.checked;
      render();
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    loadCart();
    var root = document.getElementById("calc-app");
    if (!root) return;
    root.addEventListener("click", onClick);
    root.addEventListener("change", onChange);
    render();
  });
})();
