/* État client : panier, favoris, comparaison, historique des demandes.
   Stockage local (navigateur). Interface volontairement simple pour être remplacée par une API plus tard. */
(function () {
  const KEY = "ventage:" + (window.SODISCOM_CONFIG || {}).id;
  const empty = () => ({ cart: [], favs: [], compare: [], orders: [] });
  let state = empty();
  try { state = Object.assign(empty(), JSON.parse(localStorage.getItem(KEY) || "{}")); } catch (e) { /* navigation privée */ }

  const save = () => {
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {}
    document.dispatchEvent(new CustomEvent("store:change", { detail: state }));
  };
  const valid = (id) => !!window.SODISCOM_DATA.findProduct(id);
  // Nettoie les produits supprimés du catalogue
  state.cart = state.cart.filter((l) => valid(l.id));
  state.favs = state.favs.filter(valid);
  state.compare = state.compare.filter(valid);

  window.Store = {
    get: () => state,
    cartCount: () => state.cart.reduce((n, l) => n + l.qty, 0),
    addToCart(id, qty = 1, variant = null) {
      const line = state.cart.find((l) => l.id === id && l.variant === variant);
      if (line) line.qty = Math.min(99, line.qty + qty); else state.cart.push({ id, qty, variant });
      save();
    },
    setQty(id, qty, variant = null) {
      const line = state.cart.find((l) => l.id === id && l.variant === variant);
      if (!line) return;
      if (qty <= 0) state.cart = state.cart.filter((l) => l !== line); else line.qty = Math.min(99, qty);
      save();
    },
    clearCart() { state.cart = []; save(); },
    isFav: (id) => state.favs.includes(id),
    toggleFav(id) { state.favs = state.favs.includes(id) ? state.favs.filter((x) => x !== id) : [...state.favs, id]; save(); return state.favs.includes(id); },
    inCompare: (id) => state.compare.includes(id),
    toggleCompare(id) {
      if (state.compare.includes(id)) state.compare = state.compare.filter((x) => x !== id);
      else { if (state.compare.length >= 3) return false; state.compare.push(id); }
      save(); return true;
    },
    clearCompare() { state.compare = []; save(); },
    addOrder(order) { state.orders.unshift(order); state.orders = state.orders.slice(0, 20); save(); }
  };
})();
